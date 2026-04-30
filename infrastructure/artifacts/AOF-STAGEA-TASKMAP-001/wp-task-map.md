# AOF-STAGEA-TASKMAP-001 WP0-WP13 Stage A Task Map

Verdict: `pass`

## Mapping Principle

Stage A does not implement the whole product. It converts the 40-day complete-product task pack into a guarded execution map and selects low-risk entry tasks.

Rules:

- Do not expand product scope beyond OSMX plans `93`, `94`, `95`, and `96`.
- Prefer docs, contracts, QA inventory, gates, and governance tasks first.
- Product-code tasks remain disabled or human-gated until Stage A dry-run passes.
- `shared-specs` records the queue and evidence; accepted product facts must land back in `osmx`.

## Work Package Map

| WP | Theme | Stage A Action | First Gate |
|----|-------|----------------|------------|
| WP0 | Product Shell and IA | Create navigation and product-surface readiness checklist before UI work | product_scope |
| WP1 | Core Contracts | Draft object/event/API/audit/permission contract inventory | architecture |
| WP2 | Operational Twin | Define CI type and relation contract tasks, defer implementation | architecture |
| WP3 | Observability Fabric | Define telemetry source and timeline contract tasks, defer implementation | architecture |
| WP4 | AlertOps | Define normalized alert and alert-to-incident policy tasks | architecture |
| WP5 | Workcenter / ITSM | Define ticket/change/SLA projection tasks | product_scope |
| WP6 | Incident Autopilot | Define evidence/RCA/plan recommendation traceability tasks | architecture |
| WP7 | AgentOps | Define trace/tool/evidence/human-control schema tasks | architecture |
| WP8 | Skill Fabric | Define ActionSkill and AssetExecution safety tasks | security |
| WP9 | Resilience Lab | Define experiment guardrail and recovery verification tasks | security |
| WP10 | Scenario Pack Console | Define pack manifest and three scenario smoke tasks | product_scope |
| WP11 | NeatLogic Governance | Create legal and architecture reuse governance index | legal |
| WP12 | Complete Product QA | Inventory three complete-product smoke scripts and evidence requirements | none |
| WP13 | Architecture and Technology Upgrade | Draft core boundary matrix and architecture acceptance gate | architecture |

## Stage A Ready Tasks

| Task | Why First | Writes Product Code |
|------|-----------|---------------------|
| `AOF-STAGEA-GATE-001` | Establishes quality gates before execution | No |
| `AOF-STAGEA-TASKMAP-001` | Turns WP0-WP13 into a runnable queue | No |
| `AOF-WP13-BOUNDARY-001` | Prevents complete-product implementation from becoming one-off demo code | No |
| `AOF-WP12-QA-001` | Defines how the complete product will be tested before implementation runs too far | No |
| `AOF-WP11-NEATLOGIC-001` | Keeps licensed reuse governed before importing or adapting code | No |

## Stage B Candidates

These should wait until Stage A dry-run passes:

- WP0 Product Shell IA skeleton.
- WP1 Core contract stubs.
- WP2 Operational Twin model/API skeleton.
- WP3 Telemetry source registry.
- WP4 normalized alert adapter skeleton.
- WP5 Workcenter projection skeleton.
- WP7 AgentOps trace schema.
- WP8 ActionSkill safety model.
- WP10 pack manifest preview.

## Recommended Next Task

Run `AOF-WP12-QA-001` before product-code tasks. A credible smoke and evidence map will keep the MVP honest while architecture and legal gates are still open.
