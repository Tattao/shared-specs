# PW1-WP8-SKILL-CONTRACT-001 Handoff

Status: `closed_pass`

## Operator Notes

- Use `runbook/model.DefaultActionSkillContract()` to inspect the governed ActionSkill contract.
- Use `plan.ValidateActionSkillChain()` to validate a candidate chain before future Skill Fabric consumers display or execute it.
- The old compatibility output remains available for Studio / OO exports; the AOF governed chain is additive.

## Next Consumers

- `PW1-WP8-SKILL-REGISTRY-UI-001` can use this contract to render risk, scope, version, and validation status.
- A future backend API task can expose the contract over the AOF guarded route surface if needed.
