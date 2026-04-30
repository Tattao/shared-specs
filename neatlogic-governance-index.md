# NeatLogic Reuse Governance Index

> Status: `stage-a governance draft`
> Date: `2026-04-30`
> Task: `AOF-WP11-NEATLOGIC-001`
> Source repository: `https://gitee.com/neat-logic/neatlogic-itom-all.git`
> Current remote HEAD checked by `git ls-remote`: `8de339b2ce3a8c93b8162f581e5dc060e64aa421`
> OSMX source of truth:
> - `osmx/docs/plans/91-cmdb-itsm-aiops-neatlogic-itop-evaluation.md`
> - `osmx/docs/plans/93-autonomic-operations-fabric-40-day-mvp-task-pack.md`
> - `osmx/docs/plans/94-autonomic-operations-fabric-architecture-technology-upgrade-plan.md`
> - `osmx/docs/architecture/aof-core-boundary-matrix-v0.md`

## 1. Decision

NeatLogic has been commercially and legally confirmed by the owner as reusable within the purchased authorization scope.

The operational decision for OSMX is:

```text
Reuse is allowed.
Core pollution is not allowed.
Source provenance is mandatory.
Customer delivery statements are mandatory.
OSMX core contracts remain autonomous.
```

No NeatLogic code should be copied into `osmx` core modules until a scoped implementation task records:

- authorization evidence location,
- upstream repository URL,
- upstream branch / tag / commit,
- copied files,
- modified files,
- license / delivery statement,
- security and dependency scan result,
- owning OSMX module,
- rollback plan.

## 2. Authorization Evidence Index

| Evidence | Current Status | Required Before Code Movement |
|----------|----------------|-------------------------------|
| Purchased NeatLogic authorization | Owner confirmed | Record contract / license evidence location in private legal store |
| Legal confirmation | Owner confirmed | Record legal reviewer, date, allowed usage, prohibited usage |
| Commercial authorization | Owner confirmed | Record customer delivery / redistribution / embedding scope |
| Source repository | Known | Pin exact commit/tag before copying code |
| Customer delivery statement | Missing | Produce per release / per package |
| Third-party notice | Missing | Produce before packaging reused code |
| Security scan | Missing | Required before merging reused code |
| Dependency scan | Missing | Required before merging reused code |

This public coordination repo must not store contracts, secrets, private license files, or legal documents. It may store indexes and pointers.

## 3. Source Version Index

Remote refs checked on `2026-04-30`:

| Ref | Commit |
|-----|--------|
| `HEAD` | `8de339b2ce3a8c93b8162f581e5dc060e64aa421` |
| `refs/heads/develop4.0.0` | `8de339b2ce3a8c93b8162f581e5dc060e64aa421` |
| `refs/heads/develop3.0.0` | `dd9a89e5fdd27a763ee340b8a93b9e9fcb09089f` |
| `refs/heads/release` | `31d3aefd086ef7f02da71f7ff7ae7bc9ba301116` |
| `refs/tags/3.3.0^{}` | `31d3aefd086ef7f02da71f7ff7ae7bc9ba301116` |
| `refs/tags/4.0.0^{}` | `fedf80cd8a7df8f291e6f0329e1e6215423195fe` |
| `refs/tags/v20250109^{}` | `2586820b7b1787356f404f9750d05c6e61e2cefc` |
| `refs/tags/v20250221^{}` | `62ba3e85f42097723031b7a6cae6689110d3f375` |

Default implementation recommendation:

```text
Use a tag or release branch for code movement, not floating HEAD.
Prefer `4.0.0` or an owner-approved customer deployment version after legal confirmation.
```

## 4. Reuse Lanes

| Lane | Allowed Use | OSMX Location Pattern | Forbidden |
|------|-------------|----------------------|-----------|
| Product reference | Architecture, IA, module split, workflow behavior, object semantics | `osmx/docs/plans`, `osmx/docs/architecture` | Copying code without provenance |
| Data model reference | Mapping CI, process, alert, automation, inspection objects into OSMX contracts | `docs/architecture`, future contract docs | Letting NeatLogic schema define OSMX core |
| `neatlogic-compat` | DTO translators, enum mapping, compatibility helpers | future optional module / compat package | Importing NeatLogic runtime into core |
| `neatlogic-importer` | One-way import from NeatLogic to OSMX contracts | connector / importer module | Replacing OSMX object lifecycle |
| `neatlogic-adapter` | Runtime integration through APIs or connector contracts | connector / adapter module | Direct calls from core domain services |
| `optional-enterprise-module` | Licensed packaged capability with feature gate | optional enterprise package | Mandatory base-platform dependency |
| Migration tooling | Offline migration, source audit, mapping diff | tools / migration package | Running as untracked production path |

## 5. Reusable Module Inventory

| NeatLogic Area | Reuse Value | OSMX Target | Stage A Decision |
|----------------|-------------|-------------|------------------|
| Framework | module architecture, audit, integration, health checks, permissions | platform governance reference | reference only |
| CMDB | CI model, relation, graph, discovery, sync, transaction, resource center | Operational Twin, CIEntity, CIRelation, ImpactGraph | eligible for importer / compat after contract freeze |
| Process / ITSM | process, task, channel, catalog, priority, SLA, assignment, notification | Workcenter, Ticket, ChangeRequest, AssignmentPolicy, SLAPolicy | eligible for mapping and selected reuse |
| Alert | adapter, event lifecycle, alert rule, status, action, subscription, suppression | AlertOps, NormalizedAlert, AlertSourceAdapter, CorrelationGroup | eligible for adapter pattern reuse |
| Autoexec | scripts, orchestration, job control, parameter files, runner concepts | Skill Fabric, ActionSkill, AssetExecution, Worker | reuse concepts first; code only behind execution safety |
| Inspect | application, asset, config, OS, virtualization, middleware, DB, network, container, storage checks | InspectionFinding, Evidence, KnowledgeCandidate, Scenario Packs | eligible as pack content / optional module |
| Report / Dashboard | operational reports and dashboards | Scenario Pack dashboards and Command Center widgets | reference or optional module |
| Runner | automation execution separation | Worker / AssetExecution boundary | reference only unless isolated |
| Web UI | IA and workflow affordances | OSMX product shell and module pages | reference only; keep OSMX brand / UI language |

## 6. Object Mapping

| NeatLogic Object / Concept | OSMX Core Contract | Mapping Rule |
|----------------------------|--------------------|--------------|
| CI model | `CIType` / `CIEntity` schema extension | Keep OSMX type registry as authority; preserve NeatLogic source id |
| CI instance | `CIEntity` | Import with `source=neatlogic`, `external_id`, `source_version` |
| CI relation | `CIRelation` | Normalize relation type to OSMX relation vocabulary |
| CI transaction | `AuditEvent` + `ChangeRequest` + `TimelineEvent` | Changes requiring approval enter OSMX governed action chain |
| Custom view | `TwinView` / report view candidate | Stage B+; not part of core Alpha |
| Process | `WorkflowTemplate` / `TicketWorkflow` | Do not introduce a parallel BPMN runtime in Stage A |
| Process task | `Ticket` / `WorkItem` / `IncidentTask` | Ticket lifecycle remains OSMX-owned |
| Channel | `ServiceChannel` | Service catalog entry or intake channel |
| Catalog | `ServiceCatalog` | Hierarchical catalog; tenant / scope mandatory |
| Priority | `Priority` + `Impact` + `Urgency` | Normalize to ITSM vocabulary |
| Process SLA | `SLAPolicy` | SLA clock and breach events project to timeline |
| Worker dispatcher | `AssignmentPolicy` | Assignment engine is OSMX-owned |
| Audit handler | `AuditEvent Projector` | All actions enter OSMX audit |
| Notify handler | `NotificationPolicy` | Optional outbound integration |
| Alert source | `TelemetrySource` / `AlertSourceAdapter` | Adapter-owned ingestion |
| Alert event | `NormalizedAlert` + `TimelineEvent` | OSMX alert lifecycle is authoritative |
| Alert rule | `AlertToIncidentPolicy` / suppression policy | Policy owns incident creation / correlation |
| Autoexec script | `ActionSkill` | Must include risk, scope, inputs, outputs, validation |
| Job execution | `AssetExecution` | Requires Plan / Approval / Artifact / Audit binding |
| Inspect result | `InspectionFinding` / `EvidenceBlock` | Can generate Alert, Incident, Problem, KnowledgeCandidate |

## 7. Directory and Package Boundary Proposal

No directory is created by this governance task. The following is the implementation target shape.

```text
osmx/
  docs/
    architecture/
      neatlogic-reuse-boundary.md
  third_party/
    neatlogic/
      README.md
      NOTICE.md
      SOURCE.md
      patches/
      upstream/
  osmx-go/
    internal/
      connector/
        neatlogic/
      importer/
        neatlogic/
      compat/
        neatlogic/
      optional/
        neatlogic/
```

Directory rules:

- `third_party/neatlogic/upstream` stores source snapshots only when owner approves code movement.
- `third_party/neatlogic/SOURCE.md` records upstream URL, branch/tag/commit, copied files, and checksums.
- `third_party/neatlogic/patches` records local modifications.
- `osmx-go/internal/compat/neatlogic` may translate DTOs and enums, but cannot own OSMX domain lifecycle.
- `osmx-go/internal/importer/neatlogic` imports into OSMX contracts with `source` and `external_id`.
- `osmx-go/internal/connector/neatlogic` connects to external NeatLogic deployments through connector contracts.
- `osmx-go/internal/optional/neatlogic` is feature-gated and license-gated.

## 8. Implementation Gates

Before any code reuse PR:

| Gate | Required Evidence |
|------|-------------------|
| Legal gate | internal legal evidence pointer, allowed usage, prohibited usage |
| Source gate | upstream URL, branch/tag/commit, file list, checksums |
| Boundary gate | target lane: compat / importer / adapter / optional module |
| Contract gate | mapping to OSMX `CIEntity`, `Ticket`, `ChangeRequest`, `NormalizedAlert`, `ActionSkill`, `AssetExecution`, `InspectionFinding` |
| Security gate | secret scan, dependency scan, dangerous API review |
| Build gate | OSMX build/test results for affected modules |
| Delivery gate | customer-facing statement and third-party notice |
| No-core-pollution gate | no NeatLogic runtime dependency from core platform packages |

## 9. Customer Delivery Statement Template

```text
This OSMX delivery includes [module/capability].

The following parts are OSMX original implementation:
- [list]

The following parts are derived from or adapted under the customer's NeatLogic authorization:
- source repository:
- upstream version / commit:
- copied or adapted files:
- local modifications:
- maintenance owner:
- redistribution / delivery scope:

This capability is isolated behind OSMX feature/license gates and does not replace OSMX core platform contracts.
```

## 10. Next Dispatchable Tasks

| Task | Owner Profile | Scope |
|------|---------------|-------|
| `NEATLOGIC-SOURCE-001` | `claude-code-readonly-evaluator` | Clone or inspect approved NeatLogic version read-only; produce module/file inventory |
| `NEATLOGIC-MAP-CMDB-001` | `codex-architecture` | Produce CMDB object mapping to Operational Twin contract |
| `NEATLOGIC-MAP-ITSM-001` | `codex-architecture` | Produce process / ITSM mapping to Workcenter contract |
| `NEATLOGIC-MAP-ALERT-001` | `codex-architecture` | Produce alert mapping to AlertOps contract |
| `NEATLOGIC-COMPAT-SKELETON-001` | `claude-code-implementation-worker` | Create isolated compat/importer/adapter skeleton after Stage B approval |
| `NEATLOGIC-DELIVERY-NOTICE-001` | `codex-docs-ops` | Draft notice and customer delivery statement |

Stage A stop condition:

```text
Do not copy NeatLogic code in Stage A.
Stage A produces governance, mapping, and dispatch boundaries only.
```

## 11. Toolchain Evidence Paths

The current local 24x7 delivery toolchain has already been documented here:

- `infrastructure/README.md` -> `Local Toolchain Status`
- `infrastructure/artifacts/AOF-STAGEA-TOOLCHAIN-001/summary.md`
- `infrastructure/artifacts/AOF-STAGEA-TOOLCHAIN-001/validation.md`
- `infrastructure/artifacts/AOF-STAGEA-TOOLCHAIN-001/residual-risks.md`
- `infrastructure/artifacts/AOF-STAGEA-TOOLCHAIN-001/handoff.md`

Current verified status:

- `gh` authenticated as `Tattao`.
- Claude Code `playwright` MCP connected.
- Hermes `playwright-min` MCP connected.
- Homebrew installed under user-local prefix.
- Playwright CLI and MCP installed through npm.
