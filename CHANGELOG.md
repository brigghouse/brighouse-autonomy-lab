# Changelog

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
