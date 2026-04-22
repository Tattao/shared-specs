# OSM-X 数据库架构评估报告

**报告主题**：OSM-X Control Plane Database Strategy — Keep MySQL Now, Build PostgreSQL Readiness  
**报告对象**：OSM-X / OSMX 多租户数据库智能运维平台  
**整理角色**：架构师 J  
**报告日期**：2026-04-22  
**建议状态**：可作为正式 ADR 草案与 Wave 2 开发边界输入  
**边界说明**：本文件位于 `shared-specs`，仅作为协作台账输入，不作为产品事实源；最终产品事实以 `osmx` 为准。

---

## 目录

1. [执行摘要](#1-执行摘要)
2. [现状概览](#2-现状概览)
3. [总体架构裁决](#3-总体架构裁决)
4. [什么时候需要迁移到 PostgreSQL](#4-什么时候需要迁移到-postgresql)
5. [对原始评估的关键修正](#5-对原始评估的关键修正)
6. [正式数据库战略建议](#6-正式数据库战略建议)
7. [阶段性规划](#7-阶段性规划)
8. [迁移触发阈值与评分机制](#8-迁移触发阈值与评分机制)
9. [迁移难度评估](#9-迁移难度评估)
10. [建议写入 docs 的 ADR 草案](#10-建议写入-docs-的-adr-草案)
11. [Wave 2 对 K1 的开发边界](#11-wave-2-对-k1-的开发边界)
12. [新增数据模型规则](#12-新增数据模型规则)
13. [Incident Commander 主链索引策略](#13-incident-commander-主链索引策略)
14. [本地扫描与验证命令](#14-本地扫描与验证命令)
15. [建议新增验证脚本](#15-建议新增验证脚本)
16. [PostgreSQL Readiness 验收标准](#16-postgresql-readiness-验收标准)
17. [最终裁决](#17-最终裁决)
18. [附录：参考资料](#18-附录参考资料)

---

## 1. 执行摘要

本报告建议将 OSM-X 当前数据库策略正式定为：

```text
现在不迁 PostgreSQL。
Wave 2 不做主库迁移。
但从现在开始，所有新增数据模型、查询、审计、Artifact、Incident Commander 主链，
都必须按“PostgreSQL 可迁移”标准设计。
```

当前 OSM-X 的主库 MySQL 仍然适合承载核心业务数据。项目仍处于 DB Copilot 产品化主轨与 Incident Commander 优先交付专项并行推进阶段，大规模主库迁移会显著干扰交付节奏。

同时，PostgreSQL 已经通过 TimescaleDB 存在于技术栈中。未来如果 OSM-X 进入企业级多租户、复杂审计、Artifact provenance、知识图谱多跳查询、JSONB 高频检索、数据库层 Row-Level Security 等阶段，PostgreSQL 将成为更强的控制平面主库候选。

因此，本报告建议采用：

```text
Keep MySQL Now, Build PostgreSQL Readiness
```

即：

```text
短期保持 MySQL；
中期建设 PostgreSQL readiness；
长期根据真实触发条件决定是否迁移。
```

---

## 2. 现状概览

OSM-X 是一个多租户数据库智能运维平台，当前采用多数据库架构。

| 组件 | 当前技术 | 用途 |
|---|---|---|
| 主数据库 | MySQL 8.0 | 核心业务数据，约 60+ 表 |
| 时序库 | TimescaleDB / PostgreSQL 16 | 监控指标、告警、时间序列数据 |
| 缓存 | Redis 7 | 会话、缓存、短期状态 |
| 向量库 | Qdrant | AI 知识检索、RAG、语义搜索 |

关键事实：

```text
PostgreSQL 已经在技术栈中，TimescaleDB 底层就是 PostgreSQL。
主库 MySQL 目前承载核心业务 OLTP 数据。
Qdrant 当前承担语义检索和向量知识库职责。
Redis 当前承担会话与缓存职责。
```

当前数据库架构不是“纯 MySQL 架构”，而是：

```text
MySQL control-plane OLTP
+ PostgreSQL/TimescaleDB observability time-series
+ Redis cache/session
+ Qdrant vector retrieval
```

这说明 OSM-X 已经具备 PostgreSQL 运维经验，但还没有进入主控制面数据库迁移窗口。

---

## 3. 总体架构裁决

正式裁决：

```text
采纳“不立即迁移 PostgreSQL”的结论。
采纳“中长期 PostgreSQL 更适合作为控制平面主库候选”的方向。
修正“18 个月后必迁”为“满足触发条件后立项评估”。
修正“PG 替代 Qdrant / 合并 TimescaleDB”为“可选收敛，不是默认目标”。
修正“PG 并发一定优于 MySQL”为“PG 的能力组合更适合未来平台控制面”。
```

当前最重要的不是换数据库，而是让数据库架构服务于三条主线：

```text
DB Copilot 产品化
Incident Commander 可审计闭环
未来 Autonomic Command Fabric 控制平面
```

主库迁移本身不创造产品价值。只有当 PostgreSQL 能显著增强以下能力时，才值得正式进入迁移立项：

```text
多租户隔离
审计一致性
知识图谱查询
半结构化数据治理
Artifact provenance
Incident timeline replay
运行态一致性
运维复杂度下降
企业交付合规
```

---

## 4. 什么时候需要迁移到 PostgreSQL

### 4.1 短期：现在到 6 个月，不需要迁移

当前状态适合维持 MySQL，理由如下：

1. **数据规模仍处于开发到中小生产级别**

   当前连接池和 buffer 配置更接近早期生产或中小规模部署，不构成数据库迁移压力。

2. **MySQL 对 CRUD 型业务逻辑已经足够**

   当前主库主要承担核心业务 OLTP、平台对象、用户、配置、计划、审批、执行、审计等数据。只要查询设计合理、索引充分，MySQL 能够继续支撑当前阶段。

3. **项目处于多分支并行开发阶段**

   当前存在 emergency、knowledge-sla、security-release 等多条 feature 或专项分支。主库迁移会显著影响所有分支，带来大量冲突、测试失败和交付延迟。

4. **迁移成本高于当前收益**

   Go 侧 GORM 与 Python 侧 SQLAlchemy 都已绑定当前 MySQL 方言或 MySQL 连接方式。迁移需要处理数据类型、SQL 方言、迁移脚本、测试、CI、部署配置、回滚策略等大量问题。

5. **Wave 2 的核心目标不是数据库替换**

   Wave 2 应聚焦 Incident Commander 主链：

   ```text
   Plan -> Approval -> AssetExecution -> Artifact -> Audit
   ```

   主库迁移会偏离当前最重要的产品闭环目标。

结论：

```text
短期不迁移 PostgreSQL。
短期重点是 PostgreSQL-readiness，而不是 PostgreSQL migration。
```

---

### 4.2 中期：6 到 18 个月，启动迁移评估条件

中期不应默认迁移，但应开始建立正式迁移评估机制。当以下信号出现时，应启动 PostgreSQL 主库候选评估。

| 触发信号 | 说明 |
|---|---|
| 知识图谱查询变复杂 | 项目已有 KnowledgeGraphNode / Edge、TopologyNode / Edge 等模型。当关系查询深度超过 2 层时，PostgreSQL 的递归 CTE 更适合表达多跳关系查询。 |
| JSONB 需求增多 | 多租户元数据、AI 分析结果、Artifact provenance、policy snapshot 等半结构化数据增多时，PostgreSQL JSONB + GIN 索引更适合复杂查询。 |
| 统一技术栈诉求增强 | 已在使用 TimescaleDB / PostgreSQL，维护 MySQL + PostgreSQL 两套关系型数据库会增加运维复杂度和团队认知负担。 |
| 多服务并发写入增强 | Go 控制面和 Python AI 服务如果都需要写主库，应重新评估写入边界。更推荐 Go 控制面收口写入，Python 只产出建议。 |
| 全文搜索需求增强 | 如果应用内需要结构化知识库搜索、审计原因检索、Artifact 元数据搜索，PostgreSQL tsvector / tsquery 可以成为候选能力。 |
| 审计与事件模型增强 | 如果 Audit / Timeline / Execution 逐步演进为 append-only event store，PostgreSQL 的约束、索引、事务和 JSONB 能力更适合长期治理。 |

中期建议动作：

```text
启动 PostgreSQL Readiness 专项，
但不启动主库迁移。
```

---

### 4.3 长期：18 个月以上，进入 PostgreSQL-first 决策窗口

原始评估中写到“长期 18 个月+ 建议迁移”。本报告建议修正为：

```text
18 个月后进入 PostgreSQL-first 决策窗口；
是否迁移取决于触发信号，而不是时间。
```

如果平台发展到以下阶段，PostgreSQL 将成为更优候选：

| 阶段 | PostgreSQL 优势 |
|---|---|
| 企业级多租户 | Row-Level Security 可以在数据库层实现租户隔离，比仅依赖应用层过滤更安全。 |
| AI 功能深化 | pgvector 可作为中小规模、强事务一致、业务数据强关联场景的候选能力。 |
| 时序能力收敛 | 主库迁移到 PostgreSQL 后，可以统一 PostgreSQL 技术栈，但不一定要与 TimescaleDB 合并为同一实例。 |
| 数据合规与审计 | PostgreSQL 在约束、事务、JSONB、审计/event 模型方面更适合复杂控制平面。 |
| 复杂关系查询 | 递归 CTE 能更自然地表达拓扑、血缘、依赖、知识图谱多跳关系。 |

长期目标不是“为了迁移而迁移”，而是：

```text
当 OSM-X 控制平面需要数据库层治理、复杂查询和统一 PostgreSQL 能力组合时，
再正式迁移。
```

---

## 5. 对原始评估的关键修正

### 5.1 修正一：不要绝对化“PostgreSQL 并发优于 MySQL”

原始表达中提到：

```text
Go 服务 + Python AI 服务同时写入主库，PG 的 MVCC 并发控制在高写入场景下优于 MySQL 的锁机制。
```

这个方向可以理解，但表述需要收敛。

更准确的说法是：

```text
MySQL InnoDB 本身也是多版本存储引擎，支持事务并发、一致性读和行级锁。
当 OSM-X 进入复杂事务、强一致审计、多租户隔离、递归图查询、复杂 JSON 查询和跨域分析时，
PostgreSQL 的能力组合更适合平台型控制平面。
```

不应简单表述为：

```text
PG 并发控制一定优于 MySQL。
```

架构判断应从“单点能力优劣”转向“能力组合是否更适合目标控制平面”。

---

### 5.2 修正二：全文搜索不是 PostgreSQL 独有优势

PostgreSQL 有完整的全文搜索能力，但 MySQL 也支持 FULLTEXT 索引和 `MATCH() AGAINST()`。

更准确的判断是：

```text
如果只是轻量知识标题、文档摘要、审计原因检索，MySQL 或应用侧检索可以继续支撑。
如果要做结构化知识库搜索、权限过滤、排序、全文 + JSON 条件组合，PostgreSQL tsvector/tsquery 会更自然。
如果要做大规模语义检索，仍应优先评估 Qdrant / 专用搜索引擎，而不是仅靠 PostgreSQL。
```

因此，全文搜索不能单独作为主库迁移理由。它只能作为 PostgreSQL 能力组合的一部分。

---

### 5.3 修正三：pgvector 不能简单替代 Qdrant

pgvector 可以在 PostgreSQL 中存储向量，并支持 exact / approximate nearest neighbor search、多种距离函数、PostgreSQL JOIN、事务、备份等能力。

但在 OSM-X 当前架构中，Qdrant 不是多余组件。它承担知识库/RAG/语义检索职责，并且可以独立处理向量检索的扩展性、召回策略、embedding metadata 和搜索优化。

因此，本报告建议：

```text
pgvector 是未来“中小规模、强事务一致、向量与业务数据强关联”场景的候选方案。
Qdrant 仍保留为主语义检索引擎，除非后续证明它的运维成本、权限过滤复杂度或一致性成本超过收益。
```

Wave 2 不允许做：

```text
Qdrant -> pgvector 替换
```

---

### 5.4 修正四：TimescaleDB 不应立刻和主库合并

原始评估提到：

```text
主库迁移到 PG 后，TimescaleDB 可以与主库合并，统一管理。
```

这可以作为长期可能性，但不能作为默认目标。

TimescaleDB 的指标、告警、时序数据负载与控制平面 OLTP 负载不同。高频指标写入、压缩、保留策略、连续聚合、时间窗口查询，都可能与核心业务库的事务负载互相影响。

更稳妥的路线是：

```text
可以统一 PostgreSQL 技术栈；
不一定统一同一个数据库实例；
更不应把高频指标写入和核心控制平面 OLTP 直接混在一个库里。
```

长期建议：

```text
同引擎、不同 database / schema / cluster；
按成本、隔离、备份、查询需求决定是否合并。
```

---

## 6. 正式数据库战略建议

### 6.1 当前架构裁决

```text
主库：继续 MySQL
时序：继续 TimescaleDB / PostgreSQL
缓存：继续 Redis
向量：继续 Qdrant
迁移：暂不启动
策略：从今天开始做 PostgreSQL-readiness
```

这意味着：

```text
MySQL 是当前控制面 OLTP 主库；
PostgreSQL 是长期控制面主库候选；
TimescaleDB 是当前时序库；
Qdrant 是当前语义检索主向量库；
Redis 是当前缓存与会话系统。
```

当前最优先的数据库工作不是迁移 PostgreSQL，而是：

```text
补租户字段
补项目字段
补复合索引
补查询隔离
补审计不可变语义
补 Artifact provenance
补 Incident Commander 状态链路一致性
```

---

### 6.2 与 OSM-X 产品阶段的关系

数据库策略必须服从产品阶段。

当前 OSM-X 的产品推进重心是：

```text
DB Copilot 产品化主轨
+ Incident Commander 优先交付专项
```

Wave 2 的核心主链是：

```text
Plan -> Approval -> AssetExecution -> Artifact -> Audit
```

因此，数据库架构应优先服务：

```text
状态机一致性
审批链路完整性
执行幂等性
Artifact provenance
Audit event 完整性
Command Center timeline 可回放
多租户隔离
```

而不是服务于一次大规模存储迁移。

---

## 7. 阶段性规划

### 7.1 0 到 6 个月：维持 MySQL，建立迁移伏笔

本阶段不做主库迁移。

必须做的是：

```text
1. 新增模型必须带 tenant_id / project_id 设计预留
2. 新增查询不得默认跨租户
3. 新增 raw SQL 必须避免 MySQL 专有语法
4. 新增 JSON 字段必须定义 schema_version
5. 新增 audit / artifact / execution 表必须按未来分区、归档、迁移设计
6. 生产迁移逐步从 AutoMigrate 过渡到显式 migration
7. Go 控制面收口核心写入，Python AI 子系统只产出分析与建议
```

本阶段的成功标志：

```text
Wave 2 主链表 tenant-aware、audit-aware、artifact-aware、idempotency-aware、PostgreSQL-ready。
```

---

### 7.2 6 到 18 个月：PostgreSQL 兼容性建设期

这一阶段不是迁移期，而是可迁移能力建设期。

建议新增专项：

```text
DB Portability & PostgreSQL Readiness
```

交付内容：

```text
1. MySQL-specific SQL 扫描清单
2. GORM 模型兼容性矩阵
3. SQLAlchemy / Python 侧 DB 依赖矩阵
4. MySQL -> PostgreSQL 类型映射表
5. migration tooling 规范
6. PostgreSQL shadow schema PoC
7. 关键查询 PostgreSQL EXPLAIN 验证
8. 审计、Artifact、Incident timeline 的 PostgreSQL 适配验证
9. 只读分析型数据模型在 PostgreSQL 上的 PoC
```

优先验证以下读模型：

```text
audit read model
incident timeline read model
knowledge graph read model
artifact metadata read model
reporting / analytics read model
```

不建议在这一阶段直接双写核心业务主库。

---

### 7.3 18 个月后：按触发条件进入迁移立项

18 个月后可以进入 PostgreSQL-first 决策窗口，但是否迁移必须由触发条件决定。

此时可评估的路线包括：

```text
路线 A：继续 MySQL 主库 + PostgreSQL/TimescaleDB 时序库
路线 B：MySQL 主库 + PostgreSQL 只读分析/审计投影库
路线 C：核心控制平面迁移到 PostgreSQL，TimescaleDB 保持独立
路线 D：核心控制平面 PostgreSQL + 时序 PostgreSQL 技术栈统一，但实例隔离
路线 E：部分企业客户独立 PostgreSQL 部署，形成双引擎兼容交付模型
```

默认不建议一次性大爆炸迁移。

---

## 8. 迁移触发阈值与评分机制

### 8.1 不建议用单一数据量触发迁移

原始评估中提出：

```text
当核心表超过 100 万行，或知识图谱查询出现性能瓶颈时，正式启动迁移。
```

本报告建议修正为：

```text
100 万行只是黄色预警，不是迁移触发。
```

数据量本身不是迁移理由。索引、分区、归档、读写分离、缓存、查询优化通常可以先解决大量问题。

---

### 8.2 建议触发阈值

| 触发项 | 建议动作 |
|---|---|
| 单表 > 100 万行 | 建立索引、归档、分区、慢查询监控 |
| 单表 > 1000 万行且 P95 查询 > 500ms | 进入存储策略评估 |
| 审计 / timeline / artifact > 5000 万事件 | 评估事件表分区、归档与 PostgreSQL event model |
| 知识图谱查询 > 2 跳且 P95 > 1s | 评估 PostgreSQL recursive CTE 或图数据库 |
| JSON 条件查询字段 > 5 个且频繁组合 | 评估 PostgreSQL JSONB / GIN |
| 企业租户隔离要求数据库层强约束 | 评估 PostgreSQL RLS |
| MySQL + PostgreSQL 双关系型运维成本显著升高 | 评估统一 PostgreSQL 技术栈 |
| 多客户 PoC 明确要求 PostgreSQL 交付 | 评估 PostgreSQL delivery profile |

---

### 8.3 建议迁移评分规则

满足以下条件中的 3 个以上，再启动主库迁移立项：

```text
[ ] 企业客户要求数据库层租户隔离或审计合规
[ ] Incident / Audit / Artifact 数据量导致 MySQL 查询明显复杂化
[ ] 知识图谱出现多跳递归查询，应用层拼接成本过高
[ ] JSON 元数据查询需要多个高频索引维度
[ ] MySQL + TimescaleDB 双关系型运维成本高于迁移成本
[ ] 需要基于数据库层 RLS 强化租户隔离
[ ] 需要把审计、时间线、执行状态做成强一致 append-only event store
[ ] 多客户 PoC 中 PostgreSQL 成为交付标准要求
```

满足条件后仍然不是直接迁移，而是进入：

```text
PostgreSQL Migration Feasibility Study
```

该研究必须包含：

```text
数据量评估
查询兼容性评估
ORM 兼容性评估
迁移窗口评估
回滚策略
双写/影子读策略
CI 测试矩阵
生产演练计划
客户影响评估
```

---

## 9. 迁移难度评估

| 维度 | 难度 | 原因 |
|---|---|---|
| Go GORM 模型 | 中 | GORM 支持 PostgreSQL，但 MySQL 方言函数、数据类型、索引、upsert、JSON 查询需要改写。 |
| Python SQLAlchemy | 低到中 | SQLAlchemy 方言切换相对容易，但已有连接配置、migration、测试数据、raw SQL 仍需排查。 |
| 数据迁移 | 中 | 约 60+ 表，需要处理 MySQL 到 PostgreSQL 类型映射，例如 TINYINT、DATETIME、JSON、TEXT、AUTO_INCREMENT 等。 |
| 测试覆盖 | 高 | 多分支并行开发，必须确保主链、DB Copilot、AI 子系统、Command Center、runbook 等测试全部通过。 |
| 运维切换 | 低到中 | 已有 TimescaleDB / PostgreSQL 经验，但主库切换涉及备份、恢复、监控、连接池、权限、性能调优和回滚。 |
| 客户交付 | 中到高 | 如果已有客户环境基于 MySQL，迁移会影响部署手册、运维脚本、数据备份和现场支持。 |
| 安全与合规 | 中 | PostgreSQL 可增强 RLS 与审计，但迁移期间需要避免权限回退、数据泄露和跨租户访问。 |

综合判断：

```text
迁移可行，但当前不是最优时机。
```

---

## 10. 建议写入 docs 的 ADR 草案

建议新增文件：

```text
docs/architecture/ADR-DB-001-control-plane-database-strategy.md
```

### ADR 标题

```text
Keep MySQL as current control-plane OLTP database and establish PostgreSQL readiness guardrails
```

### Status

```text
Accepted
```

### Context

OSM-X 当前采用多数据库架构：

```text
MySQL 8.0：核心业务主库
TimescaleDB / PostgreSQL 16：指标与告警时序库
Redis 7：会话与缓存
Qdrant：AI 知识检索与向量库
```

当前产品处于 DB Copilot 产品化主轨与 Incident Commander 优先交付专项并行阶段。Wave 2 的主目标是硬化：

```text
Plan -> Approval -> AssetExecution -> Artifact -> Audit
```

主库迁移会显著干扰当前交付。

### Decision

OSM-X 将在当前 Stage 1 / Wave 2 阶段继续使用 MySQL 作为主控制面 OLTP 数据库。

PostgreSQL 将通过 TimescaleDB 继续存在于技术栈中，并作为未来控制平面主库候选。

所有新增数据模型和查询必须遵守 PostgreSQL-readiness guardrails。

### Rationale

```text
1. 当前交付重点是 DB Copilot 产品化和 Incident Commander governed loop。
2. 主库迁移会干扰 Wave 2 交付。
3. 当前多租户设计可以先通过 shared schema + tenant_id/project_id 在 MySQL 上实现。
4. PostgreSQL 对未来 RLS、JSONB、递归图查询、审计/event 模型和统一关系型技术栈有长期优势。
5. 团队应现在降低未来迁移成本，但不应现在支付完整迁移成本。
```

### Non-goals

```text
1. Wave 2 不做 MySQL -> PostgreSQL 主库迁移。
2. Wave 2 不做 TimescaleDB 与控制面主库合并。
3. Wave 2 不做 Qdrant -> pgvector 替换。
4. Wave 2 不做超出 Incident Commander / DB Copilot 需要的存储平台大重构。
```

### Consequences

```text
1. 新增表必须 tenant-aware、project-aware。
2. 新增 raw SQL 必须避免 MySQL 专有语法，或明确隔离说明。
3. 新增 JSON 字段必须包含 schema_version。
4. Audit、Artifact、Execution、Incident timeline 需要为未来分区、归档、迁移预留。
5. 后续需要建立 DB portability scan 和 migration readiness checklist。
```

---

## 11. Wave 2 对 K1 的开发边界

### 11.1 允许做

K1 本轮可以做数据库架构准备，但不能做主库迁移。

允许范围：

```text
1. 增加数据库架构 ADR
2. 增加 MySQL-specific SQL 扫描脚本
3. 新增表按 tenant_id/project_id 设计
4. 为 Incident Commander 主链表补最小复合索引
5. 为 Audit / Artifact / Execution 定义 schema_version / payload_json / metadata_json 规范
6. 为 raw SQL 增加 dialect guardrail
7. 将生产建表从 AutoMigrate 逐步过渡到 migration-first 规范
8. 建 PostgreSQL shadow schema PoC 文档，但不接入主运行链路
9. 明确 Go 控制面与 Python AI 子系统的数据写入边界
10. 为未来 PostgreSQL 迁移补充类型映射文档
```

### 11.2 禁止做

K1 本轮禁止：

```text
1. 不迁移主库到 PostgreSQL
2. 不引入双写
3. 不让 Go 主平台同时依赖 MySQL 和 PostgreSQL 写核心业务
4. 不把 TimescaleDB 和主库合并
5. 不用 pgvector 替换 Qdrant
6. 不为了数据库迁移扩大 Studio / OO / Worker 功能面
7. 不因为数据库改造影响 Incident Commander 最小闭环
8. 不把 PostgreSQL readiness 做成横向平台重构
9. 不把数据库专项压过 DB Copilot 产品化和 Incident Commander Wave 2 交付
```

---

## 12. 新增数据模型规则

从 Wave 2 开始，所有新表建议遵守以下基础字段约定：

```sql
id
tenant_id
project_id
created_at
updated_at
created_by
updated_by
status
schema_version
```

对 Incident Commander 主链表，建议额外加：

```sql
incident_id
plan_id
approval_id
execution_id
artifact_id
audit_event_id
idempotency_key
risk_level
trace_id
request_id
```

对半结构化字段，建议统一命名：

```text
metadata_json
payload_json
policy_snapshot_json
provenance_json
context_snapshot_json
```

JSON 字段规则：

```text
1. 每个 JSON 字段必须有 schema_version
2. 不允许无边界塞大对象
3. 高频查询字段必须外提成普通列
4. JSON 字段不得成为跨租户过滤的唯一依据
5. tenant_id/project_id 必须是普通列，并有索引
6. JSON payload 必须区分业务数据、上下文快照、策略快照和 provenance
```

建议命名：

| 字段 | 用途 |
|---|---|
| `metadata_json` | 通用元数据，不应承载关键查询维度 |
| `payload_json` | 事件或执行结果的结构化 payload |
| `policy_snapshot_json` | 审批、风险、策略在决策时刻的快照 |
| `provenance_json` | Artifact 来源、输入、执行链路、内容 hash 等来源信息 |
| `context_snapshot_json` | Plan 或 Execution 生成时的上下文快照 |

---

## 13. Incident Commander 主链索引策略

对 Incident Commander 主链，MySQL 当前就应补充索引，不必等 PostgreSQL。

建议最小索引集合：

```sql
(tenant_id, project_id, status)
(tenant_id, incident_id, created_at)
(tenant_id, plan_id, status)
(tenant_id, approval_id, status)
(tenant_id, execution_id, status)
(tenant_id, artifact_id, created_at)
(tenant_id, audit_event_id, created_at)
(tenant_id, idempotency_key)
(trace_id)
(request_id)
```

建议对不同表落地如下：

| 表类型 | 建议索引 |
|---|---|
| incidents | `(tenant_id, project_id, status)`, `(tenant_id, created_at)` |
| plans | `(tenant_id, incident_id, status)`, `(tenant_id, project_id, created_at)` |
| approvals | `(tenant_id, plan_id, status)`, `(tenant_id, approver_id, status)` |
| asset_executions | `(tenant_id, plan_id, status)`, `(tenant_id, idempotency_key)`, `(trace_id)` |
| artifacts | `(tenant_id, incident_id, created_at)`, `(tenant_id, execution_id)` |
| audit_events | `(tenant_id, incident_id, created_at)`, `(tenant_id, subject_type, subject_id)`, `(request_id)` |
| timeline_events | `(tenant_id, incident_id, created_at)`, `(tenant_id, event_type, created_at)` |

索引原则：

```text
1. tenant_id 必须在多租户查询索引前缀中。
2. project_id 用于项目级过滤，不应只依赖应用层过滤。
3. status 和 created_at 是主链列表与 timeline 的核心查询维度。
4. idempotency_key 必须有唯一性或准唯一性约束，避免重复副作用。
5. trace_id / request_id 用于审计、排障和跨服务链路追踪。
```

---

## 14. 本地扫描与验证命令

K1 开工前必须先跑以下扫描命令。

### 14.1 当前 DB driver / ORM 使用扫描

```bash
cd /Users/apple/Exec/Code/osmx-emergency-main-sync

echo "== current DB drivers / ORM usage =="
git grep -nE \
  "gorm.Open|mysql.Open|postgres.Open|sqlalchemy|pymysql|aiomysql|psycopg|mysql\\+|postgresql\\+" \
  -- osmx-go osmx-ai app scripts alembic || true
```

### 14.2 MySQL 专有 SQL 模式扫描

```bash
echo "== MySQL-specific SQL patterns =="
git grep -nE \
  "GROUP_CONCAT|ON DUPLICATE KEY|DATE_FORMAT|JSON_EXTRACT|JSON_UNQUOTE|IFNULL|LAST_INSERT_ID|FIND_IN_SET|AUTO_INCREMENT|ENGINE=|CHARSET=|COLLATE=|tinyint\\(1\\)" \
  -- osmx-go osmx-ai app scripts alembic docs || true
```

### 14.3 Raw SQL inventory

```bash
echo "== raw SQL inventory =="
git grep -nE \
  "Raw\\(|Exec\\(|db\\.Query|db\\.Exec|SELECT |INSERT |UPDATE |DELETE |WITH " \
  -- osmx-go osmx-ai app scripts || true
```

### 14.4 AutoMigrate inventory

```bash
echo "== AutoMigrate inventory =="
git grep -n "AutoMigrate" -- osmx-go osmx-ai app || true
```

### 14.5 Tenancy fields inventory

```bash
echo "== tenancy fields inventory =="
git grep -nE \
  "tenant_id|TenantID|project_id|ProjectID" \
  -- osmx-go osmx-ai app docs | head -200
```

### 14.6 PostgreSQL readiness 文档检查

```bash
echo "== PostgreSQL readiness docs =="
git grep -nE \
  "PostgreSQL|postgres|pgvector|TimescaleDB|JSONB|RLS|recursive CTE|tenant_id|project_id|idempotency_key" \
  -- docs osmx-go osmx-ai app scripts || true
```

---

## 15. 建议新增验证脚本

建议新增文件：

```text
scripts/db-portability-scan.sh
```

建议内容：

```bash
#!/usr/bin/env bash
set -euo pipefail

echo "Scanning MySQL-specific constructs..."

git grep -nE \
  "GROUP_CONCAT|ON DUPLICATE KEY|DATE_FORMAT|JSON_EXTRACT|JSON_UNQUOTE|IFNULL|LAST_INSERT_ID|FIND_IN_SET|AUTO_INCREMENT|ENGINE=|CHARSET=|COLLATE=|tinyint\\(1\\)" \
  -- osmx-go osmx-ai app scripts alembic docs || true

echo "Scanning raw SQL entry points..."

git grep -nE \
  "Raw\\(|Exec\\(|db\\.Query|db\\.Exec" \
  -- osmx-go osmx-ai app scripts || true

echo "Scanning tenant/project coverage..."

git grep -nE \
  "tenant_id|TenantID|project_id|ProjectID" \
  -- osmx-go osmx-ai app docs || true

echo "Scanning AutoMigrate usage..."

git grep -n "AutoMigrate" -- osmx-go osmx-ai app || true

echo "DB portability scan completed."
```

K1 提 PR 时必须附上扫描结果。

---

## 16. PostgreSQL Readiness 验收标准

### 16.1 架构验收

```text
[ ] 新增 ADR 已落入 docs/architecture
[ ] Wave 2 不启动主库迁移
[ ] PostgreSQL 被定义为未来控制平面主库候选，而不是当前迁移目标
[ ] TimescaleDB 仍作为时序库，不与主库合并
[ ] Qdrant 仍作为 RAG 主向量库
[ ] Redis 仍作为缓存与会话组件
```

### 16.2 数据模型验收

```text
[ ] 新增 Incident Commander 主链表带 tenant_id/project_id
[ ] 新增主链查询带租户/项目过滤
[ ] 新增主链表有复合索引
[ ] 新增 JSON 字段有 schema_version
[ ] Artifact / Audit / Execution 表为未来分区和归档预留
[ ] idempotency_key 有索引或唯一性约束设计
```

### 16.3 SQL 与 ORM 验收

```text
[ ] 新增 raw SQL 不使用 MySQL 专有语法，或有明确隔离说明
[ ] MySQL-specific SQL 扫描结果已附在 PR 中
[ ] AutoMigrate 使用范围被识别并记录
[ ] GORM 模型新增字段与 PostgreSQL 类型兼容性已考虑
[ ] SQLAlchemy / Python 侧没有新增核心业务主库写入路径
```

### 16.4 产品交付验收

```text
[ ] 不影响 DB Copilot 产品化主轨
[ ] 不影响 Incident Commander Wave 2 闭环
[ ] 不扩大 Studio / OO / Worker 功能面
[ ] 不引入主库双写
[ ] 不引入 PostgreSQL 主库运行依赖
[ ] 不引入 pgvector 替换 Qdrant
```

---

## 17. 最终裁决

这份数据库评估可以升级成正式架构结论，但建议标题改为：

```text
OSM-X Control Plane Database Strategy:
Keep MySQL Now, Build PostgreSQL Readiness
```

最终裁决：

```text
采纳“不立即迁移 PostgreSQL”的结论。
采纳“中长期 PostgreSQL 更适合作为控制平面主库候选”的方向。
修正“18 个月后必迁”为“满足触发条件后立项评估”。
修正“PG 替代 Qdrant / 合并 TimescaleDB”为“可选收敛，不是默认目标”。
修正“PG 并发一定优于 MySQL”为“PG 的能力组合更适合未来平台控制面”。
```

K1 当前最该做的不是迁库，而是：

```text
让所有 Wave 2 新增数据结构都 tenant-aware、audit-aware、artifact-aware、idempotency-aware、PostgreSQL-ready。
```

这是既不打断当前交付，又能为未来先进性、前瞻性和扩展性埋好地基的路线。

---

## 18. 附录：参考资料

以下资料用于后续 ADR 或技术验证时参考：

- MySQL InnoDB Multi-Versioning：<https://dev.mysql.com/doc/refman/8.4/en/innodb-multi-versioning.html>
- PostgreSQL Full Text Search：<https://www.postgresql.org/docs/current/textsearch.html>
- PostgreSQL JSON / JSONB：<https://www.postgresql.org/docs/current/datatype-json.html>
- pgvector：<https://github.com/pgvector/pgvector>
- TimescaleDB 文档：<https://docs.timescale.com/use-timescale/latest/>

---

## 可复制的 K1 执行口径

```text
K1，Wave 2 不做 MySQL -> PostgreSQL 主库迁移。

当前数据库策略是：
Keep MySQL Now, Build PostgreSQL Readiness。

本轮允许做：
1. 增加数据库架构 ADR
2. 增加 DB portability scan
3. 为 Incident Commander 主链表补 tenant_id/project_id、复合索引、schema_version、idempotency_key
4. 为 Audit / Artifact / Execution 补 PostgreSQL-ready 的字段规范
5. 识别 MySQL-specific SQL 和 AutoMigrate 使用点

本轮禁止做：
1. 不迁移主库到 PostgreSQL
2. 不引入双写
3. 不合并 TimescaleDB 和主库
4. 不用 pgvector 替换 Qdrant
5. 不扩大 Studio / OO / Worker 功能面
6. 不影响 Plan -> Approval -> AssetExecution -> Artifact -> Audit 主链交付

PR 必须附：
1. db-portability-scan 结果
2. 新增/修改表的 tenant/project/index 说明
3. 是否引入 MySQL 专有语法的说明
4. 对 Incident Commander Wave 2 主链的影响说明
```
