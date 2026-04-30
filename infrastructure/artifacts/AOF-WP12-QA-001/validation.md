# Validation

Commands:

```bash
cd /Users/shitao/Projects/Codex/osmx
git diff --check
rg -n "Database Pack|Kubernetes Pack|Business Continuity|smoke|evidence" docs/reports/aof-wp12-smoke-inventory-20260430.md docs/test-cases/aof-complete-product-stage-a-smoke-plan.md docs/plans/93-autonomic-operations-fabric-40-day-mvp-task-pack.md

cd /Users/shitao/Projects/Codex/shared-specs
git diff --check
ruby -e 'require "yaml"; YAML.load_file("infrastructure/task-queue-v2.yaml"); puts "task-queue-v2.yaml: ok"'
```

Expected result:

- OSMX and shared-specs diffs pass whitespace checks.
- Smoke keywords are present in report, test-case plan, and source plan.
- `task-queue-v2.yaml` parses after status update.
