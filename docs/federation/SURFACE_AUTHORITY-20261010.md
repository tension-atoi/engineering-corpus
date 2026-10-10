# GNU6 — public surface authority and deployment gates

**Snapshot: 2026-10-10, 10:28–10:31 America/Toronto.**
This is a cross-agent boundary record, **not** a request to deploy other
applications or a permanent claim about their availability.

| Surface | Responsible program | Verified on 2026-10-10 | Publishing boundary |
| --- | --- | --- | --- |
| `gnu6.live` | GNU6 portal / Motion promotion team | Strict HTTPS valid; HTTP 200 | Another agent owns the site shell, visual direction, Motion cutover and any Coolify deployment |
| `docs.gnu6.live` | `tension-atoi/engineering-corpus` | Strict HTTPS valid; HTTP 200 | This repository owns its static documentation and reviewed federation snapshots |
| `gnosix.gnu6.live` | Gnosix product surface / separate presentation agent | **BLOCKED**: default self-signed Traefik certificate; strict TLS validation fails; diagnostic HTTPS with certificate verification disabled gave HTTP 404 | Domain **reserved for the Gnosix product**. Do not advertise it as an operational website, issue a success badge, add an active CTA, or redirect docs there until a fresh TLS+HTTP+content qualification |
| `github.com/tension-atoi/gnosix` | Gnosix source project | Public (`isPrivate=false`), `main` | GPL-3.0-or-later in source README/LICENSE; experimental/pre-release with R19 whole-product acceptance OPEN. Federation uses exact pinned source SHA only |
| `github.com/tension-atoi/in.gnu6` | in.gnu6 headless scenic/spatial/topology source | Public (`isPrivate=false`), default branch `main` | **Candidate only**: no approved source path allowlist, digest manifest, license disposition, editorial/safety review, or route admission. No import or product page |
| `github.com/tension-atoi/gnostral.rs` | gnostral.rs source lab | Public | Federated in the docs portal under pinned research constraints; not a production model-serving product |

## Canonical rule: project website ≠ documentation portal ≠ source repository

- The Gnosix product domain is `gnosix.gnu6.live`, even while unavailable.
  `docs.gnu6.live/fr/projects/gnosix/` and its English route are **technical
  documentation entrypoints**, not product homepage substitutes.
- Product UX / Motion visual shell / favicon and dynamic UI configuration
  remain with their own agent and own Git/Coolify release gates. Do not
  overwrite the production site with prototypes or embed fake routes.
- `engineering-corpus` may cite public Gnosix source files by exact commit
  and SHA-256. The documentation pipeline does **not** control product
  deployments, TLS certificates, Traefik routers or Gnosix release status.
- When strict TLS validation and a non-error HTTP response succeed on
  `gnosix.gnu6.live`, a separate **content authenticity / design / canonical
  route** check is still required before adding a production CTA.
- A repository changing to public does not automatically authorize an import,
  a stable-release claim, a license assumption, or promotion of internal
  contracts and private evidence. Every new source needs its own frozen
  manifest, license/status review, negative gates and editorial owner.

## Provenance of these observations

- GitHub public repository metadata, read directly from GitHub on
  2026-10-10 for `gnosix` and `in.gnu6`.
- Independent public HTTPS hostname checks using `curl` and
  `openssl s_client` with SNI. The Gnosix certificate subject observed
  was `CN=TRAEFIK DEFAULT CERT`; strict `curl` failed with a hostname
  mismatch. The insecure 404 probe was used **only diagnostically**, never
  as an approval of secure service availability.
- The approved GNU6 Motion commit `f03fe50` and its Animé/Off modes are
  reported by a **parallel agent**, not independently qualified by this
  documentation intake. No changes to this other worktree or deployment
  are authorized here.

**Before interpreting this file as a current availability report, rerun the
network and repository checks.** Avoid hardcoded permanent "live" claims in
generated pages based on this dated snapshot.
