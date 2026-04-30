# Validation

Commands planned for this bootstrap:

```bash
git diff --check
ruby -e 'require "yaml"; %w[infrastructure/task-queue-v2.yaml infrastructure/agent-pool-v2.yaml infrastructure/quality-gates-v2.yaml].each { |p| YAML.load_file(p); puts "#{p}: ok" }'
rg -n "/Users/apple|PostgreSQL is a future candidate|--yolo|--dangerously-skip-permissions" infrastructure/*-v2.yaml infrastructure/autonomous-delivery-mvp.md README.md AGENTS.md infrastructure/README.md
```

Results:

- `git diff --check`: pass.
- YAML parse via Ruby `YAML.load_file`: pass for `task-queue-v2.yaml`, `agent-pool-v2.yaml`, and `quality-gates-v2.yaml`.
- Legacy string scan: expected historical hits remain in v1 README sections and as disallowed flags in `agent-pool-v2.yaml`; no `PostgreSQL is a future candidate` hit remains in v2 gate files.
