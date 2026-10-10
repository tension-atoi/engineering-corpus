# MOTION-SERVICE-ADAPTER-02 — Native Docs boundary

**2026-10-10 · [CANONICAL] owned source changes; [CHECKPOINT] local qualification.**
**Workload owner:** `engineering-corpus` / `docs.gnu6.live`. **Platform owner:** GNU6 gateway and shared gnu6-design. Base: `tension-atoi/engineering-corpus` `origin/main@d09eede`, not the superseded `feat/unified-spine-postlive-01-docs-1.1.1` worktree.

## Exact scope

The owner ratified GNU6 Motion 1.0.0 as an official **standalone public demonstrator** at `https://gnu6.live/motion/index.html`. Its live deployed source is `tension-atoi/gnu6-live@17bec35`, with qualification/proof `174919b`. This Docs slice consumes the public **destination link and identity tokens**, NOT the fake scenes, the shell iframe transport, or portal privileges.

All real Docs pages continue to be autonomous native top-level documents with canonical URLs such as `https://docs.gnu6.live/fr/hub.html` and `/en/hub.html`. This adapter implements the settled Docs identity:

- Existing authentic green GNU6/gnu.in.labs 64px favicon `/gnu6/identity/gnuinlabs-64.png` and 128px touch icon. The 64px source has SHA-256 `14b67e37a197156d5df65fec3bb3d27ed2405da3b427e862fd2489e912d21e0a`.
- Green titlebar identity `docs.gnu6.live`, linking to the correct FR/EN Docs hub. The text uses the shared versioned `--g6-accent-labs-text` token; no invented hexadecimal colour.
- One real `https://gnu6.live/motion/index.html` native Motion link in the wide navigation and one in the responsive disclosure menu; existing Docs / GNU6 / Code / private-portal links stay as originally authorized.
- No remote script, no local animation injection, no iframe of Docs/Gnosix, no history spoofing, no cookie, auth, CSP, TLS or server-side contract change.
- The shared `gnu6-design 1.1.1` package and `gnu6-spine-adapter 1.0.0` lock remain byte-identical.

## Service integration contract

| Field | Contract |
|---|---|
| Purpose | Display true Docs publisher identity and link to qualified public GNU6 Motion |
| Upstream+version | `gnu6-design 1.1.1`; `gnu6-motion-public-demonstrator 1.0.0` as an external navigation destination |
| Adapter | `motion-service-adapter-02/docs-native 0.1.0`, Python renderer + Docs-specific CSS |
| Topology | Existing static Docs generator and Coolify nginx app, independent native top-level origin |
| Data authority | Docs generator, existing metadata and source registries; Motion cannot mutate Docs |
| Persistent state | Existing generated FR/EN pages only; no new database/cookies/storage |
| Dependencies | Current `site/gnu6` pinned package and existing docs build |
| Exposed contracts | Native hyperlinks to `gnu6.live/motion/index.html` and `docs.gnu6.live` canonical hub |
| Secrets | None |
| Backup/restore | Committed source + generated site; Coolify release images independently managed; no cutover in this slice |
| Upgrade | Explicit adapter increment; independent Docs repo/source and deploy qualification |
| Observability | Source validators plus responsive and accessible local browser matrix |
| Failure mode | If Motion is unavailable, external link fails natively; Docs never loses its content |
| Consumers | Docs readers FR/EN; no authentication consumer |
| Theming status | Green identity at rest; does not replace the approved animated standalone Motion experience |
| Production status | **SOURCE-CANDIDATE only**. No Docs runtime mutation, no TLS/Coolify changes |

## Proof and non-claims

`python3 scripts/build.py`, `scripts/check.py`, `test_spine.py`, `test_gnu6_design.py`, `test_hub.py` and `test_motion_service_adapter.py` PASS. **90/90** generated FR/EN HTML pages have one native green favicon, accurate domain title, two Motion links (desktop/menu), one normal system header, zero iframes, and unchanged Spine and CSP. The build reports **92** total HTML pages including nonlocalised root/error pages.

Local representative matrix: **16/16 PASS** (FR/EN hubs, Gnosix project page, API reference × desktop/mobile × light/dark). Browser checks include identity icon decoded 64px, motion navigation, zero horizontal overflow, no detected WCAG 2.2 AA axe violations, no console errors. Browser harness is `scripts/motion-browser-qualification.cjs` with `PLAYWRIGHT_ROOT` for the installed Playwright package and `MOTION_DOCS_BASE_URL` for preview origin.

**NON-CLAIMS:** No seamless real cross-origin animation is proven. Native browser document replacement still destroys the old header/body. The owner ratified native isolated domains (D6), not a persistent iframe shell with substituted address-bar identity. Source-public Gnosix/in.gnu6 does not prove `gnosix.gnu6.live` or `in.gnu6.live` are deployed; both returned HTTP 404 during 2026-10-10 inspection (Gnosix also served Traefik's default TLS certificate).

**Next bounded gate:** review/qualify any native cross-domain motion handoff against true browser frames and focus/URL semantics. The earlier radial cover candidate had measured blank frames and MUST NOT be deployed merely because its unit tests pass. Real Gnosix integration starts with a separate workload owner and TLS/router readiness. No new topological authority is implied.

## Owner clarification — intentional new design work

**[CANONICAL, 2026-10-10 11:11 EDT]** The product sites
`gnosix.gnu6.live` and `in.gnu6.live` are **yet to be written and designed**.
Their absent routes are a planned creative/product scope, not an outage requiring
repair. Existing TLS/HTTP observations are checkpoints only. The correct order is
content/authentic media → UX/design system/interactive prototype → owner review →
release version → Coolify/TLS/HTTPS qualification. Docs' already-qualified native
adapter work may continue independently and must not pretend these sites are live.

The proposed GNU6 program contract and distinct product briefs live on
`gnu6-live feat/motion-service-adapter-02-platform`; they do not transfer
product ownership to Docs or authorize changing its hosting configuration.
