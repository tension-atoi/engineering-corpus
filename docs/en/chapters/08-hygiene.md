---
id: 08-hygiene
title: "Hygiene, release & rollback"
duration: 15
status: draft
category: core
---
# Hygiene, release & rollback

> Status: methodological draft, to be adapted — not ratified in consuming projects.

## Hygiene is a continuous gate
Avoid saving all problems for a final cleanup. Use fast local controls, dependency inventory, migration traces and a known rollback procedure.

| Frequency | Gate | Evidence |
|---|---|---|
| every diff | format, lint, diff-check, secrets | output + exit status |
| every slice | targeted + adjacent tests | environment + commands |
| each milestone | invariants, API diff, docs | qualification report |
| monthly | licenses, dependencies, security | version inventory |
| pre-release | artifacts, sha256, rollback | approved gate |
| post-release | health, monitoring, reversibility | operations trace |

### Dependencies
Adopt only with rationale, license, provenance, pinned version, exit strategy and authority assessment (network, filesystem, process). Do not silently float critical dependencies.

### Separate release gate
`merge` is not `deploy`. A release needs an artifact, provenance, a human decision and a tested fallback.

### Exercise
A build is green but not reproducible. Is it deployable?

<details><summary>Self-check</summary>Block promotion, pin dependencies, compare a clean build and qualify a new artifact. Keep the last approved artifact for rollback.</details>
