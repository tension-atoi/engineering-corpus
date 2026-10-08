# gnu.in.labs — Engineering Corpus

**Open engineering methodology · Local-first · Evidence-driven · FR/EN**

> Status: `DRAFT / ADOPTION_PENDING`. This public educational corpus is not a certification of any API or an adopted standard.

Engineering Corpus is a *public, executable study surface* for collaborative software engineering: mandates, authority boundaries, architecture, implementation slices, verification, reproducible evidence, documentation and release discipline.

**Read it, challenge it, fork it, improve it.** The examples use fictional components.

## Explore

- `dist/index.html` — prebuilt static study portal, served through loopback HTTP (generated from `docs/`).
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

**Publication state:** standalone repository scaffold and build artefact, not a live deployment.

## CORPUS-01 study edition

Eight proposed methods (EC-M01–08), three executable fictional labs (EC-L01–03),
FR/EN governance and source references. All methods remain draft; see
[editorial review](reviews/CORPUS-01-editorial.md) and [UX report](reviews/CORPUS-01-ux.md).
Future official publication: **docs.gnu6.live**. No public deployment has occurred.

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
