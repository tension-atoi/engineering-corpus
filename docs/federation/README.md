# DOCS-FEDERATION-02 — Git-owned documentation, pinned public render

**Publication model:** `gnostral.rs` owns the upstream content; `engineering-corpus`
owns public presentation, a reviewed snapshot, locale navigation and deployment
qualification. The website does **not** fetch GitHub at page load or execute
third-party scripts.

## State as of 2026-10-10

- Repository: `https://github.com/tension-atoi/gnostral.rs`
- Reviewed source: exact public `main` commit stored in
  [gnostral/manifest.json](gnostral/manifest.json).
- Seven exact Markdown paths with independent SHA-256 digests.
- Route family: `/fr/projects/gnostral/`, `/en/projects/gnostral/`.
- English original technical content is visibly marked **original EN** even
  under the FR navigation; editorial FR cover text is bilingual.
- No generated API endpoint, SDK release or production inference claim.

## Update workflow

Run these only from a dedicated clean worktree. The source must be a Git
checkout with the reviewed public commit present:

```bash
# First fetch new upstream public content in the SOURCE checkout.
git -C /path/to/gnostral.rs fetch origin main

# Read-only drift detector: 0=current; 10=review candidate; 2=invalid evidence.
python3 scripts/federate_gnostral.py --check-upstream \
    --source-checkout /path/to/gnostral.rs

# Upon reviewing source changes, explicitly promote one EXACT commit.
python3 scripts/federate_gnostral.py --sync \
    --source-checkout /path/to/gnostral.rs \
    --ref <40-character-reviewed-public-commit>

# Independent build, static checks and no-remote-fetch runtime.
python3 scripts/federate_gnostral.py --verify
python3 scripts/build.py
python3 scripts/check.py
python3 scripts/test_federation.py
python3 scripts/test_hub.py
```

The manifest and seven snapshots are committed with the updated `dist/`
content as one reviewed documentation change. Coolify serves only committed
`dist/`. A change to an upstream repository creates an **update candidate**,
not an automatic redeploy.

## Required publication gates

- Public SHA plus per-file digest and fixed allowlist; no dynamic JavaScript
  request to GitHub, no secret/private repo ingestion.
- Link handling: relative Markdown references point to the exact reviewed
  GitHub source commit, not mutable `main` URLs.
- Reject edited snapshots, unexpected repositories, mutable refs, path
  traversal and source hierarchy escape.
- FR/EN routes, exactly one H1, no broken local links, full site static and
  design checks, no credential text, repeatable output.
- Deployment: publish from reviewed `engineering-corpus` Git SHA only, verify
  live hashes and unaffected routes, preserve rollback SHA/image.
- Independently verified runtime results remain separate from source code and
  from a production/service availability claim.

## Planned improvements

For more repositories, move the single-source code into a typed multi-source
manifest after independently validating path/license/visibility rules.
Automated polling or webhooks may propose a PR with the exact SHA and changed
diff; they must never promote unreviewed private/research outputs or bypass
static/Coolify qualification. A true French technical translation should be
versioned as a separately reviewed, source-referenced artifact rather than
presented as an automatic language-equivalent translation.

## DOCS-FEDERATION-03 — source drift → human-reviewed draft PR

A new **fail-closed proposal bot** watches only the seven public, exact
`gnostral.rs` Markdown paths already allowed by the federation manifest.
It does **not** subscribe to private repositories, infer product maturity
from a commit, or grant GitHub Actions GPU/runtime test authority.

1. **Detect (read-only to docs):** fetch the *canonical public*
   `gnostral.rs/main` into an isolated source checkout and compare each
   allowlisted file's byte SHA-256 against the deployed manifest.
   `CURRENT` and `SOURCE_AHEAD_NO_DOC_CHANGE` create **no PR**.
   Rewritten history, unexpected origin or executable/symlink/raw active HTML
   inputs are rejected.
2. **Prepare candidate:** generate an isolated `engineering-corpus`
   worktree at its fetched `origin/main`; import only the reviewed source
   commit, rebuild static pages and run `scripts/check.py` plus **all local
   `scripts/test_*.py` suites**, then stage only the static pages and the
   bounded source snapshot. The worktree is retained on failure for inspection.
3. **Draft PR (explicit opt-in):** independently revalidate both public
   upstream heads, docs base, staged-file allowlist and snapshot identity.
   Open a **draft** PR with file-level before/after hashes. Never merge, tag,
   force-push or deploy automatically. The draft cannot authorize a Coolify
   deployment by itself.

### Safe watch command

```bash
python3 scripts/federation_review_bot.py \
  --source-checkout /path/to/public/gnostral.rs \
  --refresh
# Exit 0: source current or ahead with no relevant Markdown change.
# Exit 10: new reviewed-doc candidate exists; requires a prepared branch.
# Exit 2: security/provenance refusal.
```

### Qualified proposal on a real changed source

```bash
python3 scripts/federation_review_bot.py \
  --source-checkout /path/to/public/gnostral.rs --refresh \
  --docs-repo /path/to/clean/engineering-corpus \
  --prepare-worktree /new/isolated/federation-worktree \
  --proposal /private/evidence/federation-proposal.json

# Default dry run re-checks public refs and does NOT commit or push:
python3 scripts/federation_draft_pr.py \
  --report /private/evidence/federation-proposal.json \
  --worktree /new/isolated/federation-worktree \
  --source-checkout /path/to/public/gnostral.rs

# Explicit, separately authorized publication as GitHub DRAFT PR only:
python3 scripts/federation_draft_pr.py \
  --report /private/evidence/federation-proposal.json \
  --worktree /new/isolated/federation-worktree \
  --source-checkout /path/to/public/gnostral.rs --publish
```

The proposal publisher uses the local `gh` authorization only when
`--publish` is provided. It never saves API tokens in the repository.
All publication operations remain traceable to a qualified local worktree.
**No GitHub Actions inference/benchmark runners are introduced.**

A recurring read-only check may identify candidates automatically; there
must still be a **separate GitHub PR review** and **separate pinned Coolify
promotion**. This control is not equivalent to automatic FR translation.

## DOCS-FEDERATION-04 — standalone VPS read-only watch

The authoritative public source registry is [sources.v1.json](sources.v1.json):
`gnostral` is an enabled external source; `engineering-corpus` is a
**disabled publisher**, preventing circular ingestion. Repositories not
publicly qualified (including private Gnosix code) are not watched.

The small Python stdlib [watcher](../../scripts/federation_vps_watch.py)
checks GitHub's **public** commit and content APIs. It fetches 7 allowed
Markdown blobs only when the upstream SHA changes, validates size/type/Git
blob integrity, checks a second branch head against concurrent updates, and
writes mode-0600 `latest.json` or `candidate.json`. These receipts contain
only repository names, commit hashes, document digests and statuses.

**No GitHub credentials, branch writes, PR creation, merge, build or
Coolify access exist in the VPS watcher.** GitHub PR preparation stays with
the separately qualified DOCS-FEDERATION-03 desktop tooling and its explicit
draft-only publication gate. Its regular ChatGPT review automation is
independent and must recheck upstream SHA before proposing a PR.

The [systemd user unit and timer](../../ops/federation/) are oneshot,
twice daily (08:17 and 20:17 UTC, randomized up to 10 min), with
`MemoryHigh=64M`, `MemoryMax=96M`, CPU quota, task limit, 90-second runtime,
read-only filesystem, and a single narrowly writable operator state
directory. User linger must be enabled and independently verified; otherwise
the watcher cannot be called autonomous.

### VPS status and rollback

```bash
systemctl --user list-timers gnu6-docs-federation-watch.timer
systemctl --user status gnu6-docs-federation-watch.service --no-pager
journalctl --user -u gnu6-docs-federation-watch.service -n 30 --no-pager
cat ~/.local/state/gnu6-docs-federation/latest.json
loginctl show-user operator -p Linger
```

Use a release directory named by its exact `engineering-corpus` SHA and
atomically update the `current` symlink only after staging verification.
Previous immutable release directories are retained for fast rollback.
`systemctl --user disable --now gnu6-docs-federation-watch.timer` stops
future checks without affecting docs.gnu6.live or other Coolify apps.

**Interpretation:** `CURRENT` means *no changed allowlisted document at
inspection time*. `SOURCE_AHEAD_NO_DOC_CHANGE` means new upstream code but
no approved Markdown update. `DOC_UPDATE_CANDIDATE` requires the separate
DOCS-FEDERATION-03 draft-PR qualification; this watcher will not create one
and never constitutes a site deployment authorization.
