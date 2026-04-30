# Validation

Commands:

```bash
python3 infrastructure/runner-v2.py next
python3 infrastructure/runner-v2.py lease AOF-STAGEA-RUNNER-SMOKE-001 --owner Codex --status running
python3 infrastructure/runner-v2.py heartbeat AOF-STAGEA-RUNNER-SMOKE-001 --owner Codex
python3 infrastructure/runner-v2.py complete AOF-STAGEA-RUNNER-SMOKE-001 --owner Codex --verdict pass
python3 infrastructure/runner-v2.py status
```

Expected result:

- `next` lists the smoke task as auto-runnable.
- `lease` sets status to `running`, owner to `Codex`, heartbeat, lease expiry, and attempts.
- `heartbeat` refreshes heartbeat and lease expiry.
- `complete` sets status to `closed`.

Actual result on 2026-04-30:

- `next` selected `AOF-STAGEA-RUNNER-SMOKE-001` before the smoke lifecycle.
- `lease` moved the task to `running`, set `owner=Codex`, and created a lease expiry.
- `heartbeat` refreshed the task heartbeat and lease expiry.
- `complete --verdict pass` moved the task to `closed`.
- Final queue status showed `AOF-STAGEA-RUNNER-SMOKE-001 | closed | P0 | gate=none | profile=codex-docs-ops | owner=Codex`.
