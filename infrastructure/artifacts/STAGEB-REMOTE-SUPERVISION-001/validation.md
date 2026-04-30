# Validation

Commands:

```bash
test -f infrastructure/artifacts/OWNER-WECHAT-SUPERVISOR-20260430/summary.md
rg -n "Do not lease tasks|Do not complete tasks|Do not close human gates|Do not modify osmx product code" infrastructure/artifacts/OWNER-WECHAT-SUPERVISOR-20260430/summary.md
python3 infrastructure/gate-runner-v2.py --task-id STAGEB-REMOTE-SUPERVISION-001 --groups post_task
python3 infrastructure/runner-v2.py doctor --strict-artifacts
python3 infrastructure/runner-v2.py stale
git diff --check
```

Expected result:

- Hermes supervision summary exists.
- Forbidden-action boundaries are explicitly recorded.
- Post-task gates pass.
- Runner doctor passes.
- No stale leases remain.

Actual result:

- `test -f infrastructure/artifacts/OWNER-WECHAT-SUPERVISOR-20260430/summary.md` passed.
- `rg` confirmed the Hermes artifact records: `Do not lease tasks`, `Do not complete tasks`, `Do not close human gates`, and `Do not modify osmx product code`.
- `python3 infrastructure/gate-runner-v2.py --task-id STAGEB-REMOTE-SUPERVISION-001 --groups post_task` wrote `gate-results.md` and `gate-results.json` with verdict `pass`.
- `python3 infrastructure/runner-v2.py doctor --strict-artifacts` passed while the task was running.
- `python3 infrastructure/runner-v2.py stale` reported `no stale leased tasks`.
- `git diff --check` passed.
- `python3 infrastructure/runner-v2.py complete STAGEB-REMOTE-SUPERVISION-001 --owner Codex --verdict pass --strict-artifacts` closed the task.
- Final `python3 infrastructure/runner-v2.py doctor --strict-artifacts` passed.
- Final `python3 infrastructure/runner-v2.py stale` reported `no stale leased tasks`.
- Final `python3 infrastructure/runner-v2.py status` reported `closed:15`.
- Final `git diff --check` passed.
