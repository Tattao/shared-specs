
# OSMX Suite Workspace Rules

## Workspace Members

- osmx: core platform repository
- osmx-emergency-main-sync: emergency scenario repository / synced integration worktree
- shared-specs: independent collaboration evidence repository for architecture decisions, contracts, task breakdowns, reviews, and handoffs

## Global Principles

1. Keep repositories independent.
2. Keep dependency direction one-way: emergency depends on core.
3. Put reusable capabilities in osmx.
4. Put scenario-specific emergency logic in osmx-emergency-main-sync.
5. Do not mix short-term convenience with long-term architecture.
6. Always explain file and repository boundaries before large changes.
7. Treat shared-specs as a non-source repository: do not add business code, secrets, runtime data, or generated artifacts.
8. Treat `osmx` as the final product source of truth. If shared-specs conflicts with `osmx`, `osmx` wins.
9. Do not make `osmx` build, test, CI, runtime, or source code depend on the current shared-specs HEAD.
10. For new autonomous delivery work, use the v2 MVP entrypoints under `infrastructure/`: `autonomous-delivery-mvp.md`, `task-queue-v2.yaml`, `agent-pool-v2.yaml`, and `quality-gates-v2.yaml`.
11. New execution lanes default to Codex-first guarded autonomy. Legacy Hermes / Claude Code mixed orchestration is historical unless a newer `osmx/docs/plans` fact source explicitly re-enables it.
12. Use environment variables such as `OSMX_WORKSPACE_ROOT`, `OSMX_REPO`, `SHARED_SPECS_REPO`, and `OSMX_ARTIFACT_ROOT`; do not introduce new hardcoded local workspace paths.

## Agent Dispatch Policy

- Architecture / boundary analysis -> may read all repositories
- Core implementation -> modify `osmx` only
- Emergency implementation -> modify `osmx-emergency-main-sync` only
- Collaboration evidence / templates / handoffs -> modify `shared-specs` only
- Test / review agents -> may read all, but must state target repository clearly
- Evaluation agents must not self-approve their own implementation work.
- Stage A autonomous delivery tasks must not auto-merge.

## Shared Specs Adoption Rule

Drafts in `shared-specs` become product truth only after their accepted behavior lands in `osmx` as code, tests, docs, runbook updates, or PR review evidence.

## Mandatory Output for Cross-Repo Tasks

For any cross-repo task, output must include:

- what belongs in core
- what belongs in emergency
- dependency direction
- migration or adoption notes
- test impact
