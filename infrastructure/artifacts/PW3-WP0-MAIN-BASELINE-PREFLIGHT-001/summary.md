# PW3-WP0 Main Baseline Preflight Summary

Date: 2026-04-30

Result: pass

Product Wave 3 is authorized by Owner to continue from the current PR branch and the Product Wave 1/2 PRs have been merged to main.

Merged baselines:

- osmx PR #57 merged at `1d57f65`.
- shared-specs PR #1 merged at `5ba2a31`.

Local Wave 3 branches:

- osmx: `codex/product-wave3-store-runtime`, `HEAD=1d57f65`, `origin/main=1d57f65`.
- shared-specs: `codex/product-wave3-store-runtime`, `HEAD=5ba2a31`, `origin/main=5ba2a31`.

Fresh local smoke:

- Backend: `http://127.0.0.1:18090`
- Frontend: `http://127.0.0.1:15190/`
- Login: pass, token length 279.
- Health: pass, `status=ok`.
- AOF runtime list endpoints: pass for twin, alerts, workcenter, autopilot, agentops, skills, resilience, and packs.

No release, production change, destructive command, migration apply, or human gate closure was performed.
