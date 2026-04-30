# Validation

Commands:

```bash
python3 -m py_compile infrastructure/worktree-preflight-v2.py
python3 infrastructure/runner-v2.py validate
python3 infrastructure/runner-v2.py next --include-human-gate
python3 infrastructure/runner-v2.py lease STAGEB-WORKTREE-PREFLIGHT-001 --owner Codex --status running
python3 infrastructure/worktree-preflight-v2.py --task-id STAGEB-WORKTREE-PREFLIGHT-001 --allow-dirty --allow-branch-mismatch
python3 infrastructure/gate-runner-v2.py --task-id STAGEB-WORKTREE-PREFLIGHT-001 --groups post_task
python3 infrastructure/runner-v2.py doctor --strict-artifacts
git diff --check
```

Expected result:

- Preflight compiles.
- v2 YAML files parse.
- Task leases successfully.
- Preflight writes `preflight.md` and `preflight.json`.
- Gate runner writes `gate-results.md` and `gate-results.json`.
- Runner doctor and diff check pass.

Actual result:

- `python3 -m py_compile infrastructure/worktree-preflight-v2.py` passed.
- `python3 infrastructure/runner-v2.py validate` passed.
- `python3 infrastructure/runner-v2.py next --include-human-gate` selected `STAGEB-WORKTREE-PREFLIGHT-001`.
- `python3 infrastructure/runner-v2.py lease STAGEB-WORKTREE-PREFLIGHT-001 --owner Codex --status running` leased the task.
- `python3 infrastructure/worktree-preflight-v2.py --task-id STAGEB-WORKTREE-PREFLIGHT-001 --allow-dirty --allow-branch-mismatch` wrote `preflight.md` and `preflight.json` with verdict `pass_with_exception`.
- The preflight exception was expected because this is an already-running delivery-ops task on `main`; strict product-code dispatch must not use these exception flags.
- Preflight confirmed all dirty files stayed inside the declared write scope and no forbidden product-code scope changed.
- `python3 infrastructure/gate-runner-v2.py --task-id STAGEB-WORKTREE-PREFLIGHT-001 --groups post_task` wrote `gate-results.md` and `gate-results.json` with verdict `pass`.
- `python3 infrastructure/gate-runner-v2.py --task-id STAGEB-WORKTREE-PREFLIGHT-001 --groups build_when_applicable` wrote `gate-results-build-skip.md` and `gate-results-build-skip.json`; product-code build gates were skipped because this task does not write product-code paths.
- `python3 infrastructure/runner-v2.py complete STAGEB-WORKTREE-PREFLIGHT-001 --owner Codex --verdict pass_with_risk --strict-artifacts` closed the task.
- Final `python3 infrastructure/runner-v2.py doctor --strict-artifacts` passed.
- Final `python3 infrastructure/runner-v2.py stale` reported `no stale leased tasks`.
- Final `python3 infrastructure/runner-v2.py status` reported `closed:14`.
- Final `git diff --check` passed.
