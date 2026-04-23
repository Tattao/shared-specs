# Task Card Template
# Copy this template for each new task. Fill all fields.
# File: infrastructure/templates/task-card.md

## Task: {TASK_ID}

| Field | Value |
|-------|-------|
| **ID** | {TASK_ID} |
| **Lane** | {LANE} |
| **Title** | {TITLE} |
| **Priority** | P0 / P1 / P2 |
| **Agent Type** | codex / claude-code |
| **Status** | pending |
| **Assigned Slot** | — |

## Source
- Plan: `{PLAN_PATH}`
- Dependency: {DEPENDS_ON}
- Blocks: {BLOCKS}

## Worktree
- Path: `{WORKTREE_PATH}`
- Branch: `{BRANCH}`
- Base: `origin/main`

## Write Scope
```
{ALLOWED_FILE_PATTERNS}
```

## Task Brief
```
{FULL_TASK_BRIEF}
```

## Forbidden Scope
```
{WHAT_NOT_TO_TOUCH}
```

## Validation
```bash
{VALIDATION_COMMANDS}
```

## Acceptance Criteria
- [ ] {CRITERION_1}
- [ ] {CRITERION_2}
- [ ] Quality gate passed: `make integration-efficiency-gate`

## Completion Record
| Field | Value |
|-------|-------|
| Verdict | — |
| Changed Files | — |
| PR | — |
| Evidence | — |
| Residual Risks | — |
