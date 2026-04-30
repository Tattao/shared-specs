# STAGEB-SMOKE-AUTOMATION-001 Validation

## Commands

Executed from `/Users/shitao/Projects/Codex/shared-specs`.

### Smoke Scaffold

```bash
python3 infrastructure/stageb-smoke-automation-v2.py --task-id STAGEB-SMOKE-AUTOMATION-001
```

Exit code: `0`

```text
task: STAGEB-SMOKE-AUTOMATION-001
verdict: pass
wrote: infrastructure/artifacts/STAGEB-SMOKE-AUTOMATION-001/smoke-results.json
wrote: infrastructure/artifacts/STAGEB-SMOKE-AUTOMATION-001/smoke-results.md
```

### Runner Doctor

```bash
python3 infrastructure/runner-v2.py doctor --strict-artifacts
```

Exit code: `0`

```text
task-queue-v2.yaml: ok
agent-pool-v2.yaml: ok
quality-gates-v2.yaml: ok
doctor: ok
```

### Diff Whitespace Check

```bash
git diff --check
```

Exit code: `0`

```text
<no output>
```

### OSMX Planning Sync Check

```bash
rg -n "STAGEB-SMOKE-AUTOMATION-001|product-code wave|Owner" ../osmx/docs/plans/00-current-plan-index.md ../osmx/docs/plans/80-wave-execution-board.md ../osmx/docs/plans/96-codex-7x24-autonomous-delivery-operating-model.md ../osmx/docs/guides/document-change-log.md
git -C ../osmx diff --check -- docs/plans/00-current-plan-index.md docs/plans/80-wave-execution-board.md docs/plans/96-codex-7x24-autonomous-delivery-operating-model.md docs/guides/document-change-log.md
```

Result: exit code `0`; references were found and `git diff --check` returned no whitespace errors for the synchronized `osmx` docs.

## Smoke Check Coverage

- `infrastructure/task-queue-v2.yaml` exists.
- Formal `STAGEB-SMOKE-AUTOMATION-001` queue task entry count is exactly `1`.
- Queue status remains `stage_b_wave0_preparation`.
- Queue stage remains `stage_b_wave0_supervised`.
- Required upstreams `STAGEB-WORKTREE-PREFLIGHT-001`, `STAGEB-REMOTE-SUPERVISION-001`, and `STAGEB-BOARD-SYNC-001` are declared dependencies and are closed.
- Required task artifact files are present.
- Local `../osmx/docs` plan/board references to `STAGEB-SMOKE-AUTOMATION-001` are present when docs exist.
