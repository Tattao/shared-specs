# Deadline Wave 1 PR / Owner Handoff

> Date: 2026-04-23 04:35 CST
> Scope: coordination text only. Final product/source truth remains in `osmx`, implementation code, tests, reviewed PRs, and runbooks.

## 2026-04-23 05:29 CST Update - PR Opened / GitHub Checks Passed / Frozen

Clean PR opened:

```text
https://github.com/Tattao/osmx/pull/44
```

Clean branch/worktree:

```text
/Users/apple/Exec/Code/osmx-dw1-main-review
dw1/command-asset-main-review
base: github/main@0a07edb
head: 302bfef
```

Important correction:

- The old 47-file staged slice remains the source-intent record in the dirty `osmx-emergency-main-sync` worktree.
- The actual PR is a clean 29-file net diff because current `github/main` already contains part of that baseline and the migration pair now includes `003_approval_execution_links.sql`.
- `frontend/playwright.config.ts` and `frontend/vite.config.ts` are included in PR #44 as an explicit test-runtime exception so Playwright does not reuse another worktree's Vite server and can proxy to the candidate backend with `VITE_API_PROXY_TARGET`.
- `osmx-go/emergency`, `osmx-go/server`, Playwright `test-results`, and local handoff docs are not included.

Latest validation to cite for PR #44:

```bash
cd frontend
npm ci
npm run build:check
E2E_FRONTEND_PORT=45174 \
E2E_ADMIN_PASSWORD=<local-admin-password> \
VITE_API_PROXY_TARGET=http://127.0.0.1:18082 \
E2E_BACKEND_BASE_URL=http://127.0.0.1:18082 \
npx playwright test \
  e2e/11-command-center-chain.spec.ts \
  e2e/12-command-center-real-chain.spec.ts \
  e2e/13-asset-flow-real-breadth.spec.ts \
  e2e/14-command-center-plan-binding.spec.ts \
  --reporter=list
```

Result: `npm ci` passed with 5 audit vulnerabilities; `npm run build:check` passed with existing Vite warnings; Playwright result was `7 passed (22.7s)`.

```bash
cd osmx-go
go test ./internal/plan/... ./internal/runbook/handler ./internal/runbook/contentpack ./internal/runbook/service ./internal/runbook/repository ./internal/repository -count=1
go test -tags runbook ./internal/runbook -count=1
go test -tags 'plan runbook' ./internal/plan -count=1
go build -tags 'plan runbook' ./cmd/server
```

Result: all passed. Go emitted the existing `$GOPATH /Users/apple/go` go.mod warning. Generated `osmx-go/server` was removed before commit.

Failed attempts recorded in PR #44:

- Startup without `OSMX_EMERGENCY_ADMIN_PASSWORD` failed.
- Startup with only `OSMX_EMERGENCY_ADMIN_PASSWORD` failed because local MySQL `root` had no passwordless access.
- First Playwright attempt timed out waiting for `5173`.
- Second Playwright attempt failed 7/7 after reusing another worktree's `15174` Vite server pointed at an unrelated `8080` backend.
- PR #44 fixes the reproducibility problem with isolated port `45174`, no server reuse, and dynamic Vite proxy target.
- First GitHub `security-gate` run failed on migration filename pairing; fixed by renaming paired artifacts to `.mysql.sql` / `.postgres.sql` and adding `003_approval_execution_links.sql`.
- First GitGuardian check failed on hardcoded credentials in new E2E specs; fixed by amending the GitHub PR commit so credentials come from environment variables. No GitGuardian-side sync or dashboard action was performed.
- Second `security-gate` run failed on missing DB-sensitive PR checklist; fixed by updating the GitHub PR body from the repository template.
- Latest GitHub checks on head `302bfef`: `security-gate` passed and `GitGuardian Security Checks` passed.
- Freeze state: PR #44 is frozen for owner review on head `302bfef`; do not add more code unless owner/reviewer feedback returns the PR.
- Disposable PostgreSQL probe after freeze: `cmd/emergency` reached `/health` and `/api/v1/auth/login` against Docker `postgres:15`, but runbook AutoMigrate logged `ERROR: type "mediumtext" does not exist`. `003_mainchain_core.postgres.sql` applied, while `003_approval_execution_links.postgres.sql` failed because `osm_runbook_execution` was absent. PostgreSQL runtime/apply closure remains a separate follow-up lane.

## Recommended Owner Decision

Accept the DW1 main-review package for review, but keep the status as:

```text
frozen_for_owner_review / GitHub checks passed / decision_ready / current_source_smoke_refreshed / pass_with_risk
```

This is not final merge-ready. It means the owner can review PR #44 as the clean DW1 main-chain package while keeping schema/migration release boundary and production/customer DB apply as explicit remaining risks.

## PR Candidate Boundary

Original implementation worktree:

```text
/Users/apple/Exec/Code/osmx-emergency-main-sync
```

Branch:

```text
batch/full-integration
```

Candidate source:

```text
git diff --cached --name-only
```

Clean PR candidate:

```text
29 net files in PR #44
```

The staged slice covers:

- Command Center path and plan/approval/execution chain.
- Asset & Flow Center read paths for native runbook, imported operation, and imported flow.
- Run Explorer linkage for execution, artifact, and audit surfaces.
- Approval/execution model and migration pair for MySQL/PostgreSQL replay.
- Focused E2E specs `11` through `14`.

Do not include unstaged non-candidate files. Do not stage or merge `osmx-go/emergency`.

## Historical 47-File Source-Intent Evidence

The following evidence belongs to the original dirty-worktree staged source intent. PR #44 already contains the updated clean-branch evidence in the 05:08 section above and in the PR body.

```bash
git diff --check && git diff --cached --check
```

Result: passed.

```bash
git diff --cached --name-only | wc -l
```

Result: `47`.

```bash
git diff --cached --name-only | grep -Fx 'osmx-go/emergency' && exit 1 || true
```

Result: passed; forbidden binary is not staged.

```bash
cd osmx-go
go test ./internal/runbook/handler ./internal/runbook/contentpack ./internal/plan/... ./internal/runbook/service ./internal/runbook/repository ./internal/repository -count=1
```

Result: passed; only the existing `$GOPATH /Users/apple/go` go.mod warning appeared.

```bash
cd frontend
npm run build:check
```

Result: passed; existing Vite dynamic import and chunk-size warnings remain non-blocking.

```bash
cd osmx-go
OSMX_SERVER_PORT=18082 go run ./cmd/emergency -config configs/emergency.yaml
```

Result: temporary current-source backend started on `18082` and was stopped after smoke.

```bash
cd frontend
VITE_API_PROXY_TARGET=http://127.0.0.1:18082 \
E2E_BACKEND_BASE_URL=http://127.0.0.1:18082 \
npx playwright test \
  e2e/11-command-center-chain.spec.ts \
  e2e/12-command-center-real-chain.spec.ts \
  e2e/13-asset-flow-real-breadth.spec.ts \
  e2e/14-command-center-plan-binding.spec.ts \
  --reporter=list
```

Result: `7 passed (34.5s)`.

## Required PR Wording

Suggested title:

```text
DW1: Command Center and Asset Flow main-chain review package
```

Suggested summary:

```text
This PR packages the Deadline Wave 1 Command Center + Asset & Flow Center main-review slice.

It closes enough of the main chain for review:
Plan -> Approval -> AssetExecution -> Artifact -> Audit

It also provides Asset & Flow Center read-path evidence for native runbook, imported operation, and imported flow surfaces.

Status is decision_ready / current_source_smoke_refreshed / pass_with_risk. This PR is ready for owner review, but it is not a final merge-ready declaration until the owner accepts the package boundary and release-time DB apply risk.
```

Suggested risk section:

```text
Remaining risks:
- pass_with_risk remains until owner accepts the schema/model/migration boundary.
- Production/customer DB apply is still a release-time risk.
- 18081 was still an old-process listener; current-source proof used temporary 18082.
- Slow SQL remains on high-row-count runbook tree/list paths and Content Pack delete cleanup; keep as follow-up performance/index work.
- Unstaged non-DW1 dirty files and osmx-go/emergency must stay out of this PR.
```

## Next Unique Executable Task

```text
Owner reviews PR #44. If accepted, continue normal PR review handling and keep status pass_with_risk until migration/release DB risk is accepted. If returned, patch only /Users/apple/Exec/Code/osmx-dw1-main-review on branch dw1/command-asset-main-review, rerun the recorded validation set, push updates to GitHub PR #44, and update this handoff plus the registry. Do not perform GitGuardian-side sync or dashboard actions. Do not treat PostgreSQL runtime smoke as passed until the runbook `mediumtext` portability blocker is fixed in a separate lane.
```
