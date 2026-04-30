# Validation

Commands:

```bash
git diff --check
ruby -e 'require "yaml"; YAML.load_file("infrastructure/task-queue-v2.yaml"); puts "task-queue-v2.yaml: ok"'
rg -n "WP13|WP12|WP11|WP0" infrastructure/task-queue-v2.yaml infrastructure/artifacts/AOF-STAGEA-TASKMAP-001/wp-task-map.md
```

Expected result:

- Diff whitespace check passes.
- Queue YAML parses.
- WP0, WP11, WP12, and WP13 are represented in either the queue or the task map.
