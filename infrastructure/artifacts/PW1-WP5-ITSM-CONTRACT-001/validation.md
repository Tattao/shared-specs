# PW1-WP5-ITSM-CONTRACT-001 Validation

## Commands

- `cd ../osmx/osmx-go && /Users/shitao/.local/go-tools/go1.25.0/bin/gofmt -w internal/aof/workcenter/contract.go internal/aof/workcenter/contract_test.go internal/api/v1/aof_handler.go internal/api/v1/aof_handler_test.go internal/router/router.go`
- `cd ../osmx/osmx-go && /Users/shitao/.local/go-tools/go1.25.0/bin/go test ./internal/aof/workcenter ./internal/api/v1 ./internal/router`
- `cd ../osmx/osmx-go && /Users/shitao/.local/go-tools/go1.25.0/bin/go test ./...`
- `cd ../osmx && python3 scripts/migration_pair_check.py --root .`
- `cd ../osmx && git diff --check -- osmx-go/internal/aof/workcenter osmx-go/internal/api/v1/aof_handler.go osmx-go/internal/api/v1/aof_handler_test.go osmx-go/internal/router/router.go docs/reference/aof-workcenter-ticket-change-contract-v0.md`

## Result

All validation commands passed.
