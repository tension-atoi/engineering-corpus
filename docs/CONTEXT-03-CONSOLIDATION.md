# CONTEXT-03 / Docs PR reconciliation

[CHECKPOINT] 2026-10-10. Rebased semantically on Docs main after merged PR #15.

## Authority
Docs main contains an independently merged, hash-locked GNU6 Motion
navbar and its actual g6-site-nav.js arrival/receiver behavior.
Do not copy the older, superseded site/motion adapter from
feat/docs-context-03-cross-domain, because it would overwrite or
duplicate that navbar.

This branch adds only the version-locked Context Core 1.0.3,
native DOM adapter, static generator hooks and tests to the current
Docs main. Both incoming and outgoing transitions call the existing
G6Motion object and existing navbar owns its labeled header links.
Context-menus become progressive enhancements. The target URL remains
native and no second design system is introduced.

## Qualification
Run python scripts/build.py and python scripts/check.py,
and joint gnu6-live Chromium two-origin harness.
GitHub PR is source-only: Coolify deployment is a separate authority.
