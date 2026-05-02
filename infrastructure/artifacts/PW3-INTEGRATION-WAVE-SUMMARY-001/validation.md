# PW3 Integration Validation

Validation performed:

- `git diff --check`
- `python3 infrastructure/runner-v2.py doctor --strict-artifacts`

Wave-level validation inherited from task artifacts:

- `cd frontend && npm run build:check`
- `cd osmx-go && /Users/shitao/.local/go-tools/go1.25.0/bin/go test ./...`
- `cd frontend && E2E_FRONTEND_BASE_URL=http://127.0.0.1:15190 npx playwright test e2e/15-aof-runtime-breadth.spec.ts --config /tmp/osmx-aof-playwright-chrome-for-testing.config.mjs`
- `python3 scripts/migration_pair_check.py --root .`
- `./scripts/db-portability-scan.sh`

Result:

- pass

Notes:

- No merge, release, production change, migration apply, or human gate closure was performed.
