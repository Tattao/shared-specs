# Validation

Commands:

```bash
python3 infrastructure/runner-v2.py status
find infrastructure/artifacts -maxdepth 2 -type f | sort
python3 - <<'PY'
from pathlib import Path
root = Path("infrastructure/artifacts")
for d in sorted(root.glob("AOF-*")):
    if not d.is_dir():
        continue
    required = ["changed-files.txt", "validation.md", "residual-risks.md", "handoff.md"]
    missing = [f for f in required if not (d / f).exists()]
    summary = "summary.md" if (d / "summary.md").exists() else ("gate-summary.md" if (d / "gate-summary.md").exists() else "missing-summary")
    print(f"{d.name}: summary={summary} missing={','.join(missing) or 'none'}")
PY
python3 infrastructure/runner-v2.py stale
git -C /Users/shitao/Projects/Codex/osmx status --short
git diff --check
test -f stage-a-owner-decision-package.md
test -f infrastructure/artifacts/AOF-STAGEA-DRYRUN-001/evaluation.md
python3 infrastructure/runner-v2.py doctor --strict-artifacts
```

Expected result:

- Queue shows Stage A tasks closed except the current dry-run while it is running.
- Closed task artifact directories include required evidence files.
- OSMX product-code directories remain untouched by this task.
- New decision package and evaluation artifact exist.
- Final `doctor --strict-artifacts` passes after the dry-run task is completed.

Actual result:

- Queue showed `closed:10, ready:1` before leasing the dry-run task.
- Required artifact check passed for all previously closed task directories.
- `osmx` had existing broad strategy-document changes, but no product-code changes were made by this task.
- `git diff --check` passed after artifact creation.
- `test -f stage-a-owner-decision-package.md` passed.
- `test -f infrastructure/artifacts/AOF-STAGEA-DRYRUN-001/evaluation.md` passed.
- `python3 infrastructure/runner-v2.py complete AOF-STAGEA-DRYRUN-001 --owner Codex --verdict pass_with_risk` closed the task.
- Final `python3 infrastructure/runner-v2.py doctor --strict-artifacts` passed.
- Final `python3 infrastructure/runner-v2.py status` reports `closed:11`.
- Final `python3 infrastructure/runner-v2.py stale` reports `no stale leased tasks`.

Known validation caveat:

- `python3 infrastructure/runner-v2.py stale` reported the active dry-run lease as stale while the lease was still valid. Investigation showed Ruby YAML timestamp serialization changed `2026-04-30T13:31:31+08:00` into `2026-04-30 13:31:31 +0800`, which `datetime.fromisoformat` does not parse. This is documented as a Stage B repair task.
