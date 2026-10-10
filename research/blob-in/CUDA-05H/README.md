# CUDA-05H — Independent GPU arithmetic witness for blob.in research

**Status:** One locally qualified **real CPU + CUDA + Vulkan compute** run with 6144 signed-int32 elements identical across all backends. **External replication PENDING**. **Original private Rust runtime and SDF parity NOT_RUN**. **Production authorization DENIED**.

This **independently authored MIT-licensed** kit deliberately avoids copying private CUDA-02/03 sources. It implements a **quadratic-distance CSG proxy** (16 integer circles, min/max/subtraction) with three independently written execution paths. It is **not the original floating-point signed-distance kernel**; success establishes a public end-to-end GPU-dispatch/calculation/readback/verification witness, not CUDA-05F equivalence or fault isolation.

## Requirements

- CPU-only: Python 3.9+; clone this repository and run `python3 validate_public.py` and `python3 oracle.py --scene primitives.bin --out /tmp/05h-cpu.bin`. The oracle output **must** hash to `613845b6341e4491efce3be997853467213ef6687770495b0d2515329678961b`.
- CUDA: NVIDIA GPU with compatible CUDA Toolkit, `nvcc`, CUDA runtime/driver and compiler toolchain.
- Vulkan: real **discrete or integrated GPU** with Vulkan 1.0+ compute queue, Vulkan loader and development headers, `cc`, `glslangValidator`. Vulkan software CPU emulation is intentionally **not** considered an equivalent hardware reproduction.
- No containers, network, root permissions, GPU reset, local service or project build system required. This is intended for a machine the researcher owns. `run.py` compiles in the selected external evidence directory and refuses to store raw data inside the public kit.

## Frozen scene and preregistration

**Protocol:** `CUDA-05H-P01`, commit `b89b266829b396d5b9569e0cbb2cd38a04f603bb`. The checked-in `primitives.bin` is **256 bytes** (16 × `int32[4]`, little-endian), SHA-256 `77759079523ca127a4c24617b42a05a08c5a7c03ebdeb36b092b9ed91387fc86`. Dimensions 96 × 64; one signed 32-bit output per sample. The math is written out in [PREREGISTRATION.md](PREREGISTRATION.md). It uses only bounded integer operations: there is **no floating-point tolerance**. A single mismatched byte fails.

## Reproduction on actual GPU

```bash
cd research/blob-in/CUDA-05H
python3 validate_public.py              # source, contract, fixed public reference hashes
python3 oracle.py --scene primitives.bin --out /tmp/05h-cpu.bin
sha256sum /tmp/05h-cpu.bin              # compare to fixed reference above
python3 run.py --output-root /tmp/blobin-cuda05h-observations
# Observe the unique PRIVATE trial-<nonce>/raw.json path printed by run.py
RAW=/tmp/blobin-cuda05h-observations/trial-<nonce>/raw.json
python3 verify.py --raw "$RAW"          # independent full numerical comparison and two falsifiers
# Do not publish raw JSON unreviewed. The source has a sanitized PUBLIC-RESULTS.json.
```

A system without CUDA or a hardware Vulkan compute adapter can **validate the published source and run CPU oracle**, but must report missing GPU gates `BLOCKED`, not PASS. `run.py` exits nonzero and retains its `FAILED_OR_BLOCKED` private receipt if a tool/device is unavailable; it never downloads tools.

**Manual alternate builds** (in a private/outside-Git output directory):

```bash
mkdir -p /tmp/05h-build
nvcc -std=c++17 -O2 -o /tmp/05h-build/cuda cuda.cu
cc -std=c11 -O2 -Wall -Wextra -Werror vulkan.c -o /tmp/05h-build/vulkan -lvulkan
glslangValidator -V compute.comp -o /tmp/05h-build/compute.spv
/tmp/05h-build/cuda primitives.bin /tmp/05h-build/cuda.bin
/tmp/05h-build/vulkan primitives.bin /tmp/05h-build/compute.spv /tmp/05h-build/vulkan.bin
cmp /tmp/05h-cpu.bin /tmp/05h-build/cuda.bin
cmp /tmp/05h-cpu.bin /tmp/05h-build/vulkan.bin
```

## Refute it

A counterexample can be one mismatched signed-int32 sample, a backend incorrectly selecting a software Vulkan adapter, a device dispatch failure, a failure to reject tampered output or a wrong reference hash despite a valid scene. Include the exact compiler/driver/SPIR-V/CPU versions, committed source revision, fixture digest, raw output digest, device and command, controls and failed attempts. Use the [public GitHub scientific issue templates](https://github.com/tension-atoi/engineering-corpus/issues/new/choose).

The independent `verify.py` **recomputes** every oracle value in Python, checks actual CUDA/Vulkan hardware dispatch receipts, byte-for-byte outputs and source hashes, then deliberately flips a CUDA output bit and truncates a Vulkan output. Both MUST fail validation. It does **not** import the acquisition script or any GPU code. A public-only validator checks package files and verifies the CPU reference without a GPU.

## Single local observation (not external replication)

One 2026-10-10 UTC run on the host NVIDIA **GeForce RTX 3070** was qualified. All three output files were exactly **24,576 bytes** with SHA-256 `613845b6341e4491efce3be997853467213ef6687770495b0d2515329678961b`. Two deliberate corruptions were rejected. The actual signed-int32 output files, driver/tool stderr and complete raw JSON are **private and not available on the public website**; their SHA-256 checksums alone do not permit an independent audit of the original observation. Anyone can generate their own bytes from the public sources.

The result is **not** evidence of GPU reset tolerance, CUDA-05F supervisor confinement, floating-point CSG parity, portability to every GPU, numerical speed or production readiness. A distinct laboratory or researcher has not yet submitted an independent reproduction.

## Provenance and evidence

- [PREREGISTRATION.md](PREREGISTRATION.md) — fixed original hypothesis and stop gates at `b89b266…` before kernels were implemented.
- [CONTRACT.json](CONTRACT.json), [primitives.bin](primitives.bin) — numeric contract and frozen fixture.
- [oracle.py](oracle.py), [cuda.cu](cuda.cu), [compute.comp](compute.comp), [vulkan.c](vulkan.c) — fully published independent implementations.
- [run.py](run.py), [verify.py](verify.py) — local acquisition and separately implemented falsification.
- [PUBLIC-RESULTS.json](PUBLIC-RESULTS.json) — de-identified, bounded local result; never mistake for an external replication.
- [SHA256SUMS.txt](SHA256SUMS.txt), [validate_public.py](validate_public.py) — public source integrity, no private raw data needed.

MIT license applies to **this new kit through the corpus LICENSE**, not to any private runtime source.
