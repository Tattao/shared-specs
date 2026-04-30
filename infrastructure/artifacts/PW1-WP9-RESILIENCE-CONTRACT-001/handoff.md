# PW1-WP9-RESILIENCE-CONTRACT-001 Handoff

Status: `closed_pass`

## Operator Notes

- Use `resilience.Schema()` to inspect required experiment fields.
- Use `resilience.Validate()` to validate a candidate experiment plan before future Resilience Lab consumers render or submit it.

## Next Consumers

- `PW1-WP9-RESILIENCE-LAB-SHELL-001` can use this contract for experiment catalog, guardrail, evidence, and score placeholders.
- A future execution task must add approval and runtime controls before any production experiment can run.
