# Lab setup

Everything runs on one Linux machine. No drone hardware, no radio, no GUI. Tested on Ubuntu 24.04 with 2 vCPU and 7 GB RAM; on Windows, use WSL2. (Spanish version: [setup.es.md](setup.es.md).)

## 1. mavaudit only (2 minutes)

```bash
git clone https://github.com/brigghouse/brighouse-autonomy-lab.git
cd brighouse-autonomy-lab
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest -q                                   # 10 tests against a reference MAVLink vehicle
```

Try it without any autopilot:

```bash
python -m mavaudit.sim.fake_vehicle --mode unsigned --port 14550 &   # also: --mode signed | v1
mavaudit scan --target udpin:127.0.0.1:14550 --duration 10 --active-probe
```

## 2. Real flight stacks in simulation (about 25 minutes of compiling)

```bash
bash scripts/setup_sitl.sh ~/sitl
source ~/sitl/venv/bin/activate && pip install -e .
```

The script builds:

- **ArduPilot Copter 4.7.2 SITL**: `~/sitl/ardupilot/build/sitl/bin/arducopter`
- **PX4 v1.18.0-rc1 SITL** with the **SIH** simulator, so Gazebo is not needed: `~/sitl/px4/build/px4_sitl_default/bin/px4`

Pick other versions with `AP_REF=Copter-4.6.3 PX4_REF=v1.17.0 bash scripts/setup_sitl.sh ~/sitl-old`.

## 3. Reproduce the published results

```bash
python scripts/run_ardupilot.py --ardupilot ~/sitl/ardupilot --out results/ardupilot-4.7.2
python scripts/run_px4.py      --px4 ~/sitl/px4       --out results/px4-1.18.0-rc1
python scripts/make_results_table.py
```

Each run takes 2-3 minutes. It starts a fresh simulator, audits each link with the default configuration, provisions the lab signing key, audits again, and verifies signatures with the key. For PX4 it also checks that an unsigned re-keying attempt is rejected.

## 4. Manual exploration

| Stack | Start | Audit |
|---|---|---|
| ArduPilot | `arducopter --model + -I0 -w --defaults Tools/autotest/default_params/copter.parm --serial1 tcp:2` | `mavaudit scan --target tcp:127.0.0.1:5760` (SERIAL0) or `:5762` (SERIAL1) |
| PX4 | `cd <rootfs> && PX4_SIM_MODEL=sihsim_quadx <px4>/build/px4_sitl_default/bin/px4 -d <px4>/build/px4_sitl_default/etc -w .` | `mavaudit scan --target udpin:127.0.0.1:14550` (GCS link) or `:14540` (onboard link) |

To use a GUI as well, QGroundControl, Mission Planner and MAVProxy (`mavproxy.py --master tcp:127.0.0.1:5760`) connect to the same ports.

## 5. Docker (optional, not built in CI)

[`docker/ardupilot/Dockerfile`](../docker/ardupilot/Dockerfile) builds the ArduPilot SITL image.

## Lab rules

1. Use simulation, a wired bench or a Faraday enclosure only. Never transmit RF or interfere with GNSS without a licence.
2. Test only your own systems, or systems you have written authorisation to test. mavaudit refuses public IP addresses by default.
3. Report new vulnerabilities to the maintainers first (coordinated disclosure). See [SECURITY.md](../SECURITY.md).
