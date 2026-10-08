---
id: 07-llm
title: "Local LLM & Copilot"
duration: 15
status: draft
category: core
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
