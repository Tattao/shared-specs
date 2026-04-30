# STAGEB-PRODUCT-WAVE2-TASKGRAPH-001 Validation

## Commands

- `ruby -e 'require "yaml"; data = YAML.load_file("infrastructure/product-wave2-task-graph-v1.yaml"); raise "bad id" unless data["graph"]["id"] == "aof-product-wave2-runtime-binding-v1"; raise "bad status" unless data["graph"]["status"] == "owner_gate_required"; raise "no tasks" unless data["tasks"].length > 0; puts "wave2 yaml: ok"'`
- `git diff --check -- infrastructure/product-wave2-task-graph-v1.yaml infrastructure/product-wave2-task-pack.md infrastructure/product-wave2-owner-gate.md infrastructure/artifacts/STAGEB-PRODUCT-WAVE2-TASKGRAPH-001`
- `cd ../osmx && git diff --check -- docs/plans/80-wave-execution-board.md docs/guides/document-change-log.md`
- `python3 infrastructure/runner-v2.py doctor --strict-artifacts`

## Result

All validation commands passed.
