---
id: lab-change
title: Lab A — Qualified change
duration: 25
status: draft
category: lab
method_id: EC-L01
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

## Reproducible trial
From repository root, without installation or a model:

```bash
python3 examples/change_lab.py --broken
# expected exit 1
python3 examples/change_lab.py
# expected exit 0
python3 scripts/test_labs.py
```

[Download the fixture](/examples/change_lab.py)

## Observation and exercise
The faulty case repeats r1 after interruption; the corrected case deduplicates r1 and denies r2. Change targets and add an independent identity: predict the action list before running.

## Evidence and limits
Retain commands, output, exit codes and HEAD. RED must fail on the duplicate or unknown symbol, never a broken environment. Fixtures execute no system action or graphics engine and certify no external API.
