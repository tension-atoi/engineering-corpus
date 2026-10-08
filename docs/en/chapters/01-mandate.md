---
id: 01-mandate
title: Mandate & slicing
duration: 12
status: draft
category: core
method_id: EC-M01
classification: proposed-principle
prerequisites:
- Git basics
- Reading a test result
artifacts:
- MANDATE.md with baseline, grants, oracle, exclusions and expiry; before/after file
  inventory.
success_criteria:
- The diff touches only the sorter; the test checks order and stability; the owner
  explicitly accepts scope. A path inventory alone does not prove sorting quality.
references:
- git-worktree
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


## Engineering problem
A notification sort is requested, but “improve” defines neither outcome nor scope.

## Reproducible method
1. Pin HEAD and Git status
2. define input [urgent, normal, urgent], expected output and sorter paths
3. name the person who can accept the diff
4. stop if storage changes become necessary.

**Responsibilities:** the author proposes and records results; the reviewer challenges the oracle; the consuming project owner decides adoption.

## Example, counterexample and failure
Example: preserve the order of the two urgent items and leave storage untouched. Counterexample: “optimize the whole system.” Failure: a new requirement silently expands scope; obtain a recorded amendment.

## Artifacts and qualification
MANDATE.md with baseline, grants, oracle, exclusions and expiry; before/after file inventory.

The diff touches only the sorter; the test checks order and stability; the owner explicitly accepts scope. A path inventory alone does not prove sorting quality.

## Transfer exercise
Apply this method to fictional Courier. Produce the artifacts above, then invent a case that invalidates an overbroad conclusion.

<details><summary>Transfer self-check</summary>The case is fictional and reproducible; baseline is identified; procedure and expected result are explicit; a failure is retained; the conclusion cites artifacts and limits. If any criterion is missing, revise before declaring the method applied.</details>
