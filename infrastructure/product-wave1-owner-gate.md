# Product Wave 1 Owner Gate

> Status: `approved`
> Date: `2026-04-30`
> Related graph: `infrastructure/product-task-graph-v1.yaml`
> Related task pack: `infrastructure/product-wave1-task-pack.md`

## 1. Decision Requested

Approve a supervised 48-72 hour Product Wave 1 that allows Codex to execute ready tasks from `product-task-graph-v1.yaml` without asking for a new "next step" confirmation after each task.

## 2. Recommended Approval Text

```text
I approve Product Wave 1 under the declared task graph and boundaries.

Codex may execute ready P0/P1 tasks in `shared-specs/infrastructure/product-task-graph-v1.yaml` for 48-72 hours.

Codex must not auto-merge, release, touch production, run destructive commands, close human gates, or exceed declared write scopes.

Codex must stop for product-scope expansion, migration/security/legal/release gates, repeated validation failure, unclear ownership, or any task not represented in the graph.
```

## 3. Scope Allowed After Approval

- Product skeleton and navigation.
- Core contracts and gated API stubs.
- Operational Twin, TelemetrySource, AlertOps, Workcenter, AgentOps, Skill, Resilience, Pack console skeletons.
- Focused tests and build checks.
- Evidence artifacts and wave summaries.

## 4. Scope Still Forbidden

- Auto-merge or release.
- Production operation.
- Secret handling or real credential changes.
- Destructive git/database commands.
- Unreviewed migration strategy changes.
- Hermes product-code write access.
- `shared-specs` as a runtime/build/test/CI/source dependency.

## 5. Expected Output

At wave close:

- task-level artifacts for completed tasks,
- failed-gate list,
- residual-risk list,
- changed file summary,
- validation summary,
- recommendation for Product Wave 2.

## 6. Current Gate State

This document is now approved by Owner message on `2026-04-30`.

Product Wave 1 is approved for supervised continuous execution under the declared boundaries.
