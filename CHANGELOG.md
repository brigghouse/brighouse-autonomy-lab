# Changelog

## 0.2.2 (2026-11-03) — channel-0 exemption measured across transports

- `scripts/ch0_configs.py` + `results/ch0-configs/`: four ArduPilot 4.7.2 SITL
  configurations moving the transport of SERIAL0 and SERIAL1 independently (TCP/UDP)
  plus a MAVLink 1 port. Shows the unsigned-accept exemption follows the channel index,
  not the link type (ch0 over UDP accepts unsigned; ch1 over UDP rejects). 23/23 agree
  with the `ardupilot-4.7.2` policy. Regression test on the recorded data.
- Paper 1: new "Index, not transport" paragraph and Table (tab:ch0); MAVLink 1 port
  measured stricter than the documentation's wording.

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
