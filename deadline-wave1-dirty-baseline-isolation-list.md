# Deadline Wave 1 Dirty Baseline Isolation List

> Date: 2026-04-23 01:00 CST
> Last refreshed: 2026-04-23 05:29 CST
> Basis: `deadline-wave1-command-asset-dispatch.md` and `deadline-wave1-owner-baseline-triage.md`
> Scope: coordination evidence only. Final product/source truth remains in `osmx`.

## Purpose

This file isolates the DW1 dirty baseline so main-chain review does not absorb peripheral debt, binary artifacts, or owner-decision items.

Latest freeze state: clean GitHub PR #44 is frozen for owner review on head `302bfef` with 29 net files and passing GitHub checks. The dirty `osmx-emergency-main-sync` baseline remains source intent only and must not be used for direct PR commits.

PostgreSQL note: disposable PostgreSQL probe reached health/login but runbook AutoMigrate failed on `mediumtext`, leaving `osm_runbook_execution` absent. Keep PostgreSQL runtime/apply closure as a separate follow-up lane, not a reason to pull extra dirty files into PR #44.

The intended split is:

1. DW1 main-chain package.
2. Owner decision package.
3. Post-isolation package.
4. Forbidden merge binaries.

## DW1 Main-Chain Keep Set

Keep these in the main-chain package:

| Area | Files |
|------|-------|
| Backend | `osmx-go/internal/app/app.go` |
| Backend | `osmx-go/internal/extension/extension.go` |
| Backend | `osmx-go/internal/plan/extension.go` |
| Backend | `osmx-go/internal/plan/extension_test.go` |
| Backend | `osmx-go/internal/plan/handler/chain_handler.go` |
| Backend | `osmx-go/internal/plan/service/chain_service.go` |
| Backend | `osmx-go/internal/plan/service/chain_service_test.go` |
| Backend | `osmx-go/internal/plan/handler/plan_handler.go` |
| Backend | `osmx-go/internal/api/v1/approval_flow_handler.go` |
| Backend | `osmx-go/internal/repository/approval_repo.go` |
| Backend | `osmx-go/internal/repository/approval_repo_test.go` |
| Backend | `osmx-go/internal/runbook/handler/audit.go` |
| Backend | `osmx-go/internal/runbook/handler/contentpack.go` |
| Backend | `osmx-go/internal/runbook/handler/contentpack_enrich_test.go` |
| Backend | `osmx-go/internal/runbook/handler/handler.go` |
| Backend | `osmx-go/internal/runbook/contentpack/manager.go` |
| Backend | `osmx-go/internal/runbook/contentpack/manager_test.go` |
| Backend | `osmx-go/internal/runbook/repository/repository.go` |
| Backend | `osmx-go/internal/runbook/repository/repository_test.go` |
| Backend | `osmx-go/internal/runbook/service/service.go` |
| Backend | `osmx-go/internal/runbook/service/service_test.go` |
| Backend | `osmx-go/internal/runbook/extension.go` |
| Backend | `osmx-go/internal/runbook/extension_test.go` |
| Backend | `osmx-go/internal/runbook/module.go` |
| Backend | `osmx-go/cmd/emergency/main.go` |
| Frontend | `frontend/src/router/index.ts` |
| Frontend | `frontend/src/api/approvals.ts` |
| Frontend | `frontend/src/api/runbook.ts` |
| Frontend | `frontend/src/types/runbook.ts` |
| Frontend | `frontend/src/components/layout/Sidebar.vue` |
| Frontend | `frontend/src/views/alerts/EventCenterView.vue` |
| Frontend | `frontend/src/views/plan/PlanListView.vue` |
| Frontend | `frontend/src/views/plan/PlanDetailView.vue` |
| Frontend | `frontend/src/views/runbook/ExecutionListView.vue` |
| Frontend | `frontend/src/views/runbook/PlanDetailView.vue` |
| Frontend | `frontend/src/views/runbook/RunbookListView.vue` |
| Frontend | `frontend/src/views/runbook/ImportedOperationView.vue` |
| Frontend | `frontend/src/views/system/AuditView.vue` |
| Frontend | `frontend/e2e/11-command-center-chain.spec.ts` |
| Frontend | `frontend/e2e/12-command-center-real-chain.spec.ts` |
| Frontend | `frontend/e2e/13-asset-flow-real-breadth.spec.ts` |
| Frontend | `frontend/e2e/14-command-center-plan-binding.spec.ts` |

## Owner Decision Package

Keep these separate until the owner explicitly decides whether they stay in DW1 or move to a follow-up slice:

| Decision area | Files |
|---------------|-------|
| Schema/model | `osmx-go/internal/model/approval.go` |
| Schema/model | `osmx-go/internal/runbook/model/model.go` |
| Schema/model | `osmx-go/internal/runbook/model/execution_model.go` |
| Migration pair | `osmx-go/migrations/003_approval_execution_links.mysql.sql` |
| Migration pair | `osmx-go/migrations/003_approval_execution_links.postgres.sql` |
| Migration index | `osmx-go/migrations/003_approval_execution_links.sql` |
| Runtime robustness | `osmx-go/internal/runbook/compiler/afl/compiler.go` |
| Runtime robustness | `osmx-go/internal/runbook/compiler/afl/compiler_test.go` |
| Runtime robustness | `osmx-go/internal/runbook/engine/engine_test.go` |
| Runtime robustness | `osmx-go/internal/runbook/engine/event_bus.go` |
| Runtime robustness | `osmx-go/internal/runbook/engine/mysql_state.go` |
| Runtime robustness | `osmx-go/internal/runbook/engine/resilience_test.go` |
| Runtime robustness | `osmx-go/internal/runbook/schedule/scheduler.go` |
| Runtime robustness | `osmx-go/internal/runbook/schedule/scheduler_test.go` |
| Runtime robustness | `osmx-go/internal/runbook/handler/oorestv2.go` |
| Runtime robustness | `osmx-go/internal/runbook/handler/trigger.go` |
| Frontend boundary | `frontend/src/views/runbook/FlowDesignerView.vue` |
| Frontend boundary | `frontend/src/components/flow/PropertyPanel.vue` |
| Frontend boundary | `frontend/vite.config.ts` |

## Post-Isolation Package

These files should stay out of the DW1 main-chain review package:

| Group | Files |
|------|-------|
| Peripheral frontend debt | `frontend/src/api/collectors.ts` |
| Peripheral frontend debt | `frontend/src/api/license.ts` |
| Peripheral frontend debt | `frontend/src/api/topology.ts` |
| Peripheral frontend debt | `frontend/src/stores/skill.ts` |
| Peripheral frontend debt | `frontend/src/views/ai/SQLOptimizeView.vue` |
| Peripheral frontend debt | `frontend/src/views/databases/DatabaseDetailView.vue` |
| Peripheral frontend debt | `frontend/src/views/license/IntegrityView.vue` |
| Peripheral frontend debt | `frontend/src/views/onboarding/OnboardingWizardView.vue` |
| Peripheral frontend debt | `frontend/src/views/runbook/WorkerListView.vue` |
| Peripheral frontend debt | `frontend/src/views/runbook/components/PropertyPanel.vue` |
| Peripheral frontend debt | `frontend/src/views/system/BackupView.vue` |
| Peripheral frontend debt | `frontend/src/views/system/CredentialView.vue` |
| Peripheral frontend debt | `frontend/src/views/tasks/TaskListView.vue` |
| Coordination / review material | `AGENTS.md` |
| Coordination / review material | `docs/plans/osmx-dual-repo-agent-operator-runbook.md` |
| Coordination / review material | `docs/plans/osmx-dual-repo-wave-board.md` |
| Test infrastructure | `frontend/playwright.config.ts` |
| Binary artifact | `osmx-go/emergency` |

## Forbidden Merge Binaries

These are prohibited from the DW1 merge candidate:

| Binary / artifact | Reason |
|-------------------|--------|
| `osmx-go/emergency` | tracked binary artifact, not product source |
| `/Users/apple/Exec/Code/osmx/docs/Automation_Center_26.1/*.pdf` | excluded from Wave 1 merge-back |
| `/Users/apple/Exec/Code/osmx/osmx-go/data/uploads/uploads/2026/04/19/*.pdf` | excluded from Wave 1 merge-back |

## Isolation Rule

Do not let any file in the owner-decision package or post-isolation package leak into the DW1 main-chain review package unless the owner explicitly promotes it.

If the owner promotes nothing else, the only acceptable merge-review slice is the DW1 main-chain keep set plus the recorded validation evidence.

`AGENTS.md`, implementation-worktree `docs/plans/*` coordination files, and `frontend/playwright.config.ts` are not product-source blockers, but they must not be silently carried into the DW1 main-review product slice. Treat them as review/tooling material unless a separate owner decision promotes them.
