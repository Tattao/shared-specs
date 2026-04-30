# OSMX Stage A Owner Decision Package

> Status: `owner decision draft`
> Date: `2026-04-30`
> Task: `AOF-STAGEA-DRYRUN-001`
> Queue: `osmx-autonomous-delivery-stage-a`
> Verdict: `pass_with_risk`

## 1. Owner Decision

Recommendation:

```text
Approve Stage A as completed.
Allow entry into Stage B preparation.
Do not enable unsupervised 24-hour product-code execution yet.
```

Reason:

- Stage A has completed more than the required 3 low-risk tasks.
- Each closed task has changed-file, validation, residual-risk, and handoff evidence.
- The queue, agent profiles, quality gates, runner, toolchain, NeatLogic governance, QA smoke inventory, and architecture boundary matrix are all present.
- No product code was modified by Stage A.
- No auto-merge or self-approval path was introduced.

The correct next state is therefore:

```text
Stage B-prep: supervised 24-hour continuous execution readiness
```

not yet:

```text
Stage C: full 7x24 autonomous product delivery
```

## 2. Stage A Evidence

Current queue result after this dry run:

| Result | Count |
|--------|-------|
| Closed tasks before dry-run closure | 10 |
| Ready tasks before dry-run closure | 0 after this task closes |
| Product-code writes | 0 |
| Auto-merge events | 0 |
| Human-gated tasks closed by external agent | 0 |

Completed task evidence:

| Task | Verdict | Evidence |
|------|---------|----------|
| `AOF-STAGEA-BOOTSTRAP-001` | closed | v2 MVP entrypoint and bootstrap artifacts |
| `AOF-STAGEA-GATE-001` | `pass_with_risk` | `quality-gates-v2.yaml`, gate summary, residual risks |
| `AOF-STAGEA-TASKMAP-001` | `pass` | WP0-WP13 Stage A task map |
| `AOF-WP13-BOUNDARY-001` | `pass_with_risk` | AOF core boundary matrix and architecture report |
| `AOF-WP12-QA-001` | `pass` | Stage A smoke inventory and test-case plan |
| `AOF-STAGEA-RUNNER-001` | `pass_with_risk` | supervised runner v2 |
| `AOF-STAGEA-RUNNER-SMOKE-001` | `pass` | real ready -> running -> closed runner lifecycle |
| `AOF-STAGEA-AGENT-ROLES-001` | `pass_with_risk` | controlled Codex / Claude Code / Hermes profiles |
| `AOF-STAGEA-TOOLCHAIN-001` | `pass_with_risk` | local toolchain install and MCP health evidence |
| `AOF-WP11-NEATLOGIC-001` | `pass_with_risk` | NeatLogic reuse governance index |

All closed task artifact directories contain:

- `changed-files.txt`
- `validation.md`
- `residual-risks.md`
- `handoff.md`

One task uses `gate-summary.md` instead of `summary.md`, and one uses `wp-task-map.md` as the domain-specific summary artifact. This is acceptable for Stage A, but Stage B should standardize on both `summary.md` and task-specific artifacts.

## 3. Gate Assessment

| Gate | Result | Notes |
|------|--------|-------|
| Source of truth | pass | `osmx/docs/plans` remains product fact source. |
| Shared-specs boundary | pass | `shared-specs` remains coordination ledger only. |
| Product-code isolation | pass | This dry run did not modify `osmx-go`, `frontend`, or `osmx-ai`. |
| No auto-merge | pass | Runner and profiles keep auto-merge forbidden. |
| No self-approval | pass | External agents cannot close human gates. |
| Human gate | pass_with_risk | This task used owner instruction as release-gate approval for evaluation package generation only. |
| Toolchain readiness | pass_with_risk | `gh`, Homebrew, Playwright, Claude MCP, and Hermes MCP are installed/healthy; stale MCP processes remain a known operational risk. |
| Runner readiness | pass_with_risk | Lifecycle works; active lease stale detection has a timestamp-format bug that must be fixed before unattended 24h runs. |
| Gate runner readiness | pass_with_risk | Gate policy exists, but some expectations still require manual interpretation. |
| NeatLogic reuse | pass_with_risk | Governance exists; source version and legal evidence pointers must be pinned before code movement. |
| QA readiness | pass_with_risk | Smoke inventory exists; automation and evidence folders are not populated yet. |

## 4. Stage B Entry Conditions

Stage B can start only as a supervised preparation wave until the following are done:

| Priority | Condition | Required Output |
|----------|-----------|-----------------|
| P0 | Fix runner timestamp parsing / stale lease false positive | `runner-v2.py` parses both ISO and Ruby YAML timestamp strings; doctor passes while a lease is active and valid |
| P0 | Add executable v2 gate runner | Gate results are written to task artifact directories |
| P0 | Add worktree / branch preflight | Product-code tasks must prove clean target worktree, branch, and write scope before dispatch |
| P0 | Sync owner decision to `osmx` docs | Accepted Stage A outcome lands in current `osmx` planning board / change log |
| P0 | Owner approves first product-code wave | Explicit owner decision for Stage B product-code task activation |
| P1 | Standardize task summary artifacts | Every closed task has `summary.md` plus task-specific artifact |
| P1 | Add smoke automation scaffold | WP12 smoke plan begins producing repeatable evidence |

## 5. Recommended Stage B Wave 0

Run this as a short guarded wave before enabling product-code implementation:

| Task | Profile | Scope |
|------|---------|-------|
| `STAGEB-RUNNER-TIME-001` | `codex-docs-ops` | Fix active lease timestamp parsing and add regression validation |
| `STAGEB-GATE-RUNNER-001` | `codex-docs-ops` | Convert v2 quality-gate policies into executable checks with artifact output |
| `STAGEB-WORKTREE-PREFLIGHT-001` | `codex-docs-ops` | Add clean worktree, branch, and write-scope preflight checklist |
| `STAGEB-BOARD-SYNC-001` | `codex-docs-ops` | Sync Stage A decision back to current `osmx` docs and change log |
| `STAGEB-SMOKE-AUTOMATION-001` | `codex-evaluation` | Create first repeatable smoke evidence scaffold for WP12 |
| `NEATLOGIC-SOURCE-001` | `claude-code-readonly-evaluator` | Read-only inventory of the approved NeatLogic branch/tag/commit after owner pins version |

Only after Wave 0 passes should Stage B enable the first product-code implementation wave.

## 6. Recommended First Product-Code Wave

The first product-code wave should be small, contract-led, and easy to evaluate:

| Work Package | First Slice | Why |
|--------------|-------------|-----|
| WP1 Core Contracts | Unified event/object/audit contract stubs | Prevents modules from growing independently. |
| WP0 Product Shell | 10 product-surface navigation skeleton behind feature gates | Makes the complete product visible without deep implementation risk. |
| WP2 Operational Twin | CI type/entity/relation API skeleton | Establishes CMDB as operational twin, not asset table. |
| WP3 Observability Fabric | Telemetry source registry skeleton | Makes full-stack monitoring first-class. |
| WP4 AlertOps | Normalized alert schema and adapter skeleton | Connects telemetry to incident flow. |
| WP7 AgentOps | AgentOpsTrace schema / UI placeholder | Makes AI activity governed from day one. |

Do not start NeatLogic code movement in this wave. Start with read-only inventory and mapping only.

## 7. External Agent Decision

Current decision:

```text
Codex remains the controller.
Claude Code may be a scoped worker or read-only evaluator.
Hermes may be a read-only supervisor or wave summarizer.
Neither Claude Code nor Hermes may close human gates, auto-merge, or become the product source of truth.
```

Recommended Stage B use:

- Claude Code: use first as `claude-code-readonly-evaluator` for NeatLogic source inventory or independent architecture review.
- Hermes: use first as `hermes-readonly-supervisor` for stale leases, missing artifacts, and wave summaries.
- Codex: keeps runner ownership, queue mutation, task closure, and owner-facing decision package generation.

## 8. Known Residual Risks

- Active lease stale detection currently has a timestamp-format issue caused by YAML parsing through Ruby; fix before unattended 24h operation.
- `quality-gates-v2.yaml` is still partly policy text, not a fully executable gate runner.
- `osmx` has broad local strategy-document changes; product-doc sync should be grouped intentionally.
- WP12 smoke plans are documented but not automated.
- NeatLogic source version is not pinned for code movement; legal/commercial evidence should remain in private legal storage.
- No Stage A task built or tested product code; Stage B product-code waves must start small and independently evaluated.

## 9. Decision Options

| Option | Decision | Consequence |
|--------|----------|-------------|
| Recommended | Approve Stage A and start Stage B Wave 0 | Safest path toward 24h continuous execution. |
| Conservative | Hold Stage B until runner timestamp and gate runner are fixed | Lower operational risk, slower progress. |
| Aggressive | Enable product-code Stage B immediately | Not recommended; runner/gate automation is not mature enough. |

Owner recommendation:

```text
Choose the recommended option.
Close Stage A.
Run Stage B Wave 0 next.
Then approve a small product-code wave.
```
