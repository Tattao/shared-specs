# PW5-WP1 Validation

Local validation in `osmx`:

- `git diff --check`
- `cd osmx-go && /Users/shitao/.local/go-tools/go1.25.0/bin/go test ./internal/aof/governance ./internal/repository ./internal/api/v1`
- `cd osmx-go && /Users/shitao/.local/go-tools/go1.25.0/bin/go test ./internal/aof/... ./internal/repository ./internal/api/v1 ./internal/app`
- `cd frontend && npm run build:check`
- `python3 scripts/migration_pair_check.py --root .`
- `DB_PORTABILITY_SCAN_MAX_LINES=80 ./scripts/db-portability-scan.sh`

Observed result: pass. Vite reported existing chunk/dynamic import warnings only.

GitHub validation:

- OSMX PR is expected to run GitGuardian and security release gates before merge.
