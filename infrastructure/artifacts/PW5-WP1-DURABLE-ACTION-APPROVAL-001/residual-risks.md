# PW5-WP1 Residual Risks

- Approval-to-executor binding remains intentionally unimplemented and must require a separate explicit human gate.
- Live DB replay remains blocked until `migration_runtime_replay` approval and disposable PostgreSQL/MySQL DSNs are supplied.
- The approval payload stores the AOF request envelope as JSON; future reporting may need dedicated query/index design if high-volume filtering becomes necessary.
