# AOF Product Wave 2 Task Pack

> Status: `owner_gate_required`
> Date: `2026-04-30`
> Source graph: `infrastructure/product-wave2-task-graph-v1.yaml`

## 1. Purpose

Product Wave 2 converts Product Wave 1 sample-only AOF surfaces into minimal runtime-bound product slices.

The goal is still guarded Alpha progress, not release readiness.

## 2. Scope

Allowed:

- runtime-backed read APIs for AOF surfaces;
- frontend binding from sample data to runtime API adapters;
- focused Go / Python / frontend tests;
- smoke evidence and DB guardrail reports;
- shared-specs task artifacts.

Forbidden:

- auto-merge or release;
- production operation;
- destructive git or database commands;
- migration apply without explicit human gate;
- security/legal/release gate closure;
- real credential or production model config changes;
- Hermes product-code write access;
- `shared-specs` as runtime/build/test/CI/source dependency.

## 3. Recommended Execution Order

```text
PW2-WP0-RUNTIME-BINDING-PREFLIGHT-001
PW2-WP2-TWIN-RUNTIME-API-001
PW2-WP2-TWIN-UI-BINDING-001
PW2-WP4-ALERTOPS-RUNTIME-API-001
PW2-WP4-ALERTOPS-UI-BINDING-001
PW2-WP5-WORKCENTER-RUNTIME-API-001
PW2-WP5-WORKCENTER-UI-BINDING-001
PW2-WP6-AUTOPILOT-RUNTIME-BINDING-001
PW2-WP6-AUTOPILOT-UI-BINDING-001
PW2-WP7-AGENTOPS-RUNTIME-API-001
PW2-WP7-AGENTOPS-UI-BINDING-001
PW2-WP8-SKILL-REGISTRY-RUNTIME-API-001
PW2-WP8-SKILL-REGISTRY-UI-BINDING-001
PW2-WP9-RESILIENCE-RUNTIME-API-001
PW2-WP9-RESILIENCE-UI-BINDING-001
PW2-WP10-PACK-REGISTRY-RUNTIME-API-001
PW2-WP10-PACK-UI-BINDING-001
PW2-WP12-RUNTIME-BREADTH-SMOKE-001
PW2-WP13-RUNTIME-BINDING-DB-GUARDRAIL-001
PW2-INTEGRATION-WAVE-SUMMARY-001
```

## 4. Stop Conditions

Stop immediately if a task requires:

- schema migration or migration apply;
- security, legal, release, or production gate decision;
- write scope not represented in `product-wave2-task-graph-v1.yaml`;
- product-scope expansion beyond runtime binding;
- repeated validation failure;
- unclear ownership or conflict with user changes.

## 5. Owner Gate Required

This pack prepares the continuous execution queue only. Product code execution requires Owner approval in `infrastructure/product-wave2-owner-gate.md`.
