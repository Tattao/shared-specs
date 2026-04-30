# PW1-WP0-SHELL-IA-001 Residual Risks

- New AOF surfaces are skeleton-only; product APIs, data loading, permission enforcement, and runtime tests still need follow-up tasks.
- Capability keys are declared in the frontend surface metadata but are not yet enforced by backend or frontend feature gates.
- Visual browser verification was not run in this step; validation covered type-check and production build.
- Product Wave 1 remains forbidden from auto-merge, release, production operations, destructive commands, human gate closure, and scope expansion.
