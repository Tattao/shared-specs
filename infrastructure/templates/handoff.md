# Agent Handoff Template
# File: infrastructure/templates/handoff.md
# Used when a session needs to transfer context to the next session

# Agent Handoff: {SLOT} / {TASK_ID}

> Generated: {TIMESTAMP}
> Verdict: **{VERDICT}**

## Current State
- **Worktree**: `{WORKTREE}`
- **Branch**: `{BRANCH}`
- **CWD**: `{CURRENT_DIRECTORY}`
- **Task**: {TASK_ID} — {TASK_TITLE}
- **Progress**: {PERCENTAGE}%

## What Was Done
{SUMMARY_OF_COMPLETED_WORK}

## Changed Files
```
{GIT_DIFF_STAT}
```

## Validation Run
```
{TEST_OUTPUT}
```

## Key Decisions
{DECISIONS_MADE}

## Blocking Issues
{BLOCKERS}

## Next Step (Single Actionable Task)
{EXACTLY_ONE_NEXT_STEP}

## Files to Read First (Next Session)
1. `{PLAN_DOC}`
2. `{HANDOFF_FILE}`
3. `{SOURCE_CODE}`
