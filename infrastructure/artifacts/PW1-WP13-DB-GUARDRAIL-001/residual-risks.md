# PW1-WP13-DB-GUARDRAIL-001 Residual Risks

- The portability scan is an inventory guardrail; it does not prove semantic equivalence for every SQL path.
- MySQL-specific patterns remain intentionally present in MySQL migration files, test fixtures, and dialect-aware helper branches.
- `AutoMigrate` remains visible in dev/bootstrap/test paths and must not be treated as the production schema fact source.
- No live PostgreSQL migration replay was run by this task because that would cross the declared migration/runtime gate.
