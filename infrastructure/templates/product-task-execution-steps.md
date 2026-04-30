# Product Task Execution Steps Template

Use this template for each product-code task after Owner product-scope approval.

## 1. Load Context

- Read the task record in `infrastructure/product-task-graph-v1.yaml`.
- Read the matching `93 / 94 / 95 / 96` source docs.
- Confirm `write_scope`, `forbidden_scope`, dependencies, validation, and acceptance.
- Run worktree preflight in strict mode before modifying product code.

## 2. Implement

- Keep edits inside declared `write_scope`.
- Prefer existing OSMX patterns and extension points.
- Do not introduce reverse dependency from `osmx` to downstream repos or `shared-specs`.
- Do not add scenario-specific logic to core unless the task explicitly defines a reusable abstraction.

## 3. Validate

Run all task validation commands.

Also run applicable checks:

- `git diff --check`
- `cd osmx-go && go test ./...` when backend changes are touched
- `cd frontend && npm run build:check` when frontend changes are touched
- `cd osmx-ai && pytest` when AI changes are touched
- `python3 scripts/migration_pair_check.py --root .` for DB-sensitive changes
- `scripts/db-portability-scan.sh` for DB-sensitive changes when available

## 4. Record Evidence

Create an artifact directory under:

```text
shared-specs/infrastructure/artifacts/<task-id>/
```

Required files:

- `changed-files.txt`
- `validation.md`
- `residual-risks.md`
- `handoff.md`

Use concise, factual notes. Include commands and results.

## 5. Stop Conditions

Stop and request Owner decision when the task would:

- expand product scope beyond the task graph,
- introduce or alter production migration strategy,
- touch secrets, credentials, license, commercial authorization, or production systems,
- require merge, release, deployment, or destructive git/database operations,
- require Hermes or Claude Code to close a human gate,
- fail validation twice for architecture, security, migration, or product-scope reasons.
