# PW1-WP6-AUTOPILOT-EVIDENCE-CONTRACT-001 Residual Risks

- The contract validates evidence and risk structure only; it does not verify evidence authenticity or perform evidence retrieval.
- No durable Autopilot output ledger exists yet.
- No live LLM generation path is wired to this contract.
- Full `osmx-ai` pytest is green, but it still emits existing async mock warnings in diagnosis and inspection tests.
