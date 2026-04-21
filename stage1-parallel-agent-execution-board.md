# Stage 1 Parallel Agent Execution Board

> Date: 2026-04-22
> Purpose: maximize safe parallel development across OSMX Stage 1 without turning `shared-specs` into a product source of truth.

## Current Baseline

- `osmx` GitHub main: `40d0a73`
- `shared-specs` main before this board: `6451fac`
- Final product facts remain in `osmx`.
- `shared-specs` records coordination evidence, task ownership, and handoffs only.

## Worktree Matrix

| Track | Worktree | Branch | Baseline | Purpose |
|------|----------|--------|----------|---------|
| A. Incident Commander Wave 2 | `/Users/apple/Exec/Code/osmx-emergency-main-sync-wave2` | `wave2/command-center-governed-loop` | `40d0a73` | Command Center governed loop hardening |
| B. DB Copilot Productization | `/Users/apple/Exec/Code/osmx-db-copilot-productization` | `stage1/db-copilot-productization` | `40d0a73` | real LLM E2E and DB Copilot productization gate |
| C. Knowledge SLA | `/Users/apple/Exec/Code/osmx-knowledge-sla` | `stage1/knowledge-sla-baseline` | `40d0a73` | retrieval quality and latency baseline |
| D. Delivery/Ops | `/Users/apple/Exec/Code/osmx-delivery-ops` | `stage1/delivery-ops-hardening` | `40d0a73` | standard deployment, smoke, and reproducible runtime |
| E. Security/Release Gate | `/Users/apple/Exec/Code/osmx-security-release` | `stage1/security-release-gate` | `40d0a73` | secret scanning, release gate, and credential hygiene evidence |
| F. Integration/Regression | `/Users/apple/Exec/Code/osmx-integration-regression` | `stage1/integration-regression-captain` | `40d0a73` | integration queue, merge readiness, and regression orchestration |

## Dispatch Rules

1. Every Agent must state its target worktree before editing.
2. Agents may read other worktrees, but must only write inside their assigned worktree unless explicitly reassigned.
3. `shared-specs` is coordination evidence only. Do not import, clone, submodule, or depend on it from product code, tests, build, CI, or runtime.
4. Studio / OO / Worker / Hermes work is allowed only when directly required by the `Command Center Governed Loop`.
5. Each worktree should produce its own branch / PR. Integration only happens through reviewed PRs into `osmx`.
6. Broad rewrites, naming churn, generated artifacts, binary outputs, and unrelated cleanup are out of scope.

## Agent Groups

### Group A: Incident Commander Wave 2

Worktree: `/Users/apple/Exec/Code/osmx-emergency-main-sync-wave2`

Canonical task brief:

```text
docs/plans/wave-2-command-center-governed-loop.md
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

## First-Wave Startup Prompts

### A1 Backend State Machine

```text
Worktree: /Users/apple/Exec/Code/osmx-emergency-main-sync-wave2

Read docs/plans/wave-2-command-center-governed-loop.md first.

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

Read docs/plans/wave-2-command-center-governed-loop.md first.

Implement or harden failed / cancelled / timed_out execution semantics, minimal artifact provenance, and backend timeline projection evidence.

Stay inside runbook/execution/audit/artifact related code. Do not add generic workflow builder behavior.
```

### A3 Command Center UI

```text
Worktree: /Users/apple/Exec/Code/osmx-emergency-main-sync-wave2

Read docs/plans/wave-2-command-center-governed-loop.md first.

Build the minimal Command Center chain explanation:
Plan -> Approval -> AssetExecution -> Artifact -> Audit.

Use existing views/routes/components where possible. Do not expand Studio / OO pages.
```

### A4 Wave 2 Evaluation

```text
Worktree: /Users/apple/Exec/Code/osmx-emergency-main-sync-wave2

Read docs/plans/wave-2-command-center-governed-loop.md first.

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

