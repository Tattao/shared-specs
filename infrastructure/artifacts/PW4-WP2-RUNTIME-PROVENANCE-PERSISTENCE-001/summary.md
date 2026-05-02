# PW4-WP2 Runtime Provenance Persistence Summary

Date: 2026-04-30

Result: pass

AOF runtime list/detail responses now include additive provenance fields:

- `schema_version`
- `runtime_source`
- `store_kind`
- `adapter_source`
- `runtime_provenance`

List responses retain array shape. Detail responses retain object shape.

The provenance contract is documented in `osmx/docs/reference/aof-runtime-provenance-contract-v0.md`.
