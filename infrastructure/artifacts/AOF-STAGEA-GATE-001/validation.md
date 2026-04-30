# Validation

Commands:

```bash
git diff --check
ruby -e 'require "yaml"; %w[infrastructure/task-queue-v2.yaml infrastructure/agent-pool-v2.yaml infrastructure/quality-gates-v2.yaml].each { |p| YAML.load_file(p); puts "#{p}: ok" }'
rg -n "PostgreSQL Primary Runtime, MySQL Compatibility Guardrails" infrastructure/quality-gates-v2.yaml
rg -n "shared-specs.*runtime|runtime.*shared-specs" infrastructure/quality-gates-v2.yaml
```

Expected result:

- Diff whitespace check passes.
- All v2 YAML files parse.
- DB strategy appears in v2 gates.
- No shared-specs runtime dependency policy is present as a forbidden gate.

Final command output is summarized in the Codex response for this run.
