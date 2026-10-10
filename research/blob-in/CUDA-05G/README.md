# CUDA-05G — Independently implemented Linux IPC falsification kit

**Research state:** `one successful local controlled trial; external replication pending`.  **GPU state:** `NOT_RUN`. **Rust CUDA-05F replication:** `BLOCKED_PRIVATE_RUNTIME_SOURCE`. **GPU production authority:** `DENIED`.

This **MIT-licensed, complete and readable fixture** is intentionally different from the original CUDA-05F Rust supervisor. It allows a third party to test one narrower claim from CUDA-05E using independently authored Perl `SO_PEERCRED` socket code, a Python orchestration script, a source-independent validator and clear negative controls.

## Exactly what can be reproduced

A Linux server actually running as host UID 65534 accepts a different host account, rejects a same-group unauthorized UID **after** `accept`, rejects a different-group UID through socket directory/file **DAC before** `accept`, then serves the authorized account again. Verify these distinctions through actual server-observed Linux peer credentials, host `/proc` UID, exit codes, socket modes and cleanup. **This does not demonstrate CUDA/Vulkan calculation or CUDA-05F Rust isolation.**

## Requirements and safety

- Linux (including `/proc/<pid>/status`, filesystem UNIX sockets and `SO_PEERCRED`) on a machine you control.
- Python 3.9+, Docker with permission to run local containers, a non-root host operator, and cached `postgres:16` image with Perl core libraries. Use a test machine or carefully scoped workstation; a rootful Docker daemon has much broader authority than these test users.
- No GPU, internet access, secrets, external services or permanent host accounts. The experiment containers have no network, read-only rootfs, dropped capabilities and `no-new-privileges`. A **short** setup/cleanup helper has `CAP_CHOWN` only. Existing containers are not touched.
- The image tag is not a signed release guarantee. The acquisition reports the exact local Docker image ID; external trials using another digest are environment variations, not bit-identical reproductions.

**Preflight image availability** (do this yourself, not automatically inside the experiment):

```bash
docker image inspect postgres:16 --format '{{.Id}}'
docker run --rm --pull never --network none --read-only --cap-drop ALL \
  --security-opt no-new-privileges --entrypoint perl postgres:16 \
  -MSocket -MIO::Socket::UNIX -e 'print qq(READY\n)'
```

## Reproduce safely

Run from the cloned **public GitHub** repository. Keep raw outputs outside the repo. Avoid shared server Docker daemons and any production workload you do not control.

```bash
cd research/blob-in/CUDA-05G
python3 acquire.py --output /tmp/blobin-05g-observation-$(date -u +%Y%m%dT%H%M%SZ)
# Copy the resulting absolute raw.json location from stdout into RAW below.
RAW=/tmp/blobin-05g-observation-<your-UTC-run>/raw.json
python3 verify.py --raw "$RAW"
python3 verify.py --raw "$RAW" --public /tmp/cuda05g-public-projection.json
python3 validate_public.py
```

If any prerequisite is absent, you should report `BLOCKED` rather than downloading or altering your system without review. **`acquire.py` refuses to overwrite an existing `raw.json`**, and the private result must not be committed or pasted into a public issue without reviewing UIDs, paths and environment details. Make a new directory per trial.

## How to falsify this result

The preregistered H0/H1 and refusal criteria are in `PREREGISTRATION.md` at commit `396c36e7aef2271544bb98d025129c6de1a73547`. Relevant counterexamples include: server observed host UID equals the client, authorized caller is denied, unauthorized connected UID is allowed, DAC outsider reaches server `accept`, or service fails to continue after refusal. A negative run must include which control failed, its exact error, system/user-namespace mapping and a usable artifact (redacted if needed). The validator deliberately forges a server host UID and a peer UID and must reject both.

**Known failed measurement attempts:** `AMENDMENT-01.md` records an unavailable local image and improper no-op cleanup; `AMENDMENT-02.md` records an overlong host UNIX socket path and a mistakenly blocked test script. Both were fixed and separately committed **before** the successful third acquisition. These were instrument failures, not evidence for or against the Linux H1 claim.

## Reporting / attribution

Use the [public research Issue templates](https://github.com/tension-atoi/engineering-corpus/issues/new/choose) for **Independent replication** or **Counterexample**. Include the experiment ID, frozen protocol commit, implementation source SHA, image digest, host mapping, commands, negative controls, raw data or a principled reason it cannot be disclosed, and conflicts of interest. We welcome failures and contradictions.

`PUBLIC-RESULTS.json` includes the single successful local fixture's **sanitized** results. The original raw JSON remains internal, so the raw SHA is evidence of custody, **not proof of external reproducibility**. A third party must perform its own run. There are no public authoritative runtime or GPU samples hidden inside the kit.

## Files and traceability

- `PREREGISTRATION.md`, `AMENDMENT-{01,02}.md` — frozen protocol and documented deviations
- `server.pl`, `client.pl`, `acquire.py` — independently implemented disposable experimental apparatus
- `verify.py` — independently written, source-independent evidence evaluator with deliberate falsifiers
- `validate_public.py`, `SHA256SUMS.txt` — public package consistency, no raw input needed
- `PUBLIC-RESULTS.json` — sanitized single-trial findings; no host IDs/paths
- `CONTRACT.json` — strict gates and unqualified CUDA-05F boundary

Repository license: [MIT](../../../LICENSE). This license covers the new kit, **not** the unreleased private Rust experiment source.
