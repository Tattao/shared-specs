# Validation

Commands:

```bash
python3 -m py_compile infrastructure/gate-runner-v2.py
python3 infrastructure/runner-v2.py validate
python3 infrastructure/runner-v2.py next --include-human-gate
python3 infrastructure/runner-v2.py lease STAGEB-GATE-RUNNER-001 --owner Codex --status running
python3 infrastructure/gate-runner-v2.py --task-id STAGEB-GATE-RUNNER-001 --groups post_task
python3 infrastructure/gate-runner-v2.py --task-id STAGEB-GATE-RUNNER-001 --groups scope --output infrastructure/artifacts/STAGEB-GATE-RUNNER-001/gate-results-scope.md --json-output infrastructure/artifacts/STAGEB-GATE-RUNNER-001/gate-results-scope.json
python3 infrastructure/runner-v2.py doctor --strict-artifacts
git diff --check
```

Expected result:

- `gate-runner-v2.py` compiles.
- v2 YAML files parse.
- The task leases successfully.
- `post_task` gates produce `gate-results.md` and `gate-results.json`.
- `scope` gates can produce policy-aware evidence, including manual review where appropriate.
- Runner doctor and diff check pass after artifacts are present.

Actual result:

- `python3 -m py_compile infrastructure/gate-runner-v2.py` passed.
- `python3 infrastructure/runner-v2.py validate` passed.
- `python3 infrastructure/runner-v2.py next --include-human-gate` selected `STAGEB-GATE-RUNNER-001`.
- `python3 infrastructure/runner-v2.py lease STAGEB-GATE-RUNNER-001 --owner Codex --status running` leased the task.
- `post_task` gates wrote `gate-results.md` and `gate-results.json` with verdict `pass`.
- `scope` gates wrote `gate-results-scope.md` and `gate-results-scope.json` with verdict `pass_with_review`.
- `scope` manual-review output included existing OSMX `shared-specs` text references and one archived path reference in `96-codex-7x24-autonomous-delivery-operating-model.md`; these were not auto-failed because the gate expectation is explicitly policy-review oriented.
- `build_when_applicable` wrote `gate-results-build-skip.md` and `gate-results-build-skip.json`; Go, frontend, and AI build gates were correctly skipped because this task does not write product-code paths.
- `python3 infrastructure/runner-v2.py complete STAGEB-GATE-RUNNER-001 --owner Codex --verdict pass_with_risk --strict-artifacts` closed the task.
- Final `python3 infrastructure/runner-v2.py doctor --strict-artifacts` passed.
- Final `python3 infrastructure/runner-v2.py status` reported `closed:13`.
- Final `python3 infrastructure/runner-v2.py stale` reported `no stale leased tasks`.
- Final `git diff --check` passed.
