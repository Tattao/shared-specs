# Multi-Agent Module Registry

> Date: 2026-04-22
> Status: active coordination ledger
> Scope: OSMX multi-agent, multi-module parallel development

## Current Dispatch Baseline

| Item | Value |
|------|-------|
| `osmx` main | `1f21695` |
| `osmx` plan governance PR | `#16` merged |
| `shared-specs` baseline before this update | `d393e1c` |
| Canonical plan entry | `osmx/docs/plans/00-current-plan-index.md` |
| Agent operating model | `osmx/docs/plans/90-agent-execution-operating-model.md` |
| Registry role | coordination ledger only, not product source of truth |

## Purpose

This file is the coordination ledger for future multi-agent development.

It does not define product truth. Final product facts remain in `osmx/docs/plans`, code, tests, runbooks, and reviewed PRs.

Use this file to prevent parallel Agent work from colliding:

- who owns which module
- which worktree and branch are active
- what each Agent may write
- which PR carries the result
- what validation evidence exists
- what conflicts Integration Captain must resolve

## Source Of Truth Boundary

| Layer | Location | Role |
|------|----------|------|
| Product facts | `/Users/apple/Exec/Code/osmx/docs/plans` | canonical plan, contract, acceptance source |
| Product code | `/Users/apple/Exec/Code/osmx` and approved worktrees | implementation source |
| Coordination ledger | `/Users/apple/Exec/Code/shared-specs` | Agent registration, handoff, evidence, conflict ledger |

Rules:

- If this file conflicts with `osmx/docs/plans`, `osmx/docs/plans` wins.
- `shared-specs` must not become a runtime / build / test / CI dependency.
- `shared-specs` must not be added as a git submodule.
- Any accepted draft here must be synchronized back into `osmx`.

## Current Agent Lanes

| Lane | Agent / owner | Worktree | Branch | Write scope | Source plan | Status | PR / evidence |
|------|---------------|----------|--------|-------------|-------------|--------|---------------|
| A | Incident Commander Wave 2 | `/Users/apple/Exec/Code/osmx-emergency-main-sync-wave2` | `wave2/command-center-governed-loop` | Command Center governed loop backend/frontend/tests | `osmx/docs/plans/70-wave-2-command-center-governed-loop.md` | active / needs rebase check on `1f21695` | OSMX PR #14 |
| B | DB Copilot Productization | `/Users/apple/Exec/Code/osmx-db-copilot-productization` | `stage1/db-copilot-productization` | DB Copilot gate, LLM smoke, PoC path | `osmx/docs/plans/01-osmx-stage-roadmap-master-plan.md` | active / needs rebase check on `1f21695` | OSMX PR #13 |
| C | Knowledge SLA | `/Users/apple/Exec/Code/osmx-knowledge-sla` | `stage1/knowledge-sla-baseline` | retrieval benchmark, knowledge health | `osmx/docs/plans/40-knowledge-evidence-plan.md` | active / needs rebase check on `1f21695` | OSMX PR #12 |
| D | Delivery/Ops | `/Users/apple/Exec/Code/osmx-delivery-ops` | `stage1/delivery-ops-hardening` | runtime, smoke, reproducible deployment | `osmx/docs/plans/90-agent-execution-operating-model.md` | active / needs rebase check on `1f21695` | OSMX PR #10 |
| E | Security/Release | `/Users/apple/Exec/Code/osmx-security-release` | `stage1/security-release-gate` | secret scan, release gate, credential hygiene evidence | `osmx/docs/plans/90-agent-execution-operating-model.md` | active / needs rebase check on `1f21695` | OSMX PR #11 |
| F | Integration/Regression | `/Users/apple/Exec/Code/osmx-integration-regression` | `stage1/integration-regression-captain` | PR queue, regression matrix, conflict map | `osmx/docs/plans/80-wave-execution-board.md` | active | local coordination |
| G | Studio / OO Compatibility | `/Users/apple/Exec/Code/osmx-studio-oo-compatibility` | `stage1/studio-oo-compatibility` | imported asset usability, wrapper, compatibility evidence | `osmx/docs/plans/30-asset-flow-center-plan.md` | active / needs rebase check on `1f21695` | OSMX PR #15 |
| H | Plan Governance | `/Users/apple/Exec/Code/osmx-plan-governance` | `docs/plan-governance-template` | numbered plan system and operating model | `osmx/docs/plans/00-current-plan-index.md` | merged | OSMX PR #16 / merge `1f21695` |

## Next Dispatch Batch

After PR #16, all implementation lanes must refresh against `osmx` main `1f21695` or later before further edits.

Recommended parallel registration:

| Batch | Agent group | First action | Output |
|-------|-------------|--------------|--------|
| R1 | Integration Captain | Re-read PR #10-#15 against `1f21695`; update merge order and conflict map | updated registry evidence |
| R1 | Evaluation Agent | Run lightweight PR-level readiness review for #10-#15 | pass / risk / blocked matrix |
| R1 | Lane Owners A-G | Confirm each worktree status, branch, diff scope, and validation evidence | completion entries below |
| R2 | Development Agents | Continue only lanes marked `pass` or `pass_with_risk` by Integration Captain | updated PRs |

Do not start new feature expansion until R1 confirms that each lane is still aligned with the numbered plans merged in PR #16.

## Registration Template

```markdown
## Agent Registration: <lane-id> / <agent-name>

- Date:
- Agent:
- Module:
- Worktree:
- Branch:
- Source plan:
- Write scope:
- Read-only dependencies:
- Expected deliverables:
- Expected validation:
- Conflict risks:
- Status:
- PR / commit:
- Evidence:
```

## Completion Template

```markdown
## Agent Completion: <lane-id> / <agent-name>

- Date:
- Verdict: pass / pass_with_risk / fail / blocked
- Changed files:
- Validation commands:
- Key results:
- PR / commit:
- Residual risks:
- Needs Integration Captain:
- Needs osmx docs sync:
```

## Integration Captain Checklist

- [ ] Every active Agent has a lane, worktree, branch, source plan, and write scope.
- [ ] No two Agents own the same write path unless explicitly coordinated.
- [ ] Every PR has validation evidence.
- [ ] PR merge order is recorded.
- [ ] Conflict risks are documented before merge.
- [ ] Accepted `shared-specs` decisions are synchronized back into `osmx`.
