# Wave 2 Mother Task Brief Dispatch

> Date: 2026-04-22
> Scope: collaboration evidence only. Final product/source truth remains `osmx`.

## OSMX Mainline State

- Repository: `Tattao/osmx`
- Current `origin/main`: `40d0a73`
- Wave 2 brief PR: `https://github.com/Tattao/osmx/pull/8`
- Wave 2 brief merge commit: `f7402ed`
- Wave 2 clean worktree note PR: `https://github.com/Tattao/osmx/pull/9`
- Wave 2 clean worktree note merge commit: `40d0a73`
- P0 cleanup PR: `https://github.com/Tattao/osmx/pull/7`
- P0 cleanup merge commit: `91c4f87`

## Canonical Wave 2 Brief

The canonical mother task brief is now in `osmx`:

```text
docs/plans/wave-2-command-center-governed-loop.md
```

K1 should treat this as the execution contract for Wave 2.

The clean local Wave 2 implementation worktree has been prepared at:

```text
/Users/apple/Exec/Code/osmx-emergency-main-sync-wave2
```

It is a worktree of `osmx-emergency-main-sync`, currently on branch `wave2/command-center-governed-loop`, tracking `github/main`.

## Execution Boundary

Wave 2 is fixed to:

```text
Command Center Governed Loop Hardening
Plan -> Approval -> AssetExecution -> Artifact -> Audit -> Command Center Timeline
```

Allowed work:

- state machine and invariants
- denied / failed / cancelled / timed_out paths
- idempotency key support
- artifact provenance
- audit event schema alignment
- backend timeline projection
- minimal Command Center chain explanation
- happy / denied / failed / idempotent / restart validation

Forbidden expansion:

- no Studio scope expansion
- no OO / Content Pack deep compatibility expansion
- no Worker platform expansion
- no Hermes second frontend
- no generic workflow builder
- no shared-specs runtime/build/test/CI dependency

## K1 Start Condition

K1 may start Wave 2 preparation after:

- local implementation worktree is clean or a fresh Wave 2 worktree is created
- `osmx-emergency-main-sync` has fetched current `origin/main`
- the working baseline includes `40d0a73` or a later main commit containing the Wave 2 brief and clean-worktree note
- operator confirms external credential rotation/revocation status for the P0 exposure

## First K1 Action

Do not start broad feature work first.

First action should be:

```text
Split docs/plans/wave-2-command-center-governed-loop.md into backend, frontend, and evaluation subtasks, then confirm the branch/worktree baseline.
```
