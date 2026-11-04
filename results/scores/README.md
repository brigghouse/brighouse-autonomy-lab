# Secure-by-default scores

Computed by `mavaudit.score`, criteria set **v2** (axioms: provenance, monotonicity, CRA-grounded weights). 0--100; grade A--E. Scores from different criteria versions are not comparable.

v2 splits v1's single "unauthenticated service exposure" criterion into the MAVLink file-transfer surface (8) and a secondary control plane (8), measured by `scripts/dds_probe.py`. A build we never probed earns nothing for the latter and is marked as a lower bound.

## Cross-section

| Configuration | Score | Grade | |
|---|---|---|---|
| IDEAL (model target) | 100.0 | A |  |
| ArduPilot 4.7.2 SERIAL1 signed | 66.0 | C | lower bound (control plane not probed) |
| PX4 1.18 GCS signed | 66.0 | C |  |
| ArduPilot 4.7.2 ch0 signed | 42.0 | D | lower bound (control plane not probed) |
| ArduPilot 4.7.2 ch0 default | 14.0 | E | lower bound (control plane not probed) |
| PX4 1.17 GCS default | 14.0 | E |  |
| PX4 1.17 GCS provisioned | 14.0 | E |  |
| PX4 1.18 GCS default | 14.0 | E |  |

## Longitudinal (per release)

| Stack | Version | Default | Provisioned (best link) | Control plane |
|---|---|---|---|---|
| ardupilot | Copter-4.6.3 | 14.0 | 42.0 | not probed (lower bound) |
| ardupilot | Copter-4.5.7 | 14.0 | 42.0 | not probed (lower bound) |
| px4 | v1.16.2 | None | None | not probed (lower bound) |
