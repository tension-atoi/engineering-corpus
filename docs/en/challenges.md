---
id: independent-challenges
title: "Replicate. Refute. Improve the evidence."
status: draft
---
# Replicate. Refute. Improve the evidence.

An invitation to independent researchers: our published observations are **falsifiable hypotheses**, not claims you are expected to endorse. We seek independent reproductions, counterexamples, alternative methods, and carefully documented negative results.

**State: scientific research draft open to critique.** [The canonical GitHub corpus](https://github.com/tension-atoi/engineering-corpus) is public, and its Issues support authenticated independent critiques and counterexamples. Some replication kits remain incomplete and are labeled accordingly. Gitea is a prospective secondary mirror, **not** the submission authority.

## Three scientific challenges

### CUDA-05D — Linux identities and namespaces

Question: can a namespace-local root user be mapped to a distinct host principal? Our single trial did **not** demonstrate such a distinction. A valid counterexample must show the actual UID observed by the receiving service using `SO_PEERCRED`, together with a control.

[Study and limits](/en/studies/cuda-05d.html) · [Bounded public data](/evidence/cuda-05d-public-results.json)

### CUDA-05E — Socket authorization and DAC

Question: can a server running under a genuinely distinct host UID reject both a connected but unauthorized client and another client blocked by filesystem access rules before connection? We observed this within a disposable Docker laboratory and invite researchers to falsify its assumptions and boundary.

[Frozen preregistration](/challenges/protocols/CUDA-05E-PREREG.md) · [Study and limits](/en/studies/cuda-05e.html) · [Bounded public data](/evidence/cuda-05e-public-results.json)

### CUDA-05F — Rust GPU supervisor and fault recovery

Question: do identity and revocation gates still hold *together* through actual CUDA/Vulkan computation and child failures? Ten operational gates passed in a bounded laboratory, while three earlier runs revealed meaningful failures. Complete runtime source is **not yet available for independent public replication**.

[Frozen preregistration](/challenges/protocols/CUDA-05F-PREREG.md) · [Study and preserved failures](/en/studies/cuda-05f.html) · [Experiment contract](/experiments/GPU-EVIDENCE-CONTRACT-v1.json)

## How independent contributions will work

A falsifying result should identify a claim and frozen Git revision, specify the machine and controls, preserve raw observations including error conditions, identify the preregistered criterion it contradicts and supply reasonable reproduction instructions. Original authors should be able to respond without erasing or changing earlier results.

The [proposed contribution contract](/challenges/CONTRIBUTING.md) and [machine-readable challenge register](/challenges/registry.json) are available. **[Submit a replication or counterexample through GitHub Issues](https://github.com/tension-atoi/engineering-corpus/issues/new/choose)** (GitHub account required). CUDA-05F replication remains limited by unpublished runtime sources.

## Our commitment

We will distinguish **observation**, **independent replication**, **falsification**, **review**, and **production authorization**. Documented disagreement must remain addressable even when it refutes our own conclusion. A private-data checksum is not access to evidence, and no local verdict is a universal claim.
