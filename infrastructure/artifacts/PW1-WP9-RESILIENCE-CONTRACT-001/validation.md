# PW1-WP9-RESILIENCE-CONTRACT-001 Validation

## Commands

- `cd ../osmx/osmx-go && /Users/shitao/.local/go-tools/go1.25.0/bin/gofmt -w internal/aof/resilience/experiment_contract.go internal/aof/resilience/experiment_contract_test.go`
- `cd ../osmx/osmx-go && /Users/shitao/.local/go-tools/go1.25.0/bin/go test ./internal/aof/resilience ./...`
- `cd ../osmx && git diff --check -- osmx-go/internal/aof/resilience docs/reference/aof-resilience-experiment-guardrail-contract-v0.md`

## Result

All validation commands passed.
