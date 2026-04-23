# Stage 1 Parallel Agent Execution Board

> Date: 2026-04-22
> Purpose: maximize safe parallel development across OSMX Stage 1 without turning `shared-specs` into a product source of truth.

## Current Baseline

- `osmx` GitHub main: `40d0a73`
- `shared-specs` main before this board: `6451fac`
- Final product facts remain in `osmx`.
- `shared-specs` records coordination evidence, task ownership, and handoffs only.

## Deadline Wave 2 Active Overlay

Date: 2026-04-23 11:41 CST

This board predates the 2026-05-15 deadline plan. The active deadline lane is now tracked in:

- `osmx/docs/plans/osmx-product-deadline-2026-05-15-delivery-plan.md`
- `osmx/docs/plans/osmx-deadline-wave1-command-asset-task-pack.md`
- `shared-specs/infrastructure/task-queue.yaml`
- `shared-specs/codex-handoff-20260423-dw2.md`
- `shared-specs/deadline-wave1-command-asset-dispatch.md`

Current deadline status:

```text
PR #44 merged / PR #45 merged / PR #46 merged / Track B LLM passed / Track C deterministic SLA passed / Track C real Qdrant passed_after_seed / Track D pass_with_environment_notes / DW2-DOC PR #48 ready / cleanup no_removals
```

Verified main baseline:

```text
origin/main = d0c0a00b4e25f3c26175d8758dab5f99f6fdf6e0
```

Remaining bounded work:

- Track C: completed. Qdrant seed and real-mode SLA rerun passed from clean worktree `/Users/apple/Exec/Code/osmx-knowledge-sla-seed`.
- Track D: pass with environment notes. Go builder and Qdrant healthcheck are fixed, frontend builds with local `nginx:latest`, old MySQL volume credentials were triaged without recording secrets, and the alternate-port full-stack health path passed.
- DW2-DOC: completed in `/Users/apple/Exec/Code/osmx-main-merge`; PR #48 opened for canonical wave board and document change log sync, and checks passed after PR body checklist formatting was fixed.
- DW2-INT cleanup: completed with no removals; active validation worktrees contain evidence and reports, and `osmx-main-merge` carries PR #48.
- Next continuation: keep PR #48 as a human merge decision, while dispatching the non-PR-watch work in parallel: Track C productization/archive, Track D Compose fresh-volume/default-port hardening, and current-main PostgreSQL apply/runtime smoke.

Context-limit rule: do not run Track D and Track C remediation in the same fragile long context. Update `codex-handoff-20260423-dw2.md` after each bounded step.

## Worktree Matrix

| Track | Worktree | Branch | Baseline | Purpose |
|------|----------|--------|----------|---------|
| A. Incident Commander Wave 2 | `/Users/apple/Exec/Code/osmx-emergency-main-sync-wave2` | `wave2/command-center-governed-loop` | `40d0a73` | Command Center governed loop hardening |
| B. DB Copilot Productization | `/Users/apple/Exec/Code/osmx-db-copilot-productization` | `stage1/db-copilot-productization` | `40d0a73` | real LLM E2E and DB Copilot productization gate |
| C. Knowledge SLA | `/Users/apple/Exec/Code/osmx-knowledge-sla` | `stage1/knowledge-sla-baseline` | `40d0a73` | retrieval quality and latency baseline |
| D. Delivery/Ops | `/Users/apple/Exec/Code/osmx-delivery-ops` | `stage1/delivery-ops-hardening` | `40d0a73` | standard deployment, smoke, and reproducible runtime |
| E. Security/Release Gate | `/Users/apple/Exec/Code/osmx-security-release` | `stage1/security-release-gate` | `40d0a73` | secret scanning, release gate, and credential hygiene evidence |
| F. Integration/Regression | `/Users/apple/Exec/Code/osmx-integration-regression` | `stage1/integration-regression-captain` | `40d0a73` | integration queue, merge readiness, and regression orchestration |
| G. Studio / OO Compatibility | `/Users/apple/Exec/Code/osmx-studio-oo-compatibility` | `stage1/studio-oo-compatibility` | `40d0a73` | bounded Studio / OO compatibility track for user-demanded imported asset usability |

## Dispatch Rules

1. Every Agent must state its target worktree before editing.
2. Agents may read other worktrees, but must only write inside their assigned worktree unless explicitly reassigned.
3. `shared-specs` is coordination evidence only. Do not import, clone, submodule, or depend on it from product code, tests, build, CI, or runtime.
4. Studio / OO / Worker / Hermes work is allowed only when directly required by the `Command Center Governed Loop`, or when explicitly scoped as the separate `G. Studio / OO Compatibility` track. G-track work must still feed `PlanStep / AssetExecution / Artifact / Audit` contracts and must not become a second product fact source.
5. Each worktree should produce its own branch / PR. Integration only happens through reviewed PRs into `osmx`.
6. Broad rewrites, naming churn, generated artifacts, binary outputs, and unrelated cleanup are out of scope.

## Agent Groups

### Group A: Incident Commander Wave 2

Worktree: `/Users/apple/Exec/Code/osmx-emergency-main-sync-wave2`

Canonical task brief:

```text
docs/plans/70-wave-2-command-center-governed-loop.md
```

| Agent | Role | Write Scope | Deliverable |
|------|------|-------------|-------------|
| A1 | Backend State Machine | `osmx-go/internal/plan`, approval-related Go code/tests | plan/approval/execution invariants and denied path |
| A2 | Execution Evidence | `osmx-go/internal/runbook`, audit/artifact/timeline projection code/tests | failed/cancelled/timed_out paths, artifact provenance, audit events |
| A3 | Command Center UI | `frontend/src/views/plan`, approvals/audit/runbook execution views, related API/types | minimal chain/timeline explanation |
| A4 | Wave 2 Evaluation | `frontend/e2e`, focused Go tests, test reports | happy / denied / failed / idempotent / restart evidence |

### Group B: DB Copilot Productization

Worktree: `/Users/apple/Exec/Code/osmx-db-copilot-productization`

| Agent | Role | Write Scope | Deliverable |
|------|------|-------------|-------------|
| B1 | Real LLM E2E Smoke | `osmx-ai`, AI smoke scripts/docs | repeatable real LLM smoke path and fallback evidence |
| B2 | DB Copilot Acceptance | `docs/plans`, `docs/reference`, focused smoke scripts | productization gate checklist and PoC path |
| B3 | DB Copilot UX Surface | DB/AI frontend views and API clients only | minimal user-facing DB Copilot flow polish |

### Group C: Knowledge SLA

Worktree: `/Users/apple/Exec/Code/osmx-knowledge-sla`

| Agent | Role | Write Scope | Deliverable |
|------|------|-------------|-------------|
| C1 | Retrieval Benchmark | `osmx-ai/app/agent_runtime/knowledge`, `osmx-ai/tests` | repeatable retrieval latency/quality benchmark |
| C2 | Knowledge Health API/Docs | Go/Python knowledge health endpoints/docs as needed | SLA baseline surfaced as checkable evidence |

### Group D: Delivery/Ops

Worktree: `/Users/apple/Exec/Code/osmx-delivery-ops`

| Agent | Role | Write Scope | Deliverable |
|------|------|-------------|-------------|
| D1 | Standard Runtime | `docker`, `deploy`, config examples, scripts | reproducible start/stop/smoke procedure |
| D2 | Smoke Automation | scripts/tests/docs only | one-command health/API smoke where possible |

### Group E: Security/Release Gate

Worktree: `/Users/apple/Exec/Code/osmx-security-release`

| Agent | Role | Write Scope | Deliverable |
|------|------|-------------|-------------|
| E1 | Secret Scan Gate | CI/scripts/docs only | repeatable high-risk secret scan gate |
| E2 | Release Checklist | release docs and validation records | release readiness checklist including credential rotation status |

### Group F: Integration/Regression

Worktree: `/Users/apple/Exec/Code/osmx-integration-regression`

| Agent | Role | Write Scope | Deliverable |
|------|------|-------------|-------------|
| F1 | Merge Captain | docs/coordination and PR queue records | PR order, conflict map, owner handoff |
| F2 | Regression Captain | test orchestration docs/scripts | consolidated build/test/smoke matrix |

### Group G: Studio / OO Compatibility

Worktree: `/Users/apple/Exec/Code/osmx-studio-oo-compatibility`

Priority reason: near-term user demand for Studio / OO imported asset usability is high enough to run in parallel, but this track must not interrupt Wave 2 Command Center governed loop hardening.

Allowed scope:

- OO Content Pack / JAR imported asset usability.
- Operation / Flow correct routing and readonly viewers.
- Compatibility status and projection/readiness evidence.
- Imported asset execution bridge that remains governed by `PlanStep / AssetExecution / Artifact / Audit`.
- Studio wrapper/subflow bridge placeholders that do not attempt full OO Studio parity.

Forbidden scope:

- Full OO Studio clone.
- OO-compatible export.
- Generic plugin marketplace.
- Bypassing Approval / Audit for imported asset execution.
- Making Studio / OO a second fact source outside `osmx`.

| Agent | Role | Write Scope | Deliverable |
|------|------|-------------|-------------|
| G1 | Compatibility Contract | `docs/plans`, `docs/reference`, change log | priority ruling, boundary, acceptance, task split |
| G2 | Backend Compatibility | content pack, AFL/CloudSlang compiler, projection/resolver tests | highest-value OO compatibility gap closure |
| G3 | Frontend Compatibility | Content Pack / Imported Operation / Imported Flow / Runbook list views | correct routing, compatibility status, readonly explanation |
| G4 | Compatibility Evaluation | focused frontend/backend tests and reports | validation matrix and no-regression evidence |

## First-Wave Startup Prompts

### A1 Backend State Machine

```text
Worktree: /Users/apple/Exec/Code/osmx-emergency-main-sync-wave2

Read docs/plans/70-wave-2-command-center-governed-loop.md first.

Implement only the backend invariants for Plan / Approval / AssetExecution:
- unapproved Plan must not create AssetExecution
- denied/rejected Approval must not create AssetExecution
- AssetExecution must bind plan_id / plan_step_id / approval_id where the current schema permits
- key transitions must create AuditEvent or testable audit evidence

Do not expand Studio / OO / Worker / Hermes. List changed files and validation commands.
```

### A2 Execution Evidence

```text
Worktree: /Users/apple/Exec/Code/osmx-emergency-main-sync-wave2

Read docs/plans/70-wave-2-command-center-governed-loop.md first.

Implement or harden failed / cancelled / timed_out execution semantics, minimal artifact provenance, and backend timeline projection evidence.

Stay inside runbook/execution/audit/artifact related code. Do not add generic workflow builder behavior.
```

### A3 Command Center UI

```text
Worktree: /Users/apple/Exec/Code/osmx-emergency-main-sync-wave2

Read docs/plans/70-wave-2-command-center-governed-loop.md first.

Build the minimal Command Center chain explanation:
Plan -> Approval -> AssetExecution -> Artifact -> Audit.

Use existing views/routes/components where possible. Do not expand Studio / OO pages.
```

### A4 Wave 2 Evaluation

```text
Worktree: /Users/apple/Exec/Code/osmx-emergency-main-sync-wave2

Read docs/plans/70-wave-2-command-center-governed-loop.md first.

Create or extend focused tests/smoke evidence for:
- happy path
- denied path
- failed path
- idempotency path
- restart/state stability path

Do not implement product features beyond test scaffolding needed for verification.
```

### B1 Real LLM E2E Smoke

```text
Worktree: /Users/apple/Exec/Code/osmx-db-copilot-productization

Focus on DB Copilot productization gate:
real LLM E2E smoke, clear fallback behavior, and repeatable validation.

Do not touch Incident Commander Wave 2 code.
```

### C1 Knowledge SLA

```text
Worktree: /Users/apple/Exec/Code/osmx-knowledge-sla

Focus on Knowledge / RAG SLA baseline:
retrieval latency, quality sample set, failure mode, and repeatable benchmark.

Do not change product strategy docs except for focused SLA evidence.
```

### D1 Standard Runtime

```text
Worktree: /Users/apple/Exec/Code/osmx-delivery-ops

Focus on standard deployment/runtime reproducibility:
config examples, startup commands, health checks, and smoke commands.

Do not reintroduce real credentials or private infrastructure addresses.
```

### E1 Secret Scan Gate

```text
Worktree: /Users/apple/Exec/Code/osmx-security-release

Focus on a repeatable security/release gate:
high-risk secret scan, private host scan, release checklist, and credential rotation evidence hooks.

Do not add runtime dependencies or external secret services without approval.
```

### F1 Integration Captain

```text
Worktree: /Users/apple/Exec/Code/osmx-integration-regression

Create the integration queue:
PR order, file ownership map, regression matrix, and conflict risks across A/B/C/D/E tracks.

Do not change business code.
```

## Current Start Recommendation

Start these Agents immediately:

- A1, A2, A3, A4
- B1
- C1
- D1
- E1
- F1

Hold B2/B3/C2/D2/E2/F2 until the first wave reports file ownership and initial validation results.

After the first wave completed, G1/G2/G3/G4 were dispatched as a bounded compatibility track because Studio / OO imported asset usability is now treated as a near-term user-demand lane. This does not change the fact that Wave 2 Incident Commander remains the primary governed-loop delivery track.

## PR Queue Created

Recommended merge/review order:

1. D Delivery/Ops: [Tattao/osmx#10](https://github.com/Tattao/osmx/pull/10)
2. E Security/Release Gate: [Tattao/osmx#11](https://github.com/Tattao/osmx/pull/11)
3. C Knowledge SLA: [Tattao/osmx#12](https://github.com/Tattao/osmx/pull/12)
4. B DB Copilot Productization: [Tattao/osmx#13](https://github.com/Tattao/osmx/pull/13)
5. A Incident Commander Wave 2: [Tattao/osmx#14](https://github.com/Tattao/osmx/pull/14)
6. G Studio / OO Compatibility: [Tattao/osmx#15](https://github.com/Tattao/osmx/pull/15)

Notes:

- PR #15 is intentionally after PR #14 because both touch runbook-facing model/frontend surfaces and should not compete with the governed-loop hardening review.
- Existing PR #1 (`batch/full-integration`) is legacy and is not part of this Stage 1 parallel queue.

## Deadline Wave 1 Dispatch Overlay

Date: 2026-04-22 20:43 CST

This overlay supersedes the old PR #10-#15 startup recommendation for the next execution step. The historical queue above remains useful as context, but the active 2026-05-15 product-deadline dispatch is now:

```text
Deadline Wave 1 - Command Center + Asset & Flow Center P0 收口
```

Canonical product source:

```text
/Users/apple/Exec/Code/osmx/docs/plans/osmx-deadline-wave1-command-asset-task-pack.md
```

Coordination ledger:

```text
/Users/apple/Exec/Code/shared-specs/deadline-wave1-command-asset-dispatch.md
```

Active lanes:

| Lane | Role | Worktree | First action | Status |
|------|------|----------|--------------|--------|
| DW1-OWNER | emergency owner | `/Users/apple/Exec/Code/osmx-emergency-main-sync` | triage dirty baseline and split backend/frontend/evaluation tasks | `done` |
| DW1-BE | backend Agent | `/Users/apple/Exec/Code/osmx-emergency-main-sync` | main-chain API, asset projection, artifact/audit linkage | `in_progress` |
| DW1-FE | frontend Agent | `/Users/apple/Exec/Code/osmx-emergency-main-sync` | Command Center path, Asset & Flow Center, viewer split, Run Explorer | `in_progress` |
| DW1-EVAL | evaluation Agent | `/Users/apple/Exec/Code/osmx-emergency-main-sync` | build / build:check / smoke / regression verdict | `in_progress` |
| DW1-DOC | docs/contract Agent | `osmx` + `shared-specs` | task pack, board, ledger, change log | `done` |

Start rule:

- DW1-OWNER triage is recorded in `deadline-wave1-owner-baseline-triage.md`; implementation lanes may continue within the listed boundaries.
- Do not let the old Wave 1 merge result count as this deadline wave's acceptance evidence.
- Do not let `shared-specs` become a runtime, build, test, CI, or submodule dependency.

Early validation:

- `go test ./internal/plan/...` passed.
- `npm run build:check` passed.
- Focused mock Playwright smoke `e2e/11-command-center-chain.spec.ts` passed.
- Focused plan/runbook Go tests passed.
- Approval/execution linkage migration pair was added under `osmx-go/migrations`.
- MySQL local live apply passed; MySQL and PostgreSQL temporary replay passed twice.
- Backend real-chain smoke passed against `cmd/emergency` at `http://127.0.0.1:18081`.
- Non-mock frontend real-chain Playwright smoke `e2e/12-command-center-real-chain.spec.ts` passed with `VITE_API_PROXY_TARGET=http://127.0.0.1:18081`.
- `git diff --check` passed across implementation, plan/status docs, and ledger docs.
- Status has moved past the old owner-review state: PR #44, PR #45, and PR #46 are merged. The active blockers are now Track D Docker Compose delivery validation and Track C Qdrant seed plus real-mode SLA rerun.
