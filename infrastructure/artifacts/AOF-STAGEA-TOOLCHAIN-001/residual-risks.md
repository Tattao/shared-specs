# Residual Risks

- Homebrew uses a user-local non-default prefix, so some binary bottles may be unavailable or require source builds.
- GitHub CLI is installed but not authenticated. Owner must run `gh auth login` before PR and CI automation can use it.
- Claude Code stdio MCP health check still fails for Playwright. Use Playwright CLI fallback or Hermes `playwright-min` until fixed.
- Hermes `playwright-min` was configured without the extra output-dir restriction because the minimal official `npx @playwright/mcp@latest` configuration is the one that connected successfully.

