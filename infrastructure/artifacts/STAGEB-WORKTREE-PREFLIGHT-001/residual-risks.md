# Residual Risks

- Strict clean-worktree preflight should be run before future product-code tasks, not after a task has already modified files.
- This task used explicit exception flags because it is itself a running delivery-ops task in the shared-specs worktree.
- Hermes WeChat remote management still needs concrete local configuration outside this repository if credentials or connector settings are required.
- Claude Code should remain task-scoped and should not receive broad standing permission to work across the repo.
- Product-code Stage B execution still needs owner approval after board sync and smoke automation.
