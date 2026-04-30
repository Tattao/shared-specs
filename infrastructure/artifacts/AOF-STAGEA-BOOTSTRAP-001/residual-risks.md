# Residual Risks

- `dispatch.py`, `health-monitor.py`, and `handoff-generator.py` still consume the v1 schema. Stage A should use v2 in manual or supervised dry-run mode until those scripts are adapted.
- Existing v1 files still contain historical `/Users/apple` and Claude/Hermes references. They are retained as DW1 / DW2 history, not as the new default entrypoint.
- `task-queue-v2.yaml` includes candidate tasks that write to `osmx`; those must run in dedicated worktrees and require owner review before any PR or merge.
- The v2 gate expectations such as `docs_or_no_matches_only` are policy semantics, not executable assertions yet.
