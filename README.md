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

Details and raw data: [results/](results/README.md) · Discussion: [paper draft](paper/paper1-draft.md) §7.

## mavaudit

```bash
pip install -e ".[dev]"
mavaudit scan --target tcp:127.0.0.1:5760 --duration 15 --active-probe --out reports/my-drone
mavaudit scan --target udpin:127.0.0.1:14550 --fail-on high      # CI gate, exit code 3
```

- **Passive by default.** It classifies every frame as MAVLink 1, unsigned MAVLink 2 or signed MAVLink 2, and never needs the key.
- **`--active-probe`** sends two read-only, unsigned requests (a parameter read and an `AUTOPILOT_VERSION` request). This catches links that sign everything they send but still accept unsigned input.
- **Findings MAV-001 to MAV-007** come with CRA Annex I references and related advisories (CVE-2026-1579, CVE-2026-32709, CVE-2020-10283). See [docs/findings.md](docs/findings.md).
- **Scope guard:** loopback and private addresses only, unless you pass `--authorized --scope-ref <id>`.
- Markdown and JSON reports.

## Reproduce the lab

```bash
bash scripts/setup_sitl.sh ~/sitl            # ~25 min on 2 vCPU: ArduPilot + PX4 (SIH, no Gazebo)
source ~/sitl/venv/bin/activate && pip install -e .
python scripts/run_ardupilot.py --ardupilot ~/sitl/ardupilot --out results/ardupilot-4.7.2
python scripts/run_px4.py --px4 ~/sitl/px4 --out results/px4-1.18.0-rc1
python scripts/make_results_table.py
```

Full guide: [docs/setup.md](docs/setup.md) (Spanish: [docs/setup.es.md](docs/setup.es.md)).

## Repository map

| Path | What |
|---|---|
| [`mavaudit/`](mavaudit/) | The auditor; `mavaudit/sim/fake_vehicle.py` is the reference vehicle used in tests |
| [`tests/`](tests/) | 10 tests: unsigned, signed and MAVLink 1 vehicles, advisories, exit codes, scope guard |
| [`scripts/`](scripts/) | SITL build and experiment runners |
| [`results/`](results/README.md) | Measured data: reports, summaries, simulator logs |
| [`paper/`](paper/paper1-draft.md) | Paper 1 draft: MAVLink signing in 2026 and the CRA |
| [`research/`](research/) | [Literature review](research/literature-review.md) (20 references, CVE tables, regulation) and [experiment plan](research/experiment-plan.md) |
| [`notebook/`](notebook/INDEX.md) | Lab notebook: diary, lessons learned, roadmap. Open the repo root as an Obsidian vault |
| [`docs/`](docs/) | Setup guides and the findings reference |

## Responsible use

This is a **defensive** project. It contains no exploit code, no attack automation and no RF tooling. Test only systems you own or are authorised in writing to test. Report new vulnerabilities to the affected project first; see [SECURITY.md](SECURITY.md). CRA mappings are technical interpretation, not legal advice.

## Cite

See [CITATION.cff](CITATION.cff). Code: Apache-2.0 ([LICENSE](LICENSE)). Paper, results and docs: CC BY 4.0. Changes: [CHANGELOG.md](CHANGELOG.md). Contributing: [CONTRIBUTING.md](CONTRIBUTING.md).
