# PW1-WP0-SHELL-IA-001 Validation

## Commands

```bash
cd ../osmx/frontend && npm run build:check
git -C ../osmx diff --check -- frontend/src/router/index.ts frontend/src/components/layout/Sidebar.vue frontend/src/views/aof/AofSurfaceView.vue docs/plans/00-current-plan-index.md docs/plans/80-wave-execution-board.md docs/guides/document-change-log.md
git diff --check -- infrastructure/artifacts/PW1-WP0-SHELL-IA-001
```

## Result

All commands passed.

`npm run build:check` completed `vue-tsc -b` and `vite build`. Vite reported the repository's existing large chunk warnings, but the build succeeded.
