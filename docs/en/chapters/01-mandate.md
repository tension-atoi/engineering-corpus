---
id: 01-mandate
title: "Mandate & slicing"
duration: 12
status: draft
category: core
---
# Mandate & slicing

> Status: methodological draft, to be adapted — not ratified in consuming projects.

## Why mandates matter
A request is not permission. A mandate binds a goal to a versioned baseline, narrow capabilities, and observable closure criteria.

| Dimension | Required question | Evidence |
|---|---|---|
| Baseline | Which repo, commit and worktree? | Fingerprint + `git status` |
| Scope | Which paths may change? | Allowed paths and exclusions |
| Authority | Who may read, write, execute or publish? | Explicit scoped grant |
| Gate | What means success or failure? | RED/GREEN checks |
| Output | What can be delivered? | Patch, evidence, docs, decision |

### Work units
A **program** contains workstreams; a **workstream** contains causal slices; each **slice** has one verifiable objective. A task list is not evidence of completion.

### Entrance gate
Begin only once dangerous unknowns are declared. Hypotheses are allowed but must be labeled.

### Exercise
Draft `MANDATE.md` for a fictional notification sorter without touching storage. Name three forbidden actions.

<details><summary>Self-check</summary>Include baseline commit, file scope, explicit prohibitions, deterministic test, stop condition and inspectable output. Deployment is not implied.</details>
