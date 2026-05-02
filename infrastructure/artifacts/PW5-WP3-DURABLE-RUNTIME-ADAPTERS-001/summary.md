# PW5-WP3 Durable Runtime Adapters Summary

Result: `closed_pass`

`osmx` connected the AOF Workcenter runtime reader to the existing approval main chain. The new adapter reads `osm_approvals` rows of type `aof_governed_action` and projects them into Workcenter runtime records.

When approval-backed rows exist, runtime provenance reports `runtime_source=store`. When no store-backed rows exist, the handler falls back to deterministic sample records and reports `runtime_source=sample`.
