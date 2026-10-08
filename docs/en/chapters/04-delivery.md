---
id: 04-delivery
title: "Delivery & verification"
duration: 12
status: draft
category: core
---
# Delivery & verification

> Status: methodological draft, to be adapted — not ratified in consuming projects.

## RED → GREEN → evidence
A slice begins with an oracle failing for the expected reason, implements the smallest change, then records results. `GREEN` without environment control is insufficient.

```mermaid
flowchart LR
  A[Baseline] --> R[Causal red test]
  R --> I[Smallest change]
  I --> G[Passing tests]
  G --> P[Evidence + comparison]
  P --> C{Review gate}
  C -->|fail| R
  C -->|pass| D[Docs and closure]
```

| Gate | Minimum observation |
|---|---|
| Preflight | Git status, tool versions |
| Causality | expected initial failure |
| Fix | targeted tests pass |
| Non-regression | adjacent tests + lint |
| Quality | diff check + security |
| Closure | commit, limits, proof |

### Isolation
One worktree or sandbox per independent slice. Never treat `main` as a testbench or remote CI as the only reproducibility evidence.

### Exercise
Write a gate that rejects an unexpected change in event count. Why is count alone inadequate?

<details><summary>Self-check</summary>Also check sorted identities or inventory digest; any exception needs causal evidence.</details>
