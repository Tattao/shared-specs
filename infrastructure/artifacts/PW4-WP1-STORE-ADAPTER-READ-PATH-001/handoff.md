# PW4-WP1 Handoff

Status: closed

Next ready task:

- `PW4-WP2-RUNTIME-PROVENANCE-PERSISTENCE-001`

Implementation notes:

- AOF runtime handlers now use `store.RuntimeReader` fields on `AOFHandler`.
- Current adapters report `runtime_source=sample`.
- Preserve the additive-only response contract in follow-on provenance work.
