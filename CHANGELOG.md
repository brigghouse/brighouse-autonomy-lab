# Changelog

## Unreleased

- Paper 1: the abstract no longer says "no prior work has stated precisely or
  measured end to end" — the related-work section already credits PAVE-MAVLink
  with formal verification and hardware testing, so the abstract contradicted it.
  It now claims only the parameterised semantics measured across stacks.
- Paper 1: CISA advisory ICSA-26-090-02 is now cited where CVE-2026-1579 is named.
- Papers 1 and 3: two tables/definitions overflowed the column by ~45 pt; fixed.
- papers/Makefile built three of the four papers; it now builds all four.

Corrections, not features. Everything below removes a claim or dates one; nothing
new is measured.

- **Withdrawn.** G6's ArduPilot half ("offers none") was absence of evidence: the
  probe captured no datagrams on a POSIX/SITL build and the silence was read as a
  result. Recorded as **not established** in the README, the paper and
  `results/dds/README.md`. The score it fed is a lower bound.
- **Withdrawn.** Two primacy claims, one in each of Papers 1 and 2, after a
  documented novelty search found prior work. Both papers now say what the evidence
  spans instead of who got there first.
- Positive control on the channel-0 probe: a case counts as `rejected` only when a
  HEARTBEAT from system 1 was seen in the window *and* a signed control read
  answered on the same link. Undecided cases are `inconclusive` and excluded from
  the agreement count. 23 cases, 4 rejections, 0 inconclusive.
- `scripts/surface_probe.py --repeat` (default 3); all three builds identical
  across runs.
- Score figures take their date from `results/scores/scores.json`, which
  `scripts/scores.py` now stamps. The date was previously typed into the generator
  and had already gone stale.
- `results/ardupilot/` removed: it was a two-second accidental run committed as
  evidence. Documented in `results/README-provenance.md`.
- CREDITS: the terminal figure was described as verbatim tool output; it was
  composited. Corrected, and the figure regenerated from a real run.
- 53 tests.

## 0.3.0 (2026-11-03) — gaps measured, score v2, a wrong ceiling corrected

- **Correction.** The "protocol ceiling" was stated as "near 70, grade C" in Paper 4, on
  the web page and in the example report. It was wrong: it quoted the best score measured
  (74) as though it were a bound. The real bound under MAVLink 2 signing alone is **82,
  grade B**; out-of-band keys raise it to 94 and link encryption to 100. Corrected
  everywhere and pinned by a test.
- G6: `scripts/dds_probe.py`, passive XRCE decoding; PX4 1.17/1.18 offer unauthenticated
  agent discovery, ArduPilot 4.7.2's build offers none.
  **Withdrawn 2026-11-04:** the ArduPilot half of that sentence was absence of evidence.
  The probe captured no datagrams and we read the silence as a clean result; it is now
  recorded as inconclusive and the score it fed is a lower bound. See README and
  `results/dds/README.md`.
- G10: `scripts/surface_probe.py`; all three runnable releases answer an FTP directory
  listing to an unauthenticated peer; `mavlink_shell` present in PX4 builds only.
- G7/G8: `scripts/allowlists.py` extracts both stacks' unsigned-accept allowlists from
  source with file/line provenance. Neither allowlists Remote ID messages.
- Score criteria v2 (`SCORE_VERSION`): attack surface 16 -> file transfer 8 + second
  control plane 8. Unprobed criteria earn nothing and the score is flagged a lower bound.
- Model: wire version added as a frame attribute and `v1_bypasses_signing` as a policy
  parameter, with `ardupilot-4.7.2-doc` encoding the documentation's reading. The
  measurement refutes it, and the parameter changes the repair cost (Paper 3).
- `scripts/synthesis_report.py` generates SYNTHESIS.md, which was previously hand-written.
- Papers: all four rebuilt. P1 gains the second-control-plane finding; P2 gains F5/F6
  (surface does not shrink; the release that added signing left the second plane open);
  P3 turns a stated limitation into a result; P4 gains the control-plane criterion and the
  ceiling correction.
- 51 tests.

## 0.2.2 (2026-11-03) — channel-0 exemption measured across transports

- `scripts/ch0_configs.py` + `results/ch0-configs/`: four ArduPilot 4.7.2 SITL
  configurations moving the transport of SERIAL0 and SERIAL1 independently (TCP/UDP)
  plus a MAVLink 1 port. Shows the unsigned-accept exemption follows the channel index,
  not the link type (ch0 over UDP accepts unsigned; ch1 over UDP rejects). 23/23 agree
  with the `ardupilot-4.7.2` policy. Regression test on the recorded data.
- Paper 1: new "Index, not transport" paragraph and Table (tab:ch0); MAVLink 1 port
  measured stricter than the documentation's wording.
- Paper 3: the four configurations folded into the conformance experiment
  (24 -> 47 recorded decisions; 20 unkeyed tautological, 4 negative control,
  23 discriminating keyed, 7 observed rejections). New paragraph arguing that
  the B/C pair is a controlled single-variable experiment rather than mere
  agreement, and that configuration D agrees for a reason the model does not
  represent (no wire-version parameter) - recorded as a limit of the model.

## 0.2.1 (2026-11-03) — honesty pass after independent audit

- **Score**: a run that observed no frames and whose probe never completed is now *unscorable* (`score: null`, `grade: "N/A"`, `insufficient_data: true`) instead of being graded. Previously an empty PX4 v1.16.2 run scored 42/D, above devices that actually ran and were insecure. Regression test added; `results/scores/*` regenerated.
- **Synthesis**: the greedy remediation search never counts no-op edits (e.g. enabling a check already on), only adds an edit that strictly reduces the failure count, iterates in a fixed order (deterministic across hash seeds) and records ties as `min_edits_alternatives`. px4-1.17 now correctly reports *no* incremental fix; ArduPilot's second edit is `drop-trusted-links` *or* `no-unsigned-rekey`. `results/model/synthesis.json` and `SYNTHESIS.md` regenerated.
- **Conformance test** now compares each model prediction with the `observed` field recorded in `results/conformance/*.json` (24 cases) and counts the discriminating keyed rejections (3), instead of a hand-copied prediction vector. Labelled as a recorded (non-CI) experiment.
- **Papers**: the ArduPilot channel-0 exemption is cited as upstream prior art (issue #34489, unmerged fix PR #34780); the 24/24 headline is reported with its evidential weight (12 tautological unkeyed cases, px4-1.17 as negative control); depth-bounded completeness is stated relative to the restricted adversary move set; the k=3 fixpoint is called empirical and the visited-set is noted not to prune; remediations are "greedy-minimal" with alternatives; Paper 4 states the ~70/C protocol ceiling and that two score inputs are analyst-declared; Paper 2 states n=2 measured releases and cites primary texts for CRA/RED dates. "First" claims are now "to our knowledge, the first".
- README: 42 tests; the ch0 model is described as source-derived, not a blind prediction. `.zenodo.json` added for the Zenodo DOI deposit. Fixed an `(A and B) or C` precedence bug in a test.
- Verified against NVD: CVE-2026-1579, CVE-2026-32709 (fixed in 1.17.0-rc2), CVE-2020-10283.

## 0.2.0 (2026-11-02)

- Active probe now requests parameter **index 0**, so it does not depend on parameter names (ArduPilot 4.7 renamed `SYSID_THISMAV` to `MAV_SYSID`). `PARAM_ERROR` also counts as an answer.
- New finding **MAV-006** (MAVLink FTP reachable by unauthenticated peers) and **MAV-007** (firmware version), from `AUTOPILOT_VERSION`.
- **MAV-005** now explains when a link signs everything it sends yet still accepts unsigned input.
- Curated advisory annotations: CVE-2026-1579, CVE-2026-32709, CVE-2020-10283.
- `--fail-on <severity>` (exit code 3) for CI, and `--json`.
- Header fields are read from raw frames, so message IDs unknown to pymavlink are attributed correctly. Uses the `all` dialect.
- Reproducible SITL lab (`scripts/setup_sitl.sh`) and experiment runners; results for ArduPilot 4.7.2, PX4 1.17.0 and PX4 1.18.0-rc1.

## 0.1.0 (2026-11-02)

- First version: MAVLink 1, unsigned and mixed-signing detection, unsigned parameter-read probe, CRA mapping, scope guard, reference vehicle and tests.
