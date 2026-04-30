# Validation

Commands:

```bash
python3 -m py_compile infrastructure/runner-v2.py
python3 infrastructure/runner-v2.py validate
python3 - <<'PY'
import importlib.util
from datetime import datetime
spec = importlib.util.spec_from_file_location("runner_v2", "infrastructure/runner-v2.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
values = [
    "2026-04-30T13:31:31+08:00",
    "2026-04-30 13:31:31 +0800",
    "2026-04-30 13:31:31.123456 +0800",
    datetime.fromisoformat("2026-04-30T13:31:31+08:00"),
]
for value in values:
    parsed = mod.parse_iso(value)
    print(repr(value), "->", parsed.isoformat() if parsed else None)
PY
python3 infrastructure/runner-v2.py next --include-human-gate
python3 infrastructure/runner-v2.py lease STAGEB-RUNNER-TIME-001 --owner Codex --status running
python3 infrastructure/runner-v2.py stale
python3 infrastructure/runner-v2.py doctor --strict-artifacts
python3 infrastructure/runner-v2.py status
git diff --check
```

Actual result:

- `python3 -m py_compile infrastructure/runner-v2.py` passed.
- `python3 infrastructure/runner-v2.py validate` passed.
- `parse_iso` returned valid timezone-aware datetimes for ISO strings, Ruby YAML strings, fractional-second Ruby YAML strings, and native `datetime` values.
- `python3 infrastructure/runner-v2.py next --include-human-gate` selected `STAGEB-RUNNER-TIME-001`.
- The task was leased to `Codex` and moved to `running`.
- The queue loaded `lease_expires_at` as `'2026-04-30 13:42:52 +0800'`.
- `parse_iso` normalized that value to `2026-04-30T13:42:52+08:00`.
- `stale_tasks` returned an empty list while the lease was still valid.
- `python3 infrastructure/runner-v2.py stale` reported `no stale leased tasks`.
- `python3 infrastructure/runner-v2.py doctor --strict-artifacts` passed while the task was running.

Final validation after completion:

- `python3 infrastructure/runner-v2.py complete STAGEB-RUNNER-TIME-001 --owner Codex --verdict pass` closed the task.
- Final `python3 infrastructure/runner-v2.py doctor --strict-artifacts` passed.
- Final `python3 infrastructure/runner-v2.py stale` reported `no stale leased tasks`.
- Final `python3 infrastructure/runner-v2.py status` reported `closed:12`.
- Final `git diff --check` passed.
