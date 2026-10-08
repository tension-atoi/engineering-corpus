# Corpus method: status and authority

**Edition:** 0.1-draft. **Authority:** educational proposal only.

## What this is

A reference methodology designed to be interrogated, forked, tested, and adapted. No claims of universal applicability, organizational adoption, or formal compliance certification.

## Invariants

1. `Intent != contract != implementation != proof != public claim`.
2. Repository code, declared interface and executable results are different evidence classes.
3. Authority is scoped by resource, operation and expiry; an assistant's presence never enlarges it.
4. Read-only observation and write capability are separate. Publishing has its own gate.
5. Private data cannot enter public documentation by convenience or by LLM summarization.
6. Do not auto-promote `experimental` to `public-stable` based on doc generation.
7. Every published normative claim has a link to a version, an owner, and an evidence record or a clear non-verification label.
8. Failing a gate blocks promotion, not exploratory work.

## Claim ladder (not an automatically ordered score)

| Evidence class | What it demonstrates | Does not demonstrate |
|---|---|---|
| E0 intention | Requirement or proposition exists | Behavior exists |
| E1 static | Symbol, code path or contract exists | Execution succeeds |
| E2 executable | Test scenario produced a result | Real-world deployment |
| E3 measured | Repeated metric with method and environment | UX parity or operational reliability |
| E4 observed | Captured real behavior with provenance | All cases handled |
| E5 integrated | Cross-subsystem path evidenced | Sustained operation |
| E6 operated | Bounded production history and monitoring | Universal correctness |

Classes have distinct meanings; they are not simple numeric confidence levels. Evidence may be contradictory, stale, or irrelevant to a new target. Include exact scope, commit, date, environment and reproducible commands.

## Document statuses

`draft` → `reviewed` → `adopted` → `deprecated` → `retired`. `rejected` is a terminal proposal status, not a deleted historical record. Only the owners of a consuming project can declare adoption there.

## Reader pathway

Read **Mandate → Authority → Contract → Delivery → Evidence → Documentation → LLM tooling → Hygiene & release**. Complete the three labs; assess against the provided checklists. This is a learning instrument, not an accreditation.

## Classification and review

See [governance](docs/en/governance.md). Document status, claim classification,
technical qualification and consumer adoption are separate axes. EC-M identities
are stable within this edition; lab fixtures demonstrate bounded scenarios.
CORPUS-01 editorial review is an author audit; an independent review is still
requested through its PR. The E0–E6 taxonomy is a proposed corpus convention,
not an external standard or a numeric confidence scale.
