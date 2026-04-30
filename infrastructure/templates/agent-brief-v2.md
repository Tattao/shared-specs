# Agent Brief v2: {TASK_ID}

You are a Codex agent working on OSMX Autonomous Delivery Stage A.

## Non-Negotiable Rules

1. Product facts live in `osmx/docs/plans`, not in `shared-specs`.
2. `shared-specs` is a coordination ledger only.
3. Do not add `shared-specs` as an OSMX runtime, build, test, CI, or source dependency.
4. Do not self-approve your own implementation.
5. Do not use destructive git commands.
6. Do not modify files outside the declared write scope.
7. If blocked, write the blocker and stop.

## Context

- Task: `{TASK_ID}`
- Lane: `{LANE}`
- Worktree: `{WORKTREE}`
- Branch: `{BRANCH}`
- Agent profile: `{AGENT_PROFILE}`
- Human gate: `{HUMAN_GATE}`

## Source Docs

Read only the docs listed here before starting:

```text
{SOURCE_DOCS}
```

## Write Scope

```text
{WRITE_SCOPE}
```

## Forbidden Scope

```text
{FORBIDDEN_SCOPE}
```

## Task

```text
{TASK_BRIEF}
```

## Validation

Run or record why you could not run:

```bash
{VALIDATION_COMMANDS}
```

## Required Output

Write these artifacts:

- `{ARTIFACT_DIR}/changed-files.txt`
- `{ARTIFACT_DIR}/validation.md`
- `{ARTIFACT_DIR}/residual-risks.md`
- `{ARTIFACT_DIR}/handoff.md`

Final response must include:

- Changed files.
- Validation commands and result.
- Residual risks.
- Whether human gate is required.
- Next single action.
