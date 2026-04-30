# STAGEB-PRODUCT-TASKGRAPH-001 Validation

## Commands

```bash
test -f infrastructure/product-task-graph-v1.yaml
test -f infrastructure/product-wave1-task-pack.md
test -f infrastructure/templates/product-task-execution-steps.md
ruby -ryaml -e 'data=YAML.load_file("infrastructure/product-task-graph-v1.yaml"); abort "too few tasks" unless data["tasks"].size >= 20; puts data["tasks"].size'
python3 infrastructure/runner-v2.py doctor --strict-artifacts
git diff --check
```

## Result

All commands passed.

The graph currently contains `28` tasks.

`runner-v2.py doctor --strict-artifacts` returned:

```text
task-queue-v2.yaml: ok
agent-pool-v2.yaml: ok
quality-gates-v2.yaml: ok
doctor: ok
```

Targeted `git diff --check` for shared-specs and synchronized `osmx` docs returned no whitespace errors.
