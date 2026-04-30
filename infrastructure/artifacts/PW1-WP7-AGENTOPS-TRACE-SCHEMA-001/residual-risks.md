# PW1-WP7-AGENTOPS-TRACE-SCHEMA-001 Residual Risks

- The AgentOpsTrace contract is side-effect free and does not persist records.
- No DB-backed ledger, replay index, cost aggregation, or retention policy exists yet.
- Evidence references are structurally validated but not authenticated.
- Full `osmx-ai` pytest passes but still emits existing async mock warnings in diagnosis and inspection tests.
