# Residual Risks

- Homebrew uses a user-local non-default prefix, so some binary bottles may be unavailable or require source builds.
- GitHub CLI is authenticated, but PR / CI automation must still respect queue ownership, human gates, and no-auto-merge policy.
- Claude Code Playwright MCP is now healthy, but stale `playwright-mcp` processes can confuse future health checks; clear stale processes before retesting if failures reappear.
- Hermes `playwright-min` was configured without the extra output-dir restriction because the minimal official `npx @playwright/mcp@latest` configuration is the one that connected successfully.
