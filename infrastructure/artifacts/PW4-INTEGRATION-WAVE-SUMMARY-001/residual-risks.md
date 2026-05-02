# PW4 Integration Residual Risks

- `migration_runtime_replay` remains open.
- Durable approval workflow persistence is not implemented.
- Request ledger is in-process and not release-grade audit storage.
- AOF runtime source still reports `sample` until durable adapters replace sample-backed readers.
- Full browser E2E should be rerun against fresh services before release readiness claims.
