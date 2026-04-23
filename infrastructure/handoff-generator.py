#!/usr/bin/env python3
"""
OSMX 24x7 Handoff Generator — creates session handoff documents
Usage: python3 handoff-generator.py --slot <slot> --verdict <pass|fail|blocked>
Part of: OSMX 24x7 Infrastructure
"""

import argparse
import subprocess
import sys
import yaml
from datetime import datetime, timezone
from pathlib import Path

INFRA_DIR = Path(__file__).parent
TASK_QUEUE = INFRA_DIR / "task-queue.yaml"
SLOTS_DIR = INFRA_DIR / "slots"

def run_cmd(cmd, timeout=30):
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return r.returncode, r.stdout.strip(), r.stderr.strip()
    except subprocess.TimeoutExpired:
        return -1, '', 'TIMEOUT'

def get_slot_state(slot_name):
    state_file = SLOTS_DIR / f"{slot_name}.state"
    if not state_file.exists():
        return {}
    state = {}
    for line in state_file.read_text().strip().splitlines():
        if '=' in line:
            k, v = line.split('=', 1)
            state[k] = v
    return state

def get_task_info(task_id):
    queue_file = INFRA_DIR / "task-queue.yaml"
    if not queue_file.exists():
        return {}
    with open(queue_file) as f:
        queue = yaml.safe_load(f)
    for t in queue.get('tasks', []):
        if t['id'] == task_id:
            return t
    return {}

def generate_handoff(slot_name, verdict, notes="", changed_files=""):
    state = get_slot_state(slot_name)
    task_id = state.get('task_id', 'unknown')
    worktree = state.get('worktree', 'unknown')
    branch = state.get('branch', 'unknown')
    
    task = get_task_info(task_id)
    
    # Collect git diff
    _, git_diff, _ = run_cmd(f"cd {worktree} && git diff --stat 2>/dev/null")
    _, git_staged, _ = run_cmd(f"cd {worktree} && git diff --cached --stat 2>/dev/null")
    _, git_log, _ = run_cmd(f"cd {worktree} && git log --oneline -5 2>/dev/null")
    
    # Collect test results if available
    _, go_test, _ = run_cmd(f"cd {worktree}/osmx-go && go test ./... 2>&1 | tail -10", timeout=120)
    _, fe_build, _ = run_cmd(f"cd {worktree}/frontend && npm run build:check 2>&1 | tail -5", timeout=120)
    
    timestamp = datetime.now().strftime('%Y%m%d-%H%M')
    handoff_file = Path(worktree) / "docs" / f"agent-handoff-{datetime.now().strftime('%Y%m%d')}.md"
    handoff_file.parent.mkdir(parents=True, exist_ok=True)
    
    content = f"""# Agent Handoff: {slot_name} / {task_id}

> Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC
> Verdict: **{verdict}**

## Context

| Field | Value |
|-------|-------|
| Slot | {slot_name} |
| Task | {task_id} — {task.get('title', 'unknown')} |
| Worktree | {worktree} |
| Branch | {branch} |
| Started | {state.get('started_at', 'unknown')} |

## What Was Done

{notes if notes else "See git diff below."}

## Changed Files

### Unstaged
```
{git_diff if git_diff else "none"}
```

### Staged
```
{git_staged if git_staged else "none"}
```

{f"### Explicit List\n```\n{changed_files}\n```" if changed_files else ""}

## Recent Commits

```
{git_log if git_log else "none"}
```

## Validation Results

### Go Tests
```
{go_test if go_test else "not run"}
```

### Frontend Build
```
{fe_build if fe_build else "not run"}
```

## Next Steps

- [ ] Review changes in {worktree}
- [ ] Run full validation: `make integration-efficiency-gate`
- [ ] Create PR if verdict is pass
- [ ] Update task-queue.yaml status

## Blocking Issues

<!-- List any blockers here -->

## Key Decisions

<!-- List any non-obvious decisions made during execution -->
"""
    
    handoff_file.write_text(content)
    print(f"Handoff written to: {handoff_file}")
    return str(handoff_file)

def main():
    parser = argparse.ArgumentParser(description='OSMX Handoff Generator')
    parser.add_argument('--slot', required=True, help='Slot name (e.g. slot-1)')
    parser.add_argument('--verdict', required=True, choices=['pass', 'pass_with_risk', 'fail', 'blocked'])
    parser.add_argument('--notes', default='', help='Free-form notes on what was done')
    parser.add_argument('--changed-files', default='', help='Explicit list of changed files')
    args = parser.parse_args()
    
    generate_handoff(args.slot, args.verdict, args.notes, args.changed_files)

if __name__ == '__main__':
    main()
