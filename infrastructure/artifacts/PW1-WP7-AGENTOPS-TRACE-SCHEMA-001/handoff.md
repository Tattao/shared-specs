# PW1-WP7-AGENTOPS-TRACE-SCHEMA-001 Handoff

Status: `closed_pass`

## Operator Notes

- Use `GET /api/v1/aof/agentops/trace/schema` to inspect the trace contract.
- Use `POST /api/v1/aof/agentops/trace/validate` to validate trace payloads before future ledger or replay consumers store them.
- Use `app.agent_runtime.agentops_trace.validate_trace` in Python runtime code for side-effect-free trace shape validation.

## Next Consumers

- `PW1-WP7-AGENTOPS-CONSOLE-001` can consume this schema for list/detail/replay placeholders.
- Future DB-backed AgentOps work should add persistence and replay behavior under a separate migration-aware task.
