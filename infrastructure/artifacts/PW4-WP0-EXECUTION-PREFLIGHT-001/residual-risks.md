# PW4-WP0 Residual Risks

- The `osmx` worktree still has pre-existing local test output modifications in:
  - `osmx-ai/tests/reports/parser_regression.json`
  - `osmx-ai/tests/stress_report.json`
- Backend/frontend smoke used already-running local services; no service restart was performed during this preflight.
- `PW4-WP4-LIVE-DB-REPLAY-EXECUTION-GATE-001` remains blocked behind `migration_runtime_replay`.
- Store adapter read-path wiring, provenance persistence, CI-ready browser evidence, and governed action API/UI work remain unimplemented until follow-on Wave 4 tasks execute.
