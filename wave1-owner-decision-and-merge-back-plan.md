# Wave 1 Owner Decision And Merge-Back Plan

> Date: 2026-04-21 21:45 CST
> Owner scope: `/Users/apple/Exec/Code/osmx`
> Implementation scope: `/Users/apple/Exec/Code/osmx-emergency-main-sync`
> Decision input: `shared-specs/wave1-main-repo-evaluation.md`
> Execution update: PR #2 merged to `main` at `2026-04-21 22:35 CST`, merge commit `ae2be3b`; docs-only closeout PR #3 merged at `2026-04-21 22:41 CST`; docs-only runbook-state PR #4 merged at `2026-04-21 23:07 CST`; docs-only shared-specs boundary PR #5 merged at `2026-04-21 23:22 CST`; current `origin/main` `57534c9`

## 1. Owner Decision

Wave:

```text
Wave 1 - WP1 main-chain contract closure + WP2/WP3 minimal smoke
```

Owner verdict:

```text
已合回 main
```

Decision meaning:

```text
Wave 1 passed main-repo acceptance, moved through the reviewed merge-back plan,
and was merged into main via PR #2.
```

Wave 2 status:

```text
blocked until a new Wave 2 mother task brief is written and dispatched
```

## 2. Current Repository Facts

Active workspace:

```text
/Users/apple/Exec/Code
```

Current checked-out branches:

```text
osmx:                     batch/full-integration @ 5db87c3
osmx-emergency-main-sync: batch/full-integration @ 5db87c3
```

Important remote topology:

```text
osmx origin:                     https://github.com/Tattao/osmx.git
osmx-emergency-main-sync origin: /Users/apple/Exec/Code/osmx
```

Implication:

```text
The practical merge-back target is `main` in the `osmx` repository.
Use a clean main worktree or PR branch. Do not perform a blind merge inside the current dirty implementation worktree.
```

## 3. Merge-Back Strategy

Recommended strategy:

```text
Use reviewed PR slices, not one blind direct merge.
```

Rationale:

1. `osmx-emergency-main-sync` contains a substantial dirty Wave 1 diff.
2. Some files have both staged and unstaged changes, so attribution must be normalized before commit.
3. `osmx` has unrelated untracked PDF/upload artifacts that must be excluded from Wave 1.
4. The Wave 1 acceptance proof is strong enough to proceed, but the merge mechanics still need review discipline.

## 4. Proposed PR Slices

### PR 1 - Backend Main Chain And Runtime Stability

Purpose:

```text
Land Plan -> Approval -> AssetExecution -> Artifact -> Audit backend closure and runtime blocker fixes.
```

Primary files:

```text
osmx-go/cmd/emergency/main.go
osmx-go/internal/api/v1/approval_flow_handler.go
osmx-go/internal/model/approval.go
osmx-go/internal/plan/handler/plan_handler.go
osmx-go/internal/plan/handler/chain_handler.go
osmx-go/internal/plan/service/chain_service.go
osmx-go/internal/plan/service/chain_service_test.go
osmx-go/internal/repository/approval_repo.go
osmx-go/internal/runbook/extension.go
osmx-go/internal/runbook/handler/audit.go
osmx-go/internal/runbook/handler/handler.go
osmx-go/internal/runbook/handler/oorestv2.go
osmx-go/internal/runbook/handler/trigger.go
osmx-go/internal/runbook/model/model.go
osmx-go/internal/runbook/repository/repository.go
osmx-go/internal/runbook/schedule/scheduler.go
osmx-go/internal/runbook/schedule/scheduler_test.go
osmx-go/internal/runbook/service/service.go
osmx-go/internal/runbook/compiler/afl/compiler.go
osmx-go/internal/runbook/compiler/afl/compiler_test.go
osmx-go/internal/runbook/engine/event_bus.go
osmx-go/internal/runbook/engine/engine_test.go
osmx-go/internal/runbook/engine/mysql_state.go
osmx-go/internal/runbook/engine/resilience_test.go
```

Special review note:

```text
`osmx-go/internal/runbook/model/execution_model.go` is deleted in the implementation diff.
Review this deletion together with `model.go` before merging.
```

Required validation:

```bash
cd /Users/apple/Exec/Code/osmx-emergency-main-sync/osmx-go
go build -tags 'plan runbook' -o /tmp/osmx-wave1-cmd-server ./cmd/server
go test -tags 'plan runbook' ./cmd/emergency ./internal/runbook/engine ./internal/runbook/compiler/afl ./internal/runbook/service ./internal/runbook/handler ./internal/runbook/acceptance ./internal/plan/... -count=1
```

### PR 2 - Frontend Command Center Minimal Chain

Purpose:

```text
Land the minimal Command Center path and execution/result backflow views.
```

Primary files:

```text
frontend/src/api/approvals.ts
frontend/src/api/runbook.ts
frontend/src/components/layout/Sidebar.vue
frontend/src/router/index.ts
frontend/src/types/runbook.ts
frontend/src/views/alerts/EventCenterView.vue
frontend/src/views/plan/PlanListView.vue
frontend/src/views/plan/PlanDetailView.vue
frontend/src/views/runbook/ExecutionListView.vue
frontend/src/views/runbook/PlanDetailView.vue
frontend/src/views/runbook/RunbookListView.vue
frontend/e2e/11-command-center-chain.spec.ts
frontend/vite.config.ts
```

Required validation:

```bash
cd /Users/apple/Exec/Code/osmx-emergency-main-sync/frontend
npm run build:check
```

Runtime smoke evidence to preserve in PR description:

```text
/command-center/plans
/command-center/plans/37bdb9bd-07c4-41f8-aa38-b1ec4b343051
/approvals
/audit-logs
/runbook/executions
```

### PR 3 - Frontend Build-Gate Debt Cleanup

Purpose:

```text
Keep `npm run build:check` green by landing unrelated-but-required type/API cleanup separately.
```

Primary files:

```text
frontend/src/api/collectors.ts
frontend/src/api/license.ts
frontend/src/api/topology.ts
frontend/src/components/flow/PropertyPanel.vue
frontend/src/stores/skill.ts
frontend/src/views/ai/SQLOptimizeView.vue
frontend/src/views/databases/DatabaseDetailView.vue
frontend/src/views/license/IntegrityView.vue
frontend/src/views/onboarding/OnboardingWizardView.vue
frontend/src/views/runbook/FlowDesignerView.vue
frontend/src/views/runbook/ImportedOperationView.vue
frontend/src/views/runbook/WorkerListView.vue
frontend/src/views/runbook/components/PropertyPanel.vue
frontend/src/views/system/AuditView.vue
frontend/src/views/system/BackupView.vue
frontend/src/views/system/CredentialView.vue
frontend/src/views/tasks/TaskListView.vue
```

Required validation:

```bash
cd /Users/apple/Exec/Code/osmx-emergency-main-sync/frontend
npm run build:check
```

Review note:

```text
This PR should not be used to introduce new Studio / OO / Worker feature scope.
It exists to keep the Wave 1 frontend acceptance gate reproducible.
```

### PR 4 - Docs And Operator State

Purpose:

```text
Land the Wave 1 status board and merge-back decision records.
```

Primary files:

```text
osmx/docs/plans/osmx-dual-repo-wave-board.md
shared-specs/wave1-emergency-owner-summary-package.md
shared-specs/wave1-main-repo-evaluation.md
shared-specs/wave1-owner-decision-and-merge-back-plan.md
shared-specs/current-baseline-assessment.md
shared-specs/README.md
```

Review note:

```text
`shared-specs` is outside the osmx Git repository in the current workspace and should be versioned as an independent collaboration evidence repository.
If this needs to be versioned with osmx, copy or mount it intentionally rather than assuming it is part of the osmx commit.
```

## 5. Exclusions

Do not include these in Wave 1 merge-back:

```text
/Users/apple/Exec/Code/osmx/docs/Automation_Center_26.1/*.pdf
/Users/apple/Exec/Code/osmx/osmx-go/data/uploads/uploads/2026/04/19/*.pdf
```

Do not start these tasks before merge-back decision is executed:

1. Wave 2 feature work.
2. New Studio interaction expansion.
3. Deep OO/JAR compatibility expansion.
4. Batch 8 / cloud platform recovery.
5. Broad refactors not required by Wave 1.

## 6. Suggested Execution Commands

Use a clean main worktree for the final merge review:

```bash
cd /Users/apple/Exec/Code/osmx
git fetch origin
git worktree add ../osmx-main-merge origin/main
```

Bring the implementation branch into the clean merge worktree for review.
Because the implementation repo currently points at local `osmx`, prefer an explicit fetch source:

```bash
cd /Users/apple/Exec/Code/osmx-main-merge
git fetch /Users/apple/Exec/Code/osmx-emergency batch/full-integration:refs/remotes/emergency/batch-full-integration
git switch -c wave1-merge-back origin/main
```

Then apply the approved PR slice strategy.

Validation after each slice:

```bash
cd /Users/apple/Exec/Code/osmx-main-merge/osmx-go
go build -tags 'plan runbook' -o /tmp/osmx-wave1-cmd-server ./cmd/server
go test -tags 'plan runbook' ./cmd/emergency ./internal/runbook/engine ./internal/runbook/compiler/afl ./internal/runbook/service ./internal/runbook/handler ./internal/runbook/acceptance ./internal/plan/... -count=1
```

```bash
cd /Users/apple/Exec/Code/osmx-main-merge/frontend
npm run build:check
```

Final gate before merge:

```bash
git diff --name-only --diff-filter=U
git status --short
```

## 7. Final State For Wave Board

The Wave 1 board should now move to:

```text
merged_to_main
```

Meaning:

```text
Main-repo acceptance passed, PR #2 was merged to main, and the next work is
Wave 1 evidence closeout plus Wave 2 task-brief preparation, not immediate
new feature development.
```
