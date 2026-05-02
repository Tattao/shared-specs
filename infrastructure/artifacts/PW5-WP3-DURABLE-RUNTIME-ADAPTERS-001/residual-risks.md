# PW5-WP3 Residual Risks

- Only the Workcenter approval-backed read path moved to store-backed data in this increment.
- Additional AOF surfaces should be migrated one at a time with provenance tests.
- High-volume filtering on approval payload JSON may need a future indexed persistence design.
