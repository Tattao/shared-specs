# OSMX Suite Shared Specs

`shared-specs` 是 `osmx` 与 `osmx-emergency-main-sync` 的共享协作层，也是未来多 Agent、多模块并行开发的协调账本。

它用于放置跨仓库协作规则、任务模板、Agent 提示词、契约索引、Agent 登记、模块 ownership、PR 队列、冲突账本和当前轮次的评估摘要；它不替代 `osmx` 主仓的事实源文档。

`shared-specs` 可以记录草案和跨角色协作过程，但不能单独决定最终产品行为。凡是被采纳并影响 OSMX 产品架构、运行链路、接口契约或验收标准的内容，必须同步落回 `osmx` 的代码、测试、docs、runbook 或 PR 证据中。

## Repository Status

`shared-specs` 是独立协作证据仓 / 非源码仓。

- 本地路径：由执行环境配置，当前推荐使用 `SHARED_SPECS_REPO`
- 远端仓库：`https://github.com/Tattao/shared-specs`
- 当前用途：沉淀跨仓规则、评审记录、任务模板、Agent 登记、模块边界、PR 队列和交付证据
- 当前限制：不放业务源码、不放密钥、不放运行数据、不替代 `osmx/docs/plans`
- 远端状态：已配置 `origin` 并推送 baseline
- 运行边界：不得作为 `osmx` 的 runtime / build / CI / test 依赖，不得作为 git submodule

## Autonomous Delivery MVP

`2026-04-30` 起，Codex / 多 Agent 7x24 自主交付的 MVP 入口为:

- [infrastructure/autonomous-delivery-mvp.md](./infrastructure/autonomous-delivery-mvp.md)
- [infrastructure/task-queue-v2.yaml](./infrastructure/task-queue-v2.yaml)
- [infrastructure/agent-pool-v2.yaml](./infrastructure/agent-pool-v2.yaml)
- [infrastructure/quality-gates-v2.yaml](./infrastructure/quality-gates-v2.yaml)
- [infrastructure/runner-v2.py](./infrastructure/runner-v2.py)

v2 配置只承担 `Stage A: 8 小时无人值守` 的试运行，不自动合并，不自我批准，不执行生产变更。旧 `task-queue.yaml`、`agent-pool.yaml`、`quality-gates.yaml` 保留为历史 DW1 / DW2 队列记录，不再作为新一轮完整体产品 Alpha 的默认入口。

运行前建议设置:

```bash
export OSMX_WORKSPACE_ROOT=/Users/shitao/Projects/Codex
export OSMX_REPO=$OSMX_WORKSPACE_ROOT/osmx
export SHARED_SPECS_REPO=$OSMX_WORKSPACE_ROOT/shared-specs
export OSMX_ARTIFACT_ROOT=$SHARED_SPECS_REPO/infrastructure/artifacts
```

## Source Of Truth

当前阶段的事实源分层固定为：

| 层级 | 权威位置 | 说明 |
|------|----------|------|
| 总计划 / 阶段口径 | `osmx/docs/plans/` | 以 `osmx` 主仓为准 |
| 应急专项实现 | `osmx-emergency-main-sync/` | 只消费主仓事实源并回报实现状态 |
| 跨仓协作账本 | `shared-specs/` | 放索引、模板、提示词、Agent 登记、handoff、PR 队列、冲突账本和评估摘要 |

如果 `shared-specs` 与 `osmx/docs/plans` 出现冲突，以 `osmx/docs/plans` 为准。

## What Belongs Here

- 多 Agent 派单模板
- 多 Agent / 多模块并行执行登记表
- worktree / branch / write-scope ownership 记录
- PR 队列、冲突账本和合流顺序
- PR / MR 审查模板
- 主控、Core、Emergency、Review Agent 标准提示词
- 跨仓库契约索引
- 当前基线评估和阅读清单
- 双仓协作边界说明

## What Does Not Belong Here

- `osmx` 主仓战略事实源全文
- `osmx-emergency-main-sync` 的业务实现代码
- 历史报告、截图、培训材料、外部 PDF
- 会让两个仓库产生第二套产品方向的计划文档
- 密钥、token、`.env`、运行数据和构建产物
- 会让 `osmx` 构建、测试或运行依赖本仓当前 HEAD 的脚本或配置

## Multi-Agent Operating Role

未来所有并行开发轮次都必须把 `shared-specs` 当作协作账本使用。

当前新任务默认采用 Codex-first guarded autonomy。旧文档里的 Hermes / Claude Code 混合编排只作为历史参考，除非新的 OSMX 事实源文档重新启用。

每个 Agent 开工前登记：

- Agent / 模块 / 角色
- worktree
- branch
- 允许写入路径
- 输入计划文档
- 预期交付物
- 可能影响的 PR 或模块

每个 Agent 收工后登记：

- changed files
- validation commands
- commit / PR
- pass / fail / blocked 结论
- 剩余风险
- 需要 Integration Captain 处理的冲突

长会话必须提前落盘，不等自动压缩救场：

- 上下文到 70% - 80% 时，在当前执行仓写入或刷新 `docs/agent-handoff-YYYYMMDD.md`。
- handoff 必须包含 `cwd`、`branch`、目标、已修改文件、已运行命令和结果、关键决策、未完成项、阻塞、下一步唯一可执行任务。
- 新会话先读最新 handoff，再读取 handoff 明确列出的输入文档；不要重新规划大路线。
- 多 Agent 不默认 fork 全历史；每个 Agent 只拿窄任务 brief、worktree、branch、write scope 和验收命令。
- 阶段结束前，把 `git diff` 状态、测试结果、失败信息和阻塞原因写回本目录、执行仓 `docs/`、`docs/plans/`、README 或 PR 描述。

历史 DW1 / DW2 可恢复入口：

以下内容保留为 2026-04-23 前后 DW1 / DW2 的历史恢复信息，不作为 `2026-04-30` 后 Codex autonomous delivery Stage A 的默认入口。

- `/Users/apple/Exec/Code/osmx-emergency-main-sync/docs/agent-handoff-20260423.md`
- PR #44 已合并，merge commit `dc0366d91da6e821efb947a7fd68fe4334f311e3`；PR #45 / PR #46 也已合并，当前 `origin/main` 为 `d0c0a00b4e25f3c26175d8758dab5f99f6fdf6e0`。
- 最新 DW2 状态：Track B 真实 LLM 冒烟通过；Track C Real Qdrant SLA 已 seed 后通过；Track D Compose alternate-port 验证为 `pass_with_environment_notes`；PR #48 等待人工合并。
- Codex 恢复入口：`codex-handoff-20260423-dw2.md` 与 `infrastructure/task-queue.yaml`。当前不再纯 watch，后续并行队列为 Track C 产品化、Track D Compose fresh-volume/default-port 强化、PostgreSQL apply/runtime smoke。

Integration Captain 在这里维护：

- 并行 Agent 队列
- 模块 ownership 矩阵
- PR 合流顺序
- 回归验证矩阵
- 跨模块冲突和裁决记录

这些记录用于协调和审计，不直接定义产品行为。任何被采纳并影响产品行为、接口契约、状态机或验收标准的内容，必须同步落回 `osmx/docs/plans`、代码、测试、runbook 或 PR。

## Current Canonical Entry Points

- [current-baseline-assessment.md](./current-baseline-assessment.md)
- [wave1-emergency-owner-summary-package.md](./wave1-emergency-owner-summary-package.md)
- [wave1-main-repo-evaluation.md](./wave1-main-repo-evaluation.md)
- [wave1-owner-decision-and-merge-back-plan.md](./wave1-owner-decision-and-merge-back-plan.md)
- [wave1-merge-back-execution-report.md](./wave1-merge-back-execution-report.md)
- [wave1-merge-back-pr-description.md](./wave1-merge-back-pr-description.md)
- [wave1-pr2-review-report.md](./wave1-pr2-review-report.md)
- [architect-j-review-handoff.md](./architect-j-review-handoff.md)
- [wave2-shared-specs-governance-boundary.md](./wave2-shared-specs-governance-boundary.md)
- [wave2-p0-public-credential-cleanup.md](./wave2-p0-public-credential-cleanup.md)
- [wave2-mother-task-brief-dispatch.md](./wave2-mother-task-brief-dispatch.md)
- [deadline-wave1-command-asset-dispatch.md](./deadline-wave1-command-asset-dispatch.md)
- [deadline-wave1-owner-baseline-triage.md](./deadline-wave1-owner-baseline-triage.md)
- [deadline-wave1-implementation-delivery-package.md](./deadline-wave1-implementation-delivery-package.md)
- [deadline-wave1-owner-merge-review-decision.md](./deadline-wave1-owner-merge-review-decision.md)
- [deadline-wave1-main-review-evaluation.md](./deadline-wave1-main-review-evaluation.md)
- [deadline-wave1-pr-owner-handoff.md](./deadline-wave1-pr-owner-handoff.md)
- [deadline-wave1-pr-slice-manifest.md](./deadline-wave1-pr-slice-manifest.md)
- [deadline-wave1-dirty-baseline-isolation-list.md](./deadline-wave1-dirty-baseline-isolation-list.md)
- [stage1-parallel-agent-execution-board.md](./stage1-parallel-agent-execution-board.md)
- [multi-agent-module-registry.md](./multi-agent-module-registry.md)
- [AGENTS.md](./AGENTS.md)
- [OSMX_OSMX-Emergency主控Agent系统提示词.md](./OSMX_OSMX-Emergency主控Agent系统提示词.md)
- [Agent系统提示词.md](./Agent系统提示词.md)
- [多Agent任务派单模板.md](./多Agent任务派单模板.md)
- [MR审查模板.md](./MR审查模板.md)

## Operating Rule

跨仓任务开始前，先读本目录的协作规则，再读 `osmx/docs/plans` 的事实源文档，最后进入对应仓库实现或评估。
