# Legal Scope Summary

Task: `AOF-WP11-NEATLOGIC-001`
Verdict: `pass_with_risk`

## Owner Confirmation

The owner previously confirmed:

- NeatLogic authorization has been purchased.
- Legal and commercial authorization have been confirmed.
- Code reuse is allowed within the confirmed authorization scope.

## Governance Decision

Reuse is allowed only through governed lanes:

- product reference,
- data model reference,
- `neatlogic-compat`,
- `neatlogic-importer`,
- `neatlogic-adapter`,
- optional enterprise module,
- offline migration tooling.

OSMX core contracts remain autonomous. NeatLogic schema or runtime must not redefine `CIEntity`, `Ticket`, `ChangeRequest`, `Incident`, `ActionSkill`, `AssetExecution`, or `AgentOpsTrace`.

## Source Reference

Repository: `https://gitee.com/neat-logic/neatlogic-itom-all.git`

Remote HEAD checked on `2026-04-30`:

```text
8de339b2ce3a8c93b8162f581e5dc060e64aa421
```

Code movement must pin an approved branch, tag, or commit before copying files.
