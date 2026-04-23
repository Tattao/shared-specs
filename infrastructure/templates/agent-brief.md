# Agent Brief Template
# This is the prompt sent to Codex or Claude Code
# File: infrastructure/templates/agent-brief.md

## Dispatch: {TASK_ID} → {SLOT}

### Context
You are Agent {TASK_ID} working on OSMX Stage 1.
Your worktree: `{WORKTREE}`
Your branch: `{BRANCH}`

### Rules
1. ONLY write inside your assigned worktree and write scope
2. Do NOT touch: {FORBIDDEN_SCOPE}
3. Do NOT start new features outside the brief
4. Do NOT add shared-specs as a dependency
5. Every DB-sensitive change must include PostgreSQL adaptation evidence

### Task
{TASK_BRIEF}

### Validation
After completing the task, run:
```bash
{VALIDATION_COMMANDS}
```

### Output Required
1. List of changed files
2. Validation results (pass/fail)
3. Any blockers or residual risks
4. If context is getting long, write a handoff to:
   `{WORKTREE}/docs/agent-handoff-YYYYMMDD.md`

### Database Guardrail
- MySQL is the current control-plane database
- PostgreSQL is a future candidate, not a runtime dependency
- No primary DB migration, no dual writes, no TimescaleDB merge, no Qdrant replacement
- New DB-sensitive changes must be MySQL/PostgreSQL portable
