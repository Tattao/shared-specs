下面给你两份可直接落地的模板：

1. **多 Agent 任务派单模板**
2. **PR / MR 审查模板**

我按你现在的结构设计：

```text
/workspace/osmx-suite/
├── osmx/
├── osmx-emergency/
├── shared-specs/
└── osmx-suite.code-workspace
```

---

# 1）多 Agent 任务派单模板

建议保存为：

```text
/workspace/osmx-suite/shared-specs/templates/agent-task-dispatch.md
```

内容如下：

```md
# OSMX Suite 多 Agent 任务派单模板

## 任务基本信息

### 任务名称
<!-- 示例：拓扑驱动应急预案编排能力建设 -->



### 任务背景
<!-- 说明为什么要做这个任务，当前痛点是什么，涉及哪个业务场景 -->



### 任务目标
<!-- 说明完成后要达到什么效果 -->



### 任务类型
请选择：

- [ ] core-only：仅涉及 `osmx`
- [ ] emergency-only：仅涉及 `osmx-emergency`
- [ ] cross-repo：同时涉及 `osmx` 与 `osmx-emergency`
- [ ] spec-only：仅涉及 `shared-specs`
- [ ] review-only：仅做审查，不直接改代码
- [ ] test-only：仅补测试或验证

---

## 一、归属判断

### 是否属于主平台能力？
- [ ] 是
- [ ] 否
- [ ] 部分是

说明：



### 是否属于应急场景能力？
- [ ] 是
- [ ] 否
- [ ] 部分是

说明：



### 是否需要沉淀到 shared-specs？
- [ ] 是
- [ ] 否

说明：



---

## 二、仓库边界拆分

### 放入 `osmx` 的内容
<!-- 只写通用、可复用、平台级能力 -->

- 



### 放入 `osmx-emergency` 的内容
<!-- 只写应急场景、预案、切换、演练、指挥调度等能力 -->

- 



### 放入 `shared-specs` 的内容
<!-- 只写架构决策、接口契约、任务说明、规则文档 -->

- 



---

## 三、依赖方向判断

### 预期依赖方向

```text
osmx-emergency -> osmx
```

### 是否存在反向依赖风险？

* [ ] 无
* [ ] 有

说明：

### 是否需要 `osmx` 先提供扩展点？

* [ ] 不需要
* [ ] 需要

需要的扩展点：

### 是否存在重复实现风险？

* [ ] 无
* [ ] 有

说明：

---

## 四、允许修改范围

### `osmx` 允许修改目录

* [ ] `docs/`
* [ ] `backend/`
* [ ] `frontend/`
* [ ] `api/`
* [ ] `contracts/`
* [ ] `plugins/`
* [ ] `tests/`
* [ ] 其他：

### `osmx-emergency` 允许修改目录

* [ ] `docs/`
* [ ] `backend/`
* [ ] `frontend/`
* [ ] `plans/`
* [ ] `templates/`
* [ ] `adapters/`
* [ ] `tests/`
* [ ] 其他：

### `shared-specs` 允许修改目录

* [ ] `architecture/`
* [ ] `api-contracts/`
* [ ] `task-boards/`
* [ ] `decisions/`
* [ ] `templates/`
* [ ] 其他：

---

## 五、禁止修改范围

### 禁止修改的仓库

* [ ] `osmx`
* [ ] `osmx-emergency`
* [ ] `shared-specs`
* [ ] 无

说明：

### 禁止修改的目录或文件

```text
示例：
osmx/backend/core/license/
osmx-emergency/backend/runtime/
shared-specs/decisions/accepted/
```

---

## 六、子 Agent 分派

## 1. 主控 Agent

### 职责

* 判断任务归属
* 拆分仓库边界
* 分派子任务
* 汇总结果
* 检查依赖方向
* 给出最终合并建议

### 是否允许直接改代码？

* [ ] 是
* [ ] 否

### 输出要求

* 任务归属判断
* 仓库边界拆分
* 子任务分派结果
* 风险与回滚说明
* 合并建议

---

## 2. 架构分析 Agent

### 目标仓库

* [ ] `osmx`
* [ ] `osmx-emergency`
* [ ] `shared-specs`
* [ ] 可跨仓库只读分析

### 允许修改

* [ ] 不允许修改，仅输出分析
* [ ] 允许修改文档
* [ ] 允许修改代码

### 输入

### 输出

### 特别要求

* 必须判断能力归属
* 必须指出 core 与 emergency 的边界
* 必须识别是否需要扩展点
* 不得直接写大块业务代码

---

## 3. Core 实现 Agent

### 目标仓库

```text
osmx
```

### 允许修改目录

```text

```

### 禁止修改目录

```text
osmx-emergency/
```

### 输入

### 输出

### 实现要求

* 只能实现通用平台能力
* 不允许写 emergency 专属语义
* 不允许引入反向依赖
* 优先提供 hook、adapter、plugin interface、strategy、registry
* 必须说明下游如何接入

---

## 4. Emergency 实现 Agent

### 目标仓库

```text
osmx-emergency
```

### 允许修改目录

```text

```

### 禁止修改目录

```text
osmx/
```

### 输入

### 输出

### 实现要求

* 只能实现应急场景能力
* 优先复用 `osmx` 能力
* 不允许复制已有 core 抽象
* 必须说明 precheck、execute、validate、rollback、audit
* 必须保留必要的人工干预点

---

## 5. 测试 Agent

### 测试对象

* [ ] `osmx`
* [ ] `osmx-emergency`
* [ ] cross-repo 契约
* [ ] 端到端流程

### 测试范围

* [ ] 单元测试
* [ ] 集成测试
* [ ] 契约测试
* [ ] 回归测试
* [ ] 失败路径测试
* [ ] 回滚测试
* [ ] 人工验证清单

### 输入

### 输出

### 测试重点

* 不只测试 happy path
* 必须覆盖失败路径
* 必须覆盖边界输入
* 必须检查兼容性
* 应急流程必须检查回滚路径

---

## 6. 审查 Agent

### 审查对象

* [ ] `osmx`
* [ ] `osmx-emergency`
* [ ] cross-repo 变更
* [ ] 文档 / 契约
* [ ] 测试

### 输入

### 输出

### 审查重点

* 仓库归属是否正确
* 是否存在主平台污染
* 是否存在反向依赖
* 是否存在重复实现
* 是否存在 breaking change
* 是否缺少测试
* 是否缺少回滚说明
* 是否缺少发布说明

---

## 七、实施顺序

建议顺序：

---

## 八、风险评估

### 兼容性风险

* [ ] 无
* [ ] 有

说明：

### Breaking Change 风险

* [ ] 无
* [ ] 有

说明：

### 架构污染风险

* [ ] 无
* [ ] 有

说明：

### 重复实现风险

* [ ] 无
* [ ] 有

说明：

### 回滚风险

* [ ] 无
* [ ] 有

说明：

### 发布风险

* [ ] 无
* [ ] 有

说明：

---

## 九、验收标准

### 功能验收

* [ ]

### 架构验收

* [ ] 不存在反向依赖
* [ ] 不存在 emergency 逻辑污染 core
* [ ] 不存在通用能力误放入 emergency
* [ ] 仓库边界清晰
* [ ] 目录职责清晰

### 测试验收

* [ ] 单元测试通过
* [ ] 集成测试通过
* [ ] 契约测试通过
* [ ] 回归测试通过
* [ ] 失败路径已验证
* [ ] 回滚路径已验证

### 文档验收

* [ ] 架构说明已更新
* [ ] 接口契约已更新
* [ ] 变更说明已更新
* [ ] 下游接入说明已更新
* [ ] 运维或操作说明已更新

---

## 十、最终合并建议

### 是否建议进入实现？

* [ ] 是
* [ ] 否
* [ ] 需要先补设计

### 是否建议进入测试？

* [ ] 是
* [ ] 否
* [ ] 需要先补实现

### 是否建议合并？

* [ ] 通过
* [ ] 有条件通过
* [ ] 不建议合并

### 合并前必须完成的事项

---

## 十一、主控 Agent 汇总结论

### 总体判断

### 推荐方案

### 不推荐方案


```

---

# 3）更适合 GitHub 的精简版 PR 模板

如果你觉得上面的 PR 模板太完整，可以在实际仓库 `.github/pull_request_template.md` 里用这版精简模板。

建议保存到：

```text
osmx/.github/pull_request_template.md
osmx-emergency/.github/pull_request_template.md
```

内容如下：

```md
# PR Summary

## Target Repository

- [ ] osmx
- [ ] osmx-emergency
- [ ] shared-specs
- [ ] cross-repo

## Change Type

- [ ] Feature
- [ ] Fix
- [ ] Refactor
- [ ] Test
- [ ] Docs
- [ ] API / Contract
- [ ] Architecture
- [ ] Release / Deployment

## What Changed?



## Why?



## Boundary Check

- [ ] This change belongs in the selected repository.
- [ ] No reverse dependency was introduced.
- [ ] No emergency-specific logic was added to osmx.
- [ ] No reusable core logic was buried inside osmx-emergency.
- [ ] No duplicated core abstraction was introduced.

## Dependency Direction

Expected:

```text
osmx-emergency -> osmx
```

Risk:

* [ ] No risk
* [ ] Potential risk
* [ ] Existing issue

Explanation:

## Core Check

Applicable to `osmx` changes:

* [ ] Generic naming
* [ ] Reusable abstraction
* [ ] Clear extension point
* [ ] No emergency-specific semantics
* [ ] Backward compatibility considered

Notes:

## Emergency Check

Applicable to `osmx-emergency` changes:

* [ ] Reuses osmx core capability
* [ ] Emergency semantics are explicit
* [ ] Precheck considered
* [ ] Execute flow considered
* [ ] Validation considered
* [ ] Rollback considered
* [ ] Audit considered
* [ ] Manual intervention considered

Notes:

## Testing

Test command:

```bash

```

Test result:

```text

```

Covered:

* [ ] Unit tests
* [ ] Integration tests
* [ ] Contract tests
* [ ] Regression tests
* [ ] Failure path
* [ ] Rollback path
* [ ] Manual verification

## Compatibility

* [ ] No breaking change
* [ ] Breaking change
* [ ] Not sure

Explanation:

## Documentation

* [ ] README updated
* [ ] Architecture docs updated
* [ ] API contracts updated
* [ ] ADR updated
* [ ] No doc update needed

## Review Conclusion

* [ ] Ready to merge
* [ ] Conditional approval
* [ ] Do not merge yet

Required before merge:

```

---

# 4）推荐的文件放置方式

你的工作区建议最终形成这样：

```text
/workspace/osmx-suite/
├── osmx/
│   ├── AGENTS.md
│   └── .github/
│       └── pull_request_template.md
│
├── osmx-emergency/
│   ├── AGENTS.md
│   └── .github/
│       └── pull_request_template.md
│
├── shared-specs/
│   ├── AGENTS.md
│   └── templates/
│       ├── agent-task-dispatch.md
│       ├── pr-review-template.md
│       └── pr-review-template-lite.md
│
└── osmx-suite.code-workspace
```

---

# 5）一个真实派单示例

比如你要做：

**“拓扑驱动应急切换预案编排能力”**

可以这样填：

```md
# OSMX Suite 多 Agent 任务派单

## 任务名称

拓扑驱动应急切换预案编排能力建设

## 任务目标

基于 OSMX 的通用拓扑抽象与编排能力，在 OSMX Emergency 中实现应急切换预案、原子动作节点、验证节点、回滚节点和演练执行流。

## 任务类型

- [x] cross-repo

## 一、归属判断

### 是否属于主平台能力？
- [x] 部分是

说明：

通用拓扑对象、动作节点注册机制、执行状态机、插件扩展点属于 `osmx`。

### 是否属于应急场景能力？
- [x] 部分是

说明：

切换预案、回滚验证、演练流程、指挥调度页面属于 `osmx-emergency`。

## 二、仓库边界拆分

### 放入 `osmx` 的内容

- 通用 `ActionNode` 接口
- 通用 `ActionRegistry`
- 通用 `PlanExecutor`
- 通用 `TopologyResolver`
- 通用执行状态模型
- 通用审计事件模型

### 放入 `osmx-emergency` 的内容

- `EmergencyPlan`
- `CutoverTask`
- `RollbackTask`
- `PrecheckNode`
- `ValidationNode`
- `DrillExecution`
- 应急切换页面
- 应急执行审计视图

### 放入 `shared-specs` 的内容

- 拓扑驱动编排设计说明
- ActionNode 契约
- EmergencyPlan 执行流说明
- ADR：为何 core 只提供通用编排能力

## 三、依赖方向判断

预期依赖方向：

```text
osmx-emergency -> osmx
```

### 是否存在反向依赖风险？

* [X] 无

### 是否需要 `osmx` 先提供扩展点？

* [X] 需要

需要的扩展点：

* ActionNode 接口
* ActionRegistry
* PlanExecutor
* TopologyResolver

## 六、子 Agent 分派

### 架构分析 Agent

输出：

* core / emergency 能力归属
* ActionNode 契约草案
* PlanExecutor 边界
* EmergencyPlan 与 core Plan 的关系

### Core 实现 Agent

目标仓库：

```text
osmx
```

允许修改：

```text
osmx/backend/
osmx/contracts/
osmx/tests/
osmx/docs/
```

输出：

* 通用 ActionNode
* 通用 ActionRegistry
* 通用 PlanExecutor
* 通用 TopologyResolver
* core 单测

### Emergency 实现 Agent

目标仓库：

```text
osmx-emergency
```

允许修改：

```text
osmx-emergency/backend/
osmx-emergency/frontend/
osmx-emergency/plans/
osmx-emergency/tests/
```

输出：

* EmergencyPlan
* CutoverTask
* RollbackTask
* ValidationNode
* DrillExecution
* 应急页面
* 场景测试

### 测试 Agent

输出：

* core 扩展点测试
* emergency 执行流测试
* 失败路径测试
* 回滚测试
* 契约测试

### 审查 Agent

输出：

* 是否存在 emergency 污染 core
* 是否存在重复实现
* 是否存在反向依赖
* 是否缺少回滚
* 是否建议合并

```

---

# 6）实际使用时的推荐规则

这两份模板的使用节奏建议固定为：

```text
需求进入
  ↓
填写 agent-task-dispatch.md
  ↓
主控 Agent 拆分任务
  ↓
Core / Emergency / Test Agent 执行
  ↓
Review Agent 按 pr-review-template.md 审查
  ↓
人工确认
  ↓
合并
```

这样你的多 Agent 协作就不会只是“几个 bot 一起写代码”，而是变成一条相对稳定的研发流水线：

```text
需求归属 -> 边界拆分 -> 分工实现 -> 测试验证 -> 审查合并
```

最重要的是，这套模板会持续保护三条边界：

```text
1. osmx 不被 emergency 场景污染
2. osmx-emergency 不重复造 core 能力
3. cross-repo 任务始终先拆边界再实现
```
