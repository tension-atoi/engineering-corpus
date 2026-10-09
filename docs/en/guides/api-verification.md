# Verify an interface before documenting it

A practical guide for distinguishing a **real exported symbol**, **tested behavior**, and **merely proposed API**. The example is deliberately fictional: it does not document any production Gnosix interface.

## 1. Start from source

[Lab B](/en/labs/02-api.html) provides the exercise. Its [api_lab.py fixture](/examples/api_lab.py) contains a symbol inventory and an observable assertion. `Queue.morph_to` is absent; `Queue.enqueue` is present in the fixture.

Consult the [pinned sources in the registry](/registry/guide-catalog.json) before reaching conclusions about freshness. A pinned revision establishes inspectable content, **not** SDK stability.

## 2. Run both cases locally

From the `engineering-corpus` repository root, with Python 3:

```sh
python3 examples/api_lab.py --symbol Queue.morph_to
# Expected exit: 1 (unknown symbol)
python3 examples/api_lab.py
# Expected exit: 0
python3 scripts/test_labs.py
```

The first failure is **intentional** and must be distinguished from a missing dependency or broken environment. Do not turn a passing teaching fixture into a guarantee about an external API.

## 3. Connect contract to evidence

Record: source SHA, requested symbol, result and exit status, test environment, and explicit limits. Classify `public-stable`, `public-experimental`, and `internal` separately; writing documentation does not grant a maturity status.

For a comparison with a public Rust interface, consult [EngineProvider v0](/en/api.html). That reference remains **experimental**, is not distributed as an SDK, and describes no HTTP endpoint. This guide's Python fixture does not qualify the Rust interface.

## 4. Review and publish

Write the same scoped conclusion in English and French, with reciprocal links and the correct maturity status. Do not publish private code, model weights, credentials, or private files. Proposed changes require separate source review.

**Evidence limit:** this guide demonstrates an educational method with a fictional program; it is not a certification or an installation guide for the Gnosix product.
