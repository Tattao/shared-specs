# Wave 1 Merge-Back PR Description

## Summary

Merge Wave 1 emergency integration into `main`.

This PR brings in the validated `batch/full-integration` work plus the final Wave 1 fixes from `osmx-emergency-main-sync`.

PR head commit:

```text
a14f425 merge: prepare Wave 1 emergency integration
```

The branch is intentionally a single-parent squashed commit rooted at `origin/main`, so the final reviewed tree is preserved without carrying old integration-branch history into PR security scanning.

Scope:

- WP1: `Plan -> Approval -> AssetExecution -> Artifact -> Audit` main-chain closure.
- WP2/WP3: minimal Command Center path and execution/result backflow.
- Runbook engine/runtime stability fixes.
- Frontend build gate cleanup needed for reproducible `npm run build:check`.
- Wave 1 status board and merge-readiness docs.
- PR review fix: `cmd/server` now registers the plan-chain routes when built with `plan runbook` tags.

## Validation

Run from `/Users/apple/Exec/Code/osmx-main-merge`:

```bash
git diff --name-only --diff-filter=U
git diff --check HEAD^..HEAD
```

```bash
cd osmx-go
go build -tags 'plan runbook' -o /tmp/osmx-wave1-cmd-server ./cmd/server
go test -tags 'plan runbook' ./cmd/emergency ./internal/runbook/engine ./internal/runbook/compiler/afl ./internal/runbook/service ./internal/runbook/handler ./internal/runbook/acceptance ./internal/plan/... -count=1
go test -tags 'plan runbook' ./internal/plan -run TestPlanExtensionRegistersChainRoutesWithRunbook -count=1
```

```bash
cd frontend
npm ci
npm run build:check
```

```bash
cd osmx-ai
python3 -m py_compile app/core/config.py
```

All commands passed.

GitHub check status:

```text
GitGuardian Security Checks: pass
```

Review report:

```text
shared-specs/wave1-pr2-review-report.md
```

## Notes

- `js-yaml` and `@types/js-yaml` were added because clean `npm ci && npm run build:check` failed without explicit declarations for `src/utils/flow-yaml.ts`.
- The tracked `osmx-go/emergency` binary was restored to the `origin/main` blob before PR creation, so this PR does not update that build artifact.
- `osmx-go/configs/emergency.yaml`, `cmd/emergency`, and `tests/acceptance-test.js` no longer carry default admin/database secrets; credentials must be provided through environment/config.
- `osmx-ai/config/config.yaml` now reads `bicqa.api_key` from `BICQA_API_KEY`, and `osmx-ai/app/core/config.py` expands that environment placeholder.
- The unrelated `docs/全方位对比HermesVSOpenClaw.pdf` binary artifact was removed from the PR branch.
- `npm ci` reports 5 audit findings. They did not block install or build and are not introduced as the Wave 1 acceptance gate.
- The PR intentionally excludes unrelated local PDFs/upload artifacts from the dirty `/Users/apple/Exec/Code/osmx` worktree.
- The GitHub PR diff API still reports `diff too_large` because the PR exceeds 20,000 changed lines; use local diff/stat commands or split follow-up PRs if web line-by-line review is required.
- Wave 2 should remain blocked until this PR is reviewed/merged or explicitly paused by the owner.
