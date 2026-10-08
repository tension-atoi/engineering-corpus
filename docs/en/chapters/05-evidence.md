---
id: 05-evidence
title: "Evidence & public truth"
duration: 16
status: draft
category: core
---
# Evidence & public truth

> Status: methodological draft, to be adapted — not ratified in consuming projects.

## Match claims with evidence
A desktop screenshot proves a bounded visual observation; a Rust test proves an executable scenario; a benchmark proves a measure **in its environment**. None establishes stability of every API.

| Class | Meaning | Example | Limitation |
|---|---|---|---|
| E0 | Intention | signed mandate | no execution |
| E1 | Static | symbol + commit | no runtime success |
| E2 | Executable | reproduced test | bounded scenario |
| E3 | Measured | median, spread, hardware | environment-specific |
| E4 | Observed | dated trace/screenshot | one observation |
| E5 | Integrated | cross-module path | no sustained operation |
| E6 | Operated | monitored history | not universal proof |

### Publication rule
Every strong claim points to `claim_id`, `source_commit`, UTC date, environment, command, exit status, artifact hash, limitations and reviewer. Stale evidence must be requalified.

### Good measurement
Publish command, warmup, repetition count, hardware, CPU/GPU limits, variability and excluded cases. Throughput and p95 latency are not interchangeable.

### Exercise
A README claims "2% idle GPU" after one screenshot. What language and experiments are required?

<details><summary>Self-check</summary>Rephrase as a bounded observation. Require defined metric, instrumentation, samples, hardware, load, baseline and uncertainty for a general claim.</details>
