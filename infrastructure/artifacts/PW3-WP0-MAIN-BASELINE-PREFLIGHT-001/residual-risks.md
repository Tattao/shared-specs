# PW3-WP0 Residual Risks

- The `osmx` worktree still has pre-existing local test output modifications in:
  - `osmx-ai/tests/reports/parser_regression.json`
  - `osmx-ai/tests/stress_report.json`
- Backend smoke used the local PostgreSQL smoke configuration and release mode; no live DB replay or migration apply was attempted.
- Redis was unavailable locally, so cache behavior was not covered by this smoke.
- Wave 3 store-backed runtime, browser E2E, and governed action gates remain unimplemented until downstream Wave 3 tasks execute.
