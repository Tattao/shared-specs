# OSMX Suite Current Baseline Assessment

> Date: 2026-04-21
> Scope: `/Users/apple/Exec/Code/osmx`, `/Users/apple/Exec/Code/osmx-emergency-main-sync`, `/Users/apple/Exec/Code/shared-specs`
> Purpose: establish the current dual-repo baseline before further multi-agent execution.

## 1. Reading Method

This assessment does not require reading every Markdown file in both repositories.

The reliable method is:

1. Read the canonical facts in `osmx/docs/plans`.
2. Confirm whether `osmx-emergency-main-sync/docs/plans` matches or diverges.
3. Check workspace rules, repo agent rules, and current Git state.
4. Use historical reports, manuals, screenshots, and PDFs only when a specific task needs them.

## 2. Canonical Reading Set

The current must-read set is:

| Priority | File | Role |
|----------|------|------|
| P0 | `osmx-suite.code-workspace` | Workspace mount and VS Code task baseline |
| P0 | `shared-specs/AGENTS.md` | Cross-repo dispatch boundary |
| P0 | `osmx/AGENTS.md` | Core platform agent boundary |
| P0 | `osmx-emergency-main-sync/AGENTS.md` | Emergency implementation agent boundary |
| P0 | `osmx/docs/plans/README.md` | Plans hub and source-of-truth declaration |
| P0 | `osmx/docs/plans/osmx-stage1-dual-track-master-plan.md` | Current stage and repository role facts |
| P0 | `osmx/docs/plans/osmx-parallel-delivery-and-multi-agent-orchestration-plan.md` | Dual-repo / multi-agent operating model |
| P0 | `osmx/docs/plans/osmx-parallel-multi-agent-prompts-and-wave1-task-pack.md` | Wave 1 mother task, subtasks, and acceptance template |
| P0 | `osmx/docs/plans/osmx-dual-repo-agent-operator-runbook.md` | Human / agent command chain and status flow |
| P0 | `osmx/docs/plans/osmx-dual-repo-wave-board.md` | Current Wave 1 public status |
| P0 | `osmx/docs/plans/osmx-incident-commander-priority-delivery-plan.md` | Incident Commander priority delivery boundary |
| P0 | `osmx/docs/plans/mainline-merge-readiness.md` | Mainline merge baseline, with caveats below |
| P0 | `osmx/docs/plans/phase-f/phase-f-completion-gate.md` | Phase F closeout and Stage 1 entry context |
| P1 | `osmx/README.md`, `osmx/ROADMAP.md` | Main repo current product and roadmap summary |
| P1 | `osmx-emergency-main-sync/README.md`, `osmx-emergency-main-sync/ROADMAP.md` | Sync worktree current product and roadmap summary |
| P1 | `osmx-emergency-main-sync/docs/plans/osmx-emergency-alignment-with-osmx-priority-plan.md` | Emergency-side mapping to the main plan |

## 3. Current Baseline Conclusions

### 3.1 Source Of Truth

`osmx/docs/plans` remains the authoritative plan source.

The emergency worktree contains synchronized copies of the key plan documents, but if the two repositories diverge, `osmx` wins.

Confirmed identical between `osmx` and `osmx-emergency-main-sync`:

- `docs/plans/README.md`
- `docs/plans/osmx-stage1-dual-track-master-plan.md`
- `docs/plans/osmx-parallel-delivery-and-multi-agent-orchestration-plan.md`
- `docs/plans/osmx-parallel-multi-agent-prompts-and-wave1-task-pack.md`
- `docs/plans/osmx-dual-repo-agent-operator-runbook.md`
- `docs/plans/osmx-dual-repo-wave-board.md`
- `docs/plans/osmx-incident-commander-priority-delivery-plan.md`
- `docs/plans/mainline-merge-readiness.md`

### 3.2 Stage And Product Positioning

Current stage:

```text
Stage 1 = DB Copilot productization main track + Incident Commander early-availability parallel track
```

Important boundaries:

- `Incident Commander` is the current first-priority delivery workstream, not the first product shell.
- The long-term sequence remains `DB Copilot -> DC Copilot -> Full-Link Observer -> Incident Commander`.
- `Studio / OO / Asset Center` must serve the incident command chain. They should not become a separate priority that outruns `WP1 -> WP2/WP3`.

### 3.3 Repository Roles

| Repository | Current role | Write responsibility |
|------------|--------------|----------------------|
| `osmx` | Strategy mother repo, plan source, contract source | Stage plan, object contracts, mainline acceptance, final merge decision |
| `osmx-emergency-main-sync` | Emergency implementation and merge-prep worktree | Implementation, integration, smoke, regression evidence |
| `shared-specs` | Cross-repo collaboration layer | Agent rules, templates, prompts, contract indexes, baseline summaries |

### 3.4 Current Wave

Current official wave:

```text
Wave 1 - WP1 main-chain contract close + WP2/WP3 minimal smoke
```

Current status from the wave board:

- Mother task: done
- Subtask split: done
- Backend implementation: done
- Frontend implementation: done
- Implementation-repo validation: done
- Emergency summary package: done
- Main repo review: done
- PR review: done
- Final merge to `main`: done via PR #2

The current Wave 1 closure question is now answered:

```text
Has Wave 1 reached the main-repo acceptance gate and merged back to main?
```

The answer is yes. PR #2 was merged into `main` at `2026-04-21 22:35 CST` with merge commit `ae2be3b`. Docs-only closeout PR #3 updated the Wave board, PR #4 aligned the operator runbook state flow, PR #5 marked `shared-specs` as an independent evidence repository, PR #6 added the shared-specs governance guardrails, and PR #7 removed public credential/private-infra traces from the current tree. Current `origin/main` is `91c4f87`.

## 4. Architecture Assessment

The architecture direction is coherent if the following model is preserved:

```text
osmx = control plane, core contracts, platform abstractions, final product shell
osmx-emergency-main-sync = emergency scenario implementation and integration proof
shared-specs = collaboration contracts and agent operating layer
```

The highest-risk architecture drift would be:

1. Treating `osmx-emergency-main-sync` as a second long-term product truth source.
2. Letting `Studio / OO / Worker` expansion outrun `WP1 -> WP2/WP3`.
3. Letting sub-agents directly declare merge readiness without the emergency owner summary and main repo review.
4. Copying reusable core abstractions into the emergency worktree instead of adopting or requesting core extension points.

## 5. Shared Specs Recommendation

Do not move all of `osmx/docs` into `shared-specs`.

Use `shared-specs` for:

- reading-set index
- cross-repo dispatch rules
- prompt templates
- PR / MR review templates
- contract indexes
- current baseline summaries

Leave in `osmx/docs`:

- stage plans
- roadmap
- strategy documents
- architecture source documents
- merge readiness definitions
- phase gates
- document change log

## 6. Current Baseline State

Update on 2026-04-21 evening:

The active workspace is now `/Users/apple/Exec/Code`, not `/Users/apple/Exec/vscode_projects/osmx-suite`.

Confirmed workspace members:

```text
/Users/apple/Exec/Code/osmx
/Users/apple/Exec/Code/osmx-emergency
/Users/apple/Exec/Code/osmx-emergency-main-sync
/Users/apple/Exec/Code/shared-specs
```

Operational target for emergency-side Wave 1 work remains:

```text
/Users/apple/Exec/Code/osmx-emergency-main-sync
```

`/Users/apple/Exec/Code/osmx-emergency` is the older feature worktree root and should not receive new Wave 1 main-sync implementation changes unless explicitly requested.

The `osmx-emergency-main-sync` worktree Git pointer was repaired after the workspace move:

```text
osmx-emergency-main-sync/.git
gitdir: /Users/apple/Exec/Code/osmx-emergency/.git/worktrees/osmx-emergency-main-sync
```

Current worktree registration is valid:

```text
/Users/apple/Exec/Code/osmx-emergency            113f517 [feature/runbook-engine]
/Users/apple/Exec/Code/osmx-emergency-main-sync  5db87c3 [batch/full-integration]
```

The previous Git conflict blocker has been resolved.

Resolved file:

```text
osmx-emergency-main-sync/osmx-go/internal/runbook/extension.go
```

Resolution kept the audit-log route registration from the stashed side and removed the conflict markers.

Validation run after resolving the conflict:

```bash
gofmt -w osmx-go/internal/runbook/extension.go
go test -tags 'plan runbook' ./internal/runbook -run '^$' -count=0
go test -tags 'plan runbook' ./internal/runbook/handler -run '^$' -count=0
go test -tags 'plan runbook' ./cmd/server -run '^$' -count=0
go test -tags 'plan runbook' ./internal/plan/... ./internal/middleware ./internal/runbook/acceptance -count=1
npm run build
npm run build:check
git -C osmx-emergency-main-sync diff --name-only --diff-filter=U
```

Results:

- No unmerged files remain.
- `internal/runbook` compiled with no test files.
- `internal/runbook/handler` compiled with no tests run.
- `cmd/server` compiled under `plan runbook` tags.
- `internal/plan/...`, `internal/middleware`, and `internal/runbook/acceptance` passed.
- `npm run build` passed.
- `npm run build:check` failed in `vue-tsc` with existing TypeScript / dependency typing errors.
- Static route search found `/plans`, `/approvals`, and `/audit-logs` route surfaces in code.
- Runtime service probes, page-level Playwright smoke, and full merge-readiness review were not run in this pass.

Still observed:

- `osmx-emergency-main-sync` has many existing modified files from Wave 1 work.
- `osmx` has untracked docs/upload artifacts.
- `osmx-emergency-main-sync` is not a clean branch; it is now conflict-clean but still contains substantial Wave 1 edits.
- Frontend type-check remains a known blocker before main-repo acceptance.

Latest validation/fix pass:

```bash
npm run build:check
npm run build
go test -tags 'plan runbook' ./internal/plan/... ./internal/middleware ./internal/runbook/acceptance -count=1
go test -tags 'plan runbook' ./cmd/server -run '^$' -count=0
git diff --name-only --diff-filter=U
```

Results:

- No unmerged files remain.
- `npm run build` passed.
- `go test -tags 'plan runbook' ./internal/plan/... ./internal/middleware ./internal/runbook/acceptance -count=1` passed.
- `go test -tags 'plan runbook' ./cmd/server -run '^$' -count=0` passed.
- Static route search confirms `/plans`, `/approvals`, and `/audit-logs` surfaces exist in frontend routes/API and backend route registration.
- A focused frontend type pass fixed Wave 1/runbook-facing `vue-tsc` errors in `PlanListView`, `ExecutionListView`, `FlowDesignerView`, `ImportedOperationView`, `RunbookListView`, `WorkerListView`, and related runbook type/property-panel files.
- `npm run build:check` still fails, but the remaining failures are now outside the Wave 1 main-chain files and cluster in older collectors, skill store, AI SQL optimize, database/license/system/task/topology views, `src/utils/flow-yaml.ts` missing `js-yaml` typing/dependency, and a Vite/Vitest/Rolldown plugin type mismatch.
- Runtime service probes and page-level Playwright smoke were still not run in this pass.

Follow-up build-check debt pass:

```bash
npm run build:check
go test -tags 'plan runbook' ./internal/plan/... ./internal/middleware ./internal/runbook/acceptance -count=1
go test -tags 'plan runbook' ./cmd/server -run '^$' -count=0
git diff --name-only --diff-filter=U
```

Results:

- `npm run build:check` passed. This includes `vue-tsc -b` and a production `vite build`.
- `go test -tags 'plan runbook' ./internal/plan/... ./internal/middleware ./internal/runbook/acceptance -count=1` passed.
- `go test -tags 'plan runbook' ./cmd/server -run '^$' -count=0` passed.
- No unmerged files remain.
- The remaining merge gate gap is runtime/page-level smoke, not static frontend or backend compilation.
- Build-check fixes were intentionally scoped to frontend type/API/dependency debt and did not expand the Wave 1 Plan -> Approval -> AssetExecution -> Artifact -> Audit behavior.

Runtime smoke and blocker-fix pass:

```bash
go run ./cmd/emergency -config configs/config.yaml
npm run dev -- --host 0.0.0.0
curl http://localhost:8080/health
curl -X POST http://localhost:8080/api/v1/auth/login
npm run build:check
go test -tags 'plan runbook' ./cmd/server -run '^$' -count=0
go test -tags 'plan runbook' ./cmd/emergency ./internal/runbook/engine ./internal/runbook/compiler/afl ./internal/runbook/service ./internal/runbook/handler ./internal/runbook/acceptance ./internal/plan/... -count=1
git diff --name-only --diff-filter=U
```

Runtime ports used:

```text
backend:  http://localhost:8080  via cmd/emergency with configs/config.yaml
frontend: http://localhost:15174 via Vite
```

Results:

- `/health`, `/api/v1/plans`, `/api/v1/approvals`, `/api/v1/audit-logs`, `/api/v1/approvals/stats`, and `/api/v1/audit-logs/stats` returned HTTP 200 after login.
- A live native runtime chain was created and completed:
  - plan: `37bdb9bd-07c4-41f8-aa38-b1ec4b343051`
  - approval: `3`
  - execution: `91804de3-b418-47c2-833b-427289a53b17`
  - final status: `COMPLETED`
  - engine execution ID: `26`
  - chain artifact count: `2`
  - execution audit total: `1`
  - backend health after execution: `200`
- Page-level Playwright smoke passed with no page errors and no HTTP 4xx/5xx for:
  - `/command-center/plans`
  - `/command-center/plans/37bdb9bd-07c4-41f8-aa38-b1ec4b343051`
  - `/approvals`
  - `/audit-logs`
  - `/runbook/executions`
- `cmd/emergency` now registers `GET /api/v1/runbook-executions/:uuid/audit`, matching the general runbook extension and removing the Command Center detail-page 404.
- Command Center plan detail now renders both execution artifacts and chain-view artifacts without assuming `format` / `artifact_type` / `status` are always present.
- `EventBus.Publish` now clones event payloads per handler to prevent concurrent map read/write panics between execution service and WebSocket consumers.
- MySQL execution-state startup now initializes the in-memory next ID from the persisted max `execution_id`, preventing post-restart duplicate `osm_execution_state.execution_id=1`.
- AFL operation compilation now sends empty/no-action operations from `__start__` to `__end__` instead of self-looping on `__start__.bindInputs`.

Remaining observations:

- Existing dirty worktree state remains substantial and should be preserved; no unrelated user changes were reverted.
- Older executions created before this pass remain in the database and some were marked crashed/failed on restart as expected.
- The implementation repo has now passed the runtime/page smoke required for the emergency-owner summary package, subject to the dirty-tree review and main-repo acceptance gate.

## 7. Next Execution Step

The emergency owner summary package has now been prepared:

```text
shared-specs/wave1-emergency-owner-summary-package.md
```

The main-repo evaluation has now also been prepared:

```text
shared-specs/wave1-main-repo-evaluation.md
```

The owner decision and merge-back plan has now been prepared:

```text
shared-specs/wave1-owner-decision-and-merge-back-plan.md
```

The merge-back execution branch has now been prepared and validated locally:

```text
/Users/apple/Exec/Code/osmx-main-merge
branch: wave1-merge-back-20260421
report: shared-specs/wave1-merge-back-execution-report.md
PR head commit: a14f425
pull request: https://github.com/Tattao/osmx/pull/2
closeout pull request: https://github.com/Tattao/osmx/pull/3
runbook state closeout pull request: https://github.com/Tattao/osmx/pull/4
shared-specs boundary pull request: https://github.com/Tattao/osmx/pull/5
shared-specs governance pull request: https://github.com/Tattao/osmx/pull/6
review report: shared-specs/wave1-pr2-review-report.md
merge commit: ae2be3b
docs closeout merge commit: fa34e47
runbook state closeout merge commit: 3bd018b
shared-specs boundary merge commit: 57534c9
P0 public credential cleanup merge commit: 91c4f87
```

Wave 1 status is now `merged_to_main`; PR #2 was reviewed, passed GitGuardian, and was merged into `main`. PR #3 closed the official Wave board status on `main`, PR #4 added `merged_to_main` to the operator runbook plus the post-Wave-1 development directory boundary, PR #5 updated `shared-specs` from a local record directory to an independent collaboration evidence repository, and PR #6 added the no-runtime-dependency guardrails for `shared-specs`.

The next task should be Wave 1 closeout / Wave 2 task-brief preparation, not immediate new feature expansion.

Recommended task:

```text
Wave 1 Closeout Agent:
Confirm current `main` is `91c4f87` and contains merge commits `ae2be3b` and `91c4f87`, archive the Wave 1/P0 evidence set, and prepare the next Wave 2 mother task brief from the canonical `osmx/docs/plans` scope.
```

Acceptance criteria:

1. `gh -R Tattao/osmx pr view 2 --json state,mergeCommit,mergedAt` reports `MERGED`.
2. `gh -R Tattao/osmx pr view 3 --json state,mergeCommit,mergedAt` reports `MERGED`.
3. `gh -R Tattao/osmx pr view 4 --json state,mergeCommit,mergedAt` reports `MERGED`.
4. `gh -R Tattao/osmx pr view 5 --json state,mergeCommit,mergedAt` reports `MERGED`.
5. `gh -R Tattao/osmx pr view 6 --json state,mergeCommit,mergedAt` reports `MERGED`.
6. `git ls-remote origin refs/heads/main` reports `91c4f8784ef7337602fb60560ccffc0e0ac56e46`.
7. The Wave board records Wave 1 as merged, not merely ready for merge.
8. The operator runbook includes `merged_to_main`, the post-Wave-1 development directory boundary, the `shared-specs` evidence-repo boundary, and the no-runtime-dependency guardrails.
9. Wave 2 remains scoped by a new owner task brief before implementation starts.
