# Deadline Wave 1 Command Center + Asset Dispatch Ledger

> Date: 2026-04-23 01:00 CST
> Scope: coordination evidence only. Final product/source truth remains in `osmx/docs/plans`, code, tests, runbooks, and reviewed PRs.

## Dispatch Summary

This file records the dispatch state for the 2026-05-15 product deadline's next execution wave.

Canonical product inputs in `osmx`:

- `docs/plans/osmx-product-deadline-2026-05-15-delivery-plan.md`
- `docs/plans/osmx-deadline-wave1-command-asset-task-pack.md`
- `docs/plans/osmx-dual-repo-wave-board.md`
- `docs/plans/osmx-oo-26-1-benchmark-gap-matrix.md`

Current task:

```text
Deadline Wave 1 - Command Center + Asset & Flow Center P0 收口
```

Target window:

```text
2026-04-24 -> 2026-04-29
```

Target acceptance:

- `G2 Command Center 主链`
- `G3 Asset & Flow Center`
- `G4 Run Explorer`
- G5 human approval / evidence chain foundation

## Baseline

| Item | Value |
|------|-------|
| Product deadline | `2026-05-15` |
| `osmx` remote main after fetch | `0a07edb` |
| `osmx` current local branch | `batch/full-integration` |
| `osmx` current local HEAD | `5db87c3` |
| Clean PR branch | `dw1/command-asset-main-review` |
| Clean PR head | `302bfef` |
| Clean PR | `https://github.com/Tattao/osmx/pull/44` |
| `shared-specs` main | `9e8b6d0` |
| Implementation target | `/Users/apple/Exec/Code/osmx-emergency-main-sync` source intent; `/Users/apple/Exec/Code/osmx-dw1-main-review` clean PR |
| Implementation target status | dirty source intent preserved; clean PR #44 opened from `github/main@0a07edb` with 29 net files; GitHub checks passed; frozen for owner review |
| Dispatch state | `frozen_for_owner_review / GitHub checks passed / asset_flow_breadth_passed / real_chain_smoke_passed / migration_replay_passed / pass_with_risk` |

Important boundary:

- `shared-specs` is a coordination ledger only.
- If this file conflicts with `osmx/docs/plans`, `osmx/docs/plans` wins.
- Do not import, clone, submodule, build from, test from, or run against `shared-specs`.
- Accepted implementation facts must be synchronized back into `osmx`.

## Lane Ownership

| Lane | Owner role | Worktree | Write scope | Expected output | Status |
|------|------------|----------|-------------|-----------------|--------|
| DW1-OWNER | `osmx-emergency-main-sync` 负责人 Agent | `/Users/apple/Exec/Code/osmx-emergency-main-sync` | coordination summary only, plus scoped docs if needed | dirty baseline triage, backend/frontend/evaluation split, final delivery package | `done` |
| DW1-BE | 后端开发 Agent | `/Users/apple/Exec/Code/osmx-dw1-main-review` | `osmx-go/internal/plan`, `osmx-go/internal/repository`, `osmx-go/internal/runbook`, `osmx-go/migrations`, focused tests | main-chain API, asset projection, artifact/audit traceability, DB readiness evidence | `PR #44 frozen / checks_passed / pass_with_risk` |
| DW1-FE | 前端开发 Agent | `/Users/apple/Exec/Code/osmx-dw1-main-review` | `frontend/src/views/plan`, `frontend/src/views/alerts`, focused e2e, test runtime config | Command Center path, Asset & Flow Center smoke, viewer routing, Run Explorer, fallback states | `PR #44 frozen / checks_passed / pass_with_risk` |
| DW1-EVAL | 评估 Agent | `/Users/apple/Exec/Code/osmx-dw1-main-review` and read-only `osmx` | focused tests, e2e, reports only | build / build:check / smoke / regression / merge readiness verdict | `PR #44 frozen / checks_passed / pass_with_risk` |
| DW1-DOC | `osmx` 文档/契约 Agent | `/Users/apple/Exec/Code/osmx` and `/Users/apple/Exec/Code/shared-specs` | plans, wave board, coordination ledger | task pack, wave board, dispatch ledger, change log | `done` |

Schema gate:

- `osmx-go/internal/model/approval.go`, `osmx-go/internal/runbook/model/model.go`, and `osmx-go/internal/runbook/model/execution_model.go` require owner decision.
- Matching MySQL/PostgreSQL migration artifacts were added under `osmx-go/migrations`.
- Local MySQL live apply passed, and MySQL/PostgreSQL temporary replay passed twice.
- Production/customer DB apply remains a release-time risk and should be rechecked in the final delivery package.

## Early / Focused / Real Validation Evidence

Latest update: 2026-04-23 03:45 CST

Clean PR refresh: 2026-04-23 05:29 CST, PR #44 (`https://github.com/Tattao/osmx/pull/44`) from `/Users/apple/Exec/Code/osmx-dw1-main-review`, head `302bfef`. GitHub `security-gate` and `GitGuardian Security Checks` passed. The credential fix was pushed to GitHub only; no GitGuardian-side sync or dashboard action was performed. PR #44 is frozen for owner review.

PostgreSQL probe after freeze: disposable Docker `postgres:15` allowed `cmd/emergency` to reach `/health` and `/api/v1/auth/login`, but runbook AutoMigrate logged `ERROR: type "mediumtext" does not exist`; `003_mainchain_core.postgres.sql` applied, and `003_approval_execution_links.postgres.sql` failed because `osm_runbook_execution` was absent. Treat PostgreSQL runtime/apply closure as a follow-up lane.

| Command | Worktree | Result |
|------|----------|--------|
| `cd osmx-go && go test ./internal/plan/...` | `/Users/apple/Exec/Code/osmx-emergency-main-sync` | passed |
| `cd frontend && npm run build:check` | `/Users/apple/Exec/Code/osmx-emergency-main-sync` | passed with non-blocking Vite warnings |
| `cd frontend && npx playwright test e2e/11-command-center-chain.spec.ts` | `/Users/apple/Exec/Code/osmx-emergency-main-sync` | passed mock-driven smoke; backend proxy `EPIPE` warnings were non-blocking |
| `cd osmx-go && go test ./internal/plan/... ./internal/runbook/handler ./internal/runbook/service ./internal/runbook/repository` | `/Users/apple/Exec/Code/osmx-emergency-main-sync` | passed |
| migration live/replay gate | `/Users/apple/Exec/Code/osmx-emergency-main-sync` | MySQL local live apply passed; MySQL and PostgreSQL temporary replay passed twice |
| backend real-chain curl smoke | `/Users/apple/Exec/Code/osmx-emergency-main-sync` | passed on `cmd/emergency` at `http://127.0.0.1:18081`; execution `COMPLETED`, 2 artifacts, 6 audit rows |
| `VITE_API_PROXY_TARGET=http://127.0.0.1:18081 E2E_BACKEND_BASE_URL=http://127.0.0.1:18081 npx playwright test e2e/12-command-center-real-chain.spec.ts` | `/Users/apple/Exec/Code/osmx-emergency-main-sync/frontend` | passed, non-mock frontend real-chain smoke |
| `VITE_API_PROXY_TARGET=http://127.0.0.1:18081 E2E_BACKEND_BASE_URL=http://127.0.0.1:18081 npx playwright test e2e/13-asset-flow-real-breadth.spec.ts --reporter=list` | `/Users/apple/Exec/Code/osmx-emergency-main-sync/frontend` | `2 passed, 1 skipped`; native runbook -> asset execution -> artifact/audit surfaces passed, imported flow readonly viewer passed with real AFL Content Pack data, imported operation skipped because real backend currently has no non-native `flow_type=operation` runbook |
| `cd osmx-go && go test ./internal/runbook/handler ./internal/runbook/contentpack` | `/Users/apple/Exec/Code/osmx-emergency-main-sync` | passed; covers robust AFL operation type detection and import-side normalization |
| `OSMX_SERVER_PORT=18082 go run ./cmd/emergency -config configs/emergency.yaml` + `VITE_API_PROXY_TARGET=http://127.0.0.1:18082 E2E_BACKEND_BASE_URL=http://127.0.0.1:18082 npx playwright test e2e/13-asset-flow-real-breadth.spec.ts --reporter=list` | `/Users/apple/Exec/Code/osmx-emergency-main-sync` | `3 passed`; current-source backend imports a real operation Content Pack fixture and opens Imported Operation / Imported Flow / native artifact-audit surfaces |
| `git diff --check` | `/Users/apple/Exec/Code/osmx-emergency-main-sync` | passed |
| `git diff --check` for DW1 plan/status files | `/Users/apple/Exec/Code/osmx` | passed |
| `git diff --check` for DW1 ledger files | `/Users/apple/Exec/Code/shared-specs` | passed |
| `cd osmx-go && go test ./internal/runbook/repository ./internal/repository -count=1` | `/Users/apple/Exec/Code/osmx-emergency-main-sync` | passed; covers runbook list lightweight projection and approval latest-by-plan lookup |
| `cd osmx-go && go test ./internal/runbook/handler ./internal/runbook/contentpack ./internal/plan/... ./internal/runbook/service ./internal/runbook/repository ./internal/repository -count=1` | `/Users/apple/Exec/Code/osmx-emergency-main-sync` | passed after repository projection / lookup-noise hardening |
| `cd osmx-go && go test -tags runbook ./internal/runbook -count=1` | `/Users/apple/Exec/Code/osmx-emergency-main-sync` | passed |
| `cd osmx-go && go test -tags 'plan runbook' ./internal/plan -count=1` | `/Users/apple/Exec/Code/osmx-emergency-main-sync` | passed |
| `cd osmx-go && go build -tags 'plan runbook' ./cmd/server` | `/Users/apple/Exec/Code/osmx-emergency-main-sync` | passed; temporary `server` artifact removed |
| DW1 PR slice manifest audit | `/Users/apple/Exec/Code/osmx-emergency-main-sync` + `/Users/apple/Exec/Code/shared-specs` | include set and staged implementation set both `47`; `osmx-go/emergency` is not staged |
| `VITE_API_PROXY_TARGET=http://127.0.0.1:18082 E2E_BACKEND_BASE_URL=http://127.0.0.1:18082 npx playwright test e2e/11-command-center-chain.spec.ts e2e/12-command-center-real-chain.spec.ts e2e/13-asset-flow-real-breadth.spec.ts e2e/14-command-center-plan-binding.spec.ts --reporter=list` | `/Users/apple/Exec/Code/osmx-emergency-main-sync/frontend` | 2026-04-23 03:44 CST refreshed; `7 passed (24.2s)` on current-source backend; temporary `18082` backend stopped after validation |
| `cd osmx-go && go test ./internal/runbook/... -count=1` | `/Users/apple/Exec/Code/osmx-emergency-main-sync` | passed; covers acceptance, compiler, contentpack, engine, handler, middleware, repository, resolver, schedule, scriptlet, service, and worker packages |
| `cd frontend && npm run build:check` | `/Users/apple/Exec/Code/osmx-emergency-main-sync` | passed with existing non-blocking Vite dynamic import / chunk-size warnings |
| `npm ci` | `/Users/apple/Exec/Code/osmx-dw1-main-review/frontend` | passed; reported 5 audit vulnerabilities (2 moderate, 3 high), no audit fix run |
| `npm run build:check` | `/Users/apple/Exec/Code/osmx-dw1-main-review/frontend` | passed with existing non-blocking Vite dynamic import / chunk-size warnings |
| `go test ./internal/plan/... ./internal/runbook/handler ./internal/runbook/contentpack ./internal/runbook/service ./internal/runbook/repository ./internal/repository -count=1` | `/Users/apple/Exec/Code/osmx-dw1-main-review/osmx-go` | passed with existing `$GOPATH /Users/apple/go` go.mod warning |
| `go test -tags runbook ./internal/runbook -count=1` | `/Users/apple/Exec/Code/osmx-dw1-main-review/osmx-go` | passed with existing `$GOPATH /Users/apple/go` go.mod warning |
| `go test -tags 'plan runbook' ./internal/plan -count=1` | `/Users/apple/Exec/Code/osmx-dw1-main-review/osmx-go` | passed with existing `$GOPATH /Users/apple/go` go.mod warning |
| `go build -tags 'plan runbook' ./cmd/server` | `/Users/apple/Exec/Code/osmx-dw1-main-review/osmx-go` | passed; generated `osmx-go/server` removed before commit |
| `E2E_FRONTEND_PORT=45174 VITE_API_PROXY_TARGET=http://127.0.0.1:18082 E2E_BACKEND_BASE_URL=http://127.0.0.1:18082 npx playwright test e2e/11-command-center-chain.spec.ts e2e/12-command-center-real-chain.spec.ts e2e/13-asset-flow-real-breadth.spec.ts e2e/14-command-center-plan-binding.spec.ts --reporter=list` | `/Users/apple/Exec/Code/osmx-dw1-main-review/frontend` | `7 passed (22.7s)` |

## Asset & Flow Reality Check

Original real backend inventory on `http://127.0.0.1:18081` before the current-source replay:

- `/api/v1/runbooks?source_type=native_yaml`: `55` native rows observed.
- `/api/v1/runbooks?source_type=afl`: `3259` imported AFL rows observed, all sampled rows are `flow_type=flow`.
- `/api/v1/runbooks?source_type=cloudslang`: `0` rows observed.
- Direct DB aggregate observed `afl / flow = 3259`, `native_yaml / flow = 55`, and no imported `flow_type=operation` rows.

Implication:

- `G3 Asset & Flow Center` now has current-source evidence for native, imported operation, and imported flow.
- `frontend/e2e/13-asset-flow-real-breadth.spec.ts` dynamically imports a minimal real Content Pack operation fixture when the database does not already contain one.
- `/api/v1/runbooks` now uses a lightweight repository projection for list responses, so list pages no longer load `source_content`, `compiled_plan`, or `original_source_content` large text fields.
- `approval_repo.GetLatestByPlanUUID`, `RunbookRepo.GetByUUID`, `ExecutionRepo.GetByPlanApproval`, and `ExecutionRepo.GetByEngineExecutionID` now use `Find + RowsAffected`, preserving `gorm.ErrRecordNotFound` semantics without emitting empty-result GORM logs.
- `/api/v1/runbooks/tree` still shows slow SQL under the old 4900+ row test database. This is recorded as a follow-up migration/index analysis item, not a DW1 slice expansion.
- `http://127.0.0.1:18081` was left running as-is; it still reflects the old dev process until restarted. The passing proof used a temporary current-source backend on `18082`, which was stopped after validation.

## First Handoff To Implementation Owner

```text
你工作在 /Users/apple/Exec/Code/osmx-emergency-main-sync。

请先不要改代码。先读取：
- /Users/apple/Exec/Code/osmx/docs/plans/osmx-product-deadline-2026-05-15-delivery-plan.md
- /Users/apple/Exec/Code/osmx/docs/plans/osmx-deadline-wave1-command-asset-task-pack.md
- /Users/apple/Exec/Code/osmx/docs/plans/osmx-dual-repo-wave-board.md
- /Users/apple/Exec/Code/shared-specs/deadline-wave1-command-asset-dispatch.md

你的第一步输出不是实现，而是：
1. 当前 worktree / branch / dirty baseline 摘要。
2. 哪些既有改动可归入 Deadline Wave 1。
3. 哪些既有改动必须隔离或暂不触碰。
4. 后端 / 前端 / 评估三张最小子任务单。
5. 是否可以把状态板从 dispatched 推到 in_progress。

禁止：
- 不要 reset / checkout / 覆盖现有改动。
- 不要扩张全量 OO Studio / AFL / CloudSlang / Worker/RAS。
- 不要让 shared-specs 成为 runtime / build / test / CI 依赖。
```

## Validation Gate

Implementation cannot report `pass` unless it can provide evidence for:

```text
Login
-> Open Command Center
-> Create/Open Incident
-> Create Plan
-> Request/Approve
-> Execute Asset/Runbook
-> View Run Explorer
-> View Artifact
-> View Audit
```

and:

```text
Open Asset & Flow Center
-> Open native runbook
-> Open imported operation
-> Open imported flow
-> Show readonly / not-supported fallback for unsupported edit surfaces
-> View recent run / artifact / audit
```

Minimum technical checks:

```bash
cd osmx-go
go build ./cmd/server
go build -tags runbook ./cmd/server
go build ./cmd/emergency
go test ./internal/runbook/...
go test ./internal/plan/...
```

```bash
cd frontend
npm install
npm run build
npm run build:check
```

Any unavailable environment must be recorded as `blocked_by_environment` and separated from product-code failure.

## Current Decision

The dispatch ledger has advanced to main-review decision handling. It now has migration replay, real Command Center chain smoke, full current-source Asset & Flow breadth smoke evidence, a delivery package, a PR slice manifest, a recoverable short-session handoff, and clean PR #44.

Current status after the 2026-04-23 05:29 CST PR #44 refresh:

```text
frozen_for_owner_review / GitHub checks passed / current_source_smoke_refreshed / asset_flow_breadth_passed / real_chain_smoke_passed / migration_replay_passed / pass_with_risk
```

This is not final product acceptance and not final merge-ready.

Owner triage:

```text
shared-specs/deadline-wave1-owner-baseline-triage.md
```

Main-review decision package:

```text
shared-specs/deadline-wave1-implementation-delivery-package.md
shared-specs/deadline-wave1-pr-slice-manifest.md
shared-specs/deadline-wave1-owner-merge-review-decision.md
shared-specs/deadline-wave1-main-review-evaluation.md
```

Recoverable Codex handoff:

```text
osmx-emergency-main-sync/docs/agent-handoff-20260423.md
```

Next action:

```text
Owner reviews PR #44. If PR feedback requires code changes, patch only /Users/apple/Exec/Code/osmx-dw1-main-review on branch dw1/command-asset-main-review, rerun the recorded validation set, push updates to GitHub, and keep status pass_with_risk until migration/release DB risk is accepted. Do not perform GitGuardian-side sync or dashboard actions. Do not continue feature/code work while frozen.
```
