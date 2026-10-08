---
id: lab-api
title: Lab B — Verified API
duration: 25
status: draft
category: lab
method_id: EC-L02
classification: recommendation
prerequisites:
- Python 3.10+
- Chapters 01–06
artifacts:
- RED/GREEN logs
- Scoped conclusion
success_criteria:
- Expected failure for the negative case; exit 0 for the positive case
references:
- python-unittest
---
# Lab B — Publish an API without hallucinating

**Fictional scenario:** an agent writes an SDK page from a fictional library.

1. Pin commit and extract public exports with rustdoc/API tooling.
2. Classify each interface: `public-stable`, `public-experimental`, `internal`.
3. Generate a draft guide with an isolated local LLM.
4. Compile minimal code in `examples/` and verify used symbols.
5. Link each claim to a fitting E1/E2/other evidence record.
6. Produce FR and EN with reciprocal links and release notes.

<details><summary>Success criteria</summary>No invented symbols, no implicit cloud egress, examples compile, classification/limits are public, and human review is recorded.</details>

## Reproducible trial
From repository root, without installation or a model:

```bash
python3 examples/api_lab.py --symbol Queue.morph_to
# expected exit 1
python3 examples/api_lab.py
# expected exit 0
python3 scripts/test_labs.py
```

[Download the fixture](/examples/api_lab.py)

## Observation and exercise
The negative case asks for Queue.morph_to, absent from the AST inventory; the positive case uses Queue.enqueue and checks its output. Add a fictional export and example, then an unknown signature. The Python fixture lowers prerequisites; transfer to Rust needs separate pinned-toolchain evidence. A model is optional: write the guide from the inventory if no authorized model is available.

## Evidence and limits
Retain commands, output, exit codes and HEAD. RED must fail on the duplicate or unknown symbol, never a broken environment. Fixtures execute no system action or graphics engine and certify no external API.
