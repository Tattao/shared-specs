# PW4-WP4 Residual Risks

- PostgreSQL/MySQL disposable runtime replay has not been executed.
- MySQL compatibility remains guardrail/evidence based, not full runtime replay passed.
- Any future replay must use disposable targets and must not mutate production.
- The human gate must remain open until Owner explicitly approves `migration_runtime_replay`.
