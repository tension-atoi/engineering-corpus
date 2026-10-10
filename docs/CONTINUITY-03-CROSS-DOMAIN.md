# CONTINUITY-03 — GNU6 native domain handoff

2026-10-10 · [CHECKPOINT] Docs local candidate source-qualified. Not deployed.

## Authority
- Canonical visual/motion source: gnu6-design 1.1.1 f03fe50.
- Context action and domain policy: tension-atoi/gnu6-live
  feat/context-03-cross-domain at 0b7afeb79e8b3907058bd92825ee5763ee113f9a,
  context-core 1.0.3.
- Docs owns only CSP-safe adapters and deterministic static rendering.

## Implementation
Self-hosted upstream g6-motion.js and g6-motion.css are immutable, pinned
by site/motion/motion.lock.json. domain.js executes in the parser head to
set docs identity ahead of the upstream handoff parse; receiver.js reveals
the incoming opaque bridge against the existing brand anchor after DOM
readiness. All JS remains same-origin; CSP is unchanged (script-src self,
connect-src none). No inline scripts, new icons, visual palette, WM
algorithms, iframe or cross-origin state transport.

The existing static context adapter imports the same generated ESM core
as GNU6 Home. Ordinary eligible clicked links and contextual navigation
to the exact peer origin call G6Motion; unrelated URLs are native.
Each page remains a real docs.gnu6.live URL with its own independent DOM.

## Proof
- Source SHA pins: site/context/context.lock.json and site/motion/motion.lock.json.
- scripts/test_context.py and scripts/test_motion.py: 90 FR/EN pages / all assets.
- Full build and check: 92 pages, CORPUS_CHECK_OK.
- Joint browser proof in gnu6-live scripts/qualify-cross-domain.cjs:
  two HTTPS browser origins using local source response interception,
  both context-menu directions, inbound domain, bridge teardown, and
  Off-mode travel in both directions. PASS.
- No production DNS/TLS, deployed Coolify, physical GPU or live CDN claims.

## Deferred
Engine in.gnu6 remains unlicensed for distribution and disconnected
from the publicly routed portal. Do not publish, deep-link a fabricated
Gnosix product or replace the native top-level domain boundary.
