# PW1-WP6-AUTOPILOT-EVIDENCE-CONTRACT-001 Summary

Verdict: `closed_pass`

## Purpose

Define an evidence-backed Incident Autopilot output contract for RCA, hypothesis, and recommendation results without changing production model configuration or adding remediation side effects.

## Implemented

- Added Go-side AOF Autopilot contract and validation in `../osmx/osmx-go/internal/aof/autopilot/evidence_contract.go`.
- Added Go tests in `../osmx/osmx-go/internal/aof/autopilot/evidence_contract_test.go`.
- Exposed guarded AOF API endpoints:
  - `GET /api/v1/aof/autopilot/schema`
  - `POST /api/v1/aof/autopilot/validate`
- Added the `autopilot.output.generated` core AOF event contract.
- Added Python-side contract mirror in `../osmx/osmx-ai/app/agent_runtime/autopilot_contract.py`.
- Added `../osmx/docs/reference/aof-incident-autopilot-evidence-contract-v0.md`.

## Acceptance Coverage

RCA, hypothesis, and recommendation outputs require evidence references and risk markers.

Recommendations additionally require human control points.

No production model configuration, live LLM routing, remediation execution, approval closure, or durable storage was added.

## Validation Recovery

Task-local Go validation and Python contract smoke validation passed first. Full `osmx-ai` pytest initially failed on existing validation-baseline issues outside the new Autopilot contract path.

`PW1-INFRA-AI-PYTEST-BASELINE-001` restored the pytest baseline, after which full `osmx-ai` pytest passed and this task was promoted to `closed_pass`.
