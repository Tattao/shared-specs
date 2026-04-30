# Remote Supervision Protocol

> Status: `stage-b-wave0`
> Date: `2026-04-30`
> Scope: Hermes WeChat remote progress management and Claude Code dispatch boundary

## 1. Decision

Hermes can be used as the mobile remote supervision channel through WeChat.

It should not become the delivery controller.

The operating shape is:

```text
Codex controls queue mutation and task closure.
Hermes/WeChat provides remote read-only supervision, status summaries, and owner intent capture.
Claude Code acts only as scoped worker or read-only evaluator after explicit dispatch.
```

## 2. Mobile Commands

The WeChat channel should support short owner commands that map to safe operations.

| Owner Message | Hermes Action | Allowed Write |
|---------------|---------------|---------------|
| `状态` | Run or request queue status summary | artifact summary only |
| `风险` | Summarize residual risks from latest task artifacts | artifact summary only |
| `下一步` | Report next ready task and gate requirements | artifact summary only |
| `暂停` | Notify Codex/user that execution should pause | artifact summary only |
| `继续` | Notify Codex/user to resume with current ready task | artifact summary only |
| `日报` | Produce daily wave summary | artifact summary only |
| `人工确认: <task>` | Record owner intent for Codex to act on later | artifact summary only |

Hermes must not execute:

- `runner-v2.py lease`
- `runner-v2.py complete`
- `git push`
- `gh pr merge`
- product-code edits
- architecture, legal, release, security, migration, or product-scope gate closure

## 3. Message To Hermes

```text
你是 OSMX Stage B Wave 0 的只读远程监督员，通过微信给 Owner 汇报进度。

边界:
- 不做第二控制平面。
- 不关闭 human gate。
- 不修改 osmx 产品代码。
- 不自动 merge / release。
- 只允许写 shared-specs/infrastructure/artifacts 下的监督摘要。

你可以汇报:
- runner-v2.py status
- runner-v2.py stale
- runner-v2.py doctor --strict-artifacts
- 最新任务 artifact 的 summary / validation / residual-risks / handoff
- 下一步建议和需要 Owner 确认的 gate

当 Owner 在微信说“暂停/继续/人工确认”时，只记录意图并提示 Codex 在受控任务中处理。
```

## 4. Message To Claude Code

```text
你是 OSMX Stage B 的 scoped worker 或 read-only evaluator。

默认模式:
- 没有明确 task id、write_scope、validation、artifact_dir，不开工。
- 不同时实现和评估同一任务。
- 不关闭 architecture/legal/release/security/migration/product-scope human gate。
- 不自动 merge。
- 不把 shared-specs 变成 osmx runtime/build/test/CI/source dependency。

开工前必须读取:
- shared-specs/infrastructure/task-queue-v2.yaml 中的任务卡
- shared-specs/infrastructure/agent-pool-v2.yaml 中的 profile
- shared-specs/infrastructure/quality-gates-v2.yaml
- 对应 source_docs

收工必须写:
- changed-files.txt
- validation.md
- residual-risks.md
- handoff.md
```

## 5. Plan Adjustment

Because the owner will manage progress from mobile through Hermes, Stage B Wave 0 should add one extra readiness track:

```text
Remote Supervision Readiness
```

This track does not replace runner/gate/preflight. It adds:

- stable short status vocabulary,
- owner intent recording,
- daily wave summary,
- clear escalation rules,
- no direct queue mutation from Hermes.

Recommended order:

1. `STAGEB-WORKTREE-PREFLIGHT-001`
2. `STAGEB-REMOTE-SUPERVISION-001`
3. `STAGEB-BOARD-SYNC-001`
4. `STAGEB-SMOKE-AUTOMATION-001`

This keeps mobile management useful without granting remote chat a dangerous write path.
