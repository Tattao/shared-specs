# Wave 2 P0 Public Credential Cleanup

> Date: 2026-04-22
> Scope: collaboration evidence only. Final product/source truth remains `osmx`.

## Trigger

Architect J identified that public `osmx` files exposed private infrastructure details and credential-like values. This must be handled before K1 starts Wave 2 feature development.

The exact sensitive values are intentionally not repeated in this record.

## OSMX PR

- Repository: `Tattao/osmx`
- Base: `main`
- Branch: `p0-public-credential-cleanup-20260422`
- PR: `https://github.com/Tattao/osmx/pull/7`
- Cleanup commit: `14f0922`
- Merge commit: `91c4f87`
- State: merged

## Cleanup Summary

PR #7 removes sensitive traces from the current tree by:

- deleting tracked backup env/config files that contained private deployment details
- redacting private infrastructure addresses from README, docs, configs, scripts, and regression fixtures
- replacing committed default passwords/API-style values with env-required placeholders or local-safe defaults
- making Docker Compose `.env` optional while requiring secret env vars when rendering compose config
- keeping the change scoped to P0 cleanup, with no Wave 2 product feature work

## Validation Evidence

Executed in `/Users/apple/Exec/Code/osmx-main-merge`:

High-risk exact-match scan covered private infrastructure IPs, the previously exposed login identifiers, the previously exposed credential literals, API-key-shaped values, AWS key IDs, and private key blocks.

Result: no remaining current-tree match for the P0 high-risk pattern.

```bash
git diff --check
python3 -m py_compile alembic/env.py scripts/tcp-proxy.py
MYSQL_ROOT_PASSWORD=example-root MYSQL_PASSWORD=example-app REDIS_PASSWORD=example-redis TIMESCALEDB_POSTGRES_PASSWORD=example-tsdb GRAFANA_ADMIN_PASSWORD=example-grafana docker compose config -q
cd osmx-go && go test ./internal/service -count=1
```

Result: pass.

Broad password/token scan still reports expected generic schema, docs, test, and placeholder references. No high-risk exact matches from the P0 pattern above remained in the current tree.

## Required Operator Action

This cleanup only removes values from the current tree. Because the repository is public and these values already existed in Git history, operators must still:

- rotate/revoke any exposed server/service credentials
- rotate/revoke any exposed API keys
- update private deployment `.env` / secret manager values
- decide whether public history cleanup is required
- treat the old credentials as compromised until rotation is confirmed

## Wave 2 Gate

K1 should not start broad Wave 2 feature work until:

- PR #7 cleanup is present on `main`
- credential rotation/revocation is confirmed outside the repo
- Wave 2 mother task brief is written against the post-cleanup main baseline
