# Validation

Commands:

```bash
python3 infrastructure/runner-v2.py validate
python3 infrastructure/runner-v2.py status
python3 infrastructure/runner-v2.py next
python3 infrastructure/runner-v2.py next --include-human-gate
python3 infrastructure/runner-v2.py activate
python3 infrastructure/runner-v2.py status
git diff --check
```

Expected result:

- v2 YAML files parse.
- queue status can be shown.
- auto-runnable next task list excludes human-gated tasks.
- human-gated task list shows `AOF-WP13-BOUNDARY-001`, `AOF-WP11-NEATLOGIC-001`, and `AOF-STAGEA-DRYRUN-001`.
- activation changes queue status to `active_stage_a`.
- diff whitespace check passes.

Actual result on 2026-04-30:

- `python3 infrastructure/runner-v2.py validate` passed for `task-queue-v2.yaml`, `agent-pool-v2.yaml`, and `quality-gates-v2.yaml`.
- `python3 infrastructure/runner-v2.py status` showed `status=active_stage_a`, `stage=stage_a_8h_unattended`, and `counts=closed:6, ready:3`.
- `python3 infrastructure/runner-v2.py next` returned `no auto-runnable ready tasks` because all remaining ready tasks require human gates.
- `python3 infrastructure/runner-v2.py next --include-human-gate` listed `AOF-STAGEA-DRYRUN-001`, `AOF-WP11-NEATLOGIC-001`, and `AOF-WP13-BOUNDARY-001`.
- `git diff --check` passed.
