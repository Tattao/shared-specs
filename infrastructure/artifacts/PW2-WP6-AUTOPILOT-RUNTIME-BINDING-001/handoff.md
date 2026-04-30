# Handoff

`PW2-WP6-AUTOPILOT-RUNTIME-BINDING-001` is ready for the dependent UI binding task.

Use these endpoints for `PW2-WP6-AUTOPILOT-UI-BINDING-001`:

- `GET /api/v1/aof/autopilot/records`
- `GET /api/v1/aof/autopilot/records/:id`

Python helper:

- `app.agent_runtime.autopilot_runtime.runtime_records()`
- `app.agent_runtime.autopilot_runtime.runtime_record_by_id(record_id)`

The runtime path remains no-LLM, read-only, and human-control preserving.
