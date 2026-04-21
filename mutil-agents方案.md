下面直接给你一版可落地的方案，适合：

* 主项目：`osmx`
* 场景子项目：`osmx-emergency`
* 开发方式：VS Code + 多 Agent 协作
* 目标：既能联动开发，又不把代码仓库搅乱

---

# OSMX + OSMX-Emergency VS Code 多项目多 Agent 工作区设计方案

## 1. 总体结论

建议采用：

**同一个 VS Code 工作区（同一个窗口） + 两个独立 Git 仓库 + 分目录 Agent 约束**

也就是：

* `osmx` 独立仓库
* `osmx-emergency` 独立仓库
* 在 VS Code 中通过一个 `.code-workspace` 同时打开
* 用 `AGENTS.md` 和工作规则约束多 Agent 的职责和边界

这是你这个场景最稳的方式。

---

## 2. 为什么这样最合适

你的两个项目不是完全无关，而是明显存在：

* 基础能力复用
* 架构对照
* 模块迁移/抽取
* 场景化增强
* 联调验证

如果分成两个窗口，问题是：

* 来回切换成本高
* 搜索和对照麻烦
* agent 不容易统一调度
* 公共模块改动后不容易同步看影响面

如果直接混成一个仓库，问题又是：

* 发布节奏容易冲突
* 权限边界不清
* 分支策略容易失控
* 后续授权/商业版拆分更麻烦

所以最佳平衡点就是：

**视图层统一，仓库层隔离，协作层受控。**

---

## 3. 推荐目录结构

建议本地目录按下面方式组织：

```text
/workspace/osmx-suite/
├── osmx/                         # 主项目，独立 Git 仓库
│   ├── AGENTS.md
│   ├── README.md
│   ├── docs/
│   ├── backend/
│   ├── frontend/
│   └── ...
│
├── osmx-emergency/               # 应急场景子项目，独立 Git 仓库
│   ├── AGENTS.md
│   ├── README.md
│   ├── docs/
│   ├── backend/
│   ├── frontend/
│   └── ...
│
├── shared-specs/                 # 可选：公共设计说明、接口契约、任务清单
│   ├── architecture/
│   ├── api-contracts/
│   ├── task-boards/
│   └── decisions/
│
└── osmx-suite.code-workspace     # VS Code 工作区文件
```

### 说明

* `osmx`：放主平台通用能力
* `osmx-emergency`：放应急指挥/切换/预案/编排等场景增强
* `shared-specs`：不放源码，放公共规则、架构决策、契约文档
* `.code-workspace`：只做“统一入口”，不承载业务代码

---

## 4. 仓库关系建议

建议保持：

* `osmx`：主线产品仓库
* `osmx-emergency`：扩展产品仓库

不要一上来就变成 monorepo。

### 原因

因为你后面很可能会遇到：

* 主产品单独发布
* 应急版单独授权
* 某些模块只允许在应急版出现
* 不同客户只交付其中一个产品线
* 插件/能力裁剪按版本授权

如果现在就把它们强塞成一个仓库，后面授权模型和交付模型都会变复杂。

---

## 5. VS Code 工作区文件示例

可以直接建一个 `osmx-suite.code-workspace`：

```json
{
  "folders": [
    {
      "name": "osmx",
      "path": "./osmx"
    },
    {
      "name": "osmx-emergency",
      "path": "./osmx-emergency"
    },
    {
      "name": "shared-specs",
      "path": "./shared-specs"
    }
  ],
  "settings": {
    "files.exclude": {
      "**/.git": true,
      "**/node_modules": true,
      "**/dist": true,
      "**/build": true
    },
    "search.exclude": {
      "**/node_modules": true,
      "**/dist": true,
      "**/build": true,
      "**/.next": true
    },
    "editor.formatOnSave": true
  }
}
```

---

## 6. 多 Agent 协作的核心原则

重点不是“同时跑几个 agent”，而是 **如何防止互相踩踏** 。

建议遵循四条铁规则：

### 规则 1：按项目分边界

* Agent A：只改 `osmx`
* Agent B：只改 `osmx-emergency`
* Agent C：只看 `shared-specs` 和 `docs`
* Agent D：只做评审和测试，不直接改核心逻辑

### 规则 2：按职责分边界

不要让所有 agent 都能“分析 + 编码 + 测试 + 重构”。

建议拆成：

* 架构分析 Agent
* 实现 Agent
* 测试 Agent
* 审查 Agent

### 规则 3：按文件夹分边界

即使都在 `osmx` 里，也要尽量限制：

* 一个 agent 改 `backend/`
* 一个 agent 改 `frontend/`
* 一个 agent 改 `docs/`

### 规则 4：主控 Agent 只做编排

主控 Agent 负责：

* 收需求
* 拆任务
* 派发
* 汇总
* 出合并建议

主控 Agent 不要直接下场大改代码。

---

## 7. 推荐的 Agent 角色设计

### 角色 A：主控编排 Agent

职责：

* 识别任务属于 `osmx` 还是 `osmx-emergency`
* 拆分任务
* 指派具体 agent
* 汇总输出
* 控制变更边界

适合处理：

* “把 OSMX 的权限体系同步到 Emergency”
* “根据主平台能力，设计应急版增强模块”

---

### 角色 B：主项目实现 Agent

职责：

* 只改 `osmx`
* 只实现主平台公共能力
* 输出对外契约和扩展点

适合处理：

* 插件机制
* 授权模型
* 基础调度框架
* 公共 UI/公共 API

---

### 角色 C：应急项目实现 Agent

职责：

* 只改 `osmx-emergency`
* 基于主项目能力做场景化扩展
* 不随意反向改主项目核心

适合处理：

* 应急预案编排
* 原子动作节点
* 切换演练流程
* 拓扑驱动处置流

---

### 角色 D：测试与验证 Agent

职责：

* 只补测试
* 只做用例
* 只做回归分析
* 不主动改业务逻辑

适合处理：

* 接口用例
* 场景回归
* 冒烟检查
* 风险清单输出

---

### 角色 E：审查与发布 Agent

职责：

* 审查代码结构
* 检查兼容性
* 检查升级风险
* 检查发布影响面

适合处理：

* 是否破坏主项目抽象
* 是否把应急逻辑污染主平台
* 是否引入循环依赖
* 是否影响授权裁剪

---

## 8. AGENTS.md 组织建议

建议每个仓库都有自己的 `AGENTS.md`，同时可在工作区层准备一份总规则文档。

---

### `osmx/AGENTS.md` 示例

```md
# OSMX Agent Rules

## Scope
This repository is the core platform repository.
Agents working here must only implement generic, reusable, platform-level capabilities.

## Allowed
- Core domain models
- Generic orchestration engine
- License framework
- Plugin loading system
- Shared UI components
- Shared APIs

## Forbidden
- Emergency-specific hardcoded workflows
- Customer-specific business logic
- Scenario-specific topology rules
- Direct changes to osmx-emergency repository

## Output Rules
- Prefer extension points over hardcoded branching
- All new modules must document purpose and boundaries
- Any breaking change must include migration notes
```

---

### `osmx-emergency/AGENTS.md` 示例

```md
# OSMX Emergency Agent Rules

## Scope
This repository is the emergency scenario product based on OSMX core capabilities.

## Allowed
- Emergency workflows
- Runbook orchestration
- Cutover plans
- Atomic action nodes
- Topology-driven response flows
- Emergency-specific UI and APIs

## Forbidden
- Refactoring OSMX core without explicit justification
- Modifying shared abstractions inside OSMX directly
- Introducing duplicated implementations when extension points already exist

## Output Rules
- Prefer adapter/plugin/extension mode
- Keep business semantics explicit
- Every new feature must state dependency on OSMX core
```

---

## 9. 任务拆分规范

以后你给 agent 派任务，尽量不要说：

“把这个功能做完。”

建议改成下面这种方式。

### 好的派单方式

```text
任务名称：应急切换编排能力建设

拆分要求：
1. 主控 Agent：先识别哪些能力应放在 osmx，哪些能力应放在 osmx-emergency
2. 主项目 Agent：仅在 osmx 中补充通用编排引擎扩展点，不实现应急场景细节
3. 应急项目 Agent：在 osmx-emergency 中实现切换预案、动作节点、验证步骤
4. 测试 Agent：补充接口测试、流程回归测试、失败回滚测试
5. 审查 Agent：检查目录边界、依赖方向、升级兼容性
```

这样 agent 才知道怎么协作，而不是全员乱改。

---

## 10. 哪些内容应该放 `osmx`

建议放在主项目 `osmx` 的内容：

* 用户/组织/权限基础框架
* 平台级授权模型
* 通用插件机制
* 通用工作流/编排引擎
* 通用任务调度框架
* 通用审计日志框架
* 通用拓扑模型抽象
* 通用告警/事件输入标准
* 通用 API 网关层
* 通用前端壳与菜单体系

一句话：

**凡是未来可能被多个产品线复用的，都尽量放 `osmx`。**

---

## 11. 哪些内容应该放 `osmx-emergency`

建议放在 `osmx-emergency` 的内容：

* 应急处置预案
* 原子启停动作节点
* 故障切换流程
* 演练编排
* 应急值守视图
* 指挥调度大屏
* 场景化 SOP
* 切换验证逻辑
* 应急联动通知策略
* 故障场景模板

一句话：

**凡是明显带“应急语义”的，尽量放 `osmx-emergency`。**

---

## 12. 如何避免“子项目反向污染主项目”

这是最关键的。

必须坚持一个原则：

**`osmx-emergency` 可以依赖 `osmx`，但不要让 `osmx` 反向依赖 `osmx-emergency`。**

也就是依赖方向必须单向：

```text
osmx  --->  提供平台基础能力
   ^
   |
osmx-emergency  ---> 基于平台能力做场景扩展
```

不能变成：

* `osmx` 里出现 emergency 特有字段
* `osmx` 里硬编码应急菜单
* `osmx` 里写死应急处置流程
* `osmx` 核心服务直接 import 应急模块

否则后面主平台就会被“场景项目”带偏。

---

## 13. 推荐的协作流程

建议固定成这个流程：

### 第 1 步：先分析归属

先判断：

* 是主平台能力？
* 还是应急扩展能力？
* 还是两边都要动？

### 第 2 步：先出边界说明

在任务开始前，先写清：

* 改哪些目录
* 不改哪些目录
* 哪部分放 `osmx`
* 哪部分放 `osmx-emergency`

### 第 3 步：分 Agent 执行

* 主项目 Agent 改主项目
* 应急 Agent 改应急项目
* 测试 Agent 补验证

### 第 4 步：统一审查

由审查 Agent 看：

* 是否越界
* 是否重复实现
* 是否破坏依赖方向
* 是否可回滚

### 第 5 步：人工合并

最后你来拍板，不建议让 agent 全自动合并到主线。

---

## 14. 适合你的一个实战例子

比如现在要做：

**“拓扑驱动应急预案编排能力”**

建议这样拆：

### 放 `osmx`

* 通用拓扑对象模型
* 节点关系抽象
* 通用编排引擎
* 执行状态机
* 原子动作注册框架
* 权限与审计基础能力

### 放 `osmx-emergency`

* 应急预案模板
* 启停顺序编排
* 切换动作节点
* 验证动作节点
* 演练任务流
* 指挥视图与应急看板

这样拆就很清晰。

---

## 15. 什么时候必须分两个窗口

虽然我建议一个工作区，但以下情况建议拆成两个窗口：

* 两边同时跑不同运行环境，日志/终端太乱
* 需要让不同 agent 拿到完全隔离的上下文
* 你正在做高风险重构，不想互相干扰
* `osmx-emergency` 已经独立演化很深
* 当前任务只改一个项目，不需要跨仓对照

也就是说：

**平时一个工作区，重构/高风险阶段可临时分窗口。**

---

## 16. 最终建议

给你一个最直接的落地结论：

### 推荐形态

* 一个 VS Code 工作区
* 一个窗口
* 两个独立仓库
* 每个仓库独立 `AGENTS.md`
* 工作区统一管理规则
* 多 Agent 按项目和职责隔离

### 不推荐形态

* 两个项目代码混一个仓库
* 多个 agent 同时无边界改两个项目
* 应急逻辑直接写进主平台核心
* 主项目反向依赖子项目

---

## 17. 一句落地版判断

**你的 `osmx` 和 `osmx-emergency`，最适合“同工作区、同窗口、独立仓库、受控协作”，而不是“完全分散开发”或“强行揉成一个仓库”。**

如果你要，我下一条可以继续直接给你两份现成内容：

1. `osmx-suite.code-workspace` 完整可用文件
2. `osmx` / `osmx-emergency` 两份可直接落地的 `AGENTS.md` 模板
