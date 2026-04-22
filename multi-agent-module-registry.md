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
| A | Incident Commander Wave 2 | `/Users/apple/Exec/Code/osmx-emergency-main-sync-wave2` | `wave2/command-center-governed-loop` | Command Center governed loop backend/frontend/tests | `osmx/docs/plans/70-wave-2-command-center-governed-loop.md` | review_ready / evidence_refresh_required | OSMX PR #14 |
| B | DB Copilot Productization | `/Users/apple/Exec/Code/osmx-db-copilot-productization` | `stage1/db-copilot-productization` | DB Copilot gate, LLM smoke, PoC path | `osmx/docs/plans/01-osmx-stage-roadmap-master-plan.md` | review_ready / blocked_by_real_llm_evidence | OSMX PR #13 |
| C | Knowledge SLA | `/Users/apple/Exec/Code/osmx-knowledge-sla` | `stage1/knowledge-sla-baseline` | retrieval benchmark, knowledge health | `osmx/docs/plans/40-knowledge-evidence-plan.md` | review_ready / evidence_refresh_required | OSMX PR #12 |
| D | Delivery/Ops | `/Users/apple/Exec/Code/osmx-delivery-ops` | `stage1/delivery-ops-hardening` | runtime, smoke, reproducible deployment | `osmx/docs/plans/90-agent-execution-operating-model.md` | review_ready / merge_candidate | OSMX PR #10 |
| E | Security/Release | `/Users/apple/Exec/Code/osmx-security-release` | `stage1/security-release-gate` | secret scan, release gate, credential hygiene evidence | `osmx/docs/plans/90-agent-execution-operating-model.md` | review_ready / merge_candidate | OSMX PR #11 |
| F | Integration/Regression | `/Users/apple/Exec/Code/osmx-integration-regression` | `stage1/integration-regression-captain` | PR queue, regression matrix, conflict map | `osmx/docs/plans/80-wave-execution-board.md` | active | local coordination |
| G | Studio / OO Compatibility | `/Users/apple/Exec/Code/osmx-studio-oo-compatibility` | `stage1/studio-oo-compatibility` | imported asset usability, wrapper, compatibility evidence | `osmx/docs/plans/30-asset-flow-center-plan.md` | blocked / rebase_required / conflicts_with_pr16_and_pr14 | OSMX PR #15 |
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

## R1 Readiness Evaluation

Date: 2026-04-22

Read-only Agents:

- Integration Captain: checked PR queue, mergeability, changed-file overlap, and conflict map.
- Evaluation Agent: checked PR checks, validation risk, and post-PR #16 evidence gaps.

Shared finding:

- `osmx` main is `1f21695`.
- PR #10-#15 were branched from old baseline `40d0a73`.
- PR #10-#14 are GitHub-mergeable, but validation evidence predates PR #16 and should be refreshed.
- PR #15 is not mergeable and must be rebased / conflict-resolved.

Recommended merge / review order:

```text
#10 -> #11 -> #12 -> #13 conditional -> #14 -> #15 blocked
```

Readiness matrix:

| PR | Lane | Status | Required next action |
|----|------|--------|----------------------|
| #10 | D Delivery/Ops | merge_candidate / pass_with_risk | refresh smoke/self-test evidence; optional Docker live compose smoke |
| #11 | E Security/Release | merge_candidate / pass_with_risk | rerun or confirm security scan/workflow on new main; confirm credential rotation remains operator action |
| #12 | C Knowledge SLA | evidence_refresh_required / pass_with_risk | rerun knowledge health and targeted pytest; record real SLA/Qdrant gap if not available |
| #13 | B DB Copilot | blocked_by_real_llm_evidence | provide real LLM endpoint/key evidence or downgrade PR to gate framework only |
| #14 | A Command Center | evidence_refresh_required / pass_with_risk | rerun Go tags, frontend build/check, Playwright, and live backend smoke if available |
| #15 | G Studio / OO | blocked / rebase_required | rebase on `1f21695` or later, resolve doc/runbook conflicts, then rerun Go/frontend tests |

## Conflict Ledger

| File / area | PRs | Risk | Handling |
|-------------|-----|------|----------|
| `Makefile` | #10, #11, #12, #13 | medium-high | merge in queue order and refresh each gate target |
| `README.md` | #10, #11 | medium | reconcile delivery and security release wording |
| `docs/reference/deployment.md` | #10, #11 | medium | reconcile deployment and security notes |
| `docs/guides/document-change-log.md` | #11, #15, main `1f21695` | high | #15 must rebase after plan-governance merge |
| `frontend/src/types/runbook.ts` | #14, #15 | high | #15 should replay after #14 or explicitly adapt types |
| `osmx-go/internal/runbook/model/model.go` | #14, #15 | high | #15 should replay after #14 or explicitly adapt model changes |
| `docs/plans` numbering / archive move | #15, main `1f21695` | high | stop editing old plan paths; sync to numbered plans |

## Next Agent Dispatch

| Agent | Worktree | Task |
|-------|----------|------|
| D1 Delivery/Ops Evidence | `/Users/apple/Exec/Code/osmx-delivery-ops` | refresh #10 smoke/self-test evidence against `1f21695` |
| E1 Security Release Evidence | `/Users/apple/Exec/Code/osmx-security-release` | refresh #11 security gate evidence against `1f21695` |
| C1 Knowledge SLA Evidence | `/Users/apple/Exec/Code/osmx-knowledge-sla` | refresh #12 deterministic tests and SLA evidence note |
| B1 DB Copilot Evidence | `/Users/apple/Exec/Code/osmx-db-copilot-productization` | resolve real LLM evidence blocker or narrow PR scope |
| A4 Command Center Regression | `/Users/apple/Exec/Code/osmx-emergency-main-sync-wave2` | refresh #14 Go/frontend/Playwright/live smoke evidence |
| G1 Studio OO Rebase | `/Users/apple/Exec/Code/osmx-studio-oo-compatibility` | rebase/resolve #15 conflicts after #14 assumptions are clear |

## R2 Dispatch Registration

Date: 2026-04-22

Dispatch baseline:

- `osmx` main: `1f21695`
- `shared-specs` registry baseline: `c2e0b92`
- Dispatch mode: parallel worker Agents

| Lane | Agent | Codex subagent | Worktree | Branch | Expected output | Status |
|------|-------|----------------|----------|--------|-----------------|--------|
| D | D1 Delivery/Ops Evidence | `Gibbs` / `019db2dc-1df3-7691-b7a1-0ed806fe6ab5` | `/Users/apple/Exec/Code/osmx-delivery-ops` | `stage1/delivery-ops-hardening` | refreshed #10 smoke/self-test evidence | dispatched |
| E | E1 Security Release Evidence | `Einstein` / `019db2dc-1e65-71b0-b577-8ee3467b52ff` | `/Users/apple/Exec/Code/osmx-security-release` | `stage1/security-release-gate` | refreshed #11 security gate evidence | dispatched |
| C | C1 Knowledge SLA Evidence | `Hume` / `019db2dc-1ed2-7ae0-b855-2f8ddf9c4de4` | `/Users/apple/Exec/Code/osmx-knowledge-sla` | `stage1/knowledge-sla-baseline` | refreshed #12 knowledge tests and SLA evidence note | dispatched |
| B | B1 DB Copilot Evidence | `Hegel` / `019db2dc-1f43-7fe1-a2d1-fafeccbe88f6` | `/Users/apple/Exec/Code/osmx-db-copilot-productization` | `stage1/db-copilot-productization` | real LLM evidence or explicit gate-framework downgrade for #13 | dispatched |
| A | A4 Command Center Regression | `Jason` / `019db2dc-1fc3-7bc2-afb2-21be21387e5c` | `/Users/apple/Exec/Code/osmx-emergency-main-sync-wave2` | `wave2/command-center-governed-loop` | refreshed #14 Go/frontend/Playwright/live smoke evidence | dispatched |
| G | G1 Studio OO Rebase | `Euler` / `019db2dc-202d-7a13-b31f-556ad1574763` | `/Users/apple/Exec/Code/osmx-studio-oo-compatibility` | `stage1/studio-oo-compatibility` | #15 rebase/conflict resolution and post-conflict validation | dispatched |

Dispatch constraints:

- Every Agent must preserve its assigned worktree/write scope.
- No Agent may update `shared-specs`; Integration Captain records summaries here.
- Product facts remain in `osmx`.
- PR #15 remains last in merge order unless Integration Captain explicitly revises the conflict map.

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
