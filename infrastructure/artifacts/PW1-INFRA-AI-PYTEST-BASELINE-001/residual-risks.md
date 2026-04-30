# PW1-INFRA-AI-PYTEST-BASELINE-001 Residual Risks

- Full `osmx-ai` pytest passes but still emits existing async mock warnings in diagnosis and inspection tests.
- The validation run used a temporary venv at `/tmp/osmx-ai-pw1-venv`; `pytest` and `pytest-asyncio` are now declared in `requirements.txt` so future environments can reproduce the test command after dependency installation.
- Redis remains an optional runtime dependency for real Redis connections; mock-backed execution/query tests no longer require it.
