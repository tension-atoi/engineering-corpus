---
id: study-cuda-05f
title: "CUDA-05F — Testing the integrated GPU chain without erasing failures"
status: draft
classification: bounded-internal-observation
---
# CUDA-05F — Testing the integrated GPU chain without erasing failures

> **Local experimental study, October 2026 · Draft pending review.** The real Rust supervisor and CUDA/Vulkan workers were exercised in disposable containers. Laboratory qualification is not a system-wide security certification or deployment authorization.

## Research question

Can properties established separately in CUDA-05C and CUDA-05E hold **together in the actual Rust service**? The experiment combines a distinct host service identity, peer-authenticated IPC, grant revocation, worker fault recovery, and genuine GPU outputs checked against a CPU numerical oracle.

Protocol **CUDA-05F-P01** was committed before acquisition as `03ba7945fe6740b2cf35dc28656ba866f66c33fb`. The shared `gnu6.gpu-evidence-contract.v1` defines 11 independent gates and explicitly prevents test success from granting authority to publish or deploy.

## Results from the fourth acquisition

| Observed control | Result |
|---|---|
| Service under a different real Linux host principal | PASS |
| Authorized client, connected UID denial via `SO_PEERCRED`, DAC denial | PASS |
| Genuine CUDA dispatch, CPU numerical parity | PASS |
| Genuine Vulkan dispatch, CPU numerical parity | PASS |
| Worker crash, grant revocation, fresh GPU execution | PASS on both backends |
| Worker timeout, grant revocation, fresh GPU execution | PASS on both backends |
| Worker/native CUDA-provider same-path substitution | Refusal and restoration observed |
| Release or production authority | **NOT_QUALIFIED** |

**Ten of eleven gates passed within the operational laboratory scope.** The eleventh remains open because there is no production authorization.

## The three runs we did not hide

- **Run 01 — Vulkan RED.** The Rust service's ELF library lookup prevented adapter selection. A discriminating probe compared RUNPATH with transitive RPATH; the repair was separately recorded.
- **Run 02 — incomplete identity evidence.** The service denied an unauthorized client but did not retain the kernel-observed UID in its own log. We amended the instrument to record actual server-side `SO_PEERCRED` observations.
- **Run 03 — IPC lifecycle RED.** A disconnected client during a Vulkan crash scenario triggered a fatal `Broken pipe`. The supervisor was changed to revoke on failed response delivery rather than exit.

**Run 04** repeated all eight finite scenarios under the amended method. These are four archived acquisitions, **not four statistically interchangeable repetitions**.

## Evidence, scope and limits

The Rust server ran as a host UID distinct from its permitted client's identity. The Unix socket enforced filesystem permissions and the service rejected a connected but unauthorized UID using kernel-provided credentials. Each render used a disposable real GPU worker with CPU parity.

**69 cumulative Rust tests** passed, and an independently written validator verified kernel-peer observations, generation transitions, negative outcomes and SHA-256-covered evidence. A deliberately forged service host UID was rejected.

**Not established:** defense against a privileged Docker daemon, malicious same-UID workers, signed provider provenance, actual GPU device loss, long-duration availability, or production Gnosix integration. Native-provider refusal is behaviorally observed; the worker's specific internal error remained suppressed.

Private raw traces contain Linux identity data and remain internal. The public dataset is a deliberately narrow projection. **A digest does not provide independent access to private evidence.** External replication has not yet been demonstrated.

**[Sanitized structured data](/evidence/cuda-05f-public-results.json)** · [Provenance receipt](/evidence/cuda-05f-manifest.json) · [Experiment contract](/experiments/GPU-EVIDENCE-CONTRACT-v1.json) · [Registry](/en/experiments.html)

## Decision

**Evidence class:** one internal E4 integrated-system observation, not ratified. **Publication:** draft pending independent scientific review. **Deployment gate:** `DENIED`. The next study should test a truly confined worker and an independent service-authority policy; resetting the GPU driving the desktop remains out of scope.
