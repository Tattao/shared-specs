#!/usr/bin/env python3
"""
OSMX 24x7 Dispatcher — core scheduling engine
Reads task-queue.yaml, assigns tasks to slots, generates agent commands.
Usage: python3 dispatch.py [--dry-run] [--slot <slot>] [--task <task-id>]
Part of: OSMX 24x7 Infrastructure
"""

import argparse
import json
import os
import subprocess
import sys
import yaml
from datetime import datetime, timezone
from pathlib import Path

INFRA_DIR = Path(__file__).parent
POOL_CONFIG = INFRA_DIR / "agent-pool.yaml"
TASK_QUEUE = INFRA_DIR / "task-queue.yaml"
SLOTS_DIR = INFRA_DIR / "slots"
SLOT_MANAGER = INFRA_DIR / "slot-manager.sh"

def load_yaml(path):
    with open(path) as f:
        return yaml.safe_load(f)

def save_yaml(path, data):
    with open(path, 'w') as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

def get_slot_state(slot_name):
    state_file = SLOTS_DIR / f"{slot_name}.state"
    if not state_file.exists():
        return {"status": "idle"}
    state = {}
    for line in state_file.read_text().strip().splitlines():
        if '=' in line:
            k, v = line.split('=', 1)
            state[k] = v
    return state

def get_available_slots(pool):
    """Return slots that are idle (not running a task)."""
    available = []
    for slot_name, slot_config in pool.get('slots', {}).items():
        state = get_slot_state(slot_name)
        if state.get('status', 'idle') != 'running':
            available.append((slot_name, slot_config))
    return available

def get_ready_tasks(queue):
    """Return tasks that are pending and all dependencies are completed."""
    tasks = queue.get('tasks', [])
    completed_ids = {t['id'] for t in tasks if t.get('status') == 'completed'}
    incomplete_ids = {t['id'] for t in tasks if t.get('status') != 'completed'}
    
    ready = []
    for task in tasks:
        if task.get('status') != 'pending':
            continue
        deps = task.get('depends_on', [])
        reverse_blockers = [
            blocker['id']
            for blocker in tasks
            if task['id'] in blocker.get('blocks', []) and blocker['id'] in incomplete_ids
        ]
        if all(d in completed_ids for d in deps) and not reverse_blockers:
            # Priority sort: P0 first, then P1, then P2
            priority_order = {'P0': 0, 'P1': 1, 'P2': 2}
            ready.append((priority_order.get(task.get('priority', 'P2'), 99), task))
    
    ready.sort(key=lambda x: x[0])
    return [t for _, t in ready]

def match_slot_to_task(slot_config, task, pool):
    """Check if a slot is suitable for a task."""
    task_agent = task.get('agent_type', 'codex')
    slot_agent = slot_config.get('agent_type', 'codex')
    
    # Exact agent match preferred, but codex slots can take codex tasks
    if task_agent == slot_agent:
        return True
    # claude-code tasks need claude-code slots
    if task_agent == 'claude-code' and slot_agent != 'claude-code':
        return False
    # codex tasks can run on any slot (with preference for codex)
    return True

def build_agent_command(task, slot_config, pool):
    """Build the actual command to execute in the tmux slot."""
    agent_type = task.get('agent_type', 'codex')
    agent_config = pool.get('agents', {}).get(agent_type, {})
    
    worktree = task['worktree']
    brief = task.get('brief', task['title'])
    
    # Escape brief for shell
    brief_escaped = brief.replace('"', '\\"').replace('$', '\\$').replace('`', '\\`')
    
    if agent_type == 'codex':
        model = agent_config.get('args_template', '--model o4-mini')
        cmd = f'cd {worktree} && codex --yolo exec {model} "{brief_escaped}"'
    else:
        # claude-code
        cmd = f'cd {worktree} && claude -p "{brief_escaped}" --dangerously-skip-permissions'
    
    return cmd

def dispatch_task(task, slot_name, slot_config, pool, queue, dry_run=False):
    """Assign a task to a slot and start it."""
    cmd = build_agent_command(task, slot_config, pool)
    
    if dry_run:
        print(f"  [DRY-RUN] Would dispatch:")
        print(f"    Slot: {slot_name}")
        print(f"    Task: {task['id']} — {task['title']}")
        print(f"    Worktree: {task['worktree']}")
        print(f"    Branch: {task['branch']}")
        print(f"    Agent: {task.get('agent_type', 'codex')}")
        print(f"    Command: {cmd[:120]}...")
        return True
    
    # Update task status
    for t in queue['tasks']:
        if t['id'] == task['id']:
            t['status'] = 'dispatched'
            t['assigned_slot'] = slot_name
            t['updated_at'] = datetime.now(timezone.utc).isoformat()
            break
    
    save_yaml(TASK_QUEUE, queue)
    
    # Call slot-manager to start
    result = subprocess.run(
        ['bash', str(SLOT_MANAGER), 'start',
         slot_name, task['id'], task['worktree'], task['branch'], cmd],
        capture_output=True, text=True
    )
    
    if result.returncode == 0:
        # Update task status to running
        for t in queue['tasks']:
            if t['id'] == task['id']:
                t['status'] = 'running'
                t['updated_at'] = datetime.now(timezone.utc).isoformat()
                t['attempts'] = t.get('attempts', 0) + 1
                break
        save_yaml(TASK_QUEUE, queue)
        print(f"  ✓ Dispatched {task['id']} → {slot_name}")
        return True
    else:
        print(f"  ✗ Failed to dispatch {task['id']}: {result.stderr}")
        return False

def run_dispatch(dry_run=False, target_slot=None, target_task=None):
    """Main dispatch loop."""
    pool = load_yaml(POOL_CONFIG)
    queue = load_yaml(TASK_QUEUE)
    
    print(f"=== OSMX 24x7 Dispatcher ===")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Mode: {'DRY-RUN' if dry_run else 'LIVE'}")
    print()
    
    # Show queue summary
    tasks = queue.get('tasks', [])
    by_status = {}
    for t in tasks:
        s = t.get('status', 'unknown')
        by_status[s] = by_status.get(s, 0) + 1
    print(f"Queue: {len(tasks)} tasks")
    for status, count in sorted(by_status.items()):
        print(f"  {status}: {count}")
    print()
    
    # Get available slots
    available = get_available_slots(pool)
    if not available:
        print("No available slots. All 6 slots are running.")
        return
    
    print(f"Available slots: {len(available)}")
    for name, cfg in available:
        print(f"  {name} ({cfg.get('agent_type')}) — {cfg.get('purpose')}")
    print()
    
    # Get ready tasks
    ready = get_ready_tasks(queue)
    if not ready:
        print("No ready tasks (all pending tasks have unmet dependencies).")
        return
    
    print(f"Ready tasks: {len(ready)}")
    
    # Filter if specific slot/task requested
    if target_task:
        ready = [t for t in ready if t['id'] == target_task]
        if not ready:
            print(f"Task {target_task} not found or not ready.")
            return
    
    # Dispatch
    dispatched = 0
    slot_capacity = len(available)
    for task in ready:
        if dispatched >= slot_capacity or not available:
            print(f"\n  All slots filled. Remaining tasks stay queued.")
            break
        
        # Find best matching slot
        for i, (slot_name, slot_config) in enumerate(available):
            if target_slot and slot_name != target_slot:
                continue
            if match_slot_to_task(slot_config, task, pool):
                dispatch_task(task, slot_name, slot_config, pool, queue, dry_run)
                available.pop(i)
                dispatched += 1
                break
    
    print(f"\nDispatched: {dispatched} tasks")

def main():
    parser = argparse.ArgumentParser(description='OSMX 24x7 Dispatcher')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be dispatched')
    parser.add_argument('--slot', help='Target specific slot (e.g. slot-1)')
    parser.add_argument('--task', help='Target specific task (e.g. DW2-BE-001)')
    args = parser.parse_args()
    
    run_dispatch(dry_run=args.dry_run, target_slot=args.slot, target_task=args.task)

if __name__ == '__main__':
    main()
