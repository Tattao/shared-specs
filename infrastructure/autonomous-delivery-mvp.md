# OSMX Autonomous Delivery MVP

> Status: active MVP draft
> Date: 2026-04-30
> Scope: turn OSMX strategy and task packs into a guarded Codex-first delivery operating system

## Purpose

This MVP moves OSMX from strategy documents to an executable autonomous delivery loop.

It is not a new product source of truth. Product facts remain in `osmx/docs/plans`. This repository remains the coordination ledger for task queue, slot state, handoff, gates, evidence index, and conflict records.

## Canonical Inputs

| Input | Role |
|-------|------|
| `osmx/docs/plans/93-autonomic-operations-fabric-40-day-mvp-task-pack.md` | Work package source, WP0-WP13 |
| `osmx/docs/plans/94-autonomic-operations-fabric-architecture-technology-upgrade-plan.md` | Architecture and technology guardrails |
| `osmx/docs/plans/95-autonomic-operations-fabric-full-product-shape-and-pilot-mvp-plan.md` | Product maturity target |
| `osmx/docs/plans/96-codex-7x24-autonomous-delivery-operating-model.md` | Autonomous delivery operating model |
| `osmx/docs/plans/90-agent-execution-operating-model.md` | Base Agent workflow and evaluation rules |

## MVP Artifacts

| File | Purpose |
|------|---------|
| `task-queue-v2.yaml` | Stage A executable queue with lease, heartbeat, human gate, artifact, and validation fields |
| `agent-pool-v2.yaml` | Codex-first slot profiles using environment-based paths |
| `quality-gates-v2.yaml` | Current OSMX guardrails, PostgreSQL primary runtime, MySQL compatibility checks, and no shared-specs runtime dependency checks |
| `runner-v2.py` | Minimal supervised runner for status, next, lease, heartbeat, complete, activate, validate, stale lease review, and doctor checks |
| `templates/task-card-v2.md` | Human-readable task card template matching `task-queue-v2.yaml` |
| `templates/agent-brief-v2.md` | Codex dispatch brief template with write scope and gate rules |

## Stage A Goal

Stage A is an 8-hour unattended run, not full 7x24 production automation.

Acceptance criteria:

- At least 3 low-risk tasks complete.
- Every task has changed files, validation evidence, residual risk, and handoff.
- No task self-approves.
- No task writes outside its declared scope.
- No task turns `shared-specs` into an OSMX runtime, build, test, CI, or source dependency.
- Failed tasks create a repair task or enter `human_gate_required`.

## Environment Contract

The v2 files avoid hardcoded local paths. Set these variables before running a dispatcher or human-assisted dry run:

```bash
export OSMX_WORKSPACE_ROOT=/Users/shitao/Projects/Codex
export OSMX_REPO=$OSMX_WORKSPACE_ROOT/osmx
export SHARED_SPECS_REPO=$OSMX_WORKSPACE_ROOT/shared-specs
export OSMX_ARTIFACT_ROOT=$SHARED_SPECS_REPO/infrastructure/artifacts
```

The old archive path under `osmx/docs/archive/local-worktree-docs-2026-04-29/shared-specs` is a historical snapshot only.

## Recommended First Run

Use a dry-run first:

```bash
cd "$SHARED_SPECS_REPO/infrastructure"
python3 - <<'PY'
from pathlib import Path
for path in ["task-queue-v2.yaml", "agent-pool-v2.yaml", "quality-gates-v2.yaml"]:
    print(path, "exists" if Path(path).exists() else "missing")
PY
```

Then manually dispatch the first task from `task-queue-v2.yaml` into a dedicated worktree. Do not auto-merge during Stage A.

## Runner v2

Use the minimal v2 runner to consume the queue safely:

```bash
cd "$SHARED_SPECS_REPO"
python3 infrastructure/runner-v2.py validate
python3 infrastructure/runner-v2.py doctor
python3 infrastructure/runner-v2.py status
python3 infrastructure/runner-v2.py next
python3 infrastructure/runner-v2.py next --include-human-gate
python3 infrastructure/runner-v2.py stale
```

The runner can lease and complete tasks, but it does not execute product-code changes:

```bash
python3 infrastructure/runner-v2.py lease AOF-WP13-BOUNDARY-001 --owner Codex --allow-human-gate
python3 infrastructure/runner-v2.py heartbeat AOF-WP13-BOUNDARY-001 --owner Codex
python3 infrastructure/runner-v2.py complete AOF-WP13-BOUNDARY-001 --owner Codex --verdict pass_with_risk
```

Human-gated tasks require explicit `--allow-human-gate`. Auto-merge remains forbidden.

## External Agent Roles

Stage A remains Codex-first guarded autonomy. Local Hermes and Claude Code can participate only through controlled profiles:

| Profile | Role | Stage A Rule |
|---------|------|--------------|
| `claude-code-readonly-evaluator` | Independent evaluator and code reviewer | Report-only writes under artifacts or reports |
| `claude-code-implementation-worker` | Scoped implementation worker | Disabled until Stage B or explicit owner gate |
| `hermes-readonly-supervisor` | Stale lease, missing artifact, and wave health supervisor | Read-only target repos; may write shared-specs artifacts |
| `hermes-wave-summarizer` | Nightly or micro-wave summary writer | Summary-only writes under shared-specs artifacts |

Hermes must not become a second control plane. Claude Code must not both implement and evaluate the same task. Neither may close architecture, legal, release, security, migration, product-scope, or production gates.

## Human Gates

The following always require human approval:

- Architecture boundary changes.
- Production migration or DB model changes.
- Security, secret, license, or commercial authorization changes.
- NeatLogic reuse scope changes.
- Customer-visible release or promise.
- Any task that fails twice.

## Stage A Exit

Stage A can graduate to 24-hour continuous execution only after:

- `task-queue-v2.yaml` shows at least 3 completed tasks.
- Evaluation and implementation are performed by different sessions or roles.
- Gate failures are not marked as complete.
- The final summary is synced back to `osmx/docs/plans/80-wave-execution-board.md` or a current OSMX plan document.
