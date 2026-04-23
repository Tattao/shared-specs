# Deadline Wave 1 Owner Baseline Triage

> Date: 2026-04-23 01:00 CST
> Last refreshed: 2026-04-23 05:29 CST
> Scope: coordination evidence only. Final product/source truth remains in `osmx`.

## Verdict

`Deadline Wave 1 - Command Center + Asset & Flow Center P0 收口` has moved from dirty-baseline triage to frozen clean PR review. GitHub PR #44 is frozen for owner review on head `302bfef`, with GitHub checks passed, migration replay, local live apply, backend real-chain smoke, frontend real-chain smoke, and full current-source Asset & Flow breadth smoke evidence.

The implementation target has no unresolved merge conflict, and the dirty baseline can be split into backend, frontend, and evaluation lanes. The reviewable candidate is now the clean PR #44 worktree, not the dirty branch. This is not a final acceptance result because owner review and release-time DB risk remain open. The current execution status is `frozen_for_owner_review / GitHub checks passed / asset_flow_breadth_passed / real_chain_smoke_passed / migration_replay_passed / pass_with_risk`.

PostgreSQL follow-up blocker: disposable PostgreSQL runtime probe reached health/login, but runbook AutoMigrate failed on `mediumtext`, so `osm_runbook_execution` was absent and `003_approval_execution_links.postgres.sql` could not apply after startup.

## Baseline

| Item | Value |
|------|-------|
| Worktree | `/Users/apple/Exec/Code/osmx-emergency-main-sync` |
| Branch | `batch/full-integration` |
| HEAD | `5db87c3` |
| Upstream | `origin/batch/full-integration` |
| Unresolved conflicts | none observed via `git diff --name-only --diff-filter=U` |
| Dirty baseline | staged + unstaged changes, including multiple `MM` files |

## Parallel Agent Inputs

| Agent | Role | Result |
|------|------|--------|
| `Socrates` | DW1-BE backend classifier | confirmed backend can enter `in_progress`; initially flagged schema/model changes for owner decision because no dirty migration pair was present |
| `Mencius` | DW1-FE frontend classifier | confirmed frontend can enter `in_progress`; flagged FlowDesigner / PropertyPanel / vite config for owner decision |
| `Planck` | DW1-EVAL validation classifier | confirmed validation entry points exist; recommended `in_progress / pass_with_risk` due dirty baseline and Go toolchain risk |
| `Pasteur` | DW1-BE-SCHEMA worker | added paired approval/execution linkage migration artifacts under `osmx-go/migrations` |
| `Einstein` | DW1-FE decision explorer | confirmed `FlowDesignerView.vue` and `frontend/src/components/flow/PropertyPanel.vue` can stay in DW1; `frontend/src/views/runbook/components/PropertyPanel.vue` should be isolated/postponed |
| `Beauvoir` | DW1-EVAL smoke explorer | confirmed focused Playwright smoke is mock-driven and only needs frontend on port `5173` |
| `Kuhn` | DW1-SCHEMA-REPLAY worker | confirmed MySQL and PostgreSQL migration replay gates pass after the MySQL migration was made idempotent |
| `Galileo` | DW1-BACKEND-SMOKE explorer | identified `cmd/emergency` as the correct real-chain backend entry because it owns the bridge endpoints |
| `Dewey` | DW1-FRONTEND-SMOKE explorer | confirmed old `11-command-center-chain.spec.ts` is mock-only and a non-mock Command Center spec is needed |
| `Leibniz` | DW1-ASSET-FLOW-SMOKE worker | added `frontend/e2e/13-asset-flow-real-breadth.spec.ts`; native and imported flow pass against the real backend, imported operation is explicitly skipped because no real operation exists |
| `Poincare` | DW1-DIRTY-BASELINE explorer | confirmed the dirty baseline cannot be merged as one package; split into DW1 main-chain keep set, owner-decision set, isolate/postpone set, and forbidden binary artifact |
| `Banach` | DW1-ASSET-FLOW-DATA explorer | confirmed native can be created through `POST /api/v1/runbooks`, while imported operation/flow requires Content Pack import or DB fixture; ordinary runbook create cannot create imported assets |
| `Euler` | DW1-IMPORTED-OP worker | normalized imported AFL source in `contentpack.Manager` and added an import-level regression for noisy operation XML |
| `Halley` | DW1-DELIVERY-PACKAGE worker | created the implementation delivery package and dirty baseline isolation list under `shared-specs` |
| `Hume` | DW1-CONTENT-PACK-FIXTURE explorer | confirmed a generated ZIP/JAR with `Content/Library/*.xml` can exercise the real Content Pack import API |

## Backend Classification

### Can Enter DW1

- `osmx-go/internal/plan/handler/chain_handler.go`
- `osmx-go/internal/plan/service/chain_service.go`
- `osmx-go/internal/plan/service/chain_service_test.go`
- `osmx-go/internal/plan/handler/plan_handler.go`
- `osmx-go/internal/api/v1/approval_flow_handler.go`
- `osmx-go/internal/repository/approval_repo.go`
- `osmx-go/internal/runbook/handler/audit.go`
- `osmx-go/internal/runbook/handler/contentpack.go`
- `osmx-go/internal/runbook/handler/contentpack_enrich_test.go`
- `osmx-go/internal/runbook/handler/handler.go`
- `osmx-go/internal/runbook/contentpack/manager.go`
- `osmx-go/internal/runbook/contentpack/manager_test.go`
- `osmx-go/internal/runbook/repository/repository.go`
- `osmx-go/internal/runbook/service/service.go`
- `osmx-go/internal/runbook/extension.go`
- `osmx-go/cmd/emergency/main.go`

Reason:

- These files directly support `Plan -> Approval -> AssetExecution -> Artifact -> Audit`.
- New chain handler/service/test provide the minimum backend route and service layer for DW1.
- Approval model/repo/handler additions bind `plan_uuid`, `runbook_uuid`, and `execution_uuid`.
- Runbook handler/repository/service/model changes add plan/approval metadata, artifact projection, execution audit, and plan filtering.

### Isolate / Do Not Touch For DW1

- `osmx-go/emergency`

Reason:

- This is a tracked binary artifact and must not be carried as a product-source change.

### Owner Decision Required

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

Reason:

- Some changes improve runtime robustness or compatibility, but they are not the minimum DW1 main chain.
- AFL / OO REST / scheduler work must not expand into deep OO / Worker / RAS scope during this wave.
- Keep only if they are required to make the DW1 smoke pass; otherwise isolate or defer.

### Owner Decision Required

- `osmx-go/internal/model/approval.go`
- `osmx-go/internal/runbook/model/model.go`
- `osmx-go/internal/runbook/model/execution_model.go`

Reason:

- These are schema/model-level changes that add or reshape `plan_uuid`, `runbook_uuid`, `execution_uuid`, `PlanUUID`, `ApprovalID`, artifacts, or execution models.
- Migration pair added:
  - `osmx-go/migrations/003_approval_execution_links.mysql.sql`
  - `osmx-go/migrations/003_approval_execution_links.postgres.sql`
  - `osmx-go/migrations/003_approval_execution_links.sql`
- MySQL migration was corrected to an idempotent `information_schema` + prepared-statement form because MySQL does not accept `ADD COLUMN IF NOT EXISTS` / `CREATE INDEX IF NOT EXISTS`.
- Local MySQL live apply against `osmx` passed.
- MySQL temporary replay passed twice.
- PostgreSQL temporary replay passed twice via the running PostgreSQL container's `psql`.

## Frontend Classification

### Can Enter DW1

- `frontend/src/router/index.ts`
- `frontend/src/api/approvals.ts`
- `frontend/src/api/runbook.ts`
- `frontend/src/types/runbook.ts`
- `frontend/src/components/layout/Sidebar.vue`
- `frontend/src/views/alerts/EventCenterView.vue`
- `frontend/src/views/plan/PlanListView.vue`
- `frontend/src/views/plan/PlanDetailView.vue`
- `frontend/src/views/runbook/RunbookListView.vue`
- `frontend/src/views/runbook/PlanDetailView.vue`
- `frontend/src/views/runbook/ExecutionListView.vue`
- `frontend/src/views/runbook/ImportedOperationView.vue`
- `frontend/src/views/system/AuditView.vue`
- `frontend/e2e/11-command-center-chain.spec.ts`
- `frontend/e2e/12-command-center-real-chain.spec.ts`
- `frontend/e2e/13-asset-flow-real-breadth.spec.ts`

Reason:

- These files cover Command Center entry, plan detail, approval/execution APIs, Run Explorer, Operation Viewer, audit, and focused e2e.

### Isolate / Do Not Touch For DW1

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

Reason:

- These are outside the DW1 Command Center / Asset & Flow / Run Explorer minimum chain.

### Owner Decision Required

- `frontend/src/views/runbook/FlowDesignerView.vue`
- `frontend/src/components/flow/PropertyPanel.vue`
- `frontend/vite.config.ts`

Reason:

- `frontend/src/views/runbook/FlowDesignerView.vue` and `frontend/src/components/flow/PropertyPanel.vue` can stay in DW1 because they support the Asset & Flow Center viewer path.
- `frontend/src/views/runbook/components/PropertyPanel.vue` should be isolated/postponed because it belongs to the deeper runbook editing surface.
- `vite.config.ts` is validation infrastructure and should only be kept if required for the DW1 focused smoke.

## Evaluation Classification

Can run early after `in_progress`:

- `cd frontend && npm run build:check`
- `cd osmx-go && go build ./cmd/server`
- `cd osmx-go && go build ./cmd/emergency`
- `cd osmx-go && go test ./internal/plan/...`
- `cd osmx-go && go test ./internal/runbook/...`

Run after implementation closes:

- `cd frontend && npm run build`
- `cd frontend && npx playwright test e2e/11-command-center-chain.spec.ts`
- Full main-chain smoke through Command Center, Plan, Approval, AssetExecution, Artifact, Audit.

Known risks:

- `osmx-go/go.mod` declares `go 1.25.0`, while the local toolchain observed by the evaluation agent is `go1.22.5`; `GOTOOLCHAIN=auto` may resolve this if network/toolchain download works.
- Dirty baseline is broad, so failures must be attributed to DW1 work, historical debt, or environment blockers before any merge decision.

## Early Validation Evidence

Date: 2026-04-22 23:27 CST

Commands run in `/Users/apple/Exec/Code/osmx-emergency-main-sync`:

```bash
cd osmx-go && go test ./internal/plan/...
```

Result:

- Passed.
- `internal/plan/service` passed in `0.030s`.
- Other `internal/plan` packages had no test files.
- Go printed `ignoring go.mod in $GOPATH /Users/apple/go` warnings, but the focused test completed successfully.

```bash
cd frontend && npm run build:check
```

Result:

- Passed.
- `vue-tsc -b` and `vite build` completed.
- Vite reported chunk-size and ineffective dynamic import warnings; these are not DW1 blockers.

```bash
git diff --check
```

Result:

- Passed in the implementation worktree.

Docs / ledger diff checks:

- `git diff --check` passed in `/Users/apple/Exec/Code/osmx` for the DW1 plan/status files.
- `git diff --check` passed in `/Users/apple/Exec/Code/shared-specs` for the DW1 ledger files.

## Focused Smoke And Schema Evidence

Date: 2026-04-22 23:42 CST

Commands run in `/Users/apple/Exec/Code/osmx-emergency-main-sync`:

```bash
cd frontend && npx playwright test e2e/11-command-center-chain.spec.ts
```

Result:

- Passed: `1 passed (9.3s)`.
- The test is mock-driven; Vite proxy `EPIPE` warnings were observed because no real backend was attached, but they did not fail the focused smoke.
- `frontend/playwright.config.ts` now starts Vite with `--host 0.0.0.0 --port 5173`, matching the Playwright web server expectation.

```bash
cd osmx-go && go test ./internal/plan/... ./internal/runbook/handler ./internal/runbook/service ./internal/runbook/repository
```

Result:

- Passed for the focused plan/runbook packages.

Schema artifacts added:

- `osmx-go/migrations/003_approval_execution_links.mysql.sql`
- `osmx-go/migrations/003_approval_execution_links.postgres.sql`
- `osmx-go/migrations/003_approval_execution_links.sql`

Diff hygiene:

- `git diff --check -- frontend/playwright.config.ts osmx-go/migrations/003_approval_execution_links.mysql.sql osmx-go/migrations/003_approval_execution_links.postgres.sql osmx-go/migrations/003_approval_execution_links.sql` passed.

## Real Chain Smoke And Replay Evidence

Date: 2026-04-23 00:10 CST

Migration gate:

- `mysql --protocol=tcp -h127.0.0.1 -P3306 -uroot ... osmx < osmx-go/migrations/003_approval_execution_links.mysql.sql` passed against the local `osmx` database.
- MySQL temporary replay database with minimal `osm_approvals` / `osm_runbook_execution` tables passed two consecutive applies and verified the new columns/indexes.
- PostgreSQL temporary replay database in the running `save-postgres` container passed two consecutive applies and verified the new columns/indexes.

Backend real-chain smoke:

- Target: `http://127.0.0.1:18081` running `cmd/emergency`.
- Flow passed: login -> create native YAML runbook -> create/activate plan -> request approval -> approve -> trigger asset execution -> read execution -> read plan chain -> read audit.
- Result: execution status `COMPLETED`; chain returned approval `approved`, asset execution `COMPLETED`, 2 artifacts, and 6 audit rows.

Frontend real-chain smoke:

- `frontend/vite.config.ts` now supports `VITE_API_PROXY_TARGET` for test-time proxy selection.
- Added `frontend/e2e/12-command-center-real-chain.spec.ts`.
- `VITE_API_PROXY_TARGET=http://127.0.0.1:18081 E2E_BACKEND_BASE_URL=http://127.0.0.1:18081 npx playwright test e2e/12-command-center-real-chain.spec.ts` passed: `1 passed (10.5s)`.

Asset & Flow breadth smoke:

- Added `frontend/e2e/13-asset-flow-real-breadth.spec.ts`.
- `VITE_API_PROXY_TARGET=http://127.0.0.1:18081 E2E_BACKEND_BASE_URL=http://127.0.0.1:18081 npx playwright test e2e/13-asset-flow-real-breadth.spec.ts --reporter=list` passed with `2 passed, 1 skipped`.
- Native path passed: real runbook creation, plan, approval, asset execution, execution detail artifact, Command Center artifact/audit, `/runbook/executions`, and `/audit-logs`.
- Imported flow path passed against real AFL Content Pack data through the readonly flow viewer.
- Imported operation path was skipped on purpose because the real backend currently has no `source_type != native_yaml` and `flow_type = operation` materialized runbook. Observed inventory: `native_yaml=55`, `afl flow=3259`, `cloudslang=0`, imported operation `0`.
- Follow-up completed in current source: `frontend/e2e/13-asset-flow-real-breadth.spec.ts` now generates a minimal real Content Pack operation fixture and imports it through `/api/v1/runbook-content-packs/import` when no operation exists.
- Current-source backend replay used temporary `OSMX_SERVER_PORT=18082 go run ./cmd/emergency -config configs/emergency.yaml` and passed `VITE_API_PROXY_TARGET=http://127.0.0.1:18082 E2E_BACKEND_BASE_URL=http://127.0.0.1:18082 npx playwright test e2e/13-asset-flow-real-breadth.spec.ts --reporter=list` with `3 passed`.
- Temporary `18082` backend was stopped after validation. The long-running `18081` dev server was not restarted and may still reflect old source until the operator restarts it.

Focused build/test replay:

- `cd frontend && npm run build:check` passed with existing non-blocking Vite warnings.
- `cd osmx-go && go test ./internal/plan/... ./internal/runbook/handler ./internal/runbook/service ./internal/runbook/repository` passed.

## Owner Decision

Move state to:

```text
in_progress / asset_flow_breadth_passed / real_chain_smoke_passed / migration_replay_passed / pass_with_risk
```

Immediate child tasks:

1. DW1-BE: continue only the backend files listed under `Can Enter DW1`; isolate binary and non-essential OO/runtime robustness work.
2. DW1-BE-SCHEMA: keep the migration pair with the idempotent MySQL form; production/live customer DB apply remains a release-time risk, but the local/replay gate is closed.
3. DW1-FE: keep the new real-chain Playwright spec and the proxy target override; isolate/postpone the deeper runbook editor `PropertyPanel.vue` unless it blocks smoke.
4. DW1-EVAL: keep the new Asset & Flow breadth spec and current-source `3 passed` evidence.
5. DW1-OWNER: use `deadline-wave1-implementation-delivery-package.md` and `deadline-wave1-dirty-baseline-isolation-list.md` to decide the merge-review slice.

Do not declare final acceptance until the dirty baseline package is explicitly isolated for review and the release owner accepts the schema/migration boundary.
