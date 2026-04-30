# STAGEB-PRODUCT-TASKGRAPH-001 Residual Risks

- The task graph is an execution plan, not approval to start product-code work.
- Product-code execution still requires `STAGEB-PRODUCT-WAVE1-OWNER-GATE-001` Owner approval.
- Several Wave 1 tasks are DB-sensitive and must run migration pair and portability checks.
- Frontend and backend tasks must not execute in the same files concurrently without integration ownership.
- This task did not validate product runtime behavior.
