# Wave 1 Main Repo Evaluation

> Date: 2026-04-21 21:36 CST
> Evaluator scope: `/Users/apple/Exec/Code/osmx`
> Implementation scope: `/Users/apple/Exec/Code/osmx-emergency-main-sync`
> Input package: `shared-specs/wave1-emergency-owner-summary-package.md`

## 1. Conclusion

Evaluation object:

```text
Wave 1 - WP1 main-chain contract closure + WP2/WP3 minimal smoke
```

Main-repo evaluation result:

```text
Pass
```

Recommendation:

```text
Move to osmx owner decision. The implementation repo has enough evidence to prepare merge-back review,
but final merge readiness still requires the osmx owner decision and a reviewed PR/merge plan.
```

## 2. Acceptance Mapping

| Gate | Required by main repo | Current evidence | Result |
|------|-----------------------|------------------|--------|
| WP1 main-chain closure | `Plan -> Approval -> AssetExecution -> Artifact -> Audit` is semantically closed | Live smoke completed with plan, approval, execution, artifacts, and audit evidence | Pass |
| WP2/WP3 minimal path | Command Center can enter plan/execution/result surfaces | Page smoke passed for plans, plan detail, approvals, audit logs, and executions | Pass |
| Build gate | Frontend type/build gate is green | `npm run build:check` passed | Pass |
| Server compile gate | Main `cmd/server` path must compile with `plan runbook` tags | `go build -tags 'plan runbook' -o /tmp/osmx-wave1-cmd-server ./cmd/server` passed | Pass |
| Regression gate | Relevant backend runbook/plan tests pass | Focused backend regression passed after fixing a test data isolation issue | Pass |
| Conflict gate | No unresolved merge conflicts | `git diff --name-only --diff-filter=U` is empty | Pass |
| Scope control | No new Studio/OO/Worker expansion for this evaluation step | This pass only fixed a runbook engine concurrency test and wrote evaluation docs | Pass |

## 3. Verification Run In This Evaluation Pass

Frontend:

```bash
cd /Users/apple/Exec/Code/osmx-emergency-main-sync/frontend
npm run build:check
```

Result:

```text
passed
```

Notes:

- Production Vite build completed.
- Only build warnings were chunk-size and ineffective dynamic import warnings; no type or build failure.

Server compile gate:

```bash
cd /Users/apple/Exec/Code/osmx-emergency-main-sync/osmx-go
go build -tags 'plan runbook' -o /tmp/osmx-wave1-cmd-server ./cmd/server
```

Result:

```text
passed
```

Backend regression:

```bash
cd /Users/apple/Exec/Code/osmx-emergency-main-sync/osmx-go
go test -tags 'plan runbook' ./cmd/emergency ./internal/runbook/engine ./internal/runbook/compiler/afl ./internal/runbook/service ./internal/runbook/handler ./internal/runbook/acceptance ./internal/plan/... -count=1
```

First result:

```text
failed in internal/runbook/engine TestSaveStateConcurrent
fatal error: concurrent map writes
```

Root cause:

```text
The test used `s := *state`, then each goroutine wrote `s.Context["iter"]`.
That shallow copy reused the same Context map across goroutines, so the panic came from test data preparation.
```

Fix:

```text
osmx-go/internal/runbook/engine/resilience_test.go now clones `state.Context` per goroutine before mutation.
```

Rerun:

```bash
go test -tags 'plan runbook' ./internal/runbook/engine -count=1
go test -tags 'plan runbook' ./cmd/emergency ./internal/runbook/engine ./internal/runbook/compiler/afl ./internal/runbook/service ./internal/runbook/handler ./internal/runbook/acceptance ./internal/plan/... -count=1
```

Rerun result:

```text
passed
```

Conflict gate:

```bash
cd /Users/apple/Exec/Code/osmx-emergency-main-sync
git diff --name-only --diff-filter=U
```

Result:

```text
empty
```

## 4. Runtime And Page Smoke Evidence

Runtime evidence is accepted from the emergency owner summary package.

Startup mode:

```text
backend:  go run ./cmd/emergency -config configs/config.yaml
frontend: npm run dev -- --host 0.0.0.0
```

Runtime ports:

```text
backend:  http://localhost:8080
frontend: http://localhost:15174
```

API probes after login returned HTTP 200:

```text
/health
/api/v1/plans?page=1&page_size=20
/api/v1/approvals?page=1&page_size=20
/api/v1/audit-logs?page=1&page_size=20
/api/v1/approvals/stats
/api/v1/audit-logs/stats
```

Live chain smoke:

```text
runbook UUID:        033afefa-cfac-4e96-ac29-bdbc043f86c4
plan UUID:           37bdb9bd-07c4-41f8-aa38-b1ec4b343051
approval ID:         3
execution UUID:      91804de3-b418-47c2-833b-427289a53b17
engine execution ID: 26
final status:        COMPLETED
artifact count:      2
execution audit:     1
backend health:      200 after execution
```

Page smoke passed with no page errors and no HTTP 4xx/5xx:

```text
/command-center/plans
/command-center/plans/37bdb9bd-07c4-41f8-aa38-b1ec4b343051
/approvals
/audit-logs
/runbook/executions
```

## 5. Risks

1. The implementation worktree is still substantially dirty. This is expected for the accumulated Wave 1 diff, but it means merge-back should use a reviewed PR or intentionally sliced merge plan rather than a blind direct merge.

2. The main `osmx` repo has unrelated untracked PDFs/upload artifacts. They are not part of this Wave 1 evaluation and should stay out of the merge-back decision.

3. Existing imported AFL runbooks compiled before the self-loop fix may still need reimport or recompile.

4. The runtime smoke observed a transient startup-order warning:

```text
No business execution found for engine ID 26
```

The chain still completed with artifacts and audit evidence, so this is a follow-up observation, not a blocker.

## 6. Suggested Owner Decision

Recommended owner verdict:

```text
准备合回 main
```

Recommended immediate action:

```text
Prepare a reviewed merge-back plan from osmx-emergency-main-sync into osmx main. Keep Wave 2 blocked until
the owner either approves merge-back or explicitly chooses a smaller PR slicing strategy.
```
