# Residual Risks

- This is a minimal gate runner, not a full dispatcher.
- Some `quality-gates-v2.yaml` expectations are intentionally classified as `manual_review` when output needs human interpretation.
- Pre-dispatch worktree cleanliness can only be useful before a task starts; this task validates `post_task` and `scope` groups instead.
- Write-scope ownership and branch preflight still need `STAGEB-WORKTREE-PREFLIGHT-001`.
- Product-code Stage B execution should remain supervised until gate group selection and preflight are integrated into dispatch.
