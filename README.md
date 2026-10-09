# gnu.in.labs — Corpus Méthodologique & Hygiène Mental

**Méthodologie ouverte · Hygiène de la pensée · Local-first · Preuves reproductibles · FR/EN**

> Status: `DRAFT / ADOPTION_PENDING`. This public educational corpus is not a certification of any API or an adopted standard.

**Corpus Méthodologique & Hygiène Mental** is a public, inspectable study project. Its first curriculum covers collaborative software engineering: mandates, authority boundaries, architecture, implementation slices, verification, reproducible evidence, documentation and release discipline. The name defines an editorial direction, **not** a claim that mental-health coursework already exists.

**Read it, challenge it, fork it, improve it.** The examples use fictional components.

## Product direction (not yet implemented)

The corpus is intended to expand beyond engineering methods. Future editions may explore ways to understand, challenge, practice and retain knowledge, with narrative or game-like learning paths where they genuinely improve comprehension. This is an intention, not a promise of XP systems, certifications, medical advice or new published chapters.

**Compatibility:** The GitHub repository remains `engineering-corpus` for now, and existing paths, chapter identifiers and the browser-local study-progress key are intentionally preserved. A future docs portal can place this independently versioned corpus under a dedicated route.

## Documentation hub (DOCS-HUB-01D)

The root of **[docs.gnu6.live](https://docs.gnu6.live/)** opens the French
documentation hub. English is at `/en/hub.html`. The **Corpus Méthodologique
& Hygiène Mental** is still independent and its study progression is unchanged.

| Public route | Meaning |
|---|---|
| `/` | Redirects to `/fr/hub.html` |
| `/fr/hub.html`, `/en/hub.html` | FR/EN federation entry point |
| `/fr/index.html`, `/en/index.html` | Existing corpus study home, unchanged |
| `/fr/chapters/*`, `/en/chapters/*` | Existing stable chapter URLs |
| `/fr/sdk.html`, `/en/sdk.html` | Transparent empty SDK inventory; **no distributable SDK qualified** |
| `/fr/api.html`, `/en/api.html` | One **experimental Rust code contract**, not an HTTP service |
| `/registry/source-catalog.json` | Versioned, machine-readable public source provenance |
| `/fr/guides.html`, `/en/guides.html` | Source-pinned draft teaching guide inventory |
| `/fr/guides/api-verification.html`, `/en/guides/api-verification.html` | RED/GREEN symbol verification using fictional local Python fixtures |
| `/fr/releases.html`, `/en/releases.html` | Explicitly empty corpus release inventory: **zero verified tags** |
| `/registry/guide-catalog.json`, `/registry/release-catalog.json` | Machine-readable, versioned guide and release provenance |

`docs/hub.json` is the editorial navigation index and
`docs/source-registry.json` is the curated, pinned source manifest.
The API section references the experimental `gnostral.rs`
`EngineProvider v0` Rust trait at an exact Git commit with source-file
SHA-256, crate version `0.0.1` and `publish = false`. This is **not a
production API, public endpoint or published SDK**. Its async/streaming
transport bindings are not included in the reference model.

No public SDK distribution is qualified. One experimental Rust contract remains
source-verified, and one draft educational guide exercises the repository's
fictional local API lab. The guide is **not** a stable SDK or production
API integration. At the 2026-10-08 verification, engineering-corpus had **no
release tags**; the release inventory is navigable but empty. Neither state
makes claims about other Gnosix projects.
Offline builds consume only the committed manifest — **no external network
access at build or browser runtime**. Verify public pins explicitly when
updating a source. The corpus remains **DRAFT / ADOPTION_PENDING**.

## Explore

- `dist/index.html` — static redirect to the FR hub; the corpus remains under `dist/fr/index.html` and `dist/en/index.html`.
- `docs/fr/` — French corpus, default reading experience.
- `docs/en/` — English corpus, same chapters and labs.
- `docs/templates/` — reusable contracts and checklists.
- `docs/diagrams/` — Mermaid sources and topology diagrams.
- `METHOD.md` — framework status, decision rules and evidence semantics.

## Local usage

```bash
# View prebuilt portal, without dependencies or API keys
python3 scripts/serve.py --port 8080
# Open http://localhost:8080

# Rebuild locally, in an isolated virtual environment
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python scripts/build.py
.venv/bin/python scripts/check.py
```

No database, no SaaS, no external fonts, no analytics, no remote scripts, no user accounts. Study completion is saved in the reader's browser only; it is not a credential or audit trail.

## Repository responsibilities

| Folder | Authority | Policy |
|---|---|---|
| `docs/` | Editable normative source | PR review + explicit status per chapter |
| `docs/templates/` | Examples, not universal rules | Adapt to each repo and authority model |
| `dist/` | Generated derivative | Do not hand-edit; rebuild before release |
| `scripts/` | Reproducible generation and lint | Read-only inputs, deterministic output |
| `assets/` | Static visual assets | No hidden network requests |

## Governance

- Public corpus changes use proposals and review; an example being published does **not** ratify policy in a separate project.
- No source from private repositories without explicit approval and a public-release review.
- No agent may infer permission to merge, push, deploy, access credentials, or change production from this corpus.
- No GitHub-hosted build or CI dependency is required for release: local verification is the default.

## License

MIT for the original content and software in this repository (see [LICENSE](LICENSE)). External tools and references retain their respective licenses. Attribution to external projects does not imply endorsement.

**Publication state:** documentation hub live at [docs.gnu6.live](https://docs.gnu6.live/), corpus study edition under [FR](https://docs.gnu6.live/fr/index.html) and [EN](https://docs.gnu6.live/en/index.html). The curriculum remains draft; infrastructure operation is not normative adoption.

## CORPUS-01 study edition

Eight proposed methods (EC-M01–08), three executable fictional labs (EC-L01–03),
FR/EN governance and source references. All methods remain draft; see the
[editorial review](reviews/CORPUS-01-editorial.md) and [publication handoff](reviews/CORPUS-01-publication.md).
The current edition is available inside **docs.gnu6.live**. The hub indexes SDKs, APIs, Guides and Releases as future areas only until public, versioned sources are qualified.

### Local checks

```bash
.venv/bin/python scripts/build.py
.venv/bin/python scripts/check.py
.venv/bin/python scripts/test_checks.py
.venv/bin/python scripts/test_labs.py
python3 examples/workspace_lab.py --output evidence/runs/workspace-trial
```

`CORPUS_CHECK_OK` checks parsed metadata, FR/EN identity/status parity, expected
page inventory, local links/fragments, static resource references and narrow
credential patterns. It does not certify editorial truth, accessibility, network
behavior outside the page, or API correctness.

### Clean qualification

The checked lock targets CPython 3.14 on Linux x86_64. It pins all three packages,
including the transitive mdurl dependency, to reviewed wheel hashes. Populate an
ignored local wheel cache once (network needed only for this provisioning step):

```bash
.venv/bin/pip download --require-hashes -r requirements.lock --dest vendor/wheels
# Commit intentional source/generated changes before running qualification.
python3 scripts/qualify.py --wheels vendor/wheels --output /tmp/corpus-qualification
```

The qualifier clones exact clean HEAD locally, creates a venv without system
packages, installs only the hash-checked local wheels, rebuilds twice, compares
bytes against committed dist, and runs positive/negative checker and lab gates.
Retain run.json and raw.log under evidence/runs and evidence/logs in your chosen
qualification record. Other Python/OS platforms require a reviewed lock expansion;
they are not covered by this run. Dependencies and wheel caches are not committed.

### Browser review and offline scope

`scripts/browser-review.js` contains optional browser-side checks for desktop, mobile,
resources and contrast. Run it only in a browser session you control and retain its
structured results and screenshots locally. Network tests cover the site's resources,
not unrelated browser extensions or browser infrastructure.

The portal needs a local HTTP server: root-relative URLs do not support opening
HTML directly through file://. It can be studied without Internet while loopback
HTTP remains available. A loaded page stays readable offline; navigating uncached
routes without a server is not guaranteed. No service worker or installed PWA is
provided. External source links are optional explicit navigation.

### Design and asset licenses

The corpus uses project-scoped CSS tokens and no third-party identity artwork.
Space Grotesk is bundled under [SIL OFL](site/fonts/SpaceGrotesk-OFL.txt), separately
from the original corpus MIT license. Statuses use text and attention cues; capsule
components are prohibited. Diagrams retain a system-font fallback in SVG image
context; descriptions and pannable full-size diagrams preserve access to meaning.
