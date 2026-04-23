# Deadline Wave 1 PR Slice Manifest

> Date: 2026-04-23 01:37 CST
> Last refreshed: 2026-04-23 05:24 CST
> Scope: coordination manifest only
> Status basis: `frozen_for_owner_review / GitHub checks passed / decision_ready / current_source_smoke_refreshed / asset_flow_breadth_passed / real_chain_smoke_passed / migration_replay_passed / pass_with_risk`

## 2026-04-23 05:29 CST Clean PR Result / Freeze

PR #44 is open:

```text
https://github.com/Tattao/osmx/pull/44
```

Clean PR branch:

```text
/Users/apple/Exec/Code/osmx-dw1-main-review
dw1/command-asset-main-review
base: github/main@0a07edb
head: 302bfef
```

Manifest correction:

- The 47-file include set below remains the original dirty-worktree source-intent boundary.
- The clean PR has 29 net files because current `github/main` already contains several source-intent files and the migration pair now includes `003_approval_execution_links.sql`.
- `frontend/playwright.config.ts` and `frontend/vite.config.ts` were explicitly admitted into PR #44 as test-runtime config. They fix the reproducibility issue where Playwright could reuse another worktree's Vite server and proxy to an unrelated backend.
- Forbidden/generated paths remain excluded: `osmx-go/emergency`, `osmx-go/server`, `frontend/test-results`, `frontend/dist`.
- GitHub checks on head `302bfef` passed: `security-gate` and `GitGuardian Security Checks`. The credential fix was completed by amending/pushing the GitHub PR branch only; no GitGuardian-side sync or dashboard action was performed.
- PR #44 is frozen for owner review. No more code changes should enter this branch unless owner/reviewer feedback returns the PR.
- Disposable PostgreSQL probe found a follow-up blocker outside the frozen PR scope: runbook AutoMigrate fails on PostgreSQL because `mediumtext` is not a PostgreSQL type, so `osm_runbook_execution` is absent and `003_approval_execution_links.postgres.sql` cannot apply after startup.

Latest clean PR gate:

```bash
git diff --stat github/main..HEAD
git diff --name-only --diff-filter=U
git diff --cached --check
git diff --cached --name-only | rg '(^|/)emergency$|osmx-go/emergency|osmx-go/server|test-results|dist/' && exit 1 || true
```

Result: PR #44 contains 29 files, no unresolved conflicts, no forbidden binary/generated output.

## Purpose

This manifest turns the DW1 review evidence into a practical PR slice boundary.

It does not make the package final merge-ready. It defines what can enter the DW1 main-review PR candidate, what needs owner grouping, and what must stay out.

## PR Candidate Include Set

These files can enter the DW1 main-review PR candidate:

### Backend Main Chain

- `osmx-go/internal/app/app.go`
- `osmx-go/internal/extension/extension.go`
- `osmx-go/internal/plan/extension_test.go`
- `osmx-go/internal/plan/handler/chain_handler.go`
- `osmx-go/internal/plan/extension.go`
- `osmx-go/internal/plan/service/chain_service.go`
- `osmx-go/internal/plan/service/chain_service_test.go`
- `osmx-go/internal/plan/handler/plan_handler.go`
- `osmx-go/internal/api/v1/approval_flow_handler.go`
- `osmx-go/internal/repository/approval_repo.go`
- `osmx-go/internal/repository/approval_repo_test.go`
- `osmx-go/internal/runbook/handler/audit.go`
- `osmx-go/internal/runbook/handler/handler.go`
- `osmx-go/internal/runbook/repository/repository.go`
- `osmx-go/internal/runbook/repository/repository_test.go`
- `osmx-go/internal/runbook/service/service.go`
- `osmx-go/internal/runbook/service/service_test.go`
- `osmx-go/internal/runbook/extension.go`
- `osmx-go/internal/runbook/extension_test.go`
- `osmx-go/internal/runbook/module.go`
- `osmx-go/cmd/emergency/main.go`

### Backend Contract / Migration

- `osmx-go/internal/model/approval.go`
- `osmx-go/internal/runbook/model/model.go`
- `osmx-go/internal/runbook/model/execution_model.go`
- `osmx-go/migrations/003_approval_execution_links.mysql.sql`
- `osmx-go/migrations/003_approval_execution_links.postgres.sql`
- `osmx-go/migrations/003_approval_execution_links.sql`

### Backend Asset Flow

- `osmx-go/internal/runbook/handler/contentpack.go`
- `osmx-go/internal/runbook/handler/contentpack_enrich_test.go`
- `osmx-go/internal/runbook/contentpack/manager.go`
- `osmx-go/internal/runbook/contentpack/manager_test.go`

### Frontend Main Chain

- `frontend/src/router/index.ts`
- `frontend/src/api/approvals.ts`
- `frontend/src/api/runbook.ts`
- `frontend/src/types/runbook.ts`
- `frontend/src/components/layout/Sidebar.vue`
- `frontend/src/views/alerts/EventCenterView.vue`
- `frontend/src/views/plan/PlanListView.vue`
- `frontend/src/views/plan/PlanDetailView.vue`
- `frontend/src/views/runbook/ExecutionListView.vue`
- `frontend/src/views/runbook/PlanDetailView.vue`
- `frontend/src/views/runbook/RunbookListView.vue`
- `frontend/src/views/runbook/ImportedOperationView.vue`
- `frontend/src/views/system/AuditView.vue`

### E2E Evidence

- `frontend/e2e/11-command-center-chain.spec.ts`
- `frontend/e2e/12-command-center-real-chain.spec.ts`
- `frontend/e2e/13-asset-flow-real-breadth.spec.ts`
- `frontend/e2e/14-command-center-plan-binding.spec.ts`

### Test Runtime Config Approved For PR #44

- `frontend/playwright.config.ts`
- `frontend/vite.config.ts`

## Owner Grouping Set

These files should be approved or rejected as grouped boundaries, not silently mixed into the PR candidate:

### Schema / Migration Group

Moved into the PR candidate include set at 2026-04-23 02:17 CST because the main-chain code depends on these fields and migrations as a durable contract.

### Runtime Robustness Group

- `osmx-go/internal/runbook/compiler/afl/compiler.go`
- `osmx-go/internal/runbook/compiler/afl/compiler_test.go`
- `osmx-go/internal/runbook/engine/engine_test.go`
- `osmx-go/internal/runbook/engine/event_bus.go`
- `osmx-go/internal/runbook/engine/mysql_state.go`
- `osmx-go/internal/runbook/engine/resilience_test.go`
- `osmx-go/internal/runbook/schedule/scheduler.go`
- `osmx-go/internal/runbook/schedule/scheduler_test.go`
- `osmx-go/internal/runbook/handler/oorestv2.go`
- `osmx-go/internal/runbook/handler/trigger.go`

### Frontend Boundary Group

- `frontend/src/views/runbook/FlowDesignerView.vue`
- `frontend/src/components/flow/PropertyPanel.vue`

## Exclude Set

These files must not enter the DW1 product-source PR slice:

- `osmx-go/emergency`
- `AGENTS.md`
- `docs/plans/osmx-dual-repo-agent-operator-runbook.md`
- `docs/plans/osmx-dual-repo-wave-board.md`
- `frontend/src/api/collectors.ts`
- `frontend/src/api/license.ts`
- `frontend/src/api/topology.ts`
- `frontend/src/stores/skill.ts`
- `frontend/src/views/ai/SQLOptimizeView.vue`
- `frontend/src/views/databases/DatabaseDetailView.vue`
- `frontend/src/views/license/IntegrityView.vue`
- `frontend/src/views/onboarding/OnboardingWizardView.vue`
- `frontend/src/views/runbook/WorkerListView.vue`
- `frontend/src/views/runbook/components/PropertyPanel.vue`
- `frontend/src/views/system/BackupView.vue`
- `frontend/src/views/system/CredentialView.vue`
- `frontend/src/views/tasks/TaskListView.vue`

## Required Pre-PR Gates

Before opening or accepting a DW1 PR candidate:

1. Confirm `osmx-go/emergency` is not staged.
2. Confirm the PR includes only the PR candidate include set plus explicitly owner-approved grouped files.
3. Re-run focused Go tests:
   - `go test ./internal/runbook/handler ./internal/runbook/contentpack ./internal/plan/... ./internal/runbook/service ./internal/runbook/repository`
4. Re-run or explicitly cite current-source Asset & Flow proof:
   - `VITE_API_PROXY_TARGET=http://127.0.0.1:<current-source-port> E2E_BACKEND_BASE_URL=http://127.0.0.1:<current-source-port> npx playwright test e2e/13-asset-flow-real-breadth.spec.ts --reporter=list`
5. If `18081` is used, restart it from current source first; otherwise keep treating it as an old-process risk.
6. Re-run whitespace checks for implementation, `osmx` docs, and `shared-specs`.

## Current Dirty Coverage Audit

Audit time: 2026-04-23 01:38 CST.

Command:

```bash
comm -23 <(git status --porcelain=v1 | sed 's/^...//' | sort) <(perl -ne 'while(/`([^`]+)`/g){print "$1\n"}' /Users/apple/Exec/Code/shared-specs/deadline-wave1-pr-slice-manifest.md | sort -u)
```

Result: no output.

Interpretation: every current dirty path in `/Users/apple/Exec/Code/osmx-emergency-main-sync` is covered by this manifest as include, owner grouping, or exclude. The remaining risk is not an unclassified file; it is enforcing the manifest during staging and PR creation.

## Historical Dirty-Worktree Staging Gate Audit

Audit time: 2026-04-23 04:30 CST.

Commands:

```bash
git status --porcelain=v1
git diff --cached --name-only
git diff --cached --name-only | wc -l
git diff --cached --name-only | grep -Fx 'osmx-go/emergency' && exit 1 || true
```

Current result: forbidden-binary gate is clean; staged set contains exactly `47` files and matches the DW1 main-review candidate include set.

Initial audit observed staged `osmx-go/emergency`, which is a forbidden binary and must not enter any DW1 PR candidate. It was removed from the staged set with `git restore --staged osmx-go/emergency`; the working-tree file remains modified and was not reverted.

The schema/model/migration group is no longer split in the staged candidate. The model files and both migration files are staged together as the owner-approved DW1 contract boundary.

Current staged classification:

| Class | Staged paths |
|-------|--------------|
| Include candidate | 47 staged files from the PR Candidate Include Set above, including schema/model/migration group and focused E2E specs |
| Owner grouping staged | none outside the include set |
| Forbidden staged | none |

Historical action was completed through the clean PR path. Do not open a direct PR from `batch/full-integration`.

Current required action for PR #44: keep the branch frozen on `/Users/apple/Exec/Code/osmx-dw1-main-review`, preserve the 29-file clean branch boundary unless owner feedback requires a scoped patch, and rerun the forbidden/generated-output gate before each push.

## Owner Decision Point

The recommended owner decision is:

```text
accept main-review package / frozen for owner review / keep pass_with_risk / do not declare final merge-ready
```

The owner should return PR #44 for fixes if any excluded file leaks into the candidate, if schema/migration grouping is split accidentally, or if current-source smoke proof cannot be refreshed.
