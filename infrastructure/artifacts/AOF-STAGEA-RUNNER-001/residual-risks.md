# Residual Risks

- `runner-v2.py` is a supervised queue runner, not a full process supervisor.
- It does not create worktrees, spawn Codex sessions, or run validation commands automatically.
- It uses narrow text updates for queue mutation to preserve readability; schema changes may require updating the runner.
- It relies on Ruby stdlib YAML parsing because Python PyYAML is not installed in this environment.
- Human gate approval remains a process step outside the runner.
