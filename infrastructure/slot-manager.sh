# Slot Manager — tmux slot lifecycle management
# Usage: ./slot-manager.sh <action> [slot-name] [options]
# Actions: init | start | stop | restart | status | health | cleanup
# Part of: OSMX 24x7 Infrastructure

set -euo pipefail

INFRA_DIR="$(cd "$(dirname "$0")" && pwd)"
SLOTS_DIR="$INFRA_DIR/slots"
LOG_DIR="$INFRA_DIR/logs"
mkdir -p "$SLOTS_DIR" "$LOG_DIR"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m'

log() { echo -e "[$(date '+%H:%M:%S')] $1"; }
ok() { log "${GREEN}✓ $1${NC}"; }
warn() { log "${YELLOW}⚠ $1${NC}"; }
err() { log "${RED}✗ $1${NC}"; }

# Parse agent-pool.yaml for slot config
get_slot_config() {
  local slot="$1"
  local field="$2"
  # Simple YAML field extraction (no pyyaml dependency)
  awk "/^  ${slot}:/{found=1} found && /${field}:/{gsub(/^[ ]*${field}:[ ]*/,\"\"); print; exit}" \
    "$INFRA_DIR/agent-pool.yaml" | tr -d '"' | tr -d "'"
}

get_all_slots() {
  awk '/^  slot-[0-9]:/{gsub(/:$/,""); print}' "$INFRA_DIR/agent-pool.yaml"
}

# === ACTIONS ===

action_init() {
  log "Initializing all slots..."
  for slot in $(get_all_slots); do
    local session=$(get_slot_config "$slot" "tmux_session")
    if tmux has-session -t "$session" 2>/dev/null; then
      warn "$slot ($session) already exists"
    else
      tmux new-session -d -s "$session" -c "/Users/apple/Exec/Code"
      echo "ready" > "$SLOTS_DIR/${slot}.state"
      ok "$slot ($session) created"
    fi
  done
  ok "Pool initialized. Use 'start' to assign tasks."
}

action_start() {
  local slot="$1"
  local task_id="$2"
  local worktree="$3"
  local branch="$4"
  local agent_cmd="$5"

  local session=$(get_slot_config "$slot" "tmux_session")

  # Verify worktree exists or create it
  if [ ! -d "$worktree" ]; then
    log "Creating worktree: $worktree from $branch"
    cd /Users/apple/Exec/Code/osmx
    git worktree add "$worktree" -b "$(basename "$branch")" origin/main 2>/dev/null || \
    git worktree add "$worktree" origin/main 2>/dev/null
  fi

  # Reset session
  if tmux has-session -t "$session" 2>/dev/null; then
    tmux kill-session -t "$session" 2>/dev/null || true
  fi
  tmux new-session -d -s "$session" -c "$worktree"

  # Execute agent command
  tmux send-keys -t "$session" "$agent_cmd" Enter

  # Record state
  cat > "$SLOTS_DIR/${slot}.state" <<EOF
slot=$slot
task_id=$task_id
worktree=$worktree
branch=$branch
agent_cmd=$agent_cmd
started_at=$(date -u +%Y-%m-%dT%H:%M:%SZ)
status=running
pid=$(tmux list-panes -t "$session" -F '#{panePid}' 2>/dev/null || echo unknown)
EOF

  ok "$slot started: task=$task_id worktree=$worktree"
}

action_stop() {
  local slot="$1"
  local session=$(get_slot_config "$slot" "tmux_session")

  if tmux has-session -t "$session" 2>/dev/null; then
    # Capture last output before killing
    tmux capture-pane -t "$session" -p > "$LOG_DIR/${slot}-$(date +%Y%m%d-%H%M%S).log" 2>/dev/null || true
    tmux kill-session -t "$session" 2>/dev/null
  fi

  # Update state
  if [ -f "$SLOTS_DIR/${slot}.state" ]; then
    sed -i '' 's/status=running/status=stopped/' "$SLOTS_DIR/${slot}.state"
    echo "stopped_at=$(date -u +%Y-%m-%dT%H:%M:%SZ)" >> "$SLOTS_DIR/${slot}.state"
  fi

  ok "$slot stopped"
}

action_restart() {
  local slot="$1"
  if [ -f "$SLOTS_DIR/${slot}.state" ]; then
    local task_id=$(awk -F= '/^task_id/{print $2}' "$SLOTS_DIR/${slot}.state")
    local worktree=$(awk -F= '/^worktree/{print $2}' "$SLOTS_DIR/${slot}.state")
    local branch=$(awk -F= '/^branch/{print $2}' "$SLOTS_DIR/${slot}.state")
    local agent_cmd=$(awk -F= '/^agent_cmd/{print $2}' "$SLOTS_DIR/${slot}.state")
    action_stop "$slot"
    sleep 2
    action_start "$slot" "$task_id" "$worktree" "$branch" "$agent_cmd"
  else
    err "No previous state for $slot"
  fi
}

action_status() {
  log "=== Slot Pool Status ==="
  for slot in $(get_all_slots); do
    local session=$(get_slot_config "$slot" "tmux_session")
    local purpose=$(get_slot_config "$slot" "purpose")
    local alive="DEAD"
    tmux has-session -t "$session" 2>/dev/null && alive="ALIVE"

    local task_id="none"
    local worktree="none"
    local status="idle"
    if [ -f "$SLOTS_DIR/${slot}.state" ]; then
      task_id=$(awk -F= '/^task_id/{print $2}' "$SLOTS_DIR/${slot}.state")
      worktree=$(awk -F= '/^worktree/{print $2}' "$SLOTS_DIR/${slot}.state")
      status=$(awk -F= '/^status/{print $2}' "$SLOTS_DIR/${slot}.state")
    fi

    echo "  $slot | $alive | task=$task_id | $status | $purpose"
  done
}

action_health() {
  log "=== Health Check ==="
  local failures=0
  for slot in $(get_all_slots); do
    local session=$(get_slot_config "$slot" "tmux_session")
    local status=$(awk -F= '/^status/{print $2}' "$SLOTS_DIR/${slot}.state" 2>/dev/null || echo "idle")

    if [ "$status" = "running" ]; then
      if tmux has-session -t "$session" 2>/dev/null; then
        ok "$slot: healthy"
      else
        err "$slot: session died — needs restart"
        failures=$((failures + 1))
      fi
    else
      warn "$slot: $status (not running)"
    fi
  done

  # Disk space check
  local disk_use=$(df -h /Users/apple | tail -1 | awk '{print $5}' | tr -d '%')
  if [ "$disk_use" -gt 90 ]; then
    err "Disk usage: ${disk_use}% — critical"
    failures=$((failures + 1))
  else
    ok "Disk usage: ${disk_use}%"
  fi

  return $failures
}

action_cleanup() {
  log "Cleaning up idle/merged worktrees..."
  cd /Users/apple/Exec/Code/osmx
  git worktree list | tail -n +2 | while read path commit branch; do
    name=$(basename "$path")
    # Skip protected worktrees
    case "$name" in
      osmx|osmx-emergency|shared-specs|osmx-main-merge|osmx-web-preview) continue ;;
    esac

    # Check if branch is merged
    dirty=$(cd "$path" 2>/dev/null && git status --porcelain 2>/dev/null | wc -l | tr -d ' ')
    if [ "$dirty" = "0" ]; then
      branch_name=$(echo "$branch" | tr -d '[]')
      if git branch -r --merged origin/main | grep -q "$branch_name"; then
        log "  Pruning: $name ($branch_name) — merged, clean"
        git worktree remove "$path" --force 2>/dev/null && ok "  Removed $name" || warn "  Failed to remove $name"
      fi
    else
      warn "  Skipping: $name — dirty ($dirty files)"
    fi
  done
  ok "Cleanup done"
}

# === MAIN ===

case "${1:-help}" in
  init)     action_init ;;
  start)    action_start "$2" "$3" "$4" "$5" "$6" ;;
  stop)     action_stop "$2" ;;
  restart)  action_restart "$2" ;;
  status)   action_status ;;
  health)   action_health ;;
  cleanup)  action_cleanup ;;
  *)
    echo "OSMX 24x7 Slot Manager"
    echo ""
    echo "Usage: $0 <action> [args]"
    echo ""
    echo "Actions:"
    echo "  init                    Initialize all 6 slots"
    echo "  start <slot> <task> <worktree> <branch> <cmd>"
    echo "  stop <slot>             Stop a running slot"
    echo "  restart <slot>          Restart from last known state"
    echo "  status                  Show all slots"
    echo "  health                  Health check all slots"
    echo "  cleanup                 Prune merged worktrees"
    ;;
esac
