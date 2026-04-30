# PW1-WP1-API-STUB-001 Validation

## Commands

```bash
/Users/shitao/.local/go-tools/go1.25.0/bin/gofmt -w internal/api/v1/aof_handler.go internal/api/v1/aof_handler_test.go internal/router/router.go internal/app/app.go internal/seed/feature_seed.go
/Users/shitao/.local/go-tools/go1.25.0/bin/go test ./internal/api/v1 ./internal/router
/Users/shitao/.local/go-tools/go1.25.0/bin/go test ./...
python3 scripts/migration_pair_check.py --root .
git -C ../osmx diff --check -- osmx-go/internal/api/v1/aof_handler.go osmx-go/internal/api/v1/aof_handler_test.go osmx-go/internal/router/router.go osmx-go/internal/app/app.go osmx-go/internal/seed/feature_seed.go
git diff --check -- infrastructure/artifacts/PW1-WP1-API-STUB-001
```

## Result

All commands passed.

The frontend build was also rerun after aligning product surface capability keys to `aof.surface.*.view`; it passed with the repository's existing Vite chunk warnings.
