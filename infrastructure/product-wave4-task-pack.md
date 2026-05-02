# AOF Product Wave 4 Task Pack

> Status: `owner_gate_required`
> Date: `2026-04-30`
> Source graph: `infrastructure/product-wave4-task-graph-v1.yaml`

## 1. Purpose

Product Wave 4 converts the Wave 3 store/governance contracts into guarded integration slices.

This package is preparation only. It does not approve Product Wave 4 product-code execution.

## 2. Scope

Allowed after explicit Product Wave 4 execution approval:

- store-adapter-backed AOF read paths;
- additive runtime provenance fields and evidence;
- CI-ready authenticated browser smoke harness;
- disposable PostgreSQL/MySQL replay only behind `migration_runtime_replay`;
- non-executing governed action request API, audit, and UI gate flows;
- focused Go/frontend validations and shared-specs task artifacts.

Forbidden:

- auto-merge or release;
- production operation;
- destructive git or database commands;
- migration apply without explicit human gate;
- human gate closure;
- security/legal/release gate closure;
- real credential or production model config changes;
- Hermes product-code write access;
- `shared-specs` as runtime/build/test/CI/source dependency;
- skill execution, pack install, or resilience experiment execution without a future human-owned approval path.

## 3. Recommended Execution Order

```text
PW4-WP0-EXECUTION-PREFLIGHT-001
PW4-WP1-STORE-ADAPTER-READ-PATH-001
PW4-WP2-RUNTIME-PROVENANCE-PERSISTENCE-001
PW4-WP3-BROWSER-E2E-CI-HARNESS-001
PW4-WP4-LIVE-DB-REPLAY-EXECUTION-GATE-001
PW4-WP5-ACTION-REQUEST-API-AUDIT-001
PW4-WP6-GOVERNED-ACTION-UI-GATE-001
PW4-INTEGRATION-WAVE-SUMMARY-001
```

`PW4-WP5` may run after `PW4-WP2`; `PW4-WP6` depends on `PW4-WP5`. `PW4-WP4` must not run unless the Owner separately approves `migration_runtime_replay` and supplies disposable replay targets.

## 4. Stop Conditions

Stop immediately if a task requires:

- Product Wave 4 execution before the Owner explicitly approves it;
- live DB replay without `migration_runtime_replay` approval and disposable DSNs;
- production environment access or real credential changes;
- write scope not represented in `product-wave4-task-graph-v1.yaml`;
- product-scope expansion beyond store-backed read path, provenance, browser evidence, DB replay gate, or governed action request gates;
- skill execution, pack install, experiment execution, or human gate closure;
- repeated validation failure;
- unclear ownership or conflict with user changes.

## 5. Owner Gate Required

This pack prepares the continuous execution queue only.

The next decision package is `infrastructure/product-wave4-owner-gate.md`.
