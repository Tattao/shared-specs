# PW5-WP4 Validation

Local validation in `osmx`:

- `cd frontend && npm run build:check`
- `cd frontend && npx playwright test --config=playwright.aof-runtime.config.ts --list`

Observed result: pass. The Playwright list command showed:

- `chromium-desktop`
- `chromium-mobile`

The authenticated browser run itself still requires a running backend/frontend environment with seeded admin credentials.
