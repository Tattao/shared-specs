# PW3-WP2 Residual Risks

- The new store package is not yet wired into AOF HTTP handlers; binding follows in `PW3-WP3-DETAIL-API-UI-BINDING-001`.
- The in-memory reader is a dev/test boundary, not a live DB adapter.
- Real PostgreSQL/MySQL replay remains blocked behind `PW3-WP5-LIVE-DB-RUNTIME-REPLAY-GATE-001`.
- Existing local `osmx` test output modifications remain outside this task:
  - `osmx-ai/tests/reports/parser_regression.json`
  - `osmx-ai/tests/stress_report.json`
