# Deadline Wave 1 Owner Merge Review Decision

> Date: 2026-04-23 CST
> Last refreshed: 2026-04-23 05:29 CST
> Scope: `shared-specs` coordination ledger only
> Status basis: `frozen_for_owner_review / GitHub checks passed / decision_ready / current_source_smoke_refreshed / asset_flow_breadth_passed / real_chain_smoke_passed / migration_replay_passed / pass_with_risk`

## Current Decision

建议结论是：**接受 DW1 main-chain review package，并冻结 PR #44 等 owner review**，但当前状态仍然是 `pass_with_risk`，**不等于最终 merge-ready**。

这意味着 owner 可以把这批改动纳入主仓 review 流程，但在 2026-05-15 deadline 之前，仍需要把 dirty baseline、schema/migration 边界、旧进程风险、以及 PostgreSQL runtime/apply follow-up 边界收口后，再做最终合并判断。

2026-04-23 05:29 CST 冻结状态：干净 GitHub PR #44 基于 `github/main@0a07edb`，head `302bfef`，29-file net diff，`security-gate` 与 `GitGuardian Security Checks` 均通过。PR #44 已冻结等 owner review；不要继续加代码，除非 owner/reviewer 返回明确反馈。

PostgreSQL probe: disposable Docker `postgres:15` 下 `cmd/emergency` 的 `/health` 和 `/api/v1/auth/login` 通过，但 runbook AutoMigrate 记录 `ERROR: type "mediumtext" does not exist`，导致 `osm_runbook_execution` 不存在；`003_mainchain_core.postgres.sql` 可 apply，`003_approval_execution_links.postgres.sql` 因缺表失败。该问题作为单独 follow-up lane，不再扩大 PR #44。

## 建议纳入 Main-Review 的文件切片

以下切片可以进入 DW1 main-review：

Exact PR gate: `deadline-wave1-pr-slice-manifest.md` currently records clean PR #44 as a 29-file net diff; `osmx-go/emergency`, `osmx-go/server`, Playwright output, and local handoff docs are not included.

### Backend main-chain

- `osmx-go/internal/app/app.go`
- `osmx-go/internal/extension/extension.go`
- `osmx-go/internal/plan/extension.go`
- `osmx-go/internal/plan/extension_test.go`
- `osmx-go/internal/plan/handler/chain_handler.go`
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

### Backend asset-flow

- `osmx-go/internal/runbook/handler/contentpack.go`
- `osmx-go/internal/runbook/handler/contentpack_enrich_test.go`
- `osmx-go/internal/runbook/contentpack/manager.go`
- `osmx-go/internal/runbook/contentpack/manager_test.go`

### Frontend main-chain

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

### E2E evidence

- `frontend/e2e/11-command-center-chain.spec.ts`
- `frontend/e2e/12-command-center-real-chain.spec.ts`
- `frontend/e2e/13-asset-flow-real-breadth.spec.ts`
- `frontend/e2e/14-command-center-plan-binding.spec.ts`

## 建议 owner 成组批准 / 暂缓的边界文件

### 建议成组批准

这些文件属于 DW1 的 schema/model/migration/runtime/front 边界，适合 owner 一并做成组决策，而不是拆散单独判：

- `osmx-go/internal/model/approval.go`
- `osmx-go/internal/runbook/model/model.go`
- `osmx-go/internal/runbook/model/execution_model.go`
- `osmx-go/migrations/003_approval_execution_links.mysql.sql`
- `osmx-go/migrations/003_approval_execution_links.postgres.sql`
- `osmx-go/migrations/003_approval_execution_links.sql`

### 建议暂缓或单独确认

这些属于 runtime robustness 或前端边界，建议 owner 在确认 main-review slice 不扩大后，再决定是否并入本次合并建议：

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
- `frontend/src/views/runbook/FlowDesignerView.vue`
- `frontend/src/components/flow/PropertyPanel.vue`
- `frontend/vite.config.ts`

## 明确禁止合并项

- **禁止合并 `osmx-go/emergency` 二进制**。这是 tracked binary artifact，不是产品源码，不应进入 DW1 merge candidate。

## 协调 / 工具文件隔离

以下 dirty 文件不属于 DW1 产品源码切片。可以作为协调或测试基础设施单独审阅，但不要混进 main-review product slice：

- `AGENTS.md`
- `docs/plans/osmx-dual-repo-agent-operator-runbook.md`
- `docs/plans/osmx-dual-repo-wave-board.md`
- `frontend/playwright.config.ts`

## 18081 / 18082 风险说明

- `http://127.0.0.1:18081` 仍是旧进程风险位，不能默认视为 current-source 证明。
- 当前 `3/3` asset-flow proof 来自临时启动的 `18082` current-source backend，验证完成后已停止。
- 因此，`18081` 上的结果只能当作历史运行痕迹，不可替代 owner 合并判断所需的当前源证明。

## 03:43 Repository Hardening Evidence

- `/api/v1/runbooks` 列表仓库查询已改为 lightweight projection，不再加载 `source_content`、`compiled_plan`、`original_source_content` 大字段。
- approval latest-by-plan、runbook get-by-uuid 与 execution lookup 空结果路径保持 `gorm.ErrRecordNotFound` 语义，同时避免 GORM 空结果日志噪声。
- 已通过 `go test ./internal/runbook/repository ./internal/repository -count=1`、DW1 核心 Go 测试、runbook/plan tag 测试、`go build -tags 'plan runbook' ./cmd/server`、当前源 18082 Playwright `11-14` 全量 smoke、diff checks、PR checklist lint、GitHub `security-gate` 和 GitGuardian check。

## 2026-05-15 Deadline 下的下一步 Gates

1. owner 接受本文件定义的 main-review slice，并保持结论为 `pass_with_risk`，不提前升级为 final merge-ready。
2. owner 对 schema/model/migration 边界做成组批准，确认 `approval` / `execution` 连接关系不会扩张到非 DW1 范围。
3. 复核 `18081` 是否已切到 current source；若未切换，则必须继续把它视为旧进程风险。
4. 在同一 source 基线下重跑 main-chain smoke，确保 `Plan -> Approval -> AssetExecution -> Artifact -> Audit` 和 `Asset & Flow` 读路径都能闭环。
5. 合并前再次核对 dirty baseline isolation，确认非 DW1 文件与二进制未泄漏进 review 包。
6. 仅在以上 gates 都收口后，再把状态从 `pass_with_risk` 推向最终 merge-ready。

## 简短结论

本轮最适合交给 owner 的动作不是“直接合并”，而是“**接受 main-review 包，冻结 PR #44，批准主链切片，暂缓边界扩张，继续保持 `pass_with_risk`**”。
