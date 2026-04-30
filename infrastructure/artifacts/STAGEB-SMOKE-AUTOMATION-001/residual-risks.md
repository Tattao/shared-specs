# STAGEB-SMOKE-AUTOMATION-001 Residual Risks

- The scaffold validates docs/ops readiness facts only; it intentionally does not exercise product runtime, frontend, backend, AI services, databases, or external integrations.
- Stage A remains `pass_with_risk`, not full autonomous-delivery approval.
- Product-code wave remains blocked until Owner explicitly approves the product-scope gate.
- Hermes WeChat remains a read-only supervision channel and must not lease, complete, close gates, modify product code, push, merge, or release.
- If `../osmx/docs` is absent in a future workspace, the script records that reference check as `skip`; in this workspace those references passed.
