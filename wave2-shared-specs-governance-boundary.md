# Wave 2 Shared Specs Governance Boundary

> Date: 2026-04-22
> Status: active governance note
> Source: Architect J revised boundary review

## 1. Revised Conclusion

`shared-specs` is a collaboration record / shared specification repository.

It is a git repository, but it is not the final source of truth for OSMX product code, architecture, or plans.

Final product truth remains in:

```text
/Users/apple/Exec/Code/osmx
```

If `shared-specs` conflicts with `osmx`, `osmx` wins.

## 2. Source-Of-Truth Layers

| Layer | Location | Role |
|-------|----------|------|
| Primary truth | `/Users/apple/Exec/Code/osmx` | Product architecture, final runbooks, final Wave board, acceptance criteria, code, schema, migrations, CI, tests, PR merge facts |
| Collaboration source | `https://github.com/Tattao/shared-specs` and `/Users/apple/Exec/Code/shared-specs` | Draft specs, cross-role records, task drafts, handoffs, review evidence |
| Emergency implementation | `/Users/apple/Exec/Code/osmx-emergency-main-sync` | Wave 2 emergency implementation worktree |
| Historical reference | `/Users/apple/Exec/Code/osmx-emergency` | Read-only historical reference, not Wave 2 development |
| Merge worktree | `/Users/apple/Exec/Code/osmx-main-merge` | Temporary PR / main merge worktree only |

Current Wave 2 branch baseline:

```text
osmx origin/main = 7dc19ef
```

## 3. Wave 2 Direction

Wave 2 remains focused on the Command Center / Incident Commander minimum auditable loop:

```text
Plan -> Approval -> AssetExecution -> Artifact -> Audit
```

`shared-specs` may hold drafts first, but anything adopted for the product must land in `osmx` as code, tests, docs, runbooks, or PR review evidence.

The following must not remain only in `shared-specs`:

- Plan / Approval / AssetExecution / Artifact / Audit state flow
- approval policy
- execution idempotency strategy
- audit event schema
- artifact provenance
- Command Center timeline query semantics
- Wave 2 acceptance criteria
- operator runbook updates

## 4. K1 Execution Rules

K1 may read `shared-specs` as collaboration input and draft context.

K1 must execute against the `osmx` source of truth and the Wave 2 implementation worktree:

```text
/Users/apple/Exec/Code/osmx
/Users/apple/Exec/Code/osmx-emergency-main-sync
```

Any design adopted from `shared-specs` must have a corresponding landing point in `osmx`:

- docs
- runbook
- tests
- code contract
- PR description

## 5. Forbidden Changes

K1 must not:

- make `shared-specs` the product final source of truth
- add `shared-specs` as an OSMX runtime dependency
- make OSMX build / test / CI depend on the current `shared-specs` HEAD
- add `shared-specs` as a git submodule
- import or read `shared-specs` from product code
- update only `shared-specs` for accepted state flows, API contracts, audit schemas, or acceptance criteria
- use `shared-specs` drafts to expand Studio / OO / Worker scope
- broaden Wave 2 beyond work directly serving `Plan -> Approval -> AssetExecution -> Artifact -> Audit`

## 6. Pre-Work Validation

Check `shared-specs`:

```bash
cd /Users/apple/Exec/Code

if [ -d shared-specs/.git ]; then
  echo "shared-specs repo exists"
  git -C shared-specs remote -v
  git -C shared-specs fetch origin --prune
  git -C shared-specs status --short
  git -C shared-specs log --oneline -5
else
  echo "shared-specs repo not found locally"
fi
```

Check Wave 2 does not accidentally depend on `shared-specs`:

```bash
cd /Users/apple/Exec/Code/osmx-emergency-main-sync

git diff --name-only origin/main...HEAD | tee /tmp/osmx_wave2_changed_files.txt
cat /tmp/osmx_wave2_changed_files.txt

grep -R "shared-specs" . \
  --exclude-dir=.git \
  --exclude-dir=node_modules \
  --exclude-dir=.next \
  --exclude-dir=dist \
  --exclude-dir=build || true
```

Allowed references:

- docs referencing `shared-specs`
- runbooks describing `shared-specs` as a collaboration source
- PR descriptions linking to `shared-specs` review records

Forbidden references:

- source code importing `shared-specs`
- tests requiring the current `shared-specs` HEAD
- build scripts cloning `shared-specs`
- CI requiring `shared-specs` access
- runtime config reading from `shared-specs`
