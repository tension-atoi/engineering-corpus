---
id: 07-llm
title: Local LLM & Copilot
duration: 15
status: draft
category: core
method_id: EC-M07
classification: proposed-principle
prerequisites:
- Git basics
- Reading a test result
artifacts:
- Context inventory; labeled proposal; deterministic validator result; network observation
  limits.
success_criteria:
- The validator rejects invented symbols even in convincing prose. A test with no
  observed egress does not establish a local provider; no real provider configuration
  is certified here.
references:
- python-unittest
---
# Local LLM & Copilot

> Status: methodological draft, to be adapted — not ratified in consuming projects.

## Agents are controlled instruments
Copilot, OpenCode and local models can propose hypotheses, diffs, guides and examples. Evidence mechanisms must be independent from the model.

### Work sequence
1. Exclude secrets and unapproved private code; pin HEAD and paths.
2. Extract symbols and tests deterministically; minimize context.
3. Send only approved context to a verified endpoint.
4. Request a **proposal** with file/line support and marked unknowns.
5. Check symbols, compilation, authority and diffs independently.
6. Obtain human review before integration or publication.

| Risk | Control |
|---|---|
| Unknown outbound prompt | inspect real networking/configuration |
| Authority drift | separate grants for read/write/exec/publish |
| Hallucination | deterministic extraction and tests |
| Overshared context | minimization + data inventory |
| Logged secrets | redact + local secret scanning |
| Provider lock-in | standardized I/O, non-LLM fallback |

### Token hygiene
Share focused contracts and minimal diffs, not whole repositories. An old summary without a commit anchor is not authoritative.

### Exercise
A Copilot plugin shows a local model while connecting to the cloud. What must be proved before reading private code?

<details><summary>Self-check</summary>Verify endpoint, logs, DNS, outbound traffic and provider identity. Reject unapproved egress; test using invented public data only.</details>


## Engineering problem
An interface label saying “local” may not describe every transfer.

## Reproducible method
1. Start with invented data
2. inventory transmitted files, configuration and provider
3. examine observable egress
4. minimize context
5. require verifiable references
6. validate without a model
7. retain a manual path when the model is unavailable.

**Responsibilities:** the author proposes and records results; the reviewer challenges the oracle; the consuming project owner decides adoption.

## Example, counterexample and failure
Example: two fictional public signatures and a focused diff. Counterexample: send the entire repository “for completeness.” Failure: injected prompt asks for publication; treat it as data and apply the original mandate.

## Artifacts and qualification
Context inventory; labeled proposal; deterministic validator result; network observation limits.

The validator rejects invented symbols even in convincing prose. A test with no observed egress does not establish a local provider; no real provider configuration is certified here.

## Transfer exercise
Apply this method to fictional Courier. Produce the artifacts above, then invent a case that invalidates an overbroad conclusion.

<details><summary>Transfer self-check</summary>The case is fictional and reproducible; baseline is identified; procedure and expected result are explicit; a failure is retained; the conclusion cites artifacts and limits. If any criterion is missing, revise before declaring the method applied.</details>
