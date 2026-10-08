# gnu.in.labs — Engineering Corpus

**Open engineering methodology · Local-first · Evidence-driven · FR/EN**

> Status: `DRAFT / ADOPTION_PENDING`. This public educational corpus is not a representation of Gnosix production maturity, its internals, or a certification of any API.

Engineering Corpus is a *public, executable study surface* for collaborative software engineering: mandates, authority boundaries, architecture, implementation slices, verification, reproducible evidence, documentation and release discipline.

**Read it, challenge it, fork it, improve it.** The examples use fictional components; no private Gnosix source is embedded.

## Explore

- `dist/index.html` — prebuilt, static, offline-friendly study portal (generated from `docs/`).
- `docs/fr/` — French corpus, default reading experience.
- `docs/en/` — English corpus, same chapters and labs.
- `docs/templates/` — reusable contracts and checklists.
- `docs/diagrams/` — Mermaid sources and topology diagrams.
- `METHOD.md` — framework status, decision rules and evidence semantics.

## Local usage

```bash
# View prebuilt portal, without dependencies or API keys
python3 -m http.server 8080 --directory dist
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
