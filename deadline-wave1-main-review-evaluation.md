# Deadline Wave 1 Main Review Evaluation

> Date: 2026-04-23
> Last refreshed: 2026-04-23 05:29 CST
> Scope: DW1 main-review evaluation for status board promotion
> Inputs:
> - `/Users/apple/Exec/Code/osmx/docs/plans/osmx-product-deadline-2026-05-15-delivery-plan.md`
> - `/Users/apple/Exec/Code/osmx/docs/plans/osmx-deadline-wave1-command-asset-task-pack.md`
> - `/Users/apple/Exec/Code/osmx/docs/plans/osmx-dual-repo-wave-board.md`
> - `/Users/apple/Exec/Code/shared-specs/deadline-wave1-implementation-delivery-package.md`
> - `/Users/apple/Exec/Code/shared-specs/deadline-wave1-dirty-baseline-isolation-list.md`
> - `/Users/apple/Exec/Code/shared-specs/deadline-wave1-owner-merge-review-decision.md`

## 2026-04-23 05:29 CST PR #44 Update / Freeze

DW1 main-review is now represented by clean PR #44:

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

The reviewable package is a 29-file clean net diff. The earlier 47-file staged slice remains historical source intent from the dirty `osmx-emergency-main-sync` worktree.

Latest validation status:

| Command | Result |
|---------|--------|
| `npm ci` | Passed; reported 5 audit vulnerabilities (2 moderate, 3 high), no audit fix run |
| `npm run build:check` | Passed with existing Vite dynamic import and chunk-size warnings |
| `go test ./internal/plan/... ./internal/runbook/handler ./internal/runbook/contentpack ./internal/runbook/service ./internal/runbook/repository ./internal/repository -count=1` | Passed with existing `$GOPATH` go.mod warning |
| `go test -tags runbook ./internal/runbook -count=1` | Passed with existing `$GOPATH` go.mod warning |
| `go test -tags 'plan runbook' ./internal/plan -count=1` | Passed with existing `$GOPATH` go.mod warning |
| `go build -tags 'plan runbook' ./cmd/server` | Passed; generated `osmx-go/server` removed before commit |
| `E2E_FRONTEND_PORT=45174 VITE_API_PROXY_TARGET=http://127.0.0.1:18082 E2E_BACKEND_BASE_URL=http://127.0.0.1:18082 npx playwright test e2e/11-command-center-chain.spec.ts e2e/12-command-center-real-chain.spec.ts e2e/13-asset-flow-real-breadth.spec.ts e2e/14-command-center-plan-binding.spec.ts --reporter=list` | `7 passed (22.7s)` |
| `python3 scripts/migration_pair_check.py --root . && git diff --check` | Passed after migration file rename and duplicate approval-index removal |
| `python3 scripts/pr_checklist_lint.py --base github/main --body "$body"` | Passed before updating GitHub PR body |
| GitHub PR checks | `security-gate` passed and `GitGuardian Security Checks` passed on head `302bfef` |
| Disposable PostgreSQL probe | `/health` and `/api/v1/auth/login` passed against Docker `postgres:15`; runbook AutoMigrate logged `ERROR: type "mediumtext" does not exist`; `003_mainchain_core.postgres.sql` applied; `003_approval_execution_links.postgres.sql` failed because `osm_runbook_execution` was absent |

Recorded failed attempts:

- Missing `OSMX_EMERGENCY_ADMIN_PASSWORD` blocked first runtime startup.
- Passwordless local MySQL `root` assumption blocked the second startup.
- Playwright/Vite port mismatch caused the first frontend smoke timeout.
- Reusing another worktree's `15174` Vite server caused the second smoke run to fail 7/7 against the wrong backend.
- PR #44 includes test-runtime config to avoid those reproducibility traps.
- First GitHub `security-gate` failed on migration filename pairing; fixed by using `.mysql.sql` / `.postgres.sql` plus `003_approval_execution_links.sql`.
- First GitGuardian check failed on hardcoded E2E credentials; fixed by amending the GitHub PR commit to read credentials from environment variables. No GitGuardian-side sync or dashboard action was performed.
- Second `security-gate` failed on missing DB-sensitive PR checklist; fixed by updating PR #44 body with the repository template.
- PostgreSQL runtime/apply probe did not pass; this is now recorded as a follow-up blocker, not a reason to keep changing frozen PR #44.

## Conclusion

Recommended status-board outcome: `frozen_for_owner_review / GitHub checks passed / decision_ready / current_source_smoke_refreshed / pass_with_risk`.

PR #44 is suitable for the main-review decision step and is frozen for owner review, but it is **not** a final merge-ready declaration. The owner still needs to decide whether to accept the current main-review package or return it for fixes and boundary tightening.

## G2 Command Center

Verdict: `pass_with_risk`.

Assessment:
- The Command Center chain is evidence-backed enough for main review.
- The intended flow `Incident -> Plan -> Approval -> AssetExecution -> Artifact -> Audit` has recorded real-chain coverage.
- Focused Go coverage and real-chain smoke both passed, so G2 is no longer a speculative or mock-only result.

Residual risk:
- The schema/migration release boundary still needs owner grouping before final merge-ready.
- The long-running `18081` process remains a current-source ambiguity unless the operator restarts it.

## G3 Asset & Flow Center

Verdict: `pass_with_risk`.

Assessment:
- Asset & Flow breadth is now proved on current source, including the asset-type split needed for review.
- The recorded `3 passed` current-source breadth smoke covers native runbook, imported operation, and imported flow paths.
- The asset-center result is therefore strong enough for main review, not just for implementation self-check.

Residual risk:
- The proof came from a temporary `18082` backend, so it should stay isolated as validation evidence rather than being treated as the permanent runtime baseline.
- Dirty baseline isolation still matters because unrelated files and binaries must not leak into the product review slice.

## G4 Run Explorer

Verdict: `pass_with_risk`.

Assessment:
- Run Explorer now has enough evidence to explain execution, step, artifact, and audit linkage for DW1 main review.
- The real-chain smoke evidence shows the execution path is not just nominal; it is linked to the approval and artifact/audit trail.
- This is sufficient for the status board to enter decision-ready handling.

Residual risk:
- Production/customer DB apply remains a release-time risk, not something the current review package can fully close.
- Final owner acceptance still depends on keeping schema/migration decisions grouped and bounded.

## Validation Already Recorded

- `cd osmx-go && go test ./internal/plan/... ./internal/runbook/handler ./internal/runbook/service ./internal/runbook/repository`
- `cd osmx-go && go test ./internal/runbook/handler ./internal/runbook/contentpack`
- `VITE_API_PROXY_TARGET=http://127.0.0.1:18081 E2E_BACKEND_BASE_URL=http://127.0.0.1:18081 npx playwright test e2e/12-command-center-real-chain.spec.ts`
- `OSMX_SERVER_PORT=18082 go run ./cmd/emergency -config configs/emergency.yaml`
- `VITE_API_PROXY_TARGET=http://127.0.0.1:18082 E2E_BACKEND_BASE_URL=http://127.0.0.1:18082 npx playwright test e2e/13-asset-flow-real-breadth.spec.ts --reporter=list`
- `git diff --check`
- Migration replay evidence: MySQL local live apply passed; MySQL/PostgreSQL temporary replay passed
- `cd osmx-go && go test ./internal/runbook/repository ./internal/repository -count=1`
- `cd osmx-go && go test ./internal/runbook/handler ./internal/runbook/contentpack ./internal/plan/... ./internal/runbook/service ./internal/runbook/repository ./internal/repository -count=1`
- `cd osmx-go && go test -tags runbook ./internal/runbook -count=1`
- `cd osmx-go && go test -tags 'plan runbook' ./internal/plan -count=1`
- `cd osmx-go && go build -tags 'plan runbook' ./cmd/server`
- `VITE_API_PROXY_TARGET=http://127.0.0.1:18082 E2E_BACKEND_BASE_URL=http://127.0.0.1:18082 npx playwright test e2e/11-command-center-chain.spec.ts e2e/12-command-center-real-chain.spec.ts e2e/13-asset-flow-real-breadth.spec.ts e2e/14-command-center-plan-binding.spec.ts --reporter=list` (`7 passed`)
- `cd osmx-go && go test ./internal/runbook/... -count=1`
- `cd frontend && npm run build:check`
- DW1 manifest gate: include set and staged implementation set both `47`; forbidden binary `osmx-go/emergency` is not staged

## 2026-04-23 04:30 CST Refresh

The handoff task was executed against `/Users/apple/Exec/Code/osmx-emergency-main-sync` after the recoverable handoff was written.

| Command | Result |
|---------|--------|
| `git diff --check && git diff --cached --check` | Passed |
| `git diff --cached --name-only \| wc -l` | `47` |
| `git diff --cached --name-only \| grep -Fx 'osmx-go/emergency' && exit 1 \|\| true` | Passed; forbidden binary is not staged |
| `go test ./internal/runbook/handler ./internal/runbook/contentpack ./internal/plan/... ./internal/runbook/service ./internal/runbook/repository ./internal/repository -count=1` | Passed; only the existing `$GOPATH /Users/apple/go` go.mod warning appeared |
| `npm run build:check` | Passed; existing Vite dynamic import and chunk-size warnings remain non-blocking |
| `OSMX_SERVER_PORT=18082 go run ./cmd/emergency -config configs/emergency.yaml` | Temporary current-source backend started on `18082` and was stopped after smoke |
| `VITE_API_PROXY_TARGET=http://127.0.0.1:18082 E2E_BACKEND_BASE_URL=http://127.0.0.1:18082 npx playwright test e2e/11-command-center-chain.spec.ts e2e/12-command-center-real-chain.spec.ts e2e/13-asset-flow-real-breadth.spec.ts e2e/14-command-center-plan-binding.spec.ts --reporter=list` | `7 passed (34.5s)` |

Observed risk from refresh:

- `18081` was still listening before the run and remains an old-process risk unless restarted from current source.
- Slow SQL warnings were still observed on high-row-count runbook tree/list paths and Content Pack delete cleanup. Keep this as follow-up performance/index work, not as a DW1 scope expansion.

## Must Keep Risks

1. Production/customer DB apply is still a release-time risk.
2. `18081` is still an old-process risk and must not be treated as current-source proof.
3. Dirty baseline isolation must remain strict so peripheral work does not enter the DW1 review slice.
4. Forbidden binary `osmx-go/emergency` must stay out of the merge candidate.
5. Schema/migration owner grouping must remain intact, especially around approval/execution linkage.
6. `/api/v1/runbooks/tree` slow SQL under the old high-row-count test database should remain a follow-up migration/index analysis item.

## Owner Decision Options

1. `accept main-review package`
   - Use this when the owner accepts the current evidence set, keeps the conclusion at `pass_with_risk`, and advances the state board to decision handling.

2. `return for fixes`
   - Use this when the owner wants tighter dirty-baseline isolation, clearer schema/migration grouping, or a refreshed current-source smoke proof before proceeding.

## Final Position

DW1 PR #44 is frozen for `decision_ready / current_source_smoke_refreshed`, and GitHub checks have passed on head `302bfef`; the package is still `pass_with_risk` and should not be described as final merge-ready yet. PostgreSQL runtime/apply closure remains blocked by runbook `mediumtext` portability and must be handled as a separate follow-up lane.
