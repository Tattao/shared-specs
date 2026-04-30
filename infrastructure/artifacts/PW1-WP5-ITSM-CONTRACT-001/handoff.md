# PW1-WP5-ITSM-CONTRACT-001 Handoff

Status: `closed_pass`

## Operator Notes

- Use `GET /api/v1/aof/workcenter/schema` to inspect the Ticket and ChangeRequest contract definitions.
- Use `POST /api/v1/aof/workcenter/validate` with `type: "ticket"` or `type: "change_request"` and a `payload` object to validate caller-owned records.
- The implementation is intentionally side-effect free: it validates and normalizes contract payloads but does not persist, synchronize, or notify external systems.

## Next Consumers

- A future WorkCenter UI shell can use the schema endpoint to render required fields and validation copy.
- A future ITSM connector task should map provider-specific ticket/change status values onto this contract before adding runtime side effects.
