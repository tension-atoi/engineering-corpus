---
id: study-gnostral-rtx3070
title: "Gnostral — RTX 3070 qualification: MoE and memory-aware placement"
status: draft
classification: bounded-local-inference-experiment
---
# Gnostral — MoE inference under GPU memory pressure

> Repeated bounded local experiment, **no verified external reproduction**. Neither production qualification nor a GPU supervisory authority.

## Q-010: avoid repeated Q2_K/Q3_K CPU expert copies

Same Qwen3-30B-A3B Q2_K on an RTX 3070 8 GiB, three server launches per arm, naturally complete answers.

| Median | Original Strata | Q-010 candidate |
|---|---:|---:|
| Six-check response decoding | 9.51 tok/s | 20.18 tok/s |
| Total GPU card memory peak | 2,344 MiB | 2,351 MiB |
| Process-tree RSS | 22,094 MiB | 22,172 MiB |

Observed median throughput ratio is **2.12×**, with six byte-identical paired answers. However, the **first trial failed** its GPU ambient reclaim gate (+196 MiB for a 128 MiB limit). A second independent run with unchanged thresholds passed. The Rust unsafe borrowed-weight projection has not undergone a complete memory-safety audit. No superiority over llama.cpp is established.

## Q-011: GPU-aware placement at load time

A separate **2,048 MiB CUDA memory reservation**, without sustained competing GPU computation, changed placement for the same 48-layer model:

| Three starts | Control | GPU memory reserved |
|---|---|---|
| GPU layers | 22, 21, 21 | 13, 12, 13 |
| Median six-check decoding | 20.88 tok/s | 20.15 tok/s |

**Startup placement adaptation is observed**, not live remapping of loaded layers. PagedAttention was disabled for both mixed CPU/GPU configurations.

## Method, limitations and falsifiability

GPU memory is whole-card usage including desktop workloads; RSS is not private PSS. Three runs per condition cannot establish general performance. Q-011 text varied across starts: task structure was checked, not general answer quality. Raw logs and model weights are not distributed with this page; a private-data SHA alone does not establish public reproducibility.

**[Sanitized public observations](/evidence/gnostral-rtx3070-public-results.json)** · **[Research registry](/en/experiments.html)**

Statuses: external replication PENDING; mixed PagedAttention NOT_QUALIFIED; production authorization DENIED.
