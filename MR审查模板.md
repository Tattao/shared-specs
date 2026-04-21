下面给你两份可直接落地的模板：

1. **PR / MR 审查模板**

我按你现在的结构设计：

```text
/workspace/osmx-suite/
├── osmx/
├── osmx-emergency/
├── shared-specs/
└── osmx-suite.code-workspace
```

---


```

---

# 2）PR / MR 审查模板

建议保存为：

```text
/workspace/osmx-suite/shared-specs/templates/pr-review-template.md
```

也可以分别复制到：

```text
osmx/.github/pull_request_template.md
osmx-emergency/.github/pull_request_template.md
```

内容如下：

```md
# OSMX Suite PR / MR 审查模板

## 一、变更基本信息

### PR 标题
<!-- 示例：core: add generic action node registry -->



### 关联任务 / Issue
<!-- 示例：#123 或 shared-specs/task-boards/xxx.md -->



### 目标仓库
- [ ] `osmx`
- [ ] `osmx-emergency`
- [ ] `shared-specs`
- [ ] cross-repo

### 变更类型
- [ ] 新功能
- [ ] Bug 修复
- [ ] 重构
- [ ] 测试补充
- [ ] 文档更新
- [ ] 接口调整
- [ ] 架构调整
- [ ] 发布 / 部署调整
- [ ] 其他：



---

## 二、变更摘要

### 本次改了什么？



### 为什么要改？



### 不在本次范围内的内容



---

## 三、仓库归属审查

### 本次变更是否放对仓库？
- [ ] 是
- [ ] 否
- [ ] 部分需要调整

说明：



### 是否涉及 `osmx`
- [ ] 否
- [ ] 是

若涉及，说明属于哪类平台能力：

- [ ] 通用领域模型
- [ ] 通用编排能力
- [ ] 插件 / 扩展点
- [ ] 通用权限
- [ ] 通用授权 / License / Capability
- [ ] 通用审计
- [ ] 通用拓扑抽象
- [ ] 公共 API
- [ ] 公共 UI
- [ ] 测试工具
- [ ] 文档
- [ ] 其他：



### 是否涉及 `osmx-emergency`
- [ ] 否
- [ ] 是

若涉及，说明属于哪类应急能力：

- [ ] 应急预案
- [ ] 切换流程
- [ ] 回切流程
- [ ] 演练流程
- [ ] 原子动作节点
- [ ] 验证步骤
- [ ] 指挥调度视图
- [ ] 应急看板
- [ ] 场景 API
- [ ] 场景测试
- [ ] 其他：



### 是否涉及 `shared-specs`
- [ ] 否
- [ ] 是

若涉及，说明属于哪类内容：

- [ ] 架构说明
- [ ] ADR
- [ ] 接口契约
- [ ] 任务拆分
- [ ] 规则模板
- [ ] 发布说明
- [ ] 其他：



---

## 四、依赖方向审查

### 当前依赖方向是否正确？

预期方向：

```text
osmx-emergency -> osmx
```

* [ ] 正确
* [ ] 存在风险
* [ ] 不正确

说明：

### 是否出现反向依赖？

* [ ] 否
* [ ] 是

检查项：

* [ ] `osmx` 没有 import / require / reference `osmx-emergency`
* [ ] `osmx` 没有 emergency 专属字段
* [ ] `osmx` 没有 emergency 专属流程
* [ ] `osmx` 没有 emergency 专属菜单
* [ ] `osmx` 没有 customer-specific 逻辑

问题说明：

---

## 五、边界审查

### 是否存在主平台污染？

* [ ] 否
* [ ] 是

说明：

### 是否存在通用能力误放入 `osmx-emergency`？

* [ ] 否
* [ ] 是

说明：

### 是否存在重复实现？

* [ ] 否
* [ ] 是

说明：

### 是否应抽象为 core 扩展点？

* [ ] 否
* [ ] 是

建议扩展点：

---

## 六、设计审查

### 是否符合设计目标？

* [ ] 是
* [ ] 否
* [ ] 部分符合

说明：

### 是否引入新的抽象？

* [ ] 否
* [ ] 是

新增抽象：

### 是否有清晰输入 / 输出？

* [ ] 是
* [ ] 否

说明：

### 是否有清晰失败处理？

* [ ] 是
* [ ] 否
* [ ] 不适用

说明：

### 是否有清晰回滚路径？

* [ ] 是
* [ ] 否
* [ ] 不适用

说明：

---

## 七、代码审查

### 代码结构

* [ ] 目录位置合理
* [ ] 模块职责清晰
* [ ] 命名清晰
* [ ] 无明显重复逻辑
* [ ] 无无关改动
* [ ] 无临时调试代码
* [ ] 无硬编码敏感配置
* [ ] 无明显性能退化风险

问题说明：

### Core 代码专项检查

适用于 `osmx`：

* [ ] 命名足够通用
* [ ] 没有 emergency 专属语义
* [ ] 没有 customer-specific 逻辑
* [ ] 提供了合理扩展点
* [ ] 下游接入方式清晰
* [ ] 向后兼容性已考虑

问题说明：

### Emergency 代码专项检查

适用于 `osmx-emergency`：

* [ ] 复用了 core 能力
* [ ] 没有重复造 core 能力
* [ ] 应急语义清晰
* [ ] precheck 清晰
* [ ] execute 清晰
* [ ] validate 清晰
* [ ] rollback 清晰
* [ ] audit 清晰
* [ ] 支持必要人工干预

问题说明：

---

## 八、接口 / 契约审查

### 是否修改 API？

* [ ] 否
* [ ] 是

说明：

### 是否修改数据结构？

* [ ] 否
* [ ] 是

说明：

### 是否修改配置项？

* [ ] 否
* [ ] 是

说明：

### 是否需要更新接口契约？

* [ ] 否
* [ ] 是

应更新位置：

```text
shared-specs/api-contracts/
```

说明：

### 是否存在兼容性影响？

* [ ] 否
* [ ] 是

说明：

---

## 九、测试审查

### 已完成测试类型

* [ ] 单元测试
* [ ] 集成测试
* [ ] 契约测试
* [ ] 回归测试
* [ ] 失败路径测试
* [ ] 回滚测试
* [ ] 手工验证
* [ ] 暂未测试

### 测试命令

```bash

```

### 测试结果

```text

```

### 未覆盖测试

```text

```

### 是否只覆盖 happy path？

* [ ] 否
* [ ] 是

说明：

### 是否需要补充测试？

* [ ] 否
* [ ] 是

建议补充：

---

## 十、应急流程专项审查

适用于 `osmx-emergency`。

### 是否涉及应急执行流？

* [ ] 否
* [ ] 是

若是，请检查：

* [ ] 有 precheck
* [ ] 有 execute
* [ ] 有 validate
* [ ] 有 rollback
* [ ] 有 audit
* [ ] 有状态可视化
* [ ] 有失败处理
* [ ] 有人工干预点
* [ ] 有操作日志
* [ ] 有误操作防护

### 失败路径说明

### 回滚路径说明

### 人工干预说明

### 审计说明

---

## 十一、安全与权限审查

### 是否涉及权限控制？

* [ ] 否
* [ ] 是

说明：

### 是否涉及 License / Capability 控制？

* [ ] 否
* [ ] 是

说明：

### 是否涉及敏感操作？

* [ ] 否
* [ ] 是

说明：

### 是否需要操作审计？

* [ ] 否
* [ ] 是

说明：

### 是否存在安全风险？

* [ ] 否
* [ ] 是

说明：

---

## 十二、兼容性与迁移审查

### 是否为 breaking change？

* [ ] 否
* [ ] 是
* [ ] 不确定

说明：

### 是否需要迁移脚本？

* [ ] 否
* [ ] 是

说明：

### 是否需要升级说明？

* [ ] 否
* [ ] 是

说明：

### 是否影响旧配置？

* [ ] 否
* [ ] 是

说明：

### 是否影响下游项目？

* [ ] 否
* [ ] 是

影响范围：

---

## 十三、文档审查

### 是否需要更新文档？

* [ ] 否
* [ ] 是

应更新：

* [ ] README
* [ ] 架构文档
* [ ] API 文档
* [ ] 操作文档
* [ ] 部署文档
* [ ] 运维文档
* [ ] ADR
* [ ] 任务说明
* [ ] 其他：

### 文档是否已更新？

* [ ] 是
* [ ] 否
* [ ] 不适用

说明：

---

## 十四、发布审查

### 是否影响发布流程？

* [ ] 否
* [ ] 是

说明：

### 是否需要更新版本号？

* [ ] 否
* [ ] 是

说明：

### 是否需要发布说明？

* [ ] 否
* [ ] 是

说明：

### 是否支持回滚？

* [ ] 是
* [ ] 否
* [ ] 不适用

回滚方式：

---

## 十五、审查结论

### Review Agent 结论

* [ ] 通过
* [ ] 有条件通过
* [ ] 不建议合并

### 结论说明

### 必须修改项

### 建议优化项

### 可后续处理项

---

## 十六、合并前 Checklist

提交人确认：

* [ ] 我已确认变更放在正确仓库
* [ ] 我已确认没有引入反向依赖
* [ ] 我已确认没有把 emergency 逻辑污染到 core
* [ ] 我已确认没有把通用能力误埋在 emergency
* [ ] 我已确认测试已执行或说明未执行原因
* [ ] 我已确认兼容性影响已说明
* [ ] 我已确认回滚方式已说明
* [ ] 我已确认文档已更新或说明无需更新
* [ ] 我已确认无敏感信息、密钥、临时调试代码

审查人确认：

* [ ] 仓库边界通过
* [ ] 依赖方向通过
* [ ] 代码结构通过
* [ ] 测试覆盖通过
* [ ] 兼容性通过
* [ ] 发布风险可接受

---

## 十七、最终合并建议

### 是否允许合并？

* [ ] 允许合并
* [ ] 暂缓合并
* [ ] 不允许合并

### 合并条件

### 合并后跟进事项

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
