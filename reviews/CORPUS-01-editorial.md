# CORPUS-01 — Editorial review

**Review type:** manual editorial audit assisted by repository checks. This is not an independent owner approval.
**Scope:** public branch changes from `main` through the CORPUS-01C candidate; fictional examples and public evidence only.
**Status:** draft corpus; owner merge approval pending.

## Findings and corrections

- The README linked to two review files that were absent. It now links to this review and the existing publication handoff.
- The French references page contained English explanations. Those descriptions are now translated while retaining the original source titles and stable classification identifiers.
- The Markdown builder set `typographer=True`, but the CommonMark preset does not enable the replacement and smart-quote core rules. The build now explicitly disables automatic punctuation rewriting. The source-language convention is recorded in `CONTRIBUTING.md`; code, commands, identifiers, URLs and literal quotations remain unchanged.
- `.gitignore` contained a duplicate `vendor/` entry; the duplicate was removed.

## Content and public-evidence assessment

The eight methods and three fictional labs consistently identify their status as proposals. They distinguish external references, corpus recommendations, executable evidence and consumer adoption. The workspace lab demonstrates preservation of uncommitted data, divergent branches and ancestry checks in a synthetic repository. No private project source or real operator data is required to reproduce it.

The audit of 22 files from the earlier internal candidate classified 8 `PUBLIC_SAFE`, 6 `PUBLIC_REDACTABLE`, 8 `INTERNAL_ONLY`, and 0 `UNKNOWN`. Redactable items were replaced by current sanitized records or generic public instructions. Internal infrastructure, authenticated UI, local profile and host-specific build evidence remain outside this branch. The sanitized summary and artifact manifest are the only new qualification records committed here.

## Remaining review limits

- This audit does not constitute the owner's human approval to merge.
- Browser and assistive-technology review has not been rerun on the final post-correction commit. No WCAG conformance or learning-effectiveness claim is made.
- No Coolify resource, image, healthcheck, DNS route, TLS certificate or production behavior has been tested or changed by this review.
- The 54-file static artifact must be rebuilt, requalified and matched to its manifest after these editorial corrections. Its final commit must be recorded before merge approval.
