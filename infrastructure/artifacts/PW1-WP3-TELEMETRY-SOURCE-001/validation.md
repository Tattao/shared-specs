# PW1-WP3-TELEMETRY-SOURCE-001 Validation

## Commands

```bash
/Users/shitao/.local/go-tools/go1.25.0/bin/gofmt -w internal/aof/telemetry/source_registry.go internal/aof/telemetry/source_registry_test.go internal/api/v1/aof_handler.go internal/api/v1/aof_handler_test.go internal/router/router.go
/Users/shitao/.local/go-tools/go1.25.0/bin/go test ./internal/aof/telemetry ./internal/api/v1 ./internal/router
/Users/shitao/.local/go-tools/go1.25.0/bin/go test ./...
python3 scripts/migration_pair_check.py --root .
git -C ../osmx diff --check -- osmx-go/internal/aof/telemetry/source_registry.go osmx-go/internal/aof/telemetry/source_registry_test.go osmx-go/internal/api/v1/aof_handler.go osmx-go/internal/api/v1/aof_handler_test.go osmx-go/internal/router/router.go docs/reference/aof-telemetry-source-registry-v0.md
git diff --check -- infrastructure/artifacts/PW1-WP3-TELEMETRY-SOURCE-001
```

## Result

All commands passed.
