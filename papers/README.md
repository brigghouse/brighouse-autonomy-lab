# Papers

Four IEEEtran preprints, all reproducible from the data and models in this repository.
Figures and data tables are regenerated from `results/` before each build, so the PDFs
never drift from the measurements. Published as preprints on ResearchGate (CC BY 4.0);
none has been peer reviewed.

| # | Directory | Title | DOI |
|---|---|---|---|
| 1 | [`paper1-signing/`](paper1-signing/) | *Signed but Unprotected: A Formal and Empirical Study of MAVLink 2 Message-Signing Defaults and Their Bearing on the EU Cyber Resilience Act* | [10.13140/RG.2.2.20818.31689](https://doi.org/10.13140/RG.2.2.20818.31689) |
| 2 | [`paper2-longitudinal/`](paper2-longitudinal/) | *A Decade of Defaults: How "Secure by Default" Evolved in the MAVLink Flight Stacks (ArduPilot and PX4, 2016–2026)* | [10.13140/RG.2.2.27660.27529](https://doi.org/10.13140/RG.2.2.27660.27529) |
| 3 | [`paper3-formal/`](paper3-formal/) | *Acceptance Semantics for MAVLink 2 Signing: Bounded Symbolic Analysis and Model-Based Conformance Testing of Flight Stacks* | [10.13140/RG.2.2.20949.38885](https://doi.org/10.13140/RG.2.2.20949.38885) |
| 4 | [`paper4-score/`](paper4-score/) | *Scoring "Secure by Default": A Reproducible, CRA-Grounded Metric with a Drone Command-Link Instantiation* | [10.13140/RG.2.2.34371.16164](https://doi.org/10.13140/RG.2.2.34371.16164) |

What each one does and does not establish is stated in its own abstract; the short
version: Paper 2's *measured* evidence covers two releases, its *version-control*
evidence covers the decade, and Paper 1's CRA crosswalk claims no primacy.

## Build

```bash
pip install -e ".[dev]"            # from repo root
make -C papers all                 # regenerate data + figures, then compile all four
make -C papers paper1-signing      # one paper
```

Requires a TeX Live install with `IEEEtran`, `tikz`, `algorithm2e`/`algpseudocode`,
`booktabs`, and `latexmk`.

## How the papers relate

- **Paper 1** is the applied study: what current stacks do, interpreted through a
  compact acceptance model, mapped to the CRA. It is self-contained.
- **Paper 3** deepens the model into a formal treatment (operational semantics,
  soundness and depth-bounded completeness, a liveness-constrained remediation search,
  and model-based conformance testing). Papers 1 and 3 cross-reference.
- **Paper 2** extends Paper 1's cross-sectional measurement over the release history,
  grounded in version-control milestones.
- **Paper 4** turns the measured findings into a 0–100 score with a letter grade,
  released as code with a property-test suite; it depends on Papers 1 and 3 for its
  inputs and adds nothing new to the measurements.

## Data provenance

Every figure and table is produced by a script from committed data:

- `papers/common/make_figures.py` → `papers/common/figures/*.pdf` from `results/*/summary.json`
  and `results/model/model-results.json`.
- `scripts/longitudinal_report.py` → `papers/paper2-longitudinal/results_table.tex` and
  `fig_longitudinal.pdf` from `results/longitudinal/index.json`.
- `mavaudit/model/report.py` and `mavaudit/model/synthesis.py` → `results/model/`.

Nothing in the figures is hand-drawn. Bibliography: `papers/common/refs.bib` (verified
entries; see `research/literature-review.md` and `research/lit-review-2-*.md`).
