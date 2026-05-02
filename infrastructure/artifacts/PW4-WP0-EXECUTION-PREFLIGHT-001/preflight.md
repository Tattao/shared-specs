# PW4-WP0 Preflight

## Source

Wave 4 execution source:

- `shared-specs/infrastructure/product-wave4-task-graph-v1.yaml`
- `shared-specs/infrastructure/product-wave4-owner-gate.md`
- `shared-specs/infrastructure/product-wave4-task-pack.md`

Owner gate:

- Owner approved Wave 4 graph preparation and owner gate setup on `2026-04-30`.
- Owner approved the recommended Wave 4 execution plan with message `按建议执行` on `2026-04-30`.
- `PW4-WP4-LIVE-DB-REPLAY-EXECUTION-GATE-001` remains blocked until separate `migration_runtime_replay` approval and disposable DSNs are provided.

## Git Baseline

`osmx`:

- Branch: `codex/product-wave3-store-runtime`
- HEAD: `17063fe`
- Dirty files present before Wave 4 product-code edits:
  - `osmx-ai/tests/reports/parser_regression.json`
  - `osmx-ai/tests/stress_report.json`

`shared-specs`:

- Branch: `codex/product-wave3-store-runtime`
- HEAD: `1ae06a6`
- origin branch: `origin/codex/product-wave3-store-runtime=1ae06a6`
- Dirty files before this artifact closeout:
  - `infrastructure/product-wave4-owner-gate.md`
  - `infrastructure/product-wave4-task-graph-v1.yaml`
  - `infrastructure/product-wave4-task-pack.md`

## Local Services

Existing local services were available:

```text
Backend:  http://127.0.0.1:18090
Frontend: http://127.0.0.1:15190/
```

Service checks:

```text
GET http://127.0.0.1:18090/api/v1/health -> 200
HEAD http://127.0.0.1:15190/ -> 200
```

## Smoke Results

```json
{"loginCode":0,"tokenLength":279}
{"endpoint":"/api/v1/health","status":200,"code":0,"runtime":12,"health":"ok"}
{"endpoint":"/api/v1/aof/twin/nodes","status":200,"code":0,"count":3}
{"endpoint":"/api/v1/aof/alerts/records","status":200,"code":0,"count":1}
{"endpoint":"/api/v1/aof/workcenter/records","status":200,"code":0,"count":1}
{"endpoint":"/api/v1/aof/autopilot/records","status":200,"code":0,"count":3}
{"endpoint":"/api/v1/aof/agentops/traces","status":200,"code":0,"count":1}
{"endpoint":"/api/v1/aof/skills/records","status":200,"code":0,"count":1}
{"endpoint":"/api/v1/aof/resilience/records","status":200,"code":0,"count":1}
{"endpoint":"/api/v1/aof/packs/records","status":200,"code":0,"count":1}
```

## Stop Conditions

Codex must stop before:

- product-scope expansion outside `product-wave4-task-graph-v1.yaml`
- migration apply or live DB replay without separate human approval
- security, legal, release, or human gate closure
- production environment changes
- destructive commands
- pack install, skill execution, or experiment execution
- repeated validation failure or unclear ownership
