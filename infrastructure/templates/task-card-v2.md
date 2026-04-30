# Task Card v2: {TASK_ID}

| Field | Value |
|-------|-------|
| ID | `{TASK_ID}` |
| Lane | `{LANE}` |
| Priority | `{PRIORITY}` |
| Status | `{STATUS}` |
| Agent Profile | `{AGENT_PROFILE}` |
| Human Gate | `{HUMAN_GATE}` |

## Source Docs

- `{SOURCE_DOC_1}`
- `{SOURCE_DOC_2}`

## Worktree

- Worktree: `{WORKTREE}`
- Branch: `{BRANCH}`
- Base: `origin/main`

## Write Scope

```text
{WRITE_SCOPE}
```

## Forbidden Scope

```text
{FORBIDDEN_SCOPE}
```

## Task Brief

```text
{TASK_BRIEF}
```

## Validation

```bash
{VALIDATION_COMMANDS}
```

## Required Artifacts

- `{ARTIFACT_DIR}/changed-files.txt`
- `{ARTIFACT_DIR}/validation.md`
- `{ARTIFACT_DIR}/residual-risks.md`
- `{ARTIFACT_DIR}/handoff.md`

## Acceptance Criteria

- [ ] Work stays inside declared write scope.
- [ ] `git diff --check` passes.
- [ ] Validation evidence is recorded.
- [ ] Residual risks are recorded.
- [ ] Evaluation owner is different from implementation owner.
- [ ] No runtime/build/test/CI/source dependency on `shared-specs` is introduced.
- [ ] Human gate is satisfied when required.

## Completion Record

| Field | Value |
|-------|-------|
| Verdict | `pass` / `pass_with_risk` / `fail` / `blocked` |
| Changed Files | |
| Validation | |
| Artifact Directory | |
| Residual Risks | |
| Next Single Action | |
