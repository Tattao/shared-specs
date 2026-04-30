# PW1-WP9-RESILIENCE-LAB-SHELL-001 Validation

- `cd ../osmx/frontend && npm run build:check`
- `cd ../osmx && git diff --check -- frontend/src/views/aof/AofSurfaceView.vue frontend/src/api/aof.ts frontend/src/types/aof.ts`

Both commands passed. Build emitted existing Vite chunk/dynamic import warnings only.
