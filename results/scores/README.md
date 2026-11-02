# Secure-by-default scores

Computed by `mavaudit.score` (axioms: provenance, monotonicity, CRA-grounded weights). 0--100; grade A--E.

## Cross-section

| Configuration | Score | Grade |
|---|---|---|
| IDEAL (model target) | 100.0 | A |
| ArduPilot 4.7.2 SERIAL1 signed | 70.0 | C |
| PX4 1.18 GCS signed | 70.0 | C |
| ArduPilot 4.7.2 ch0 signed | 42.0 | D |
| PX4 1.17 GCS default | 20.0 | E |
| PX4 1.17 GCS provisioned | 20.0 | E |
| ArduPilot 4.7.2 ch0 default | 14.0 | E |
| PX4 1.18 GCS default | 14.0 | E |

## Longitudinal (per release)

| Stack | Version | Default | Provisioned (best link) |
|---|---|---|---|
| ardupilot | Copter-4.6.3 | 14.0 | 42.0 |
| ardupilot | Copter-4.5.7 | 14.0 | 42.0 |
