# Product Wave 2 Owner Gate

> Status: `approved`
> Date: `2026-04-30`
> Related graph: `infrastructure/product-wave2-task-graph-v1.yaml`
> Related task pack: `infrastructure/product-wave2-task-pack.md`

## 1. Decision Requested

Approve a supervised 48-72 hour Product Wave 2 that allows Codex to execute ready P0/P1 tasks from `product-wave2-task-graph-v1.yaml` without asking for a new "next step" confirmation after each task.

## 2. Recommended Approval Text

```text
I approve Product Wave 2 under the declared task graph and boundaries.

Codex may execute ready P0/P1 tasks in `shared-specs/infrastructure/product-wave2-task-graph-v1.yaml` for 48-72 hours.

Codex must not auto-merge, release, touch production, run destructive commands, apply migrations without a human gate, close human gates, or exceed declared write scopes.

Codex must stop for product-scope expansion, migration/security/legal/release gates, repeated validation failure, unclear ownership, or any task not represented in the graph.
```

## 3. Scope Allowed After Approval

- AOF runtime-backed read API slices.
- Frontend runtime binding for Product Wave 1 skeletons.
- Focused Go, Python, and frontend validations.
- Smoke evidence and DB guardrail reports.
- Wave summary and next-wave proposal.

## 4. Scope Still Forbidden

- Auto-merge or release.
- Production operation.
- Secret or real credential changes.
- Production model config changes.
- Destructive git/database commands.
- Migration apply without explicit human gate.
- Security/legal/release gate closure.
- Hermes product-code write access.
- `shared-specs` as runtime/build/test/CI/source dependency.

## 5. Current Gate State

This document is now approved by Owner message on `2026-04-30`.

Product Wave 2 is approved for supervised continuous execution under the declared task graph and boundaries.
