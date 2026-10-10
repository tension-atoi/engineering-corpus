---
id: study-cuda-05e
title: "Exercising a real host-UID authorization boundary"
status: draft
classification: bounded-internal-observation
---
# Exercising a real host-UID authorization boundary

> **Experimental study · 9 October 2026 · Draft pending review.** A disposable Docker lab observation, not a security certification or GPU supervisor deployment.

## Research question

Can a Linux service running under a **different host principal** from its client authorize that client, deny another principal that can connect to the socket, and block a third client through filesystem permissions?

## Criteria frozen before acquisition

Protocol **CUDA-05E-P01** was committed as `84f82a786d80981edd824a2d9c81f4bbfd105c71` before the trial. It independently tests three controls: actual service identity on the host, application authorization through `SO_PEERCRED`, and discretionary access control on the Unix socket.

The first setup attempt failed **before any identity observation**: `chmod` lacked sufficient authority after `chown`. A preregistered-protocol amendment was separately committed as `fbd752d322a148f6d83279bef5cf04b4f9436374` before new acquisition. It reordered operations without granting additional capabilities. The aborted setup remains in the research history.

## Observations from the completed trial

| Control or treatment | Observation | Limited interpretation |
|---|---|---|
| Service in a disposable Debian container | Its host UID differed from the permitted client's UID, corroborated by `/proc` and Docker configuration. | Actual host-principal separation for this fixture. |
| Authorized client | Connection allowed. | Positive control. |
| Rejected client with group-level socket access | Connection succeeded, then `SO_PEERCRED` authorization denied it. | Application UID rejection exercised. |
| Client without filesystem permission | Connection blocked before the server's `accept`. | DAC denial independent of application authorization. |
| Authorized client after rejections | Connection allowed again. | Service continuity in this test. |

The service-owned directory used mode `0710`; the socket used `0660`. This is **one completed experiment**, without statistical repetitions. No CUDA/Vulkan workload was included.

## What it does not establish

The Docker daemon remains privileged above the tested principals. Consequently, this does **not** qualify isolation against the host administrator, the real CUDA-05C Rust supervisor, physical GPU-loss recovery or production operations.

Full raw logs—including local process identity data—remain private. The public projection includes only bounded verdicts, a raw digest and pinned Git provenance. **A checksum cannot independently disclose private evidence.** External replication is not yet demonstrated.

**[Sanitized public observations](/evidence/cuda-05e-public-results.json)** · [Experiment registry](/en/experiments.html) · [Reusable experiment template](/templates/EXPERIMENT.md)

## Discriminating next experiment

Run the **actual CUDA-05C Rust supervisor** under a dedicated service principal, with truly permitted and rejected clients, without risking the desktop session or resetting its GPU. Independently qualify IPC permissions, worker confinement, native provider integrity and recovery behavior.

**Evidence class:** single internal E4 observation. **Production gate:** `DENIED`. **Status:** `draft`; independent review pending.
