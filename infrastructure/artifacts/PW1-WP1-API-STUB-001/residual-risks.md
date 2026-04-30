# PW1-WP1-API-STUB-001 Residual Risks

- API stubs return static contract metadata; they do not yet persist AOF objects, events, audit projections, or timeline projections.
- The `aof_core_contract` gate protects the contract endpoints, but per-surface capability enforcement remains in `PW1-WP0-FEATURE-GATE-001`.
- The validation endpoint checks required payload fields only; semantic validation and idempotency persistence are future tasks.
- Product Wave 1 remains forbidden from auto-merge, release, production operations, destructive commands, human gate closure, and scope expansion.
