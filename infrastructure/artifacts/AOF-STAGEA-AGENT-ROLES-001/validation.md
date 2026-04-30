# Validation

Commands:

```bash
python3 infrastructure/runner-v2.py validate
python3 infrastructure/runner-v2.py doctor
python3 infrastructure/runner-v2.py doctor --strict-artifacts
python3 infrastructure/runner-v2.py stale
python3 infrastructure/runner-v2.py status
python3 -m py_compile infrastructure/runner-v2.py
git diff --check
```

Expected result:

- v2 YAML files parse.
- all task profiles and slot profiles resolve.
- closed tasks have required artifact files.
- no active lease is stale.
- no whitespace errors are present.

Actual result on 2026-04-30:

- `python3 infrastructure/runner-v2.py validate` passed for `task-queue-v2.yaml`, `agent-pool-v2.yaml`, and `quality-gates-v2.yaml`.
- `python3 infrastructure/runner-v2.py doctor` returned `doctor: ok`.
- `python3 infrastructure/runner-v2.py doctor --strict-artifacts` returned `doctor: ok`.
- `python3 infrastructure/runner-v2.py stale` returned `no stale leased tasks`.
- `python3 -m py_compile infrastructure/runner-v2.py` passed.
- `git diff --check` passed.
