# PW3 Integration Residual Risks

- AOF runtime surfaces remain primarily sample-backed until Wave 4 wires store adapters into read paths.
- WP5 produced a gate package only; actual disposable PostgreSQL/MySQL runtime replay is still blocked by `migration_runtime_replay`.
- Browser E2E is local authenticated evidence; CI harness, trace/HAR/screenshot persistence, and field-level assertions remain future work.
- Governed action request gates are contract-only until API, approval persistence, audit persistence, and UI request flows are added.
- Existing local `osmx` dirty baseline remains outside Wave 3:
  - `osmx-ai/tests/reports/parser_regression.json`
  - `osmx-ai/tests/stress_report.json`
