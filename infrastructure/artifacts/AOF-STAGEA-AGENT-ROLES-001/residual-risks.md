# Residual Risks

- Hermes and Claude Code profiles are configured, but no daemon currently launches them automatically.
- `doctor` checks queue consistency and required artifacts; it does not execute product build, frontend, AI, or browser smoke commands.
- GitHub automation still needs a working `gh` CLI or GitHub MCP before PR and CI loops become fully automated.
- Enabling Claude Code as a Stage A implementation worker or Hermes as active orchestrator still requires a human gate and a scoped task.

