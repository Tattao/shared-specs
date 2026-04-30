# Validation

Commands:

```bash
command -v brew
brew --version
brew doctor
command -v gh
gh --version
gh auth status
command -v playwright
playwright --version
command -v playwright-mcp
npm list -g --depth=0 @playwright/mcp playwright
claude mcp get playwright
hermes mcp list
python3 infrastructure/runner-v2.py doctor --strict-artifacts
```

Actual result on 2026-04-30:

- `brew` is available at `/Users/shitao/.local/bin/brew`; Homebrew is installed at `/Users/shitao/.homebrew`.
- `brew doctor` reports the expected non-default prefix warning.
- `gh` is available at `/Users/shitao/.local/bin/gh`, version `2.92.0`.
- `gh auth status` reports login to GitHub account `Tattao` with `repo` and `workflow` scopes.
- `playwright` is available, version `1.59.1`.
- `playwright-mcp` is available; `@playwright/mcp@0.0.71` is installed globally.
- Claude Code user MCP `playwright` now reports `Status: Connected` in `claude mcp get playwright`.
- `claude mcp list` reports all configured MCP servers connected, including `playwright`.
- Hermes MCP `playwright-min` is enabled and reports 22 browser tools.
- `python3 infrastructure/runner-v2.py doctor --strict-artifacts` passed before this artifact was created.

Follow-up retest:

- A strict temporary Claude runtime MCP test logged `MCP server "playwright": Successfully connected`.
- After clearing stale `playwright-mcp` processes, the user-scope Claude MCP health check also recovered.

Current retest on `2026-04-30`:

- `command -v brew` resolves to `/Users/shitao/.homebrew/bin/brew`.
- `/Users/shitao/.local/bin/brew` exists as a symlink to `/Users/shitao/.homebrew/bin/brew`.
- `brew --version` reports `Homebrew >=4.3.0`.
- `command -v gh` resolves to `/Users/shitao/.local/bin/gh`.
- `gh --version` reports `gh version 2.92.0 (2026-04-28)`.
- `gh auth status` reports login to GitHub account `Tattao`; token value is intentionally not recorded.
- `command -v playwright` resolves to `/Users/shitao/.local/nodejs/current/bin/playwright`.
- `playwright --version` reports `Version 1.59.1`.
- `command -v playwright-mcp` resolves to `/Users/shitao/.local/nodejs/current/bin/playwright-mcp`.
- `npm list -g --depth=0 @playwright/mcp playwright` reports `@playwright/mcp@0.0.71` and `playwright@1.59.1`.
- `claude mcp get playwright` reports user-scope `playwright` MCP as `Status: Connected`, command `npx -y @playwright/mcp@latest`.
- `hermes mcp list` reports `playwright-min` over `npx @playwright/mcp@latest` as enabled.
