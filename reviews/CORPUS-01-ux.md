# CORPUS-01 — Browser and accessibility report

Browser: actual BrowserOS neo Chromium via its local MCP, 2026-10-08.
Targets: desktop 1440×1000; emulated mobile 390×844 and 320×700; 720px reflow proxy
for a 1440px viewport at 200% zoom. This is a bounded functional review, not WCAG
certification, physical-device testing or a screen-reader user study.

## Reproduced defects

| Defect | Baseline evidence | Correction |
|---|---|---|
| Mobile close link only navigated to content | baseline-failures.json: open=true, expanded=true | Named close button, explicit state transition and focus restoration |
| Stored JSON null interrupted state initialization | baseline-failures.json: aria-pressed=null | Validate object shape and known boolean identities; storage notice for errors |
| No empty-search feedback | Source review and browser flow | Live result count/empty message; accent-insensitive reset tested |
| Context anchor lost on language switch after hash navigation | Browser desktop phase failed FR EN context | Update reciprocal link on hashchange and activation |
| Progress meter and count were hardcoded | Source: ten identities; style width mutation | Catalog-driven 11 identities and native progress value/label |
| Home contained two H1s | Parsed generated HTML | Demote introductory note heading; one main H1 |
| Contribution link led to templates | Source and link target | Dedicated bilingual governance route |
| Lifecycle endpoint clipped by SVG viewBox | Visual review + checker RED: rectangle clipped | Derive minimum viewBox width from node extents; static geometry gate |
| Narrow diagrams became unreadable miniatures | Visual resources.png inspection | Focusable horizontal region, minimum diagram width, textual equivalent and open-SVG link |
| Capsules conflicted with supplied design rules | gnosix_DS V3.4.1 SEMANTICS.md and user mandate | Status/duration text with attention cue; no capsule styling |
| Unknown route had no explicit recovery contract | Redirect-only 404 artifact | Bilingual 404 page; preview sends HTTP 404 and home links |
| Relative links, fragments and invalid statuses escaped checker | baseline-checker.json | Parsed validation and six negative controls |

## Results and evidence

Raw structured evidence is in `evidence/logs/corpus-01/`; browser phases are in
`scripts/browser-review.js`. A final qualification manifest ties hashes and the exact
HEAD to the PR. Screenshots show appearance; functional results establish their own
scenarios rather than inferring behavior from pixels.

| Gate | Evidence | Observed scope |
|---|---|---|
| Desktop search | desktop.json | Accents, empty result feedback and restore all 13 links |
| Local study | desktop.json | Native progress value, toggling, shared FR/EN identity, null/array/string/malformed storage and blocked writes |
| Language context | desktop.json | Same lesson and section-2 anchor, preserved studied state |
| Keyboard | desktop.json / mobile.json | Skip link focus, menu opening focus, wrap, Escape/close and return focus |
| Mobile | mobile.json | 390/320px without page overflow; CDP touch activation opens menu |
| Semantics | pages-01…08.json | 32 localized pages, one main H1, proper locale, bounded overflow/resources inspection |
| Contrast | contrast.json | Eight actual text/background samples ≥4.5:1; not exhaustive |
| Reflow/motion | zoom.json | 720px reflow proxy, reduced motion disables transitions and smooth scroll |
| Diagrams | resources.json / resources.png | All three images load; descriptions, full-size pan and source links |
| Offline | resources.json | Loaded page and SVG remain readable with network disabled |
| Resource loading | resources.json / pages-*.json | Local CSS/JS/font/SVG only in inspected resource timings |
| Error route | resources.json | Unknown URL returns HTTP 404, bilingual page and recovery links |

Typography uses locally bundled Space Grotesk under OFL. Method metadata and code use
the same interface family with weight/tabular-number differentiation. The SVG image
labels retain a documented system-font fallback: external font loads inside SVG image
contexts are unreliable, and this pass did not rebuild their source artwork. Body
descriptions provide the diagram meaning without depending on image text.

## Limits and recommendations

No screen-reader session, Firefox/Safari run, physical phone, exhaustive color scan,
or browser-native zoom action was performed. The zoom check is a reflow proxy. Mobile
keyboard uses focus/Enter because the MCP convenience click mis-targeted a control
under emulation; explicit CDP touch activation separately passed. The browser scripts
wait for initialized state rather than treating a navigation return as application
readiness. These tool-level failures are not silently promoted to product defects.

Resource timings cover this site, not extensions, browser infrastructure or all
possible exfiltration paths. CSP forbids connections; optional external references
are explicit navigation. The portal works without Internet when the local HTTP server
is running. Loaded pages stay readable disconnected; uncached offline navigation and
file:// opening are not supported. No service worker is introduced.

Before a wider accessibility claim, test assistive technology, native 200% zoom,
high-contrast/forced colors and physical touch, with independent readers. Deployment
must configure the same 404 behavior, HTTP headers and approved domain separately.
