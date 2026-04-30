# PW1-WP3-TELEMETRY-SOURCE-001 Residual Risks

- Registry metadata is code-backed and read-only; TelemetrySource instances are not persisted.
- Credential binding, source health tracking, ingestion runtime, and idempotency storage remain future tasks.
- Security-sensitive source registration still requires a later security gate before real credentials are accepted.
- Product Wave 1 remains forbidden from auto-merge, release, production operations, destructive commands, human gate closure, and scope expansion.
