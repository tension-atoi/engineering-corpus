---
id: study-cuda-05g
title: "CUDA-05G — Independently test a real Linux identity boundary"
status: draft
classification: independently-implemented-fixture-local-trial
---
# CUDA-05G — Independently test a real Linux identity boundary

> **Open research draft · one complete local trial · external replication pending.** This is **new independently implemented public code**, not a release of the original private blob.in Rust runtime. It tests one narrow Linux UID/DAC property previously examined in CUDA-05E.

## Falsifiable question

Can a Unix-socket server under a genuinely distinct host UID allow its intended caller, reject a connected but unapproved UID **after connection**, prevent an outsider from connecting through filesystem **DAC**, then serve the original caller again? The receiving server must log real kernel-supplied `SO_PEERCRED` credentials, and its actual host UID must be corroborated through `/proc`.

**Preregistered protocol:** commit `396c36e7aef2271544bb98d025129c6de1a73547`, experiment `CUDA-05G-P01`. New fixture code is distributed under the corpus MIT license.

## Observations, not endorsements

| Gate | Single local trial |
|---|---|
| Real host UID differs from caller | PASS |
| Initial allowed caller | PASS |
| Socket-connectable, unapproved UID | Server-observed DENIED |
| Different-group DAC outsider | Connection refused **before** server accept |
| Allowed client after denial | PASS |
| Server exit and cleanup | PASS |
| Independent checker falsification tests | Two forgeries rejected |
| Original CUDA-05F Rust supervisor and CUDA/Vulkan | **BLOCKED / NOT_RUN** |

Only **one completed trial** passed. Two earlier acquisitions remain documented as method failures: missing locally cached container image, followed by an overlong Unix socket path and an invalid DAC-negative fixture. Amendments preceded retries rather than rewriting the outcome.

## Replicate or challenge it yourself

The kit includes entirely new source, positive and negative controls, offline container orchestration, an independently authored evidence evaluator, SHA-256 source manifest and explicit falsification predicates.

**[Public source, protocol and reproduction instructions](https://github.com/tension-atoi/engineering-corpus/tree/main/research/blob-in/CUDA-05G)** · [Bounded public observations](/evidence/cuda-05g-public-results.json) · [Submit a counterexample](https://github.com/tension-atoi/engineering-corpus/issues/new/choose)

A researcher may rerun the fixture on **their own controlled Linux machine with rootful Docker**, retain original observations, and submit negative, divergent or uncertain results. Do not probe production systems for this research challenge.

## Boundaries

The implementation is open, **but no third-party independent replication has been received yet**. Rootful Docker remains a privileged ambient authority. No native CUDA provider, Vulkan calculation, GPU-loss event, CPU/GPU parity, or private CUDA-05F supervisor fault-recovery path was reproduced. The original raw observations remain private; their digest does not provide public access to that dataset.

**Conclusion:** a runnable falsification kit for the Linux IPC sub-hypothesis, **not** a GPU runtime reproduction, security certification or production authorization.
