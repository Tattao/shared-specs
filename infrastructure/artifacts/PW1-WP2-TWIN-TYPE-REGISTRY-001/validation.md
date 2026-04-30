# PW1-WP2-TWIN-TYPE-REGISTRY-001 Validation

## Commands

```bash
/Users/shitao/.local/go-tools/go1.25.0/bin/gofmt -w internal/aof/twin/type_registry.go internal/aof/twin/type_registry_test.go internal/api/v1/aof_handler.go internal/api/v1/aof_handler_test.go internal/router/router.go
/Users/shitao/.local/go-tools/go1.25.0/bin/go test ./internal/aof/twin ./internal/api/v1 ./internal/router
/Users/shitao/.local/go-tools/go1.25.0/bin/go test ./...
python3 scripts/migration_pair_check.py --root .
git -C ../osmx diff --check -- osmx-go/internal/aof/twin/type_registry.go osmx-go/internal/aof/twin/type_registry_test.go osmx-go/internal/api/v1/aof_handler.go osmx-go/internal/api/v1/aof_handler_test.go osmx-go/internal/router/router.go docs/reference/aof-operational-twin-type-registry-v0.md
git diff --check -- infrastructure/artifacts/PW1-WP2-TWIN-TYPE-REGISTRY-001
```

## Result

All commands passed.
