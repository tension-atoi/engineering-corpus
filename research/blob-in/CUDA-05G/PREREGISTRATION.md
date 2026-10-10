# CUDA-05G-P01 — Independent Linux UID/IPC replication fixture

**Protocol status:** frozen before implementing or running the CUDA-05G fixture. This is a new, independent implementation of the *Linux identity / DAC* boundary investigated in CUDA-05E, **not** a replication of CUDA-05F GPU, native-provider integrity, or a production Rust system.

## Objective and falsifier

H0: with a service genuinely running under a different host UID from its caller, either the server cannot permit its intended caller, cannot reject an unauthorized but socket-connectable UID using kernel-reported `SO_PEERCRED`, cannot enforce the DAC barrier before `accept`, or cannot continue accepting an authorized caller after refusal. Any missing observation or unmet predicate falsifies successful replication in this environment.

H1 (bounded): a newly authored, finite, offline Perl Unix-socket server launched under host UID 65534, with owner-only directory mode 0710 and socket 0660, independently permits caller host UID as confirmed by `SO_PEERCRED`; denies a same-group but non-allowed UID 65533 after `accept`; a different-group UID 65532 cannot establish a socket connection; and a later permitted client is again served. For the setup, host user creates the temporary directory and sets mode 0710 *before* one ephemeral `CAP_CHOWN`-only helper assigns ownership to service UID 65534.

## Trial population / environment

One ephemeral server container and four client trials, Docker daemon locally available, Linux and cached `debian:trixie-slim` image, `--network none`, `--read-only`, all capabilities dropped in client/server, `no-new-privileges`, bounded memory/PIDs, bind-mounted dedicated ephemeral directory, no permanent account, no VPS connection, no GPU reset. Positive control = authorized / PING before and after rejection; connected negative = UID 65533 in allowed group; DAC negative = UID 65532 in different group. The server's host UID must be observed through `/proc/<container PID>/status`, not deduced from Docker's `--user` flag alone. Server MUST observe `SO_PEERCRED` UID 65533 for the connected denial. Parent/socket owner and access mode must be checked.

## Fixed rules and refusal conditions

- All **four** attempts and **exactly three** server accepts are required; the DAC denial is never counted as a server-side authentication decision.
- Server-observed peer UID and authorization decision MUST be logged internally, not inferred from a client invocation.
- Service and its clients must exit cleanly; no residual experiment containers or temporary directory ownership. No `docker run --privileged`, no host network, no password/secret environment read.
- Missing tools, inaccessible Docker, different user mappings, untrusted account assumptions, absent non-destructive cleanup, or unexpected crashes yield `NOT_QUALIFIED` or `BLOCKED`, never PASS.
- Report exact time, image immutable digest if available, Docker user namespace settings, UID quartet, directory/socket modes, commands' exit codes and private raw log. No raw host IDs in the public projection.
- A separately implemented offline validator must independently recompute the gates and reject at least two deliberate falsifications (forged host UID, reversed denied peer).
- A public checksum is **not** externally accessible raw evidence. Public claim stays narrow: reproducible fixture source and protocol, one local run, and limits; no statistical reliability inference.

## CUDA-05F boundary

CUDA-05F's private Rust supervisor, full native CUDA provider and private original measurements are **not released by this protocol**. Falsification proposals are welcome, but independent reproduction of CUDA-05F remains `BLOCKED_PRIVATE_RUNTIME_SOURCE`; a successful CUDA-05G fixture can only validate the kernel UID/DAC sub-hypothesis, not real CUDA/Vulkan parity, fault recovery or release authority.
