# Experiment registry — DOCS-HUB-01F

This is a **curated, versioned, bilingual catalogue of bounded internal research observations**, not an agent authority service, security certification, public API, or claim of production operation.

## Admission contract

An experiment may enter `registry.json` only if:

1. Its `protocol_commit` is immutable, predates measurement and can be resolved to a specific method.
2. The procedure declares a research question, falsifier, positive and negative controls, inclusion/exclusion criteria, equipment and uncertainty.
3. Raw observations are retained *internally* with UTC timestamps, execution statuses, error outcomes and hashes; amendments are never edited back into preregistration.
4. A separate transformation produces a structured **public allowlisted projection**; no private identifiers, credentials, filesystem paths, PID/UID or live service endpoints are published.
5. An independently implemented checker recomputes material claims against the source data, rejects a deliberately forged conclusion and verifies raw/public hashes.
6. A claim is explicitly scoped to E0–E6 **as local corpus terminology**, and each record distinguishes `status`, `review`, `external_reproduction` and `production_authorization`.
7. An E4 *single internal observation* may appear publicly only as a marked draft with the caveat that the raw data is private and independent external verification is unavailable. A hash alone is not disclosure.
8. Public deployment is a distinct action requiring a review of visibility, privacy, provenance and user authority; passing a build never promotes `draft` to ratified.

## Pipeline de preuves / Evidence pipeline

See [PIPELINE.md](PIPELINE.md) for the dual-language research protocol, source-to-public ingestion boundary, falsification rules and reproducible commands. The matching CUDA-05F contract is pinned at [GPU-EVIDENCE-CONTRACT-v1.json](GPU-EVIDENCE-CONTRACT-v1.json).

## Entries in v2026-10-09.2

- `CUDA-05D`: Linux user-namespace-root identity remained the same host UID; subordinate mapping failed in this trial. Distinct-principal gate **NOT_QUALIFIED**.
- `CUDA-05E`: in a one-trial rootful-Docker fixture, different actual host principals, SO_PEERCRED allow/deny and DAC rejection were observed. No Rust GPU integration or production authorization; Docker daemon remains privileged.
- `CUDA-05F`: the real Rust supervisor was exercised under a distinct host UID with actual CUDA/Vulkan GPU workers, revocation, child faults and binary substitution. Four acquisitions retained; ten operational lab gates pass, release authorization NOT_QUALIFIED.

## Reproduce editorial qualification

```bash
python scripts/build.py
python scripts/check.py
python scripts/test_checks.py
python scripts/test_labs.py
```

`check.py` includes experiment-registry and paired-study source-to-dist consistency tests and negative falsifiers. It cannot substitute for independent access to private experiment evidence. Preserve the complete source run separately and never overwrite an observation to match an expected outcome.

**Research owner and external reviewer:** independent review is pending, not implicitly delegated to the assistant.
