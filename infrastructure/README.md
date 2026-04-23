# OSMX 24x7 Infrastructure

> Automated parallel development framework for OSMX Stage 1
> Deadline: 2026-05-15
> Last updated: 2026-04-23

## Architecture

```
┌──────────────────────────────────────────────────────────┐
│                    Hermes (Coordinator)                   │
│  - Parses ROADMAP → generates task cards                 │
│  - Assigns tasks to slots via dispatch.py                │
│  - Monitors health via health-monitor.py                 │
│  - Generates handoffs via handoff-generator.py           │
└───────────┬──────────────────────────┬───────────────────┘
            │                          │
    ┌───────▼───────┐          ┌──────▼────────┐
    │  agent-pool   │          │  task-queue   │
    │  .yaml        │          │  .yaml        │
    │  (6 slots)    │          │  (tasks)      │
    └───────┬───────┘          └──────┬────────┘
            │                         │
    ┌───────▼───────┐          ┌──────▼────────┐
    │ slot-manager  │◄─────────│  dispatch.py  │
    │ .sh           │          │  (scheduler)  │
    │ (tmux CRUD)   │          └───────────────┘
    └───────┬───────┘
            │
    ┌───────▼───────────────────────────────────┐
    │  tmux pool: 6 slots                       │
    │  slot-1 (BE/Go)     slot-4 (QA/Test)     │
    │  slot-2 (FE/Vue)    slot-5 (DB/Migration) │
    │  slot-3 (AI/Arch)   slot-6 (Docs/Int)     │
    └───────────────────────────────────────────┘
```

## Components

| File | Purpose |
|------|---------|
| `agent-pool.yaml` | Slot definitions: 6 slots, agent types, tmux bindings |
| `task-queue.yaml` | Priority-ordered task cards with dependencies |
| `quality-gates.yaml` | Pre/post dispatch validation rules |
| `dispatch.py` | Core scheduler: reads queue → assigns to slots → starts agents |
| `slot-manager.sh` | tmux lifecycle: init, start, stop, restart, status, health, cleanup |
| `health-monitor.py` | Background watchdog: checks slots + system, auto-recovers |
| `handoff-generator.py` | Creates handoff documents for session continuity |
| `templates/` | task-card, agent-brief, handoff, slot-state templates |
| `slots/` | Runtime state files (one per slot) |
| `logs/` | Execution logs |

## Quick Start

### 1. Initialize the pool
```bash
cd /Users/apple/Exec/Code/shared-specs/infrastructure
bash slot-manager.sh init
```

### 2. Dry-run dispatch (see what would happen)
```bash
.venv/bin/python dispatch.py --dry-run
```

### 3. Live dispatch (assign tasks to slots)
```bash
.venv/bin/python dispatch.py
```

### 4. Check status
```bash
bash slot-manager.sh status
.venv/bin/python health-monitor.py --once
```

### 5. Health monitor (background, 5-min interval)
```bash
.venv/bin/python health-monitor.py --interval 300 --auto-recover &
```

### 6. Generate handoff when task completes
```bash
.venv/bin/python handoff-generator.py --slot slot-1 --verdict pass --notes "Implemented X"
```

## Workflow

```
1. Hermes analyzes ROADMAP/plan docs
2. Hermes creates task cards in task-queue.yaml
3. dispatch.py assigns tasks to available slots
4. slot-manager.sh starts tmux sessions with agent commands
5. Codex/Claude Code executes in isolated worktrees
6. health-monitor.py watches for failures
7. Agent completes → generates handoff
8. Hermes validates → quality gates → PR
9. PR merged → next tasks unblocked → goto 3
```

## Agent Types

| Type | Tool | Best For | Max Timeout |
|------|------|----------|-------------|
| `codex` (fast-exec) | `codex --yolo exec` | Deterministic, well-scoped tasks | 10 min |
| `claude-code` (deep-reason) | `claude -p` | Architecture, debugging, complex logic | 15 min |

## Slot Assignment Strategy

- **slot-1, slot-2**: Codex fast-exec → Backend + Frontend implementation
- **slot-3, slot-6**: Claude Code deep-reason → AI/Python + Docs/Integration
- **slot-4**: Codex fast-exec → QA/Test validation
- **slot-5**: Codex fast-exec → DB/Migration work

## Guardrails

1. Each slot writes ONLY to its assigned worktree
2. No slot may depend on `shared-specs` at runtime
3. DB-sensitive changes must pass `migration_pair_check.py` and `db-portability-scan.sh`
4. All PRs must pass `make integration-efficiency-gate`
5. AutoMigrate is dev/bootstrap only — not production schema management
6. PostgreSQL is a future candidate, not a current runtime dependency

## Source of Truth

| Layer | Location |
|-------|----------|
| Product facts | `osmx/docs/plans/` |
| Product code | `osmx` + approved worktrees |
| Coordination ledger | `shared-specs/` (including this infrastructure/) |
| Infrastructure config | `shared-specs/infrastructure/` |

If this infrastructure config conflicts with `osmx/docs/plans`, `osmx/docs/plans` wins.

## Dependencies

- Python 3.10+ with `pyyaml`
- Local runner: use `.venv/bin/python`; system `python3` may not have `pyyaml`
- tmux 3.6a
- codex CLI 0.118+
- claude CLI 2.1+
- gh CLI (for PR management)
- Git worktree support

## Current Task Queue

See `task-queue.yaml` for the live queue. As of 2026-04-23:

| Task | Priority | Status | Depends On |
|------|----------|--------|------------|
| DW1-MERGE | P0 | completed | — |
| DW2-BE-001 PostgreSQL text portability | P0 | completed | DW1-MERGE |
| DW2-DB-001 Runbook text migration | P0 | completed | DW1-MERGE |
| DW2-B-LLM-001 real LLM smoke | P0 | completed | DW1-MERGE |
| DW2-C-SLA-DET-001 deterministic SLA | P0 | completed | DW1-MERGE |
| DW2-C-QDRANT-SEED-001 seed SLA test knowledge | P0 | pending | DW2-C-SLA-DET-001 |
| DW2-C-SLA-REAL-RERUN | P0 | pending | DW2-C-QDRANT-SEED-001 |
| DW2-D-COMPOSE-001 Docker Compose delivery validation | P0 | pending | DW2-BE-001, DW2-DB-001 |
| DW2-FE-001 Auth browser smoke | P1 | completed | DW1-MERGE |
| DW2-DOC-001 Board sync | P1 | pending | remaining DW2 gates |
| DW2-INT-001 Worktree cleanup | P2 | pending | — |
