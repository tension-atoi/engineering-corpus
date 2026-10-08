---
id: lab-change
title: "Lab A — Qualified change"
duration: 25
status: draft
category: lab
---
# Lab A — Qualify a code change

**Fictional scenario:** a UI component changes anchor during animation without losing state or triggering privileged actions.

| Step | Expected output |
|---|---|
| Mandate | Scope paths, HEAD, forbidden actions |
| Contract | Target, interruption, lifecycle and authority |
| Oracle | Failing test for interruption/restart |
| Implementation | Small patch in isolated worktree |
| Verification | Unit, integration, captures and diff |
| Publication | Separate behavioral proof from marketing |

### Trap
A smooth animation can hide a duplicate system action. Your oracle must isolate that causality.

<details><summary>Success criteria</summary>No production changes; explicit interruption contract; a test proving action uniqueness; dated evidence; demonstrable rollback.</details>
