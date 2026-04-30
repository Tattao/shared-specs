# PW1-WP13-DB-GUARDRAIL-001 Validation

## Commands

- `cd ../osmx && python3 scripts/migration_pair_check.py --root .`
- `cd ../osmx && ./scripts/db-portability-scan.sh`
- `cd ../osmx && DB_PORTABILITY_SCAN_MAX_LINES=80 ./scripts/db-portability-scan.sh`
- `cd ../osmx && git diff --check -- scripts/db-portability-scan.sh docs/reports/aof-wp13-db-guardrail-20260430.md`

## Result

All validation commands passed.

The migration pair check reported 8 dialect-paired migration families and accepted the existing standalone migration allow-list.
