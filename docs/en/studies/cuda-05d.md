---
id: study-cuda-05d
title: "Why namespace root does not prove a separate host identity"
status: draft
classification: bounded-internal-observation
---
# Why namespace root does not prove a separate host identity

> **Experimental study, 9 October 2026 · Not ratified · Partially reproducible externally.** This page reports a bounded result on one Linux workstation. It is not a certification of agent isolation or production security.

## Question

Does a process running as `root` inside a user namespace necessarily have a **different identity as seen by the host service**? The experiment distinguishes a process's namespace-local identity from the kernel identity returned by `SO_PEERCRED` on a Unix socket.

## Criteria frozen before collecting data

Protocol **CUDA-05D-P01** was committed as `ee0ea36bae0950c04e13100c7f53cf7e643c82c4` before acquisition. It specifies a baseline connection, a client launched with `unshare --user --map-root-user`, an automatic subordinate-UID mapping attempt, and independent evidence validation. Genuine host-principal isolation would require **different host UIDs**, a service running under another real identity, and both accepted and denied cross-UID access tests.

If those conditions are absent, the preregistered outcome is `NOT_QUALIFIED`. The standard is not revised to fit the observed result.

## Three observations on one workstation

| Trial | Observation | Supported scope |
|---|---|---|
| Baseline socket connection | The host server's peer UID equals the host process UID. | Measurement control passed. |
| Namespace `--map-root-user` | The client sees UID 0 **inside** its namespace, while `SO_PEERCRED` still sees **the baseline host UID**. | This namespace did not create a separate host principal here. |
| Subordinate mapping `--map-auto` | The attempt failed with `newuidmap: Could not set caps`. | Subordinate mappings are unqualified in this environment; the underlying cause is not established. |

These attempts were made **once on 9 October 2026**. They do not generalize to all Linux kernels, rootless container runtimes or machines with correctly delegated UID mapping.

## Observation, interpretation and authority

**Observed (E4, internal):** the identity comparison was captured through kernel peer credentials. **Interpretation:** namespace-local UID 0 is not evidence of host-level separation. **Engineering gate:** `NOT_QUALIFIED` for a distinct service principal; `DENIED` for production authorization. CUDA-05C separately demonstrates recovery after child-process faults, not physical GPU loss or different host-user accounts.

The method could be replicated elsewhere, but the complete source repository and raw traces remain internal. A checksum alone does not let an outsider verify unavailable evidence. The public data contains only derived outcomes and the internal raw-data digest—no hostname, numeric UID or PID.

**[Inspect structured observations](/evidence/cuda-05d-public-results.json)** · [Provenance and review-status manifest](/evidence/cuda-05d-manifest.json).

## Reuse the method

The downloadable **[EXPERIMENT research contract](/templates/EXPERIMENT.md)** separates preregistered hypotheses, controls, raw data, transformations, independent validation and publication authority. Negative outcomes must be retained, not erased.

## What would qualify the next claim

Use a **disposable** environment with two genuine host principals. Demonstrate an allowed and a rejected socket connection, preserve the `SO_PEERCRED` observations, and test GPU faults independently without endangering the graphical session. Retain timestamped logs, exit codes, data schema, negative outcomes and the exact reproduction procedure.

A failed hypothesis still yields useful evidence. Rewording it into a marketing promise does not turn it into certification.

## Publication gate

**Evidence class:** E4 for a single internal observation, not E5/E6. **Document status:** draft, independent review pending. **External access to complete sources:** not currently available. This study grants no agent authority.
