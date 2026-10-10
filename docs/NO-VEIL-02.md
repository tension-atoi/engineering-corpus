# NO-VEIL-02 — Native cross-origin navigation and BFCache safety

2026-10-10 · [CANONICAL] Ratified no-veil policy adapted from pending PR #17; [CHECKPOINT] browser qualification.

## Regression

GNU6's public portal served both React Router integrated documents and traditional links to the Docs domain. The old `g6-motion.css` implemented a full-screen opaque pseudo-element under `html[data-g6-bridge]`. G6Motion set `covered` during native document transitions. When navigating API / SDK, the veil could appear; the user also reported a black screen after Back. The black Back screen was not consistently reproduced in our 600ms-delay baseline run, but the cause of an opaque restored state is plausible and eliminated by construction.

## Repair

- Remove the overlay CSS entirely: no full-screen bridge selector or painted pseudo-element.
- Keep the compatibility `G6Motion.bridge` interface **inert** (`active=false`; cover/reveal are resolved no-ops).
- Clear any stale `data-g6-bridge`/arrival state at initialization and on `pagehide` and `pageshow` (including BFCache restores).
- Disable the old global link interception in the Docs context adapter. Native standalone pages must load naturally; no masking or invented continuity.
- Preserve the unchanged header G6Rig/G6Bar primitives and the versioned static study pages.
- Update the context adapter lock without modifying external identity/OIDC, docs data, URLs or route authority.

## Proven

- Build regenerated **92 HTML pages**; only shared Motion/Context assets changed in dist.
- `scripts/check.py` complete PASS, including design 1.1.1, static shell, context locks, NO-VEIL-02 safety and immutable 18-document export.
- Existing export provenance verification adapted to a merged Git checkout: compare the contents independently of `source_commit`, which is intentionally pinned to an ancestor commit; do **not** edit the immutable exported document.

## Non-claims

Native navigation between distinct origins is not a persistent DOM. No animated body/sidebar masking is introduced. Production cutover and operator browser acceptance require separate qualification and may be rolled back independently of the GNU6 gateway.
