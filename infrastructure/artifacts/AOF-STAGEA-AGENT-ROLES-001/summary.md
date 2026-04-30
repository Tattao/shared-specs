# AOF-STAGEA-AGENT-ROLES-001 Summary

Verdict: `pass_with_risk`

## Purpose

Make local Hermes and Claude Code usable in the OSMX 24x7 delivery system without letting either tool bypass Codex-first guarded autonomy.

## What Changed

- Added controlled Claude Code and Hermes profiles to `agent-pool-v2.yaml`.
- Added external-agent quality gates to `quality-gates-v2.yaml`.
- Added runner `doctor` and `stale` commands.
- Added artifact checks before successful task completion.
- Updated README and MVP docs with the Codex / Claude Code / Hermes division of labor.

## Decision

Codex remains the Stage A controller. Claude Code is a scoped worker or read-only evaluator. Hermes is a read-only supervisor or wave summarizer.

No external agent may close human gates, auto-merge, or make `shared-specs` a runtime/build/test/CI dependency of OSMX.

