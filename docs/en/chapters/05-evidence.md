---
id: 05-evidence
title: Evidence & public truth
duration: 16
status: draft
category: core
method_id: EC-M05
classification: proposed-principle
prerequisites:
- Git basics
- Reading a test result
artifacts:
- EVIDENCE.json; raw samples; median calculation; bounded claim.
success_criteria:
- Another reader obtains 10 ms from all five values. This teaching calculation is
  not a real benchmark; five samples cannot establish a reliable p95.
references:
- python-statistics
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


## Engineering problem
Fictional Beacon reports general latency from one favorable sample.

## Reproducible method
1. Define metric, unit and population
2. pin code and environment
3. warm up then run at least five repetitions
4. retain every sample
5. compute median and range
6. link the public statement to the manifest and exclusions.

**Responsibilities:** the author proposes and records results; the reviewer challenges the oracle; the consuming project owner decides adoption.

## Example, counterexample and failure
Fictional samples [9,10,10,11,100] ms: median 10 ms, range 9–100 ms. Counterexample: remove 100 without a predefined rule. Failure: engines use different sampling parameters; disclose the deviation and repeat a comparable experiment.

## Artifacts and qualification
EVIDENCE.json; raw samples; median calculation; bounded claim.

Another reader obtains 10 ms from all five values. This teaching calculation is not a real benchmark; five samples cannot establish a reliable p95.

## Transfer exercise
Apply this method to fictional Courier. Produce the artifacts above, then invent a case that invalidates an overbroad conclusion.

<details><summary>Transfer self-check</summary>The case is fictional and reproducible; baseline is identified; procedure and expected result are explicit; a failure is retained; the conclusion cites artifacts and limits. If any criterion is missing, revise before declaring the method applied.</details>
