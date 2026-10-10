# Independent verification & contradiction — proposed public contribution contract

**State: OPEN FOR CRITIQUE on the public GitHub source repository through its already enabled Issues.** Independent reproduction of CUDA-05F remains limited by non-public runtime sources.

This space is intended for researchers with no employment, project or institutional relationship to gnu.in.labs. A failed reproduction or a falsifying result is welcome. Attribution, contradictory evidence, negative controls, and disagreement with our interpretation must remain visible.

## Minimum submission package

1. **Claim being challenged:** stable experiment ID, precise claim, frozen source/protocol commit and optional alternative hypothesis.
2. **Independence:** declare whether instrumentation/code was copied, adapted or written independently; describe conflicts of interest and any assistance from the original authors.
3. **System and procedure:** OS/kernel, driver/GPU/runtime, permissions, exact commands and sequence, controls, inclusion criteria, attempts and repetitions; redact personal details and credentials.
4. **Original results:** raw timestamps, exit codes, standard output, measured units, errors and negative runs, data file SHA-256. Provide complete observations or explain constraints; a digest alone does not disclose private material.
5. **Falsification:** show which preregistered decision criterion is contradicted. Report cases of NOT_RUN/UNKNOWN/NOT_QUALIFIED without treating them as PASS.
6. **Reproduction kit:** runnable, licensed code/fixtures or a clear, isolated algorithm; instructions for deterministic and real-hardware stages. No production host changes or destructive GPU reset required.
7. **Review:** scientific or security concern receives a public issue with acknowledgement, reproduction attempt, dissenting interpretation and resolution/status. Do not alter past recorded data to hide failures.

## Public submission and privacy boundaries

- **Canonical collaboration:** [tension-atoi/engineering-corpus](https://github.com/tension-atoi/engineering-corpus), via authenticated [GitHub Issues](https://github.com/tension-atoi/engineering-corpus/issues/new/choose) and pull requests. GitHub sign-in is required to submit; reading the public repo needs no account.
- **Secondary mirror:** Gitea on the VPS is not yet configured as an anonymous-readable mirror. It is **not** the upstream collaboration surface, and no mirrored Issues or PRs are claimed.
- Freeze a public research protocol and provide licensed safe fixtures before claiming full reproducibility. CUDA-05E currently provides its frozen protocol but not a complete runnable kit; CUDA-05F exposes its protocol/contract and sanitized results but **not the full private Rust supervisor or raw host data**.
- Do not submit secrets, private host identifiers, unreleased runtime sources, credentials or instructions targeting production infrastructure.
- Preserve failures, alternative explanations and dissent. A research draft may be published before peer review, whereas production authorization remains independent and DENIED.
- Suggested labels: `replication`, `counterexample`, `failed-reproduction`, `methodology`, `new-experiment`, `needs-evidence`, `accepted`, `unresolved`.

A public challenge remains a scientific question, not an invitation to attack live services. Use independently controlled laboratory machines and safe non-destructive fixtures.
