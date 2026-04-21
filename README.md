# OSMX Suite Shared Specs

`shared-specs` 是 `osmx` 与 `osmx-emergency-main-sync` 的共享协作层。

它用于放置跨仓库协作规则、任务模板、Agent 提示词、契约索引和当前轮次的评估摘要；它不替代 `osmx` 主仓的事实源文档。

`shared-specs` 可以记录草案和跨角色协作过程，但不能单独决定最终产品行为。凡是被采纳并影响 OSMX 产品架构、运行链路、接口契约或验收标准的内容，必须同步落回 `osmx` 的代码、测试、docs、runbook 或 PR 证据中。

## Repository Status

`shared-specs` 是独立协作证据仓 / 非源码仓。

- 本地路径：`/Users/apple/Exec/Code/shared-specs`
- 远端仓库：`https://github.com/Tattao/shared-specs`
- 当前用途：沉淀跨仓规则、评审记录、任务模板和交付证据
- 当前限制：不放业务源码、不放密钥、不放运行数据、不替代 `osmx/docs/plans`
- 远端状态：已配置 `origin` 并推送 baseline
- 运行边界：不得作为 `osmx` 的 runtime / build / CI / test 依赖，不得作为 git submodule

## Source Of Truth

当前阶段的事实源分层固定为：

| 层级 | 权威位置 | 说明 |
|------|----------|------|
| 总计划 / 阶段口径 | `osmx/docs/plans/` | 以 `osmx` 主仓为准 |
| 应急专项实现 | `osmx-emergency-main-sync/` | 只消费主仓事实源并回报实现状态 |
| 跨仓协作规则 | `shared-specs/` | 放索引、模板、提示词和评估摘要 |

如果 `shared-specs` 与 `osmx/docs/plans` 出现冲突，以 `osmx/docs/plans` 为准。

## What Belongs Here

- 多 Agent 派单模板
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
- [AGENTS.md](./AGENTS.md)
- [OSMX_OSMX-Emergency主控Agent系统提示词.md](./OSMX_OSMX-Emergency主控Agent系统提示词.md)
- [Agent系统提示词.md](./Agent系统提示词.md)
- [多Agent任务派单模板.md](./多Agent任务派单模板.md)
- [MR审查模板.md](./MR审查模板.md)

## Operating Rule

跨仓任务开始前，先读本目录的协作规则，再读 `osmx/docs/plans` 的事实源文档，最后进入对应仓库实现或评估。
