---
id: 03-contract
title: Architecture & contracts
duration: 14
status: draft
category: core
method_id: EC-M03
classification: proposed-principle
prerequisites:
- Git basics
- Reading a test result
artifacts:
- CONTRACT.md; transition table; executable Lab A example; action identity journal.
success_criteria:
- A valid request produces one action; a denied request produces none. The teaching
  model does not prove continuity of a real graphics engine.
references:
- python-unittest
---
# Architecture & contracts

> Status: methodological draft, to be adapted — not ratified in consuming projects.

## Separate responsibilities
A library exposes capabilities; a profile composes policies and behavior; a surface renders state; an authority layer decides whether an action can execute.

| Responsibility | Contract | Explicit non-goal |
|---|---|---|
| Geometry | typed transforms and rectangles | no content selection |
| Motion | continuity and interruption | no system action grant |
| Rendering | visible projection of state | no data provenance invention |
| Content | identity and state | no authorization |
| Events | order and causality | no authority amplification |
| Data providers | provenance, freshness, error | no mutation grant |
| Policy/actions | scoped capability checks | no theme decisions |

### Interface contract
Define inputs, outputs, errors, ownership, lifecycle, concurrency, cancellation, deprecation and `public/internal/experimental` status.

### Transition example
When a surface changes anchor mid-flight, define observed start, target state, interruption rules and geometry invariants. Smooth visuals do not prove correct responsibility boundaries.

### Exercise
An animated menu starts a process. Where is authority checked? What happens after denial?

<details><summary>Self-check</summary>Permission belongs at the execution boundary, not inside an easing function. The UI may reflect an explicit denied state without granting any authority.</details>


## Engineering problem
A fictional menu preserves state during interruption but may trigger the same action twice.

## Reproducible method
1. Name idle, moving, denied and done states
2. define request_id/target inputs
3. assign action ownership
4. specify duplicates and cancellation
5. write interruption, denial and restart oracles.

**Responsibilities:** the author proposes and records results; the reviewer challenges the oracle; the consuming project owner decides adoption.

## Example, counterexample and failure
Example: a restart changes target but preserves request_id. Counterexample: the renderer launches the action on every frame. Failure: retry gets a new identity and bypasses deduplication; define retry identity in the contract.

## Artifacts and qualification
CONTRACT.md; transition table; executable Lab A example; action identity journal.

A valid request produces one action; a denied request produces none. The teaching model does not prove continuity of a real graphics engine.

## Transfer exercise
Apply this method to fictional Courier. Produce the artifacts above, then invent a case that invalidates an overbroad conclusion.

<details><summary>Transfer self-check</summary>The case is fictional and reproducible; baseline is identified; procedure and expected result are explicit; a failure is retained; the conclusion cites artifacts and limits. If any criterion is missing, revise before declaring the method applied.</details>
