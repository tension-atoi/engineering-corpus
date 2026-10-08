---
id: lab-api
title: "Lab B — Verified API"
duration: 25
status: draft
category: lab
---
# Lab B — Publish an API without hallucinating

**Fictional scenario:** an agent writes an SDK page from a local Rust crate.

1. Pin commit and extract public exports with rustdoc/API tooling.
2. Classify each interface: `public-stable`, `public-experimental`, `internal`.
3. Generate a draft guide with an isolated local LLM.
4. Compile minimal code in `examples/` and verify used symbols.
5. Link each claim to a fitting E1/E2/other evidence record.
6. Produce FR and EN with reciprocal links and release notes.

<details><summary>Success criteria</summary>No invented symbols, no implicit cloud egress, examples compile, classification/limits are public, and human review is recorded.</details>
