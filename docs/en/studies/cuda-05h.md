---
id: study-cuda-05h
title: "CUDA-05H — An inspectable, falsifiable CPU/CUDA/Vulkan compute witness"
status: draft
classification: independent-public-numeric-witness
---
# CUDA-05H — An inspectable, falsifiable CPU/CUDA/Vulkan compute witness

> **Open research, one local hardware trial.** An independently implemented MIT-licensed project runs an identical frozen binary scene through Python CPU, native CUDA and native Vulkan compute. **External replication is pending**; the original private blob.in engine is neither released nor reproduced.

## Preregistered hypothesis and numerical workload

Protocol **CUDA-05H-P01** was frozen **before** implementing device kernels at Git commit `b89b266829b396d5b9569e0cbb2cd38a04f603bb`. The fixture contains 16 immutable primitives over a 96 × 64 grid. Each primitive has a center, radius and union/intersection/subtraction operation. The expression `q=(x-cx)²+(y-cy)²-r²` is an **integer quadratic geometry proxy**, **not** the private engine's floating-point signed distance algorithm.

**Pass criterion:** exactly **6,144 signed 32-bit outputs** or **24,576 bytes**, bitwise identical across CPU, CUDA and Vulkan, with zero tolerance. One mismatching byte falsifies parity. Vulkan must dispatch on a discrete or integrated **physical GPU**, not on a CPU software adapter.

## RTX 3070 observations

| Backend / negative control | Observed behavior | Verdict |
|---|---|---|
| Independently recomputed Python CPU oracle | Full 6,144 values | PASS |
| Native compiled CUDA | RTX 3070 CUDA GPU kernel, sync/readback | PASS |
| Native Vulkan/SPIR-V | RTX 3070 GPU compute and fence/readback | PASS |
| Bit-flipped CUDA output | Independent checker rejects it | PASS |
| Truncated Vulkan output | Independent checker rejects it | PASS |

All three output files share SHA-256 `613845b6341e4491efce3be997853467213ef6687770495b0d2515329678961b`. The separately implemented numerical checker reports **8/8 operational gates**. A public-only source/CPU reference validator runs without GPU drivers.

## Independent replication and counterexamples

**[Full new CPU, CUDA, GLSL, Vulkan code and reproduction protocol](https://github.com/tension-atoi/engineering-corpus/tree/main/research/blob-in/CUDA-05H)** · [Structured public observations](/evidence/cuda-05h-public-results.json) · [Submit a replication or counterexample](https://github.com/tension-atoi/engineering-corpus/issues/new/choose)

A CPU-only researcher can reproduce the CPU oracle and check the source manifest, but **cannot claim GPU parity**. Report exact GPU/driver/compiler versions, shader parameters, output digests, negative controls and unsuccessful attempts. No production system probing, privileged host changes or GPU reset is required.

## Validity limits

This is an **independently written GPU compute witness**, not a reproduction of the original CUDA-02/03 signed-distance renderer, the CUDA-05F Rust supervisor, worker isolation or cross-vendor reliability. Local raw samples/tool logs remain private, and their public hashes do not provide external access. Researchers can generate their own raw outputs using the fully published source code.

**Exact statuses:** external replication `PENDING`; original CUDA-05F `BLOCKED_PRIVATE_RUNTIME_SOURCE`; CUDA-05F GPU parity `NOT_RUN`; production authorization `DENIED`.
