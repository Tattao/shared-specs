# PW1-WP0-FEATURE-GATE-001 Residual Risks

- AOF surfaces are still skeleton pages; disabled behavior is visible but there are no deep product workflows to suppress yet.
- Existing feature toggle API is tenant scoped, but per-action write capabilities must be added by later implementation tasks.
- The frontend currently keeps disabled surfaces visible in read-only placeholder mode rather than hiding menu entries.
- Product Wave 1 remains forbidden from auto-merge, release, production operations, destructive commands, human gate closure, and scope expansion.
