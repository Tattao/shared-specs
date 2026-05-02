# Product Wave 4 Owner Gate

> Status: `approved`
> Date: `2026-04-30`
> Related graph: `infrastructure/product-wave4-task-graph-v1.yaml`
> Related task pack: `infrastructure/product-wave4-task-pack.md`

## 1. Current Decision State

Owner approved Product Wave 4 task graph preparation and owner gate setup on `2026-04-30`.

Owner then approved the recommended Product Wave 4 execution plan with the message `按建议执行` on `2026-04-30`.

`PW4-WP4-LIVE-DB-REPLAY-EXECUTION-GATE-001` remains separately blocked until `migration_runtime_replay` approval and disposable DSNs are provided.

## 2. Decision Requested

Product Wave 4 execution is approved for non-DB-replay tasks under the declared graph and boundaries.

## 3. Approval Text

```text
Approved by Owner message: 按建议执行

Codex may execute ready P0/P1 tasks in `shared-specs/infrastructure/product-wave4-task-graph-v1.yaml`.

Codex must not auto-merge, release, touch production, run destructive commands, apply migrations without a human gate, close human gates, or exceed declared write scopes.

Codex must stop for product-scope expansion, migration/security/legal/release gates, repeated validation failure, unclear ownership, or any task not represented in the graph.

`PW4-WP4-LIVE-DB-REPLAY-EXECUTION-GATE-001` still requires separate `migration_runtime_replay` approval and disposable DSNs before any replay execution.
```

## 4. Scope Allowed After Approval

- AOF store-adapter read path binding.
- Runtime provenance and adapter source evidence.
- CI-ready authenticated browser breadth smoke evidence.
- Governed action request API, audit, and UI gate flows that remain non-executing.
- Wave summary and next-wave proposal.

## 5. Scope Still Forbidden

- Auto-merge or release.
- Production operation.
- Secret or real credential changes.
- Production model config changes.
- Destructive git/database commands.
- Migration apply without explicit human gate.
- Human gate closure.
- Security/legal/release gate closure.
- Hermes product-code write access.
- `shared-specs` as runtime/build/test/CI/source dependency.
- Skill execution, pack install, or resilience experiment execution without a future human-owned approval path.

## 6. Current Gate State

Product Wave 4 execution is approved for non-DB-replay tasks under the declared task graph and boundaries.

`PW4-WP4-LIVE-DB-REPLAY-EXECUTION-GATE-001` must not execute until the Owner separately approves `migration_runtime_replay` and provides disposable replay targets.
