# PW1-WP6-AUTOPILOT-EVIDENCE-CONTRACT-001 Validation

## Passed

- `cd ../osmx/osmx-go && /Users/shitao/.local/go-tools/go1.25.0/bin/gofmt -w internal/aof/autopilot/evidence_contract.go internal/aof/autopilot/evidence_contract_test.go internal/api/v1/aof_handler.go internal/api/v1/aof_handler_test.go internal/router/router.go`
- `cd ../osmx/osmx-go && /Users/shitao/.local/go-tools/go1.25.0/bin/go test ./internal/aof/autopilot ./internal/api/v1 ./internal/router`
- `cd ../osmx/osmx-go && /Users/shitao/.local/go-tools/go1.25.0/bin/go test ./...`
- `cd ../osmx/osmx-ai && /tmp/osmx-ai-pw1-venv/bin/python - <<'PY' ... PY`
- `cd ../osmx/osmx-ai && PATH=/tmp/osmx-ai-pw1-venv/bin:$PATH pytest -q`
- `cd ../osmx && python3 scripts/migration_pair_check.py --root .`
- `cd ../osmx && git diff --check -- osmx-go/internal/aof/autopilot osmx-go/internal/api/v1/aof_handler.go osmx-go/internal/api/v1/aof_handler_test.go osmx-go/internal/router/router.go osmx-ai/app/agent_runtime/autopilot_contract.py docs/reference/aof-incident-autopilot-evidence-contract-v0.md`

## Recovered Failures

Full `osmx-ai` pytest initially failed twice with 45 failures unrelated to the new Autopilot contract path:

- Redis executor tests required optional `redis` async package for mock-backed execution.
- `tests/test_llm_client_config.py` expects `LLMClient.local_address` and `_llm_client_kwargs`.
- Skill approval/regression and tool contract tests failed under the temporary Python 3.12 pytest environment with `asyncio.get_event_loop()` runtime errors.

These were repaired under `PW1-INFRA-AI-PYTEST-BASELINE-001`. Final full pytest result: `422 passed, 1 skipped`.
