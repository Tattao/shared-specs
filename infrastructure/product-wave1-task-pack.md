# AOF Product Wave 1 Task Pack

> Status: `owner_gate_required`
> Date: `2026-04-30`
> Source graph: `infrastructure/product-task-graph-v1.yaml`

## 1. Purpose

This task pack turns the complete-product Alpha plan into a continuous execution package.

It exists to remove repeated "what next?" pauses. Once the Owner approves the matching product-scope gate, Codex can pull ready tasks from the graph until a hard gate is hit.

## 2. Wave 1 Scope

Wave 1 is a product skeleton and core contract wave. It is allowed to create platform skeletons, contracts, gated routes, UI shells, evidence scaffolds, and tests.

It is not allowed to:

- merge or release without Owner approval,
- touch production environments,
- run destructive git or database commands,
- bypass migration pair checks,
- grant Hermes product-code write access,
- turn `shared-specs` into runtime/build/test/CI/source dependency.

## 3. Task Groups

| Group | Task ids | Goal |
|-------|----------|------|
| Product shell | `PW1-WP0-*` | 10 product surfaces appear behind gates |
| Core contracts | `PW1-WP1-*` | object/event/API/audit/permission contracts freeze |
| Twin and telemetry | `PW1-WP2-*`, `PW1-WP3-*` | CI types, telemetry source, timeline skeleton |
| Alert and workcenter | `PW1-WP4-*`, `PW1-WP5-*` | alert schema, ticket/change shell |
| AI governance | `PW1-WP6-*`, `PW1-WP7-*` | evidence-backed Autopilot and AgentOps trace |
| Execution and resilience | `PW1-WP8-*`, `PW1-WP9-*` | skill/execution safety and experiment guardrail |
| Scenario pack | `PW1-WP10-*` | pack manifest and console skeleton |
| Governance and QA | `PW1-WP11-*`, `PW1-WP12-*`, `PW1-WP13-*` | legal/source pin, smoke/audit evidence, DB guardrails |
| Integration | `PW1-INTEGRATION-WAVE-SUMMARY-001` | wave closeout and Wave 2 selection |

## 4. Continuous Execution Rule

After Owner approval:

1. Run strict worktree preflight before the first product-code task.
2. Pick the highest-priority ready task whose dependencies are satisfied.
3. Execute only within the declared write scope.
4. Write required artifacts.
5. Run task validation and applicable gate runner checks.
6. If validation passes, move to the next ready task.
7. Stop only for product-scope, migration, security, legal, release, destructive command, production operation, repeated validation failure, or unclear write-scope gates.

## 5. First Recommended Order

```text
PW1-WP1-CORE-CONTRACT-DOC-001
PW1-WP0-SHELL-IA-001
PW1-WP1-API-STUB-001
PW1-WP0-FEATURE-GATE-001
PW1-WP2-TWIN-TYPE-REGISTRY-001
PW1-WP3-TELEMETRY-SOURCE-001
PW1-WP4-ALERT-SCHEMA-001
PW1-WP7-AGENTOPS-TRACE-SCHEMA-001
PW1-WP12-SMOKE-EVIDENCE-UPGRADE-001
PW1-WP13-DB-GUARDRAIL-001
```

Frontend shell tasks can run after the matching backend/contract task is ready. Evaluation tasks should not be handled by the same implementation owner.

## 6. Owner Gate Required

This pack does not approve product-code work by itself.

The next decision package is `infrastructure/product-wave1-owner-gate.md`.
