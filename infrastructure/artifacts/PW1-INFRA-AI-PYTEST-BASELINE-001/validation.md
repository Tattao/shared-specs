# PW1-INFRA-AI-PYTEST-BASELINE-001 Validation

## Commands

- `cd ../osmx/osmx-ai && /tmp/osmx-ai-pw1-venv/bin/python -m pytest tests/test_executors.py::TestRedisExecutor tests/test_llm_client_config.py tests/test_skill_approval_bridge.py tests/test_skill_regression.py tests/test_tool_contract.py -q`
- `cd ../osmx/osmx-ai && /tmp/osmx-ai-pw1-venv/bin/python -m pytest -q`
- `cd ../osmx/osmx-ai && PATH=/tmp/osmx-ai-pw1-venv/bin:$PATH pytest -q`
- `cd ../osmx/osmx-go && /Users/shitao/.local/go-tools/go1.25.0/bin/go test ./...`
- `cd ../osmx && git diff --check -- osmx-ai/app/agent_runtime/executors/redis_executor.py osmx-ai/app/core/config.py osmx-ai/app/core/llm_client.py osmx-ai/tests/conftest.py osmx-ai/requirements.txt`
- `cd shared-specs && git diff --check -- infrastructure/product-task-graph-v1.yaml`

## Result

All validation commands passed.

Full `osmx-ai` pytest result: `422 passed, 1 skipped`.
