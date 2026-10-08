# CORPUS-01 execution plan

Baseline: `22d5ebc43016588462a72e395afcc1d647d5150b`. Branch: `corpus-01-editorial-qualification`.
Mandate: qualify an inspectable public educational corpus; preserve fictional examples,
static hosting, FR/EN parity and browser-only study state. No merge or deployment.

## Design

Keep Markdown as editorial source and the Python generator as the static derivative.
Give all eight methods and three labs explicit identity, classification, prerequisites,
outputs, success criteria and references. Add operational examples and bounded proof.
Separate documentary status from technical qualification and consumer adoption.

## Tasks and gates

- [x] Audit all FR/EN chapters and both existing labs; record priorities against baseline.
- [x] Reproduce browser faults before correcting state, navigation, semantics and errors.
- [x] Enrich eight methods and two labs; add executable fictional Git topology lab.
- [x] Define governance, editions, objections and classification without consumer ratification.
- [x] Strengthen checks: parsed metadata, parity, relative links and fragments, resources,
      exact page inventory, generated drift and negative fixtures.
- [x] Rebuild committed source in a clean checkout and isolated pinned environment twice;
      compare artifact bytes and record commands, versions, hashes and limitations.
- [x] Review desktop/mobile browser, keyboard, contrast, storage failures, language context,
      loaded resources, offline scope and 404 behavior; retain screenshots and raw results.
- Integration: commit/push branch and open PR with publication handoff. Attach qualification to the
      final exact HEAD externally to avoid a self-referential committed manifest.

## Review focus

Corrupt or blocked browser storage; absent search results; mobile hidden focus targets;
language switches within a lesson; stale generated files; unknown routes; dirty workspaces;
divergent histories; examples whose output cannot establish the claimed property.

## Status gates

`EDITORIAL_REVIEWED`: every unit audited, priorities resolved or recorded, FR/EN parity checked;
this is an author review, not independent ratification.
`TECHNICALLY_QUALIFIED`: clean pinned rebuild, zero drift, checker negative controls,
fictional labs and bounded desktop/mobile browser matrix pass at the referenced HEAD.
`DEPLOYMENT_PENDING`: deployment is a separate owner decision and must rehearse rollback.
