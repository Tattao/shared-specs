# PW1-WP6-AUTOPILOT-EVIDENCE-CONTRACT-001 Handoff

Status: `closed_pass`

## Operator Notes

- Use `GET /api/v1/aof/autopilot/schema` to inspect RCA, hypothesis, and recommendation requirements.
- Use `POST /api/v1/aof/autopilot/validate` to validate output payloads before any future incident workflow consumes them.
- Use `app.agent_runtime.autopilot_contract.validate_output` in Python runtime code when validating generated agent output.

## Validation Note

The task graph requires full `cd osmx-ai && pytest`. That command now passes after `PW1-INFRA-AI-PYTEST-BASELINE-001` restored the `osmx-ai` validation baseline.

## Suggested Next Consumer

`PW1-WP6-RCA-PANEL-SHELL-001` may consume this contract from the frontend once selected by the ready-task scheduler.
