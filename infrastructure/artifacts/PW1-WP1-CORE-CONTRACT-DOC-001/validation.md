# PW1-WP1-CORE-CONTRACT-DOC-001 Validation

## Commands

```bash
git -C ../osmx diff --check -- docs/reference/aof-core-contract-v0.md docs/plans/94-autonomic-operations-fabric-architecture-technology-upgrade-plan.md docs/guides/document-change-log.md
rg -n "AOF Core Contract v0|Unified Event Contract|Permission Matrix|Timeline" ../osmx/docs/reference/aof-core-contract-v0.md ../osmx/docs/plans/94-autonomic-operations-fabric-architecture-technology-upgrade-plan.md
git diff --check -- infrastructure/artifacts/PW1-WP1-CORE-CONTRACT-DOC-001
```

## Result

All commands passed.

The keyword scan found the new contract and expected sections in `aof-core-contract-v0.md`, and targeted `git diff --check` returned no whitespace errors.
