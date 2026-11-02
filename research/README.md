# Research

This directory holds the evidence base for the four papers in [`../papers/`](../papers/README.md).

## Literature reviews (verified references)

- [`literature-review.md`](literature-review.md) — MAVLink security, CVEs, and the CRA/RED/2019-945 regulatory landscape (37 verified references).
- [`lit-review-2-formal-longitudinal-regulatory.md`](lit-review-2-formal-longitudinal-regulatory.md) — the three research gaps this programme fills, with search evidence and ~55 verified references:
  1. **Formal verification.** No prior work models the actual MAVLink 2 signing scheme (truncated MAC, per-stream timestamp window, `SETUP_SIGNING` TOFU) in any formal tool; the only MAVLink formal work models it *without* native authentication.
  2. **Longitudinal defaults.** Security-defaults evolution has been measured for TLS, Android, and OpenSSL, but never for a robotic/flight stack.
  3. **Regulatory crosswalk.** Published crosswalks are process-level; none maps CRA Annex I to *measurable protocol properties* or produces evidence by executing checks against an implementation.

## The model and its outputs

The executable acceptance-semantics model lives in [`../mavaudit/model/`](../mavaudit/model/); its computed outputs are in [`../results/model/`](../results/model/):

- `model-results.json` / `README.md` — property matrix from bounded exploration.
- `synthesis.json` / `SYNTHESIS.md` — minimal liveness-preserving remediations per policy.

## Measurements

- [`experiment-plan.md`](experiment-plan.md) — the cross-sectional plan (E1–E5).
- [`../results/`](../results/README.md) — cross-sectional audits, the longitudinal study, model outputs, conformance, and scores.

## How the gaps map to the papers

| Gap | Paper |
|---|---|
| Formal model of MAVLink signing | 3 (and the model section of 1) |
| Longitudinal flight-stack defaults | 2 |
| Measurable CRA crosswalk | 1 (crosswalk) and 4 (score) |

All references are verified against Crossref/arXiv/publisher pages; uncertain items are tagged `[VERIFY]`.
