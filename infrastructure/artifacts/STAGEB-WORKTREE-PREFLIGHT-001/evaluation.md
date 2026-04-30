# Evaluation: STAGEB-WORKTREE-PREFLIGHT-001

Verdict: `pass_with_risk`

## Scope Check

Allowed write scope:

- `infrastructure/worktree-preflight-v2.py`
- `infrastructure/remote-supervision-protocol.md`
- `infrastructure/briefs/hermes-wechat-stageb-supervision.md`
- `infrastructure/briefs/claude-code-stageb-worker-evaluator.md`
- `infrastructure/task-queue-v2.yaml`
- `infrastructure/artifacts/STAGEB-WORKTREE-PREFLIGHT-001/**`

Forbidden product-code scope was respected:

- `../osmx/osmx-go/**`
- `../osmx/frontend/**`
- `../osmx/osmx-ai/**`

## Key Results

- Preflight can load task metadata from `task-queue-v2.yaml`.
- It resolves environment-based worktree paths.
- It checks git worktree existence, branch match, clean state, write scope, forbidden scope, and human gate visibility.
- It writes Markdown and JSON evidence.
- It supports explicit exception flags for already-running tasks.

## Hermes / Claude Code Decision

Hermes should be given the WeChat supervision brief now, because the owner plans to manage progress from mobile.

Claude Code should not be given a broad standing instruction. It should receive the Claude brief only together with a specific task id, write scope, validation commands, and artifact directory.

## Plan Adjustment

Stage B Wave 0 should include a remote-supervision readiness slice before product-code execution:

1. runner timestamp stability,
2. executable gate runner,
3. worktree preflight,
4. Hermes WeChat remote supervision protocol,
5. OSMX board sync,
6. smoke automation scaffold.

## Residual Risk

This task produces the protocol and briefs, but it does not configure the actual Hermes WeChat channel. That should be done as a separate supervised task if configuration files or credentials are involved.
