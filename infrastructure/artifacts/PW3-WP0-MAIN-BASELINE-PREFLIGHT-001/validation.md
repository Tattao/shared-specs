# PW3-WP0 Validation

Validation performed:

- `gh pr view 57 --json state,mergedAt,mergeCommit,url`
- `gh pr view 1 --json state,mergedAt,mergeCommit,url,isDraft,mergeStateStatus`
- `git fetch origin main`
- `git rev-parse --short HEAD`
- `git rev-parse --short origin/main`
- `git status --short`
- Backend restart on `http://127.0.0.1:18090`
- Frontend restart on `http://127.0.0.1:15190/`
- Authenticated API smoke against AOF runtime endpoints
- Frontend root smoke with `curl -fsS http://127.0.0.1:15190/`

Results:

- osmx PR #57: merged, merge commit `1d57f65f6be2bdc559e30ee649a706572531b4db`.
- shared-specs PR #1: merged, merge commit `5ba2a31119ff54c8362320659929d33b3798b5e0`.
- osmx local branch is based on `origin/main=1d57f65`.
- shared-specs local branch is based on `origin/main=5ba2a31`.
- Backend health returned `status=ok`.
- Frontend returned Vite HTML.
- AOF runtime endpoint smoke passed for eight read-only list endpoints.

Pending validation after artifact write:

- `git diff --check`
- `python3 infrastructure/runner-v2.py doctor --strict-artifacts`
