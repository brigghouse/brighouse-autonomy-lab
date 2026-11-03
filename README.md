# Brighouse Autonomy Security Lab

[![ci](https://github.com/brigghouse/brighouse-autonomy-lab/actions/workflows/ci.yml/badge.svg)](https://github.com/brigghouse/brighouse-autonomy-lab/actions/workflows/ci.yml)
![license](https://img.shields.io/badge/license-Apache--2.0-blue)

Defensive security research on **MAVLink drones and autonomous systems**, with a focus on what the **EU Cyber Resilience Act (CRA)** now requires from manufacturers. By [Ian Brighouse](https://www.linkedin.com/in/ian-brighouse-349548338) / Brighouse Security Labs.

This repository contains:

- **mavaudit**, a key-less MAVLink security auditor with CRA-mapped findings;
- a **reproducible SITL lab**: ArduPilot and PX4 built from source, headless, with no hardware or RF;
- **measured results** on ArduPilot Copter 4.7.2, PX4 v1.17.0 and PX4 v1.18.0-rc1;
- a **paper draft** and a referenced **literature review**.

## Key findings (2026-11-02, simulation)

| | ArduPilot 4.7.2 | PX4 v1.17.0 (stable) | PX4 v1.18.0-rc1 |
|---|---|---|---|
| Signing on by default | no | no | no |
| Unauthenticated parameter read answered (default) | yes | yes | yes |
| MAVLink FTP advertised to unauthenticated peer (default) | yes | yes | yes |
| Signing can be enabled | yes | **no: not in the release** | yes |
| After provisioning: unsigned input rejected | SERIAL1 yes; **SERIAL0 / channel 0 no, by design** | n/a | yes, on both links |
| Unsigned re-key after first key rejected | not tested | n/a | yes |
| Read-only FTP directory listing answered (default) | yes (25 B) | yes (101 B) | yes (110 B) |
| `mavlink_shell` present in the build (static check) | no | yes | yes |
| Unauthenticated second control plane (uXRCE-DDS) | none in this build | **yes** | **yes** |

Two of those rows need a word of care. The FTP row says *answered*, not merely advertised:
we asked for a directory listing and got one. The second-plane row is a measurement of a
build, not of a project — ArduPilot's source defaults `DDS_ENABLE` to 1 where the subsystem
is compiled in, and this SITL build does not compile it.

Details and raw data: [results/](results/README.md). Per-campaign write-ups, each with its
own limits section:

| | What it measures |
|---|---|
| [`results/ch0-configs/`](results/ch0-configs/README.md) | Whether ArduPilot's unsigned-accept exemption follows the channel index or the transport (it follows the index) |
| [`results/dds/`](results/dds/README.md) | The second control plane, and whether a MAVLink key reaches it (it does not) |
| [`results/surface/`](results/surface/README.md) | What each release answers to a peer that has presented no credential |
| [`results/allowlists/`](results/allowlists/README.md) | The exceptions to signing, extracted from source with file and line |
| [`results/scores/`](results/scores/README.md) | The secure-by-default score per configuration, criteria v2 |

## Research papers

Four reproducible IEEE-format papers build on this data and model (see [papers/](papers/README.md)):

1. **Signed but Unprotected** — measurement + a formal acceptance model + a CRA conformance crosswalk. The model, derived from reading `GCS_Signing.cpp`, reproduces the ArduPilot ch0 "signed yet unprotected" behaviour that the SITL measurement then confirms. (That behaviour is tracked upstream as [ArduPilot#34489](https://github.com/ArduPilot/ardupilot/issues/34489) with fix PR [#34780](https://github.com/ArduPilot/ardupilot/pull/34780), unmerged as of Nov 2026; our contribution is the independent measurement, the formal model and the CRA mapping, not the discovery. `results/ch0-configs/` adds the discriminating runs: the exemption follows the channel *index*, not the transport — SERIAL0 over UDP still accepts unsigned commands, SERIAL1 over the same UDP does not; 23/23 observations match the model.)
2. **A Decade of Defaults** — longitudinal study: signing was added to ArduPilot in 2016 and PX4 in 2026, and *never* shipped on by default.
3. **Acceptance Semantics for MAVLink 2 Signing** — bounded symbolic analysis + model-based conformance testing; a liveness-constrained search shows ArduPilot needs two independent fixes where PX4 1.18 needs one.
4. **Scoring Secure by Default** — a reproducible, CRA-grounded 0–100 metric that prices the ch0 pitfall numerically (50 vs 74) and states the bound plainly: a link configured as well as MAVLink 2 signing alone allows scores **82, grade B**, never higher. The last 18 points need out-of-band key provisioning (12) and link encryption (6), neither of which the protocol provides.

To our knowledge, no prior work gives a formal model of MAVLink signing, a decade-long measurement of flight-stack defaults, or a measurable CRA conformance score (see [research/](research/)). · Discussion: [paper draft](paper/paper1-draft.md) §7.

## mavaudit

```bash
pip install -e ".[dev]"
mavaudit scan --target tcp:127.0.0.1:5760 --duration 15 --active-probe --out reports/my-drone
mavaudit scan --target udpin:127.0.0.1:14550 --fail-on high      # CI gate, exit code 3
```

- **Passive by default.** It classifies every frame as MAVLink 1, unsigned MAVLink 2 or signed MAVLink 2, and never needs the key.
- **`--active-probe`** sends two read-only, unsigned requests (a parameter read and an `AUTOPILOT_VERSION` request). This catches links that sign everything they send but still accept unsigned input.
- **A worked example of the report** this produces is in [docs/example-free-check.md](docs/example-free-check.md), including the score breakdown, the protocol ceiling, and an explicit list of what was not tested.
- **Findings MAV-001 to MAV-007** come with CRA Annex I references and related advisories (CVE-2026-1579, CVE-2026-32709, CVE-2020-10283). See [docs/findings.md](docs/findings.md).
- **Scope guard:** loopback and private targets only. Before the active probe it also checks the address the traffic actually came from. An active probe over a serial port, which could go out over a telemetry radio, requires `--authorized --scope-ref <id>`.
- Markdown and JSON reports.

## Reproduce the lab

```bash
bash scripts/setup_sitl.sh ~/sitl            # ~25 min on 2 vCPU: ArduPilot + PX4 (SIH, no Gazebo)
source ~/sitl/venv/bin/activate && pip install -e .
python scripts/run_ardupilot.py --ardupilot ~/sitl/ardupilot --out results/ardupilot-4.7.2
python scripts/run_px4.py --px4 ~/sitl/px4 --out results/px4-1.18.0-rc1
# PX4 1.17.0: PX4_REF=v1.17.0 bash scripts/setup_sitl.sh ~/sitl-117, then run_px4.py --px4 ~/sitl-117/px4
python scripts/make_results_table.py
```

Full guide: [docs/setup.md](docs/setup.md) (Spanish: [docs/setup.es.md](docs/setup.es.md)).

## Repository map

| Path | What |
|---|---|
| [`mavaudit/`](mavaudit/) | The auditor; `mavaudit/sim/fake_vehicle.py` is the reference vehicle used in tests |
| [`tests/`](tests/) | 42 tests: auditor (unsigned, signed, signing-exempt and MAVLink 1 vehicles, advisories, exit codes, scope guard), the formal model (incl. conformance against recorded SITL observations) and the score (incl. the empty-run guard) |
| [`scripts/`](scripts/) | SITL build and experiment runners |
| [`results/`](results/README.md) | Measured data: reports, summaries, simulator logs |
| [`paper/`](paper/paper1-draft.md) | Paper 1 draft: MAVLink signing in 2026 and the CRA |
| [`research/`](research/) | [Literature review](research/literature-review.md) (20 academic references plus 17 regulatory and project sources, CVE tables) and [experiment plan](research/experiment-plan.md) |
| [`notebook/`](notebook/INDEX.md) | Lab notebook: diary, lessons learned, roadmap. Open the repo root as an Obsidian vault |
| [`docs/`](docs/) | Setup guides, the findings reference, and an example report |

## Responsible use

This is a **defensive** project. It contains no exploit code, no attack automation and no RF code. Note that on a serial telemetry radio the active probe *would* be transmitted, which is why it needs explicit authorisation there. Test only systems you own or are authorised in writing to test. Report new vulnerabilities to the affected project first; see [SECURITY.md](SECURITY.md). CRA mappings are technical interpretation, not legal advice.

## Cite

See [CITATION.cff](CITATION.cff). Code: Apache-2.0 ([LICENSE](LICENSE)). Paper, results and docs: CC BY 4.0. Changes: [CHANGELOG.md](CHANGELOG.md). Contributing: [CONTRIBUTING.md](CONTRIBUTING.md).
