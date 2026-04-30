# STAGEB-RUNNER-TIME-001 Summary

Verdict: `pass`

## Purpose

Fix the active lease stale-detection false positive discovered during `AOF-STAGEA-DRYRUN-001`.

## What Changed

- Hardened `runner-v2.py` timestamp parsing.
- Added `STAGEB-RUNNER-TIME-001` to `task-queue-v2.yaml`.
- Advanced the queue state to `stage_b_wave0_preparation` / `stage_b_wave0_supervised`.

## Decision

`runner-v2.py` now accepts both:

- ISO timestamps written by the runner, such as `2026-04-30T13:31:31+08:00`.
- Ruby YAML timestamp strings read back from the queue, such as `2026-04-30 13:31:31 +0800`.

The active lease stale check no longer misclassifies a valid running task as stale.
