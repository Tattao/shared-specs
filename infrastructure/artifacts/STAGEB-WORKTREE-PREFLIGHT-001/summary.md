# STAGEB-WORKTREE-PREFLIGHT-001 Summary

Verdict: `pass_with_risk`

## Purpose

Add a Stage B preflight check for worktree, branch, and write-scope readiness before product-code tasks can be dispatched.

## What Changed

- Added `infrastructure/worktree-preflight-v2.py`.
- Added `infrastructure/remote-supervision-protocol.md`.
- Added Hermes WeChat and Claude Code dispatch briefs.
- Added `STAGEB-WORKTREE-PREFLIGHT-001` to `task-queue-v2.yaml`.

## Decision

Product-code tasks should not be dispatched until they pass strict preflight without `--allow-dirty` or `--allow-branch-mismatch`.

For already-running delivery-ops tasks, the preflight tool can run with explicit exceptions so the artifact records why it is not a clean pre-dispatch proof.

Hermes should receive the WeChat supervision brief. Claude Code should receive its worker/evaluator brief only when a concrete task is dispatched.
