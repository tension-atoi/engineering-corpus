---
id: 03-contract
title: "Architecture & contracts"
duration: 14
status: draft
category: core
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
