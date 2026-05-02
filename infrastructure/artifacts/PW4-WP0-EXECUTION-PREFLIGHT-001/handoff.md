# PW4-WP0 Handoff

Status: closed

Wave 4 can proceed to:

- `PW4-WP1-STORE-ADAPTER-READ-PATH-001`

Use these baselines:

- osmx: `17063fe` on `codex/product-wave3-store-runtime`
- shared-specs: `1ae06a6` on `codex/product-wave3-store-runtime`

Local services are available for follow-on Wave 4 work:

- Backend: `http://127.0.0.1:18090`
- Frontend: `http://127.0.0.1:15190/`

Preserve hard limits:

- no auto-merge or release
- no production changes
- no destructive commands
- no migration apply, live DB replay, or live DB mutation without human gate
- no human/security/legal/release gate closure
- no pack install, skill execution, or experiment execution
