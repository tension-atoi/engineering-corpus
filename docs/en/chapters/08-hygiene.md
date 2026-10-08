---
id: 08-hygiene
title: Hygiene, release & rollback
duration: 15
status: draft
category: core
method_id: EC-M08
classification: proposed-principle
prerequisites:
- Git basics
- Reading a test result
artifacts:
- Git inventory; preserved-work hashes; ancestry log; previous and candidate artifacts;
  fallback result.
success_criteria:
- Lab C demonstrates byte preservation and divergence of two branches. It does not
  simulate every submodule, conflict, ignored file or hook in a real repository.
references:
- git-worktree
- git-merge-base
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


## Engineering problem
A branch change can abandon uncommitted work; a green build may refer to a different delivered artifact.

## Reproducible method
1. Inventory HEAD, index, tracked/untracked files and worktrees
2. preserve bytes before mutation
3. start from an explicit baseline
4. check ancestry both ways
5. qualify the final artifact
6. rehearse fallback on a fictional copy.

**Responsibilities:** the author proposes and records results; the reviewer challenges the oracle; the consuming project owner decides adoption.

## Example, counterexample and failure
Example: work in a separate worktree while preserving dirty files. Counterexample: reset --hard to obtain a “clean” workspace. Failure: same branch name is mistaken for same commit; compare exact identifiers.

## Artifacts and qualification
Git inventory; preserved-work hashes; ancestry log; previous and candidate artifacts; fallback result.

Lab C demonstrates byte preservation and divergence of two branches. It does not simulate every submodule, conflict, ignored file or hook in a real repository.

## Transfer exercise
Apply this method to fictional Courier. Produce the artifacts above, then invent a case that invalidates an overbroad conclusion.

<details><summary>Transfer self-check</summary>The case is fictional and reproducible; baseline is identified; procedure and expected result are explicit; a failure is retained; the conclusion cites artifacts and limits. If any criterion is missing, revise before declaring the method applied.</details>
