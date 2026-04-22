# Multi-Agent Module Registry

> Date: 2026-04-22
> Status: active coordination ledger
> Scope: OSMX multi-agent, multi-module parallel development

## Current Dispatch Baseline

| Item | Value |
|------|-------|
| `osmx` main | `bf33368` |
| `osmx` plan governance PR | `#16` merged |
| `shared-specs` baseline before this update | `f3edcfe` |
| Canonical plan entry | `osmx/docs/plans/00-current-plan-index.md` |
| Agent operating model | `osmx/docs/plans/90-agent-execution-operating-model.md` |
| Database architecture ADR | `osmx/docs/architecture/ADR-DB-001-control-plane-database-strategy.md` |
| Database architecture assessment | `shared-specs/OSMX_Database_Architecture_Assessment.md` |
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
- `OSMX_Database_Architecture_Assessment.md` has been synchronized into `osmx/docs/architecture/ADR-DB-001-control-plane-database-strategy.md`; the ADR is now the canonical product-architecture record.
- `shared-specs` must not become a runtime / build / test / CI dependency.
- `shared-specs` must not be added as a git submodule.
- Any accepted draft here must be synchronized back into `osmx`.

## Database Architecture Guardrail

Starting 2026-04-22, every new plan, PR review, implementation task, and Agent handoff must account for the database architecture assessment.

Updated execution requirement from 2026-04-22 13:18 CST:

```text
Every DB-sensitive change must synchronously adapt to PostgreSQL.
```

This means DB-sensitive PRs must design, implement, or explicitly validate the MySQL and PostgreSQL behavior together. It still does not authorize a primary database migration, production dual writes, TimescaleDB/control-plane database merging, or Qdrant replacement.

- Current strategy: keep MySQL as the control-plane OLTP database now; synchronously adapt DB-sensitive work for PostgreSQL.
- Wave 2 must not start a MySQL to PostgreSQL primary database migration.
- PostgreSQL is a future control-plane primary database candidate, not a current runtime dependency.
- TimescaleDB remains the observability time-series store; do not merge it with the control-plane primary database in Wave 2.
- Qdrant remains the primary semantic / RAG vector store; do not replace it with pgvector in Wave 2.
- New data models and queries must be tenant-aware, project-aware, audit-aware, artifact-aware, idempotency-aware, and PostgreSQL-ready.
- New raw SQL must avoid MySQL-specific syntax, or include explicit MySQL/PostgreSQL dialect isolation, tests or scan evidence, and a follow-up risk note.
- New JSON fields must include a `schema_version`, and high-frequency filter fields must be promoted to normal indexed columns.
- Incident Commander work must preserve the main chain: `Plan -> Approval -> AssetExecution -> Artifact -> Audit`.
- PRs that touch data models, migrations, queries, audit, artifact, execution, or Incident Commander state must include DB portability / PostgreSQL synchronous adaptation notes.

Canonicalization status:

- OSMX PR `#22` promoted the accepted decision into `osmx/docs/architecture/ADR-DB-001-control-plane-database-strategy.md`.
- OSMX PR `#22` added `scripts/db-portability-scan.sh`.
- Future product decisions should cite the OSMX ADR first; this shared-specs assessment remains a coordination source and historical input.

## Current Agent Lanes

| Lane | Agent / owner | Worktree | Branch | Write scope | Source plan | Status | PR / evidence |
|------|---------------|----------|--------|-------------|-------------|--------|---------------|
| A | Incident Commander Wave 2 | `/Users/apple/Exec/Code/osmx-emergency-main-sync-wave2` | `wave2/command-center-governed-loop` | Command Center governed loop backend/frontend/tests | `osmx/docs/plans/70-wave-2-command-center-governed-loop.md` | merged / live_smoke_risk | OSMX PR #14 / merge `81a7709` |
| B | DB Copilot Productization | `/Users/apple/Exec/Code/osmx-db-copilot-productization` | `stage1/db-copilot-productization` | DB Copilot gate, LLM smoke, PoC path | `osmx/docs/plans/01-osmx-stage-roadmap-master-plan.md` | framework_merged / real_llm_replay_passed | OSMX PR #13 / merge `591bc29`; supplemental PR #20 / merge `6b02668`; board sync PR #21 / merge `86dab5d` |
| C | Knowledge SLA | `/Users/apple/Exec/Code/osmx-knowledge-sla` | `stage1/knowledge-sla-baseline` | retrieval benchmark, knowledge health | `osmx/docs/plans/40-knowledge-evidence-plan.md` | merged / real_mode_gap | OSMX PR #12 / merge `91fcadc` |
| D | Delivery/Ops | `/Users/apple/Exec/Code/osmx-delivery-ops` | `stage1/delivery-ops-hardening` | runtime, smoke, reproducible deployment | `osmx/docs/plans/90-agent-execution-operating-model.md` | merged / pass_with_risk | OSMX PR #10 / merge `7be68f6` |
| E | Security/Release | `/Users/apple/Exec/Code/osmx-security-release` | `stage1/security-release-gate` | secret scan, release gate, credential hygiene evidence | `osmx/docs/plans/90-agent-execution-operating-model.md` | merged / pass_with_risk | OSMX PR #11 / merge `51250db` |
| F | Integration/Regression | `/Users/apple/Exec/Code/osmx-integration-regression` | `docs/tools-stage1-wave2-template-pack` | PR queue templates, regression dispatcher tooling, historical references | `osmx/docs/plans/80-wave-execution-board.md` | docs_tools_template_merged | OSMX PR #23 / merge `330003e` |
| G | Studio / OO Compatibility | `/Users/apple/Exec/Code/osmx-studio-oo-compatibility` | `stage1/studio-oo-compatibility` | imported asset usability, wrapper, compatibility evidence | `osmx/docs/plans/30-asset-flow-center-plan.md` | merged / after_14_replay_done | OSMX PR #15 / merge `cc08f53` |
| H | Plan Governance | `/Users/apple/Exec/Code/osmx-plan-governance` | `docs/plan-governance-template` | numbered plan system and operating model | `osmx/docs/plans/00-current-plan-index.md` | merged | OSMX PR #16 / merge `1f21695` |
| I | DB Portability / PostgreSQL Adaptation | `/Users/apple/Exec/Code/osmx-business-scope` and scoped follow-up worktrees | `db/business-scope-postgres-adaptation`, docs sync branches | DB-sensitive model/migration/raw SQL/query paths | `osmx/docs/architecture/ADR-DB-001-control-plane-database-strategy.md` | active_guardrail / latest_merged | OSMX PR #27 / merge `001bfb7`; board sync PR #28 / merge `9e32e35` |

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

## R2 Completion Summary

Date: 2026-04-22

All six dispatched Agents reported back.

R2 here is the completion ledger, not the live merge queue. The current merge order and replay requirements are captured in R3 below.

| Lane | PR | Agent | Result | Evidence / remaining risk |
|------|----|-------|--------|----------------------------|
| D | #10 | D1 Delivery/Ops Evidence | `pass_with_risk`, merge candidate | self-test, script syntax, compose config, `git diff --check` passed; live Docker smoke blocked by unavailable Docker daemon / local runtime |
| E | #11 | E1 Security Release Evidence | `pass_with_risk`, merge candidate | `make security-release-gate` passed with 0 blocking findings; strict review-only mode exits 2 due public IP literal; credential rotation remains operator action |
| C | #12 | C1 Knowledge SLA Evidence | `pass_with_risk` | deterministic health/benchmark, targeted pytest, `make knowledge-regression` passed; real Go/Qdrant mode not configured |
| B | #13 | B1 DB Copilot Evidence | `blocked`, gate framework only | real LLM env missing; smoke is `expected_blocked`; acceptance is `blocked` with `real_llm_smoke=expected_blocked` |
| A | #14 | A4 Command Center Regression | `pass_with_risk`, merge readiness review | Go tags, frontend build/check/build, Playwright governed-loop tests passed; live backend smoke blocked by local MySQL credential |
| G | #15 | G1 Studio OO Rebase | `review_ready`, after-#14 replay required | PR #15 is now mergeable/clean against `1f21695`; docs conflict resolved into new numbered plan system; still overlaps #14 runbook type/model files |

Current GitHub PR state after R2:

- #10: `MERGEABLE`, GitGuardian pass.
- #11: `MERGEABLE`, security-gate pass, GitGuardian pass.
- #12: `MERGEABLE`, GitGuardian pass.
- #13: `MERGEABLE`, GitGuardian pass, functionally blocked by missing real LLM evidence.
- #14: `MERGEABLE`, GitGuardian pass.
- #15: `MERGEABLE`, GitGuardian pass, should remain after #14.

R2 merge recommendation:

```text
Merge candidates now: #10 -> #11
Next evidence/merge review: #12 -> #14
Conditional/framework-only: #13
After #14 replay required: #15
```

## R3 Dispatch / Merge Plan

Date: 2026-04-22

This is the active handoff order after the latest Integration Captain queue replay. It supersedes the earlier R2 merge recommendation for merge sequencing, while keeping R2 as the completion record.

### 3.1 Active merge order

1. `#10` may merge first.
2. `#11` must be replayed / rebased after `#10` lands.
3. `#12` and `#14` stay in the later recheck lane, not the immediate merge lane.
4. `#13` cannot be approved as a full productization pass because the real LLM evidence is missing.
5. `#15` must replay after `#14` is clarified and merged.

### 3.2 Replay / conflict notes

- `#11` rebase focus: `Makefile` and `docs/reference/deployment.md`.
- `#12` and `#14` remain evidence-refresh candidates and should be rechecked after the queue settles.
- `#13` remains gate-framework-only until real LLM evidence exists.
- `#15` stays after `#14` because it still depends on the post-#14 type/model shape.

### 3.3 Boundary and scope rules

- `shared-specs` is a coordination ledger only.
- `shared-specs` must not be added to runtime imports, build steps, test commands, or CI dependencies.
- Accepted coordination notes here must still be synchronized back into `osmx` product facts when they change plan or merge order.
- This file records dispatch, evidence, and replay order; it does not define product behavior.

## R3 Execution Summary

Date: 2026-04-22

R3 merge execution completed for the non-blocked lanes.

| PR | Lane | Result | Merge commit / state | Evidence |
|----|------|--------|----------------------|----------|
| #10 | D Delivery/Ops | merged | `7be68f6` | GitGuardian passed; R2 smoke evidence retained; Docker live smoke remains environment-dependent |
| #11 | E Security/Release | replayed after #10, merged | `51250db` | `git diff --check` passed; `make security-release-gate` passed; GitGuardian and security-gate passed |
| #12 | C Knowledge SLA | replayed after #11, merged | `91fcadc` | `make knowledge-regression` passed with `38 passed, 1 skipped`; GitGuardian and security-gate passed; real Go/Qdrant mode still not configured |
| #14 | A Command Center | merged | `81a7709` | Go tagged tests, frontend build/check/build, and Playwright governed-loop spec passed; live backend smoke blocked by local MySQL credentials |
| #15 | G Studio / OO Compatibility | replayed after #14, merged | `cc08f53` | `git diff --check`, frontend build/check, route compatibility test, Go runbook tests, GitGuardian, and security-gate passed |
| #13 | B DB Copilot | merged, framework-only | merge `591bc29` | Framework-only merge retained; real LLM evidence later closed by supplemental PR #20 |

Current `osmx` main after R3:

```text
591bc29 Merge PR #13: DB Copilot gate framework
```

Open integration-relevant PRs:

- `#13` is merged as `gate_framework_only / real_llm_blocker_open`.
- old `#1` remains open and dirty; it is not part of the R3 merge queue.

Canonical docs sync:

- `#17` updated `osmx/docs/plans/80-wave-execution-board.md` and `docs/guides/document-change-log.md` so the main repo no longer lists #10-#15 as open R3 queue items.
- `#17` merge commit: `88b1be0`.

Post-R3 follow-up status:

- `#13` was replayed onto `main @ 88b1be0`, retitled as a DB Copilot productization gate framework PR, and updated with explicit framework-only merge guidance.
- Latest `#13` validation: Python syntax checks passed, frontend `npm run build:check` passed, `make security-release-gate` passed, and `make db-copilot-acceptance-check` returned the expected blocked result because `real_llm_smoke=expected_blocked`.
- Live backend smoke on clean `main @ 88b1be0` still fails before startup with MySQL credential error: `Error 1045 (28000): Access denied for user 'root'@'localhost' (using password: NO)`.

Post-R3 #13 framework-only merge:

- `#13` merged at `591bc29` with explicit framework-only wording.
- Merge scope: DB Copilot gate framework, evidence JSON shape, UI / acceptance entry point, and blocker visibility.
- At that point, DB Copilot productization gate was not completed because `real_llm_smoke_latest.json` was not `status=passed`.
- Historical blocker at that point: `192.168.1.6` LLM was expected available, but this machine routed it through Clash Verge TUN (`utun6 / 198.18.0.1`), so passed evidence could not yet be reproduced.
- Superseded by P4 below: real LLM replay is now passed.
- This ledger records coordination state only; canonical product status is synchronized to `osmx/docs/plans/80-wave-execution-board.md`.

## P4 DB Copilot Real LLM Replay

Date: 2026-04-22

- OSMX PR `#20` merged at `6b02668`.
- Scope: supplemental real LLM replay evidence for DB Copilot productization, plus optional `OSMX_LLM_LOCAL_ADDRESS` support for TUN/VPN local direct routes.
- LLM endpoint: `http://192.168.1.6:8000/v1`
- Model: `Qwen3.5-27B.Q4_K_M.gguf`
- API type: `completions`
- Route note: default route still reports `utun6 / 198.18.0.1`, but binding the local source IP `10.198.168.101` reaches the LAN LLM endpoint and produces reproducible HTTP evidence.
- Evidence file: `osmx-ai/tests/reports/real_llm_smoke_latest.json`
- Result: `status=passed`; `tool_calls=["SmokeDatabaseContextTool"]`; `providers=["native","llm_fallback"]`; non-empty LLM reply.
- Acceptance summary: `python3 scripts/db_copilot_acceptance_check.py` returned `status=passed`, `blocked=false`, and `gate_scope=productization_gate`.
- Validation: Python compile passed; real LLM smoke passed; acceptance check passed; `git diff --check` passed; `make security-release-gate` passed; frontend `npm run build:check` passed.
- Not run: pytest, because the available local Python environments did not have pytest installed.

Current `osmx` main after P4:

```text
6b02668 Merge PR #20: DB Copilot real LLM replay evidence
```

## P5 Wave Board Snapshot Sync

Date: 2026-04-22

- OSMX PR `#21` merged at `86dab5d`.
- Scope: synchronized `osmx/docs/plans/80-wave-execution-board.md` from the post-#19 snapshot to the post-#20 / real LLM replay state.
- Result: canonical wave board now lists `#20`, records `framework_merged / real_llm_replay_passed`, and points Stage 1 DB Productization to DB Copilot product acceptance / PoC refinement.
- Validation: `git diff --check` passed; `make security-release-gate` passed locally with 0 blocking findings and 1 existing review-level public IP finding; GitHub `security-gate` and GitGuardian checks passed.
- Boundary: this registry only mirrors the coordination state. Product facts remain in `osmx/docs/plans`, reviewed PRs, tests, and runtime evidence.

Current `osmx` main after P5:

```text
86dab5d Docs: sync wave board after real LLM replay
```

## P6 Database Architecture Guardrail Canonicalization

Date: 2026-04-22

- OSMX PR `#22` merged at `0d3bfab`.
- Scope: canonicalized `OSMX_Database_Architecture_Assessment.md` into `osmx/docs/architecture/ADR-DB-001-control-plane-database-strategy.md` and added `scripts/db-portability-scan.sh`.
- Result: future plans, PR reviews, Agent handoffs, and implementations must account for `Keep MySQL Now, Build PostgreSQL Readiness`.
- Guardrail: Wave 2 does not start MySQL to PostgreSQL primary database migration, does not introduce dual writes, does not merge TimescaleDB with the control-plane database, and does not replace Qdrant with pgvector.
- Validation: `bash -n scripts/db-portability-scan.sh` passed; `scripts/db-portability-scan.sh` completed; `git diff --check` passed; `make security-release-gate` passed locally with 0 blocking findings and 1 existing review-level public IP finding; GitHub `security-gate` and GitGuardian checks passed.
- Boundary: `shared-specs` remains coordination-only; the canonical architecture record is now in `osmx`.

Current `osmx` main after P6:

```text
0d3bfab Docs: add database readiness guardrails
```

## P2 Local Runtime Smoke Docs Sync

Date: 2026-04-22

- OSMX PR `#19` merged at `8aa855f`.
- Scope: documented local source-runtime startup with placeholder-only `.env.local.example`, host MySQL env overrides, and local smoke command.
- Runtime evidence: Go server, AI service, and frontend were started from `/Users/apple/Exec/Code/osmx-post13-docs`; `FRONTEND_BASE_URL=http://localhost:15174 ./scripts/smoke.sh --mode local-runtime` passed.
- Secret boundary: no real MySQL password or `.env.local` file was committed.

## P3 Legacy Integration Queue Triage

Date: 2026-04-22

Worktree inspected:

- `/Users/apple/Exec/Code/osmx-integration-regression`
- Branch: `stage1/integration-regression-captain`
- Status: behind current `main`; contains local draft changes and untracked queue / matrix / dispatcher files.

Conclusion:

- Do not treat the old local R3 / Stage 1 queue drafts as the current merge source of truth.
- Current product / merge facts are in `osmx/docs/plans/80-wave-execution-board.md`, reviewed PRs, and this coordination ledger.
- `shared-specs` remains coordination-only and must not become a runtime / build / test / CI dependency.

| Path | Classification | Next action |
|------|----------------|-------------|
| `docs/plans/stage1-wave2-integration-queue.md` | cleanup / archive | Superseded by merged R3 board and registry; do not publish as current queue. If kept, mark historical and remove active `D -> E -> C -> B -> A` merge instructions. |
| `docs/plans/README.md` | cleanup | Drop the new index entry unless a historical / reference PR is opened; it currently points readers at a superseded queue. |
| `Makefile` | separate docs/tools PR only | Keep only if the dispatcher is accepted as a generic utility; do not merge from this stale branch directly. |
| `docs/reference/README.md` | separate docs/tools PR only | Useful as an index if the reference templates are promoted together. |
| `docs/reference/stage1-wave2-pr-checklist.md` | keep as reusable template | Candidate for a future docs/tools PR after removing stale queue assumptions and aligning with current numbered plans. |
| `docs/reference/stage1-wave2-ownership-conflict-matrix.md` | keep as reusable template | Candidate for a future docs/tools PR as a conflict-map template, not as a current owner truth table. |
| `docs/reference/stage1-wave2-regression-matrix.md` | keep as reusable template | Candidate for a future docs/tools PR after aligning commands with current `scripts/smoke.sh --mode local-runtime` and post-#19 docs. |
| `docs/reference/stage1-wave2-regression-orchestration.md` | keep as reusable template | Candidate for a future docs/tools PR if the dispatcher is retained. |
| `scripts/check_worktree_health.sh` | keep as reusable script | Script syntax passed; promote only through a fresh branch based on current main. |
| `scripts/regression_dispatcher.sh` | keep as reusable script / needs polish | Script syntax and `--list` passed; full queue dry-run correctly reports missing local `.venv` and frontend dependencies in the stale worktree. Promote only after updating track names and prerequisites. |

Read-only checks run:

- `bash -n scripts/check_worktree_health.sh` passed.
- `bash -n scripts/regression_dispatcher.sh` passed.
- `./scripts/regression_dispatcher.sh --list` passed.
- `./scripts/regression_dispatcher.sh --queue D E C B A --dry-run` returned blockers for missing `.venv` and `frontend/node_modules`, so it is not current pass evidence.

## R4 / P7 Parallel Execution Dispatch

Date: 2026-04-22 13:07 CST

Baseline:

- `osmx` main: `0d3bfab Docs: add database readiness guardrails`
- `shared-specs` main: `8aba3f2`
- Canonical DB architecture record: `osmx/docs/architecture/ADR-DB-001-control-plane-database-strategy.md`
- Current strategy: `Keep MySQL Now, Build PostgreSQL Readiness`

| Agent | Agent id | Workstream | Worktree | Write scope | DB guardrail | Status |
|-------|----------|------------|----------|-------------|--------------|--------|
| Harvey | `019db396-4982-7303-b0af-224d12b87000` | Runtime acceptance | `/Users/apple/Exec/Code/osmx-post13-docs` | read-only runtime checks | `not_applicable` | dispatched |
| Epicurus | `019db396-49f0-7dd0-82b0-932d02cfc9ae` | PR #1 umbrella closure | `/Users/apple/Exec/Code/osmx-post13-docs` | GitHub PR comment / close only | `not_applicable`; follow-up PRs must apply ADR-DB-001 | dispatched |
| Bohr | `019db396-4a6f-7640-b044-8141d283ae4a` | DB portability baseline review | `/Users/apple/Exec/Code/osmx-post13-docs` | read-only scan / classification | `pass/read_only_baseline` | dispatched |
| Confucius | `019db396-4adf-7cb1-9fc9-50d54332d834` | Integration regression docs/tools cleanup | `/Users/apple/Exec/Code/osmx-integration-regression` | docs/tools only; no product code; no shared-specs | `not_applicable`; must not imply DB migration | dispatched |

Parallel constraints:

- No Agent may start a PostgreSQL primary database migration.
- No Agent may introduce primary-store dual writes.
- No Agent may merge TimescaleDB with the control-plane primary database.
- No Agent may replace Qdrant with pgvector.
- Any follow-up PR touching data models, migrations, raw SQL, audit, Artifact, Execution, or Incident Commander state must include `scripts/db-portability-scan.sh` evidence or a scoped equivalent.

## R4 / P7 Completion Summary

Date: 2026-04-22 13:15 CST

| Workstream | Result | Evidence | DB guardrail | Residual risk |
|------------|--------|----------|--------------|---------------|
| PR #1 umbrella closure | completed | PR #1 closed after comment; previous state `CONFLICTING`, `DIRTY`, `changedFiles=243` | `not_applicable`; follow-up PRs must apply ADR-DB-001 | Residual value must be split into small PRs |
| DB portability baseline | completed | `scripts/db-portability-scan.sh` run by Bohr; classified findings | `pass/read_only_baseline` | `DATE_FORMAT`, `AutoMigrate`, and old migration tenant/project drift need follow-up |
| Integration docs/tools cleanup | merged | OSMX PR #23 merged at `330003e`; checks passed | `not_applicable` | Template wording may need wave-specific refinement later |
| Runtime acceptance | completed with local fallback | OSMX and Emergency frontends returned HTTP 200; Emergency `/health` ok; login token length 249; `/api/v1/plans` returned plan `37bdb9bd-07c4-41f8-aa38-b1ec4b343051`; major frontend paths returned HTTP 200 | `not_applicable` | Browser visual inspection still recommended |

Current `osmx` main after R4 / P7:

```text
330003e docs/tools: demote stage1 wave2 references
```

Current open OSMX PRs:

```text
none
```

Next recommended split:

1. DB portability minimal fix PR: `trend_service.go` and `report_repo.go` time-bucket SQL portability, with scan evidence.
2. Runtime browser acceptance report PR or docs note, only if visual inspection finds gaps.
3. Small residual PRs from former PR #1 only after each has a single owner, narrow write scope, validation evidence, and ADR-DB-001 result.

## R5 / P8 PostgreSQL Synchronous Adaptation Dispatch

Date: 2026-04-22 13:18 CST

Baseline:

- `osmx` main: `330003e docs/tools: demote stage1 wave2 references`
- `shared-specs` main: `6c473fc`
- User requirement: from now on, DB-sensitive work must synchronously adapt to PostgreSQL.

Interpretation:

- Required: MySQL + PostgreSQL dialect/type/index/query impact must be designed and validated together for DB-sensitive changes.
- Still forbidden: primary database migration, primary-store dual writes, TimescaleDB/control-plane database merge, Qdrant to pgvector replacement.

| Agent | Agent id | Workstream | Worktree | Write scope | PostgreSQL adaptation requirement | Status |
|-------|----------|------------|----------|-------------|-----------------------------------|--------|
| Bacon | `019db3a0-569c-7120-aabc-72e4075f9008` | DB time-bucket code adaptation | `/Users/apple/Exec/Code/osmx-db-portability-timebucket` | `trend_service.go`, `report_repo.go`, focused tests | Must replace scattered MySQL-only `DATE_FORMAT` with MySQL/PostgreSQL dialect-aware behavior | dispatched |
| Laplace | `019db3a0-5728-7f22-81a4-c4490825f049` | PostgreSQL synchronous guardrail docs | `/Users/apple/Exec/Code/osmx-db-sync-guardrails` | ADR and plan docs only | Must upgrade wording from readiness to synchronous adaptation without authorizing migration | dispatched |
| Newton | `019db3a0-578f-79c1-ac63-d516d2574088` | Runtime browser / HTTP acceptance | `/Users/apple/Exec/Code/osmx-post13-docs` | read-only runtime checks | `not_applicable`, but record any DB-query runtime errors as adaptation risk | dispatched |
| McClintock | `019db3a0-580b-78e3-b4f6-04963863d581` | DB architecture decision review | `/Users/apple/Exec/Code/osmx-post13-docs` | read-only decision review | Must recommend how `business_systems` / `AutoMigrate` move toward MySQL/PostgreSQL-compatible migration practice | dispatched |

## R5 / P8 Completion Summary

Date: 2026-04-22 13:27 CST

| Workstream | Result | Evidence | PostgreSQL adaptation result | Residual risk |
|------------|--------|----------|------------------------------|---------------|
| DB time-bucket adaptation | merged | OSMX PR #24 merged at `aaee95d`; changed `trend_service.go`, `report_repo.go`, and focused tests | `pass`; MySQL keeps `DATE_FORMAT` / `DATE`, PostgreSQL uses `date_trunc` / `to_char` behind helper functions | Unsupported GORM dialectors now return explicit errors |
| PostgreSQL synchronous guardrail docs | merged | OSMX PR #25 merged at `a8ad0ac` | `pass`; DB-sensitive PRs must include MySQL/PostgreSQL dialect, type, index, test impact and PostgreSQL adaptation conclusion | Enforcement depends on future PR review discipline |
| Runtime browser / HTTP acceptance | completed | `15174`, `15175`, `18081` reachable; Emergency login, plans API, plan detail, approvals, executions, runbook executions, and audit logs passed; screenshots in `/tmp/osmx-acceptance-artifacts*` | `not_applicable`; no DB dialect/runtime query errors observed | Minor async URL sampling race after login, visually passed |
| DB architecture decision review | completed | McClintock read ADR, migration, models, repos, services, and `AutoMigrate` path | `blocked_for_future_schema_prs` unless tenant/project, migration-first, and PostgreSQL compatibility notes are present | `business_systems` / `business_databases` need schema/service scoped follow-up |
| Wave board sync | merged | OSMX PR #26 merged at `06f3942` | `pass`; board records PostgreSQL synchronous adaptation as active guardrail | none |

Current `osmx` main after R5 / P8:

```text
06f3942 Docs: sync board after PostgreSQL adaptation wave
```

Current open OSMX PRs:

```text
none
```

Next recommended split:

1. Schema scope PR: make `business_systems` / `business_databases` explicitly tenant/project scoped, migration-first, and MySQL/PostgreSQL-compatible.
2. AutoMigrate policy PR: document and, if needed, enforce dev-only/bootstrap behavior while making explicit migrations the schema source of truth.
3. DB-sensitive PR template/checklist update: make PostgreSQL adaptation evidence a blocking checklist item for model/migration/raw SQL/audit/artifact/execution changes.

## R6 / P9 Business Scope PostgreSQL Adaptation Completion Summary

Date: 2026-04-22 13:56 CST

Scope:

- Worktree: `/Users/apple/Exec/Code/osmx-business-scope`
- Implementation branch: `db/business-scope-postgres-adaptation`
- Board sync branch: `docs/post27-board-sync`
- Canonical OSMX board: `osmx/docs/plans/80-wave-execution-board.md`

Results:

| Workstream | Result | Evidence | PostgreSQL adaptation result | Residual risk |
|------------|--------|----------|------------------------------|---------------|
| Business scope implementation | merged | OSMX PR #27 merged at `001bfb7`; changed business models, repos, service, handler, OSM onboarding, focused repository tests, and dialect-specific migrations | `pass_with_risk`; MySQL file uses `BIGINT UNSIGNED` / `AUTO_INCREMENT` / `DATETIME(3)` / `ON UPDATE`; PostgreSQL file uses `BIGSERIAL` / `BIGINT` / `TIMESTAMPTZ` / explicit indexes | SQL migrations are review artifacts while startup still relies on GORM AutoMigrate |
| Business scope docs sync | merged | OSMX PR #28 merged at `9e32e35`; wave board now records #27 and next DB portability lane | `pass`; board keeps PostgreSQL synchronous adaptation active | none |

Validation evidence from #27:

- `go test ./internal/repository ./internal/service ./internal/api/v1` passed.
- `scripts/db-portability-scan.sh > /tmp/osmx-business-scope-db-portability-staged.txt` completed and showed the new MySQL migration patterns as explicit dialect-specific artifacts.
- `git diff --cached --check` passed before #27 commit.
- `make security-release-gate` passed locally with 0 blocking findings and the existing review-level public IP finding.
- GitHub #27: GitGuardian and `security-gate` passed.
- GitHub #28: GitGuardian and `security-gate` passed.

Current `osmx` main after R6 / P9:

```text
9e32e35 Merge PR #28: Sync board after business scope merge
```

Current open OSMX PRs:

```text
none
```

Next recommended split:

1. Fix the existing full-suite blocker in `osmx-go/internal/agent/runtime_client.go`: `go test ./...` fails on five `fmt.Errorf` non-constant format string vet errors. Keep this as a narrow PR.
2. AutoMigrate policy PR: document and, if needed, enforce dev-only/bootstrap behavior while making explicit migrations the schema source of truth.
3. DB-sensitive template/checklist PR: make PostgreSQL adaptation evidence a blocking checklist item for model/migration/raw SQL/audit/artifact/execution changes.

## R7 / P10 Go Full-Suite Restoration Completion Summary

Date: 2026-04-22 14:01 CST

Scope:

- Worktree: `/Users/apple/Exec/Code/osmx-business-scope`
- Implementation branch: `fix/agent-runtime-vet-errors`
- Board sync branch: `docs/post29-board-sync`

Results:

| Workstream | Result | Evidence | DB guardrail | Residual risk |
|------------|--------|----------|--------------|---------------|
| Agent runtime vet fix | merged | OSMX PR #29 merged at `c7f9fa0`; replaced five dynamic `fmt.Errorf(msg)` calls with `errors.New(msg)` | `not_applicable`; no data model, migration, raw SQL, audit, artifact, execution, or DB query changes | none observed |
| Go full-suite validation | passed | `go test ./...` passed locally after #29 patch | `not_applicable` | none observed |
| Board sync | merged | OSMX PR #30 merged at `6203dc9`; board records #29 and moves next lane to AutoMigrate policy / DB-sensitive checklist | `not_applicable`; docs-only sync | none |

Validation evidence:

- `go test ./...` passed.
- `git diff --check` passed.
- `make security-release-gate` passed locally with 0 blocking findings and the existing review-level public IP finding.
- GitHub #29: GitGuardian and `security-gate` passed.
- GitHub #30: GitGuardian and `security-gate` passed.

Current `osmx` main after R7 / P10:

```text
6203dc9 Merge PR #30: Sync board after Go test restoration
```

Current open OSMX PRs:

```text
none
```

Next recommended split:

1. AutoMigrate policy PR: document and, if needed, enforce dev-only/bootstrap behavior while making explicit migrations the schema source of truth.
2. DB-sensitive PR template/checklist update: make PostgreSQL adaptation evidence a blocking checklist item for model/migration/raw SQL/audit/artifact/execution changes.
3. Runtime/browser revalidation: keep current services available and rerun local smoke after pulling `6203dc9` into the runtime worktree.

## R8 / P11 Parallel Dispatch

Date: 2026-04-22 14:05 CST

Baseline:

- `osmx` main: `6203dc9 Merge PR #30: Sync board after Go test restoration`
- `shared-specs` main before dispatch: `df56aa8`
- User instruction: increase task count and parallelism while preserving PostgreSQL synchronous adaptation.

| Agent | Agent id | Workstream | Worktree | Branch | Write scope | DB guardrail | Status |
|-------|----------|------------|----------|--------|-------------|--------------|--------|
| Bernoulli | `019db3d7-a901-72c2-a2bf-a0ddb1850a75` | AutoMigrate policy | `/Users/apple/Exec/Code/osmx-automigrate-policy` | `docs/automigrate-policy` | docs only: ADR / operating model / board / change log | Must state AutoMigrate is dev/bootstrap only; no migration/dual-write authorization | dispatched |
| Leibniz | `019db3d7-aa31-7510-8da5-01e57babb4b3` | DB-sensitive PR checklist | `/Users/apple/Exec/Code/osmx-db-sensitive-checklist` | `docs/db-sensitive-checklist` | `.github` PR template and docs only | Must require PostgreSQL adaptation evidence for DB-sensitive PRs | dispatched |
| Fermat | `019db3d7-aabb-7f53-a390-ca1753a01480` | Runtime revalidation | `/Users/apple/Exec/Code/osmx-runtime-revalidation` | `runtime/latest-main-revalidation` | read-only runtime checks | `not_applicable`; record DB/runtime errors if observed | dispatched |
| Meitner | `019db3d7-ab4a-7b42-b83c-6cacfd9522fd` | Next DB-sensitive scope review | `/Users/apple/Exec/Code/osmx-next-db-scope` | `review/next-db-scope` | read-only scan/review | Must recommend next scope without migration/dual-write/TimescaleDB/Qdrant scope creep | dispatched |

Parallel constraints:

- Bernoulli and Leibniz both touch docs/plans, so Integration Captain must merge one before replaying the other.
- Runtime and scope-review Agents are read-only and may finish independently.
- No Agent may add `shared-specs` as a runtime/build/test/CI dependency.
- Accepted facts must be synchronized back to OSMX canonical docs before being treated as product truth.

## R8 / P11 Parallel Completion Summary

Date: 2026-04-22 14:30 CST

| Workstream | Result | Evidence | DB guardrail | Residual risk |
|------------|--------|----------|--------------|---------------|
| AutoMigrate policy | merged | Bernoulli produced commit `d2f20ba`; OSMX PR #31 merged at `703e2b5`; changed ADR, operating model, board, change log | `pass`; AutoMigrate is documented as dev/bootstrap/local startup only, explicit migration artifacts are the schema review/source-of-truth direction | none |
| DB-sensitive PR checklist | merged | Leibniz produced commit `fc02510` after replay; OSMX PR #32 merged at `1adff14`; added `.github/pull_request_template.md` and docs sync | `pass`; DB-sensitive PRs must include PostgreSQL adaptation, MySQL/PostgreSQL impact, scan/test evidence, and forbidden non-goals | checklist compliance depends on review discipline |
| Runtime revalidation | completed / read-only | Fermat verified `15174`, `15175`, `18081`; `FRONTEND_BASE_URL=http://127.0.0.1:15174 ./scripts/smoke.sh --mode local-runtime` passed | `not_applicable`; no DB runtime errors observed in smoke | services are healthy but version-unconfirmed because processes run from `osmx-post13-docs` / `osmx-emergency-main-sync`, not latest main checkout |
| Next DB-sensitive scope review | completed / read-only | Meitner recommended P0 execution / approval / audit / Artifact main-chain models, P1 runbook execution state manager, P2 business-system migration/model alignment | `review_only`; no migration/dual-write/TimescaleDB/Qdrant scope creep | next implementation still needs a narrow PR and tests |
| Board sync | merged | OSMX PR #33 merged at `bf33368`; board records #31/#32, runtime version caveat, and next DB-sensitive scope | `not_applicable`; docs-only sync | none |

Validation evidence:

- #31: `git diff --check`; GitGuardian and `security-gate` passed.
- #32: `git diff --check`; `make security-release-gate`; GitGuardian and `security-gate` passed.
- #33: `git diff --check`; GitGuardian and `security-gate` passed.
- Runtime smoke: `FRONTEND_BASE_URL=http://127.0.0.1:15174 ./scripts/smoke.sh --mode local-runtime` passed.

Current `osmx` main after R8 / P11:

```text
bf33368 Merge PR #33: Sync board after DB checklist merge
```

Current open OSMX PRs:

```text
none
```

Next recommended split:

1. Runtime latest-main rebaseline: restart OSMX / Emergency services from a single latest-main checkout and rerun local smoke plus browser paths, so health evidence is version-confirmed.
2. DB-sensitive P0 implementation prep: inspect execution / approval / audit / Artifact main-chain models and create a narrow MySQL/PostgreSQL adaptation plan before editing.
3. Runbook state manager adaptation: evaluate `osmx-go/internal/runbook/engine/mysql_state.go` after the main-chain model scope is bounded.

## R9 / P12 Rolling 8-Task Dispatch

Date: 2026-04-22 14:38 CST

Baseline:

- `osmx` main: `bf33368 Merge PR #33: Sync board after DB checklist merge`
- `shared-specs` main before dispatch: `98456b8`
- Requested parallelism: 8 tasks.
- Tool concurrency limit observed: 6 active Agent threads; therefore R9 uses a rolling queue of 8 tasks, with 6 active and 2 queued.

Active Agents:

| Agent | Agent id | Workstream | Worktree | Branch | Write scope | Status |
|-------|----------|------------|----------|--------|-------------|--------|
| Huygens | `019db3e8-62f0-78e2-a1db-ffd12f1949a6` | Runtime latest-main rebaseline | `/Users/apple/Exec/Code/osmx-runtime-main-rebaseline` | `runtime/main-rebaseline` | no code commits; runtime/tmux only | active |
| Hegel | `019db3e8-6472-70a3-bb92-38c82be9fb20` | Main-chain model adaptation | `/Users/apple/Exec/Code/osmx-db-mainchain-adaptation` | `db/mainchain-model-adaptation` | main-chain model files only | active |
| Lovelace | `019db3e9-093f-7130-b21e-0a72986f8970` | Runbook state adaptation | `/Users/apple/Exec/Code/osmx-runbook-state-adaptation` | `db/runbook-state-adaptation` | `mysql_state.go` and focused tests only | active |
| Herschel | `019db3e9-09e9-77b0-96ec-6a6149de1f89` | Main-chain migration artifacts | `/Users/apple/Exec/Code/osmx-mainchain-migration-artifacts` | `db/mainchain-migration-artifacts` | migrations only | active |
| Jason | `019db3e9-0a79-7c33-af04-bfdfe364309c` | DB adaptation test matrix | `/Users/apple/Exec/Code/osmx-db-test-matrix` | `review/db-adaptation-test-matrix` | read-only | active |
| Kant | `019db3e9-0ae6-72e2-ad39-cc40d2966182` | DB portability scan review | `/Users/apple/Exec/Code/osmx-db-portability-scan-review` | `review/db-portability-scan-next` | read-only | active |

Queued Agents:

| Workstream | Worktree | Branch | Reason queued |
|------------|----------|--------|---------------|
| Runtime browser latest-main review | `/Users/apple/Exec/Code/osmx-runtime-browser-review` | `review/runtime-browser-latest-main` | waiting for one active slot |
| P11/P12 integration review | `/Users/apple/Exec/Code/osmx-p11-integration-review` | `review/p11-integration-review` | waiting for one active slot |

R9 constraints:

- DB-sensitive work must complete `.github/pull_request_template.md` evidence if it becomes a PR.
- No primary database migration, no dual writes, no TimescaleDB/control-plane merge, and no Qdrant replacement.
- Workers may commit only inside their assigned write scopes.
- Read-only Agents must not edit files or commit.

## R9 / P12 Completion Summary

Date: 2026-04-22 14:55 CST

Final integration result:

- `osmx` main after closeout: `00140fa Merge PR #36: Sync board after P12 merges`
- Merged PRs:
  - #34 `db/runbook-state-adaptation` -> `732c020`
  - #35 `db/mainchain-migration-artifacts` -> `f476de8`
  - #36 `docs/post35-board-sync` -> `00140fa`
- Current open OSMX PRs after closeout: `none`
- Canonical docs sync: `docs/plans/80-wave-execution-board.md` and `docs/guides/document-change-log.md` updated in #36.

Agent outcomes:

| Agent | Workstream | Verdict | Output |
|-------|------------|---------|--------|
| Huygens | Runtime latest-main rebaseline | pass | Started latest-main Go `8080`, AI `5001`, frontend `25174` from `/Users/apple/Exec/Code/osmx-runtime-main-rebaseline`; `scripts/smoke.sh --mode local-runtime` passed |
| Hegel | Main-chain model adaptation | pass_with_risk | Read-only/no merge; confirmed execution / approval / audit / artifact model risks around `type:json`, `type:longtext`, `type:mediumtext`, tenant/project gaps, idempotency and schema-version gaps |
| Lovelace | Runbook state adaptation | pass_with_risk | Produced #34; replaced runbook state `mediumtext` tags with portable `text`, made `updated_at` updates explicit, added focused tests |
| Herschel | Main-chain migration artifacts | pass_with_risk | Produced #35; added `osmx-go/migrations/README.md` as a migration artifact gap index only, not DDL implementation evidence |
| Jason | DB adaptation test matrix | pass_with_risk | Read-only/no merge; produced next validation matrix and identified missing DB-backed approval, live `/plans -> /approvals -> /audit-logs`, `MySQLStateManager`, and migration syntax/parity tests |
| Kant | DB portability scan review | pass_with_risk | Read-only/no merge; identified P0 blockers in runbook state store naming/AutoMigrate and startup datasource paths `gorm.Open(mysql.Open(...))` |
| Pasteur | Runtime browser review | pass_with_risk | Read-only/no merge; old `15174` / `15175` render login, `18081` health works, but old checkout processes must not be used as latest-main proof |
| Ramanujan | P11/P12 integration review | pass_with_risk | Read-only/no merge; confirmed ADR/board/operating-model alignment and shared-specs ledger-only boundary; flagged board drift before #36 |

Validation evidence:

- #34: `git diff --check`; `cd osmx-go && go test ./internal/runbook/...`; `cd osmx-go && go test ./...`; `scripts/db-portability-scan.sh`.
- #35: `git diff --check HEAD~1..HEAD`; `ls -1 osmx-go/migrations`.
- #36: `git diff --check`.
- GitHub checks: GitGuardian and `security-gate` passed on #34, #35, and #36.

Remaining risks / next recommended split:

1. P0 datasource factory: `osmx-go/internal/app/app.go` and `osmx-go/cmd/emergency/main.go` still open `gorm.Open(mysql.Open(...))`; add a narrow driver/dialect selection layer with MySQL default and PostgreSQL startup smoke path.
2. P0 runbook state store boundary: `MySQLStateManager` naming and AutoMigrate boundary are still MySQL-shaped; #34 reduced type/timestamp risk only.
3. P1 main-chain explicit migrations: add paired `003_mainchain_core.mysql.sql` and `003_mainchain_core.postgres.sql` only after model shape is settled; do not invent tenant/project columns where current Go models lack them.
4. P1 test harness: add DB-backed approval/audit/artifact tests and migration syntax/parity checks for MySQL and PostgreSQL.
5. Runtime UX proof: latest-main services are available at `http://127.0.0.1:25174/`, but authenticated business-page browser smoke still needs a token/session fixture.

Ledger boundary:

- `shared-specs` remains a coordination ledger only.
- Accepted facts from this section were synchronized back to canonical `osmx` docs in PR #36.

## R10 / P13 Efficiency Gate Completion Summary

Date: 2026-04-22 15:53 CST

Final integration result:

- `osmx` main after closeout: `90e09c3 Merge PR #38: Sync board after efficiency gates`
- Merged PRs:
  - #37 `ops/integration-efficiency-gates` -> `bfef6fa`
  - #38 `docs/post37-board-sync` -> `90e09c3`
- Current open OSMX PRs after closeout: `none`
- Canonical docs sync: `docs/plans/80-wave-execution-board.md`, `docs/plans/90-agent-execution-operating-model.md`, and `docs/guides/document-change-log.md` updated in #37/#38.

Efficiency gates now available:

- `scripts/pr_checklist_lint.py`: lints PR bodies and blocks DB-sensitive PRs that omit checklist evidence.
- `scripts/migration_pair_check.py`: verifies MySQL/PostgreSQL migration artifact pairing, with explicit standalone allow-list for TimescaleDB-only migrations.
- `scripts/runtime_provenance.py`: captures repo commit, branch, dirty state, endpoint health, listener PID, and process cwd for runtime evidence.
- `make integration-efficiency-gate`: runs security scan, migration pair check, DB portability scan, and PR checklist lint.
- GitHub `security-gate`: now runs security scan, migration pair check, DB portability scan, and PR checklist lint on pull requests.

Validation evidence:

- #37 GitHub checks: GitGuardian and `security-gate` passed.
- #38 GitHub checks: GitGuardian and `security-gate` passed.
- Local gate replay: `make integration-efficiency-gate` passed; security scan still reports one existing REVIEW-only public IP in `osmx-go/internal/runbook/worker/register.go`.
- PR lint replay passed against #34, #35, and #36 bodies.
- Latest-main runtime evidence after #38:
  - Worktree: `/Users/apple/Exec/Code/osmx-runtime-main-rebaseline`
  - Commit: `90e09c3`
  - Go: `http://127.0.0.1:8080/api/v1/health` -> 200
  - AI: `http://127.0.0.1:5001/api/v1/ai/health` -> 200
  - Frontend: `http://127.0.0.1:25174/` -> 200
  - `scripts/smoke.sh --mode local-runtime` passed with explicit `GO_BASE_URL`, `AI_BASE_URL`, and `FRONTEND_BASE_URL`.
  - `scripts/runtime_provenance.py` passed and showed all listener cwd values under `/Users/apple/Exec/Code/osmx-runtime-main-rebaseline`.

Next recommended split:

1. P0 datasource factory: implement a narrow Go datasource factory for `osmx-go/internal/app/app.go` and `osmx-go/cmd/emergency/main.go`, with MySQL default and PostgreSQL selectable by config/env.
2. P0 PostgreSQL startup smoke: add a no-migration PostgreSQL service startup smoke path that proves driver selection and health can run against a PostgreSQL DSN.
3. P1 runbook state store boundary: rename or wrap `MySQLStateManager` behind a dialect-neutral interface and keep AutoMigrate limited to dev/bootstrap.
4. P1 main-chain migration artifacts: only after model shape is settled, add paired `003_mainchain_core.mysql.sql` and `003_mainchain_core.postgres.sql`.
5. P1 authenticated browser smoke: add token/session fixture so `25174` can prove logged-in business pages, not only login/public health.

Ledger boundary:

- `shared-specs` remains a coordination ledger only.
- Accepted facts from this section were synchronized back to canonical `osmx` docs in PR #37/#38.

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
