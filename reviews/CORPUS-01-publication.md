# CORPUS-01 — Publication handoff

Official future domain: **docs.gnu6.live**, per owner instruction. No DNS, hosting,
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
3. Provision static hosting for docs.gnu6.live with HTTPS, MIME types, the bundled font,
   explicit 404 response, CSP headers and no telemetry; review the concrete config.
4. Test FR/EN routes, recovery links, resource loading and mobile study on staging.
5. Obtain owner approval of hostname, artifact digest, config and rollback target.
6. Record operator, UTC, exact commit, artifact manifest and post-deployment route checks.

## Rollback

The first publication cannot assume a prior Coolify image. If the new route fails,
disable the corpus resource's domain route in the hosting control plane (or stop the
new resource) to return `docs.gnu6.live` to the pre-publication edge response. This withdraws the
site; it is not a content restore. If a prior release is later approved, preserve its
manifest and static artifact outside the resource before rollout. Restore by selecting
that exact artifact's source commit in Coolify, verifying its checkout and manifest,
then packaging/redeploying it; do not rely on a cached image or rebuild documentation
on the VPS. No previously approved public release or rollback has been claimed here.

The deployment checklist records the conditions required for a first-release withdrawal
and any future content restore.

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
