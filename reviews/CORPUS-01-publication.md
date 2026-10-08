# CORPUS-01 — Publication handoff

Official future domain: **doc.gnu6.live**, per owner instruction. No DNS, hosting,
merge or deployment is authorized in this mission. Publication remains pending.

## Gates and interpretation

`EDITORIAL_REVIEWED` means the recorded author review covers the eight FR/EN methods,
two original labs and new workspace lab. It does not mean independent approval or
consumer adoption. All documentary statuses remain `draft`.

`TECHNICALLY_QUALIFIED` may be asserted only for the exact HEAD in the final manifest:
clean cloned checkout, isolated hash-pinned dependencies, committed dist matches two
rebuilds, coherence and negative controls, fictional labs, bounded browser matrix.
Any code/content/asset change invalidates the prior qualification for the new HEAD.

`DEPLOYMENT_PENDING` persists until an owner approves a concrete static artifact and
hosting change. Independent PR review is still required before integration.

## Reproducibility scope

CPython 3.14 on Linux x86_64; markdown-it-py 4.0.0, PyYAML 6.0.3, mdurl 0.1.2.
requirements.lock records reviewed wheel hashes. The builder provisions exclusively
from a local ignored cache, without network or system site-packages. Two consecutive
builds on one host match committed bytes; other OS/Python/platform combinations are
not qualified. No GitHub Actions or hosted builder is required.

Evidence manifests cannot embed their own final commit hash without a circular
dependency. Committed evidence binds tested inputs and artifact hashes; the final
external run and PR record bind the finished exact HEAD. Preserve both, and verify
the HEAD in the PR still matches before accepting any claim.

## Release preparation

1. Complete independent editorial/translation and PR review; record unresolved objections.
2. Requalify the accepted exact commit; package only dist with its byte manifest.
3. Provision static hosting for doc.gnu6.live with HTTPS, MIME types, the bundled font,
   explicit 404 response, CSP headers and no telemetry; review the concrete config.
4. Test FR/EN routes, recovery links, resource loading and mobile study on staging.
5. Obtain owner approval of hostname, artifact digest, config and rollback target.
6. Record operator, UTC, exact commit, artifact manifest and post-deployment route checks.

## Rollback

Keep the previous approved static artifact and its manifest in a separate immutable
release directory. Before changing live hosting, rehearse switching a staging server
between prior and candidate directories, compare their byte manifests and check root,
FR/EN lesson and unknown route. On regression, point hosting back to that preserved
directory and rerun route/health checks. Do not rebuild the old commit as a substitute
for retaining the old artifact. Log the rollback decision and actual target.

No public rollback has been performed; no production site exists in this mission.
The previous scaffold is a reference artifact, not an approved deployed release.

## Material limits

Introductory proposals; no consumer ratification, provider assurance, API certification,
WCAG conformance claim or learner-effectiveness study. Browser scope is Chromium with
emulated mobile, selected contrast measurements and reflow proxy. No guaranteed
uncached navigation while the HTTP server is unavailable. Other builder platforms
need lock expansion. Supplied design-system mapping is scoped, not full conformance.
Inherited SVG labels keep a documented system-font fallback.

Recommended next work: independent external learner trial with fictional repositories,
FR/EN translation review, assistive-technology and physical-device checks, then a
separately authorized static deployment and rollback rehearsal.
