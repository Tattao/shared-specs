# PW3-WP2 Handoff

Status: closed

Next ready tasks:

- `PW3-WP3-DETAIL-API-UI-BINDING-001`
- `PW3-WP6-GOVERNED-ACTION-GATES-001`

Implementation notes:

- Use `store.Scope` for future handler binding.
- Keep existing route contracts stable for frontend compatibility.
- Use `store.Provenance` internally or as additive fields only.
- Do not add migrations or raw SQL in follow-on handler binding.
