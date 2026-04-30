# PW1-WP8-SKILL-CONTRACT-001 Validation

## Commands

- `cd ../osmx/osmx-go && /Users/shitao/.local/go-tools/go1.25.0/bin/gofmt -w internal/runbook/model/action_skill_contract.go internal/runbook/model/action_skill_contract_test.go internal/plan/action_skill_contract.go internal/plan/action_skill_contract_test.go`
- `cd ../osmx/osmx-go && /Users/shitao/.local/go-tools/go1.25.0/bin/go test ./internal/runbook/... ./internal/plan/...`
- `cd ../osmx && git diff --check -- osmx-go/internal/runbook/model/action_skill_contract.go osmx-go/internal/runbook/model/action_skill_contract_test.go osmx-go/internal/plan/action_skill_contract.go osmx-go/internal/plan/action_skill_contract_test.go docs/reference/aof-action-skill-asset-execution-contract-v0.md`

## Result

All validation commands passed.
