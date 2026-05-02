# PW3-WP1 Store Contract Refine Summary

Date: 2026-04-30

Result: pass

Refined the AOF store-backed runtime read contract before Wave 3 product-code changes.

Key decisions:

- Runtime reads use explicit `tenant_id` scope and `project_id` where applicable.
- Runtime list/detail APIs expose `runtime_source`, `store_kind`, `object_ref`, evidence refs, optional audit/idempotency provenance, and `loaded_at`.
- ObjectStore, EventStore, EvidenceStore, TraceStore, and PackRegistry read roles are explicitly mapped.
- Sample fallback is allowed only as explicit dev/demo fallback and must be marked `sample` or `hybrid`.
- Store-backed runtime work remains read-only until human-gated live DB replay and migration decisions.
