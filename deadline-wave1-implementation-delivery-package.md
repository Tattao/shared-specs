# Deadline Wave 1 Implementation Delivery Package

> Date: 2026-04-23 01:00 CST
> Last refreshed: 2026-04-23 05:29 CST
> Basis: `deadline-wave1-command-asset-dispatch.md` and `deadline-wave1-owner-baseline-triage.md`
> Scope: coordination evidence only. Final product/source truth remains in `osmx` and the implementation worktree.

## Conclusion

`Deadline Wave 1 - Command Center + Asset & Flow Center P0 收口` is ready for a main-review delivery package and PR #44 is frozen for owner review, but it is not a final merge-ready declaration.

The current package should be treated as:

```text
frozen_for_owner_review / GitHub checks passed / decision_ready / current_source_smoke_refreshed / asset_flow_breadth_passed / real_chain_smoke_passed / migration_replay_passed / pass_with_risk
```

The main-chain path is closed enough to package, and the imported operation fixture/classification blocker is now closed in current source. Final acceptance still depends on owner packaging of the dirty baseline and schema/migration release boundary. PostgreSQL runtime/apply closure remains a follow-up lane because the disposable PostgreSQL probe hit runbook `mediumtext` AutoMigrate incompatibility.

## Files That Can Enter The DW1 Main-Chain Package

These files are the DW1 main-chain keep set from the owner triage and dispatch ledger.

The exact current PR slice gate is recorded in `deadline-wave1-pr-slice-manifest.md`; as of 2026-04-23 05:29 CST, clean GitHub PR #44 is frozen on head `302bfef` with a 29-file net diff and passing GitHub checks.

| Area | Files |
|------|-------|
| Backend main chain | `osmx-go/internal/plan/handler/chain_handler.go` |
| Backend main chain | `osmx-go/internal/plan/extension.go` |
| Backend main chain | `osmx-go/internal/plan/extension_test.go` |
| Backend main chain | `osmx-go/internal/plan/service/chain_service.go` |
| Backend main chain | `osmx-go/internal/plan/service/chain_service_test.go` |
| Backend main chain | `osmx-go/internal/plan/handler/plan_handler.go` |
| Backend main chain | `osmx-go/internal/api/v1/approval_flow_handler.go` |
| Backend main chain | `osmx-go/internal/repository/approval_repo.go` |
| Backend main chain | `osmx-go/internal/repository/approval_repo_test.go` |
| Backend main chain | `osmx-go/internal/runbook/handler/audit.go` |
| Backend asset-flow | `osmx-go/internal/runbook/handler/contentpack.go` |
| Backend asset-flow | `osmx-go/internal/runbook/handler/contentpack_enrich_test.go` |
| Backend main chain | `osmx-go/internal/runbook/handler/handler.go` |
| Backend asset-flow | `osmx-go/internal/runbook/contentpack/manager.go` |
| Backend asset-flow | `osmx-go/internal/runbook/contentpack/manager_test.go` |
| Backend main chain | `osmx-go/internal/runbook/repository/repository.go` |
| Backend main chain | `osmx-go/internal/runbook/repository/repository_test.go` |
| Backend main chain | `osmx-go/internal/runbook/service/service.go` |
| Backend main chain | `osmx-go/internal/runbook/service/service_test.go` |
| Backend main chain | `osmx-go/internal/runbook/extension.go` |
| Backend main chain | `osmx-go/internal/runbook/extension_test.go` |
| Backend main chain | `osmx-go/internal/runbook/module.go` |
| Backend main chain | `osmx-go/internal/app/app.go` |
| Backend main chain | `osmx-go/internal/extension/extension.go` |
| Backend main chain | `osmx-go/cmd/emergency/main.go` |
| Frontend main chain | `frontend/src/router/index.ts` |
| Frontend main chain | `frontend/src/api/approvals.ts` |
| Frontend main chain | `frontend/src/api/runbook.ts` |
| Frontend main chain | `frontend/src/types/runbook.ts` |
| Frontend main chain | `frontend/src/components/layout/Sidebar.vue` |
| Frontend main chain | `frontend/src/views/alerts/EventCenterView.vue` |
| Frontend main chain | `frontend/src/views/plan/PlanListView.vue` |
| Frontend main chain | `frontend/src/views/plan/PlanDetailView.vue` |
| Frontend main chain | `frontend/src/views/runbook/ExecutionListView.vue` |
| Frontend main chain | `frontend/src/views/runbook/PlanDetailView.vue` |
| Frontend main chain | `frontend/src/views/runbook/RunbookListView.vue` |
| Frontend main chain | `frontend/src/views/runbook/ImportedOperationView.vue` |
| Frontend main chain | `frontend/src/views/system/AuditView.vue` |
| Frontend main chain | `frontend/e2e/11-command-center-chain.spec.ts` |
| Frontend main chain | `frontend/e2e/12-command-center-real-chain.spec.ts` |
| Frontend main chain | `frontend/e2e/13-asset-flow-real-breadth.spec.ts` |
| Frontend main chain | `frontend/e2e/14-command-center-plan-binding.spec.ts` |

## Owner Decision Package

These files need an explicit owner call before the overall DW1 package can be treated as fully closed:

| Decision area | Files | Why it needs owner decision |
|---------------|-------|-----------------------------|
| Schema/model shape | `osmx-go/internal/model/approval.go` | approval linkage fields and merge boundary impact |
| Schema/model shape | `osmx-go/internal/runbook/model/model.go` | runbook model shape affects approval / execution / artifact wiring |
| Schema/model shape | `osmx-go/internal/runbook/model/execution_model.go` | execution model reshaping affects persistence contract |
| Schema/migration pair | `osmx-go/migrations/003_approval_execution_links.mysql.sql` | MySQL migration strategy is already replayed locally, but production apply remains a release-time decision |
| Schema/migration pair | `osmx-go/migrations/003_approval_execution_links.postgres.sql` | PostgreSQL paired artifact exists, but disposable PostgreSQL runtime/apply probe found the runbook `mediumtext` blocker before this linkage script could apply |
| Schema/migration index | `osmx-go/migrations/003_approval_execution_links.sql` | migration pair index required by the repository migration pair checker |
| Runtime robustness | `osmx-go/internal/runbook/compiler/afl/compiler.go` | useful for compatibility, but not the minimum DW1 main-chain slice |
| Runtime robustness | `osmx-go/internal/runbook/compiler/afl/compiler_test.go` | tied to compatibility and classifier behavior rather than the narrow main chain |
| Runtime robustness | `osmx-go/internal/runbook/engine/engine_test.go` | evidence and regression only; keep if it is still needed for the smoke contract |
| Runtime robustness | `osmx-go/internal/runbook/engine/event_bus.go` | runtime hardening, but outside the minimum chain |
| Runtime robustness | `osmx-go/internal/runbook/engine/mysql_state.go` | startup stability fix is useful, but should stay owner-approved |
| Runtime robustness | `osmx-go/internal/runbook/engine/resilience_test.go` | test-side isolation fix, not a product surface change |
| Runtime robustness | `osmx-go/internal/runbook/schedule/scheduler.go` | scheduler compatibility, not the minimal DW1 chain |
| Runtime robustness | `osmx-go/internal/runbook/schedule/scheduler_test.go` | validation for scheduler behavior, not minimum chain content |
| Runtime robustness | `osmx-go/internal/runbook/handler/oorestv2.go` | compatibility surface that can stay out unless smoke requires it |
| Runtime robustness | `osmx-go/internal/runbook/handler/trigger.go` | runtime pathway hardening, but not the main chain itself |
| Frontend boundary | `frontend/src/views/runbook/FlowDesignerView.vue` | can stay in DW1, but owner must decide if it belongs in this merge slice |
| Frontend boundary | `frontend/src/components/flow/PropertyPanel.vue` | supports the asset-flow viewer path, but may be sliced separately |
| Frontend boundary | `frontend/vite.config.ts` | validation infrastructure; keep only if needed for the focused smoke path |

## Post-Isolation Package

These are the non-DW1 or postponed dirty changes that should stay out of the main-chain review package:

| Group | Files | Isolation reason |
|------|-------|------------------|
| Peripheral frontend debt | `frontend/src/api/collectors.ts` | unrelated to the DW1 main chain |
| Peripheral frontend debt | `frontend/src/api/license.ts` | unrelated to the DW1 main chain |
| Peripheral frontend debt | `frontend/src/api/topology.ts` | unrelated to the DW1 main chain |
| Peripheral frontend debt | `frontend/src/stores/skill.ts` | unrelated to the DW1 main chain |
| Peripheral frontend debt | `frontend/src/views/ai/SQLOptimizeView.vue` | outside DW1 scope |
| Peripheral frontend debt | `frontend/src/views/databases/DatabaseDetailView.vue` | outside DW1 scope |
| Peripheral frontend debt | `frontend/src/views/license/IntegrityView.vue` | outside DW1 scope |
| Peripheral frontend debt | `frontend/src/views/onboarding/OnboardingWizardView.vue` | outside DW1 scope |
| Peripheral frontend debt | `frontend/src/views/runbook/WorkerListView.vue` | outside DW1 scope |
| Peripheral frontend debt | `frontend/src/views/runbook/components/PropertyPanel.vue` | deeper runbook editor surface; explicitly postponed |
| Peripheral frontend debt | `frontend/src/views/system/BackupView.vue` | outside DW1 scope |
| Peripheral frontend debt | `frontend/src/views/system/CredentialView.vue` | outside DW1 scope |
| Peripheral frontend debt | `frontend/src/views/tasks/TaskListView.vue` | outside DW1 scope |
| Coordination / review material | `AGENTS.md` | not part of the DW1 product-source slice |
| Coordination / review material | `docs/plans/osmx-dual-repo-agent-operator-runbook.md` | implementation-worktree coordination doc; keep outside product slice unless separately approved |
| Coordination / review material | `docs/plans/osmx-dual-repo-wave-board.md` | implementation-worktree coordination doc; keep outside product slice unless separately approved |
| Test infrastructure | `frontend/playwright.config.ts` | validation tooling; keep outside product slice unless explicitly needed for the focused smoke path |
| Binary artifact | `osmx-go/emergency` | tracked binary; do not carry as product-source change |

## Forbidden Merge Binaries

Do not merge these artifacts into any DW1 candidate:

| Binary / artifact | Reason |
|-------------------|--------|
| `osmx-go/emergency` | tracked binary artifact, not product source |
| `/Users/apple/Exec/Code/osmx/docs/Automation_Center_26.1/*.pdf` | excluded from Wave 1 merge-back |
| `/Users/apple/Exec/Code/osmx/osmx-go/data/uploads/uploads/2026/04/19/*.pdf` | excluded from Wave 1 merge-back |

## Validation Already Recorded

These checks are already recorded in the source docs and are the evidence basis for this package:

| Command | Result |
|---------|--------|
| `cd osmx-go && go test ./internal/plan/...` | passed |
| `cd frontend && npm run build:check` | passed with non-blocking Vite warnings |
| `cd frontend && npx playwright test e2e/11-command-center-chain.spec.ts` | passed mock-driven smoke |
| `cd osmx-go && go test ./internal/plan/... ./internal/runbook/handler ./internal/runbook/service ./internal/runbook/repository` | passed |
| migration live/replay gate | MySQL local live apply passed; MySQL and PostgreSQL temporary replay passed twice |
| backend real-chain curl smoke | passed on `cmd/emergency` at `http://127.0.0.1:18081` |
| `VITE_API_PROXY_TARGET=http://127.0.0.1:18081 E2E_BACKEND_BASE_URL=http://127.0.0.1:18081 npx playwright test e2e/12-command-center-real-chain.spec.ts` | passed |
| `VITE_API_PROXY_TARGET=http://127.0.0.1:18082 E2E_BACKEND_BASE_URL=http://127.0.0.1:18082 npx playwright test e2e/12-command-center-real-chain.spec.ts --reporter=list` | 2026-04-23 01:47 CST failed before fix because execution remained `RUNNING` in API while engine had completed |
| `osmx-go/internal/runbook/service/service.go` terminal state reconciliation | fixed fast-completion race where business execution could be overwritten back to `RUNNING` after engine terminal state |
| `VITE_API_PROXY_TARGET=http://127.0.0.1:18082 E2E_BACKEND_BASE_URL=http://127.0.0.1:18082 npx playwright test e2e/12-command-center-real-chain.spec.ts --reporter=list` | 2026-04-23 01:48 CST passed after fix; `1 passed (5.9s)`; temporary backend stopped and `18082` no longer listening |
| `VITE_API_PROXY_TARGET=http://127.0.0.1:18081 E2E_BACKEND_BASE_URL=http://127.0.0.1:18081 npx playwright test e2e/13-asset-flow-real-breadth.spec.ts --reporter=list` | `2 passed, 1 skipped` |
| `cd osmx-go && go test ./internal/runbook/handler ./internal/runbook/contentpack` | passed |
| `OSMX_SERVER_PORT=18082 go run ./cmd/emergency -config configs/emergency.yaml` + `VITE_API_PROXY_TARGET=http://127.0.0.1:18082 E2E_BACKEND_BASE_URL=http://127.0.0.1:18082 npx playwright test e2e/13-asset-flow-real-breadth.spec.ts --reporter=list` | `3 passed`; temporary backend stopped after validation |
| `OSMX_SERVER_PORT=18082 go run ./cmd/emergency -config configs/emergency.yaml` + `VITE_API_PROXY_TARGET=http://127.0.0.1:18082 E2E_BACKEND_BASE_URL=http://127.0.0.1:18082 npx playwright test e2e/13-asset-flow-real-breadth.spec.ts --reporter=list` | 2026-04-23 01:45 CST refreshed; `3 passed (21.6s)`; temporary backend stopped and `18082` no longer listening |
| `lsof -nP -iTCP:18081 -sTCP:LISTEN` / `lsof -nP -iTCP:18082 -sTCP:LISTEN` | `18081` still listening; `18082` not listening; `18081` remains an old-process risk |
| `go test ./internal/runbook/handler ./internal/runbook/contentpack ./internal/plan/... ./internal/runbook/service ./internal/runbook/repository` | passed |
| `cd osmx-go && go test ./internal/runbook/handler ./internal/runbook/contentpack ./internal/plan/... ./internal/runbook/service ./internal/runbook/repository` | 2026-04-23 01:40 CST passed; only GOPATH go.mod warning |
| `cd osmx-go && go test ./internal/runbook/...` | 2026-04-23 01:44 CST passed; covers compiler/afl, contentpack, engine, handler, schedule, service, worker, and related packages |
| `cd frontend && npm run build:check` | 2026-04-23 01:40 CST passed; only existing Vite dynamic import / chunk size warnings |
| `git diff --check` for DW1 plan/status files | passed |
| `git diff --check` for DW1 ledger files | passed |
| `cd osmx-go && go test ./internal/runbook/repository ./internal/repository -count=1` | 2026-04-23 03:43 CST passed; covers runbook list lightweight projection and approval latest-by-plan lookup |
| `cd osmx-go && go test ./internal/runbook/handler ./internal/runbook/contentpack ./internal/plan/... ./internal/runbook/service ./internal/runbook/repository ./internal/repository -count=1` | 2026-04-23 03:43 CST passed after repository projection / lookup-noise hardening |
| `cd osmx-go && go test -tags runbook ./internal/runbook -count=1` | 2026-04-23 03:43 CST passed |
| `cd osmx-go && go test -tags 'plan runbook' ./internal/plan -count=1` | 2026-04-23 03:43 CST passed |
| `cd osmx-go && go build -tags 'plan runbook' ./cmd/server` | 2026-04-23 03:43 CST passed; temporary `server` artifact removed |
| DW1 PR slice manifest audit | 2026-04-23 05:29 CST clean; PR #44 has 29 net files, GitHub checks passed, and forbidden/generated outputs are excluded |
| Disposable PostgreSQL probe | `/health` and login passed; `003_mainchain_core.postgres.sql` applied; `003_approval_execution_links.postgres.sql` failed because runbook AutoMigrate hit `mediumtext` and left `osm_runbook_execution` absent |
| `VITE_API_PROXY_TARGET=http://127.0.0.1:18082 E2E_BACKEND_BASE_URL=http://127.0.0.1:18082 npx playwright test e2e/11-command-center-chain.spec.ts e2e/12-command-center-real-chain.spec.ts e2e/13-asset-flow-real-breadth.spec.ts e2e/14-command-center-plan-binding.spec.ts --reporter=list` | 2026-04-23 03:44 CST passed; `7 passed (24.2s)` on current-source backend; temporary `18082` backend stopped |
| `cd osmx-go && go test ./internal/runbook/... -count=1` | 2026-04-23 03:45 CST passed |
| `cd frontend && npm run build:check` | 2026-04-23 03:45 CST passed with existing non-blocking Vite dynamic import / chunk-size warnings |
| `git diff --check && git diff --cached --check` | 2026-04-23 04:30 CST passed |
| `git diff --cached --name-only \| wc -l` and forbidden binary gate | 2026-04-23 04:30 CST staged set remained `47`; `osmx-go/emergency` was not staged |
| `go test ./internal/runbook/handler ./internal/runbook/contentpack ./internal/plan/... ./internal/runbook/service ./internal/runbook/repository ./internal/repository -count=1` | 2026-04-23 04:30 CST passed; only existing `$GOPATH /Users/apple/go` warning |
| `cd frontend && npm run build:check` | 2026-04-23 04:31 CST passed with existing non-blocking Vite warnings |
| `OSMX_SERVER_PORT=18082 go run ./cmd/emergency -config configs/emergency.yaml` + `VITE_API_PROXY_TARGET=http://127.0.0.1:18082 E2E_BACKEND_BASE_URL=http://127.0.0.1:18082 npx playwright test e2e/11-command-center-chain.spec.ts e2e/12-command-center-real-chain.spec.ts e2e/13-asset-flow-real-breadth.spec.ts e2e/14-command-center-plan-binding.spec.ts --reporter=list` | 2026-04-23 04:32 CST passed; `7 passed (34.5s)` on current-source backend; temporary `18082` backend stopped |

## Remaining Blockers

1. Production/customer DB apply remains a release-time risk and should be rechecked before any final acceptance claim.
2. The long-running `http://127.0.0.1:18081` backend was not restarted, so it may still reflect the old source until the operator restarts it.
3. The dirty baseline still needs owner enforcement during actual review so owner-decision, post-isolation, coordination/tooling files, and forbidden binaries do not leak into the main-chain product slice.
4. `/api/v1/runbooks/tree` still shows slow SQL under the old 4900+ row test database. A compound index or cache change should be handled as a follow-up with explicit MySQL/PostgreSQL migration analysis, not silently added to the DW1 slice.

## Next Owner Decision

The next owner call is to accept the implementation delivery package boundary and decide the final merge-review slice. The recommended decision is recorded in `deadline-wave1-owner-merge-review-decision.md`.

If the owner accepts the main-chain slice plus schema/migration boundary, the package can move through owner review on frozen PR #44. If not, the dirty baseline must remain explicitly isolated and the wave should stay in `pass_with_risk`. PostgreSQL runtime/apply closure must not be claimed until the runbook `mediumtext` portability blocker is fixed in a separate lane.
