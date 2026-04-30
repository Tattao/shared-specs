# PW1-WP3-TIMELINE-PROJECTION-001 Validation

## Commands

```bash
/Users/shitao/.local/go-tools/go1.25.0/bin/gofmt -w internal/aof/timeline/projection.go internal/aof/timeline/projection_test.go internal/api/v1/aof_handler.go internal/api/v1/aof_handler_test.go internal/router/router.go
/Users/shitao/.local/go-tools/go1.25.0/bin/go test ./internal/aof/timeline ./internal/api/v1 ./internal/router
/Users/shitao/.local/go-tools/go1.25.0/bin/go test ./...
git -C ../osmx diff --check -- osmx-go/internal/aof/timeline/projection.go osmx-go/internal/aof/timeline/projection_test.go osmx-go/internal/api/v1/aof_handler.go osmx-go/internal/api/v1/aof_handler_test.go osmx-go/internal/router/router.go docs/reference/aof-timeline-projection-contract-v0.md
git diff --check -- infrastructure/artifacts/PW1-WP3-TIMELINE-PROJECTION-001
```

## Result

All commands passed.
