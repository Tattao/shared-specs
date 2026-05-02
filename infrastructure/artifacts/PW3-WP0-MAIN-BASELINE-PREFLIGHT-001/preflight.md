# PW3-WP0 Preflight

## Source

Wave 3 execution source:

- `shared-specs/infrastructure/product-wave3-task-graph-v1.yaml`

Owner gate:

- Owner confirmed both Product Wave 1/2 PRs can be merged.
- Owner approved Product Wave 3 continuing from the current PR branch.

## Git Baseline

`osmx`:

- Branch: `codex/product-wave3-store-runtime`
- HEAD: `1d57f65`
- origin/main: `1d57f65`
- Dirty files present before Wave 3 product edits:
  - `osmx-ai/tests/reports/parser_regression.json`
  - `osmx-ai/tests/stress_report.json`

`shared-specs`:

- Branch: `codex/product-wave3-store-runtime`
- HEAD: `5ba2a31`
- origin/main: `5ba2a31`
- Dirty files: only this PW3-WP0 artifact set after preflight writing.

## Local Services

Backend was restarted from latest `osmx` main baseline:

```text
OSMX_SERVER_PORT=18090 OSMX_SERVER_MODE=release OSMX_ADMIN_PASSWORD=admin123 /Users/shitao/.local/go-tools/go1.25.0/bin/go run ./cmd/server -config configs/config.pg-smoke.yaml
```

Frontend was restarted from latest `osmx` main baseline:

```text
npm exec vite -- --host 127.0.0.1 --port 15190 --config /tmp/osmx-vite-18090.mjs
```

Runtime notes:

- Backend connected to the configured PostgreSQL smoke database.
- Backend ran in `release` mode, so no AutoMigrate path was invoked.
- Redis at `127.0.0.1:6379` was unavailable; server continued without cache.

## Smoke Results

```json
{"loginCode":0,"tokenLength":279}
{"endpoint":"/api/v1/health","status":"ok","runtime":13}
{"endpoint":"/api/v1/aof/twin/nodes","status":200,"code":0,"count":3}
{"endpoint":"/api/v1/aof/alerts/records","status":200,"code":0,"count":1}
{"endpoint":"/api/v1/aof/workcenter/records","status":200,"code":0,"count":1}
{"endpoint":"/api/v1/aof/autopilot/records","status":200,"code":0,"count":3}
{"endpoint":"/api/v1/aof/agentops/traces","status":200,"code":0,"count":1}
{"endpoint":"/api/v1/aof/skills/records","status":200,"code":0,"count":1}
{"endpoint":"/api/v1/aof/resilience/records","status":200,"code":0,"count":1}
{"endpoint":"/api/v1/aof/packs/records","status":200,"code":0,"count":1}
```

Frontend root returned Vite HTML from `http://127.0.0.1:15190/`.

## Stop Conditions

Codex must stop before:

- product-scope expansion outside `product-wave3-task-graph-v1.yaml`
- migration apply or live DB mutation without human approval
- security, legal, release, or human gate closure
- production environment changes
- destructive commands
- pack install, skill execution, or experiment execution
- repeated validation failure or unclear ownership
