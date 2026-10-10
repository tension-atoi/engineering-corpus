# CUDA-05H-P01 — Independently implemented GPU geometry-compute witness

**Frozen before writing device kernels or making measurements.** Pre-registered test is an **independent arithmetic analogue**, not the unavailable private CUDA-02/03 signed-distance implementation or the CUDA-05F supervisor. Results cannot be promoted to CUDA-05F parity, fault isolation or production authorization.

## Hypothesis and falsification

Can a third party obtain **exact bitwise numerical agreement** among an independently implemented CPU Python oracle, a native compiled CUDA GPU kernel, and a native Vulkan 1.0+ compute shader executing on real physical GPU hardware, given an identical immutable 16-primitive binary scene, and distinguish deliberately corrupted results?

**H0:** a backend cannot compile, cannot select real GPU hardware, fails synchronization/readback, diverges at one or more 32-bit output samples, or fails to reject a mutated result. No partial PASS. **H1 (bounded):** on the same input, all three produce **exact** little-endian signed `int32` outputs for a 96×64 grid (6144 elements), and a separate validator rejects at least two controlled corruptions. The numeric workload is a simple **quadratic-distance surrogate** for signed-distance constructive geometry (not Euclidean SDF): for each primitive `(cx,cy,r,op)` compute `q=(x-cx)^2+(y-cy)^2-r^2` with only 32-bit signed integers; first op must be union (0), subsequent ops 0 union => `min`, 1 intersection => `max`, 2 subtraction => `max(current,-q)`. Coordinates within 0..95/0..63; radius 3..19. No arithmetic overflow permitted. For the CPU oracle, use independent Python code with no GPU libraries; for CUDA use an actual `__global__` kernel and explicit host-device memory copy; for Vulkan use a GLSL/SPIR-V compute shader with storage buffers and a native Vulkan host dispatcher. Do not call CPU oracle from a purported GPU backend.

## Frozen workload and methods

- Fixed deterministic 16-primitive binary fixture, **4 little-endian signed 32-bit integers per primitive**, generated from a disclosed deterministic formula; full fixture bytes and SHA-256 committed to Git before acquisition. Dimensions 96×64, exactly 6144 samples, output 24576 bytes.
- The binary fixture is loaded from the same file by all GPU backends, and CPU oracle reads identical bytes. Shader bounds checks must prevent out-of-bounds writes. Vulkan must select a **discrete or integrated GPU**; CPU or virtual adapters are not qualified. CUDA must report a real CUDA device.
- Build tools: native `nvcc`, C compiler and Vulkan loader/development headers, `glslangValidator`; no network dependency or container required. Each build/readback runs locally with a finite host-side deadline. GPU shader/kernel fault injection, GPU resets and privileged device changes are prohibited.
- Pass/fail: SHA256 computed on each output byte stream, exact byte comparison by a separate Python validator, no NaN/tolerance conversion. Reject at least (1) one-bit-flipped CUDA output, (2) truncated Vulkan output. Report elapsed host wall-clock separately (no performance-claim gate).
- Missing CUDA, Vulkan discrete/integrated adapter, required tools, permission or device is `BLOCKED`/`NOT_QUALIFIED`, never inferred PASS; a CPU-only participant can still run the oracle and validate the fixture/negative tests.
- Qualify on the actual host RTX3070 if hardware available, but never infer cross-vendor portability or physical-device fault recovery from one run.

## Provenance, output boundary and release

Keep local build binaries, GPU driver version, device identity, full raw outputs and logs **outside public Git**. Publish new independent MIT-licensed fixture, source, build commands, validator, pinned fixture and a sanitized JSON report of one trial including hashes and documented limitations. The existing private Rust GPU runtime is not copied or relicensed. Public research draft is allowed independently of GPU deployment; `cuda05f_runtime_replication=BLOCKED_PRIVATE_RUNTIME_SOURCE`, `cuda05f_gpu_parity=NOT_RUN`, `production_authorization=DENIED`. External independent replication remains **pending** until a third party performs and reports it.

**STOP:** preserve every negative trial before changes, amend protocol/instrument explicitly in Git, and rerun with a fresh unique observation identifier. Never rewrite previous raw results to GREEN.
