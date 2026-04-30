# Residual Risks

- v2 gate expectations such as `docs_or_no_matches_only` and `only_historical_warning_or_96` still require either manual interpretation or a future v2 gate runner.
- `dispatch.py` still targets v1 schema and should not be used to auto-run Stage A v2 tasks yet.
- Some old v1 docs retain historical `/Users/apple`, Hermes, Claude, and `--yolo` references; they are explicitly marked as legacy but not deleted.
- Product-code tasks in the v2 queue still need dedicated worktrees and owner review before execution.
