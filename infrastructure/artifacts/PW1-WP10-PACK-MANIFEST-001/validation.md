# PW1-WP10-PACK-MANIFEST-001 Validation

## Commands

- `cd ../osmx/osmx-go && /Users/shitao/.local/go-tools/go1.25.0/bin/gofmt -w internal/aof/pack/manifest_contract.go internal/aof/pack/manifest_contract_test.go`
- `cd ../osmx/osmx-go && /Users/shitao/.local/go-tools/go1.25.0/bin/go test ./internal/aof/pack ./...`
- `cd ../osmx && python3 scripts/migration_pair_check.py --root .`
- `cd ../osmx && git diff --check -- osmx-go/internal/aof/pack docs/reference/aof-scenario-pack-manifest-contract-v0.md`

## Result

All validation commands passed.
