# Handoff

`PW2-WP7-AGENTOPS-RUNTIME-API-001` is ready for the dependent UI binding task.

Use these endpoints for `PW2-WP7-AGENTOPS-UI-BINDING-001`:

- `GET /api/v1/aof/agentops/traces`
- `GET /api/v1/aof/agentops/traces/:id`

Python helper:

- `app.agent_runtime.agentops_runtime.runtime_traces()`
- `app.agent_runtime.agentops_runtime.runtime_trace_by_id(trace_id)`

The runtime path remains read-only and replay-safe.
