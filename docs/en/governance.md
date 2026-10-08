---
id: governance
title: Governance
status: draft
category: governance
---
# Governance and objections

## Classification and authority
| Class | Meaning | Decision |
|---|---|---|
| proposed-principle | A method proposal to test | No implicit ratification |
| external-standard | Identified external normative text | Cite organization, version and scope; no automatic compliance |
| recommendation | Contextual advice | Publish prerequisites and exceptions |
| ratified-decision | A corpus-specific decision | Requires owner, date, scope and accepted ADR |

All eight methods and three labs remain `draft`. CORPUS-01 is an author review of editorial quality, not automatic promotion to `adopted`. This edition introduces no ratified methodological decisions.

## Propose or challenge
Open an issue with EC-M/EC-L identity, edition/commit, challenged claim, reproducible counterexample and consequence. An objection may challenge the oracle itself. Provide fictional data and a proposed FR/EN correction.

The maintainer acknowledges, assigns a reviewer, records evidence and disagreement, then answers: accepted, amendment required, deferred with reason, or rejected with reason. The objection remains inspectable. An accepted PR records a repository decision; it ratifies no policy in another project.

## States and editions
`draft → reviewed → adopted → deprecated → retired`; `rejected` retains a declined proposal. `reviewed` requires a named reviewer and review scope. `adopted` requires an owner and ADR; its authority is limited to this corpus. Consumers ratify their adaptations separately.

Documentary editions are identified by catalog, commit, change notes and manifest. Compatible corrections increment patch; a new method increments minor; an incompatible contract change requires a new major edition and migration guide. This convention is a governance proposal for review, not an already published release.

## Publication gate
Clean isolated build, zero drift, link/metadata checks, positive and negative labs, FR/EN review, browser matrix and explicit limits. Evidence targets exact HEAD. Merge is separate from deployment. Future official domain: `doc.gnu6.live`.

## Privacy and local study
Progress is a browser-local preference shared between FR/EN and removable through site data. It is neither a credential nor evidence of competence. With blocked storage, it lasts for the current page. No account or cloud service is required.

## Contribution
Include problem, baseline, sources, example/counterexample, FR/EN, results and limits. Do not submit private code, secrets, model weights or personal traces. Tutorials guide learning; references describe contracts; guides give methods; runbooks govern authorized operations.
