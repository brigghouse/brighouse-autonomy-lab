# mavaudit findings reference

Each finding maps to Regulation (EU) 2024/2847 (Cyber Resilience Act), Annex I. The mapping is a technical interpretation, **not** legal advice or a conformity assessment.

| ID | Severity | Trigger | CRA Annex I | Typical fix |
|---|---|---|---|---|
| **MAV-001** | medium | Any MAVLink 1 frame from the endpoint. MAVLink 1 cannot carry a signature. | I.2(b) secure by default, I.2(f) integrity | Force MAVLink 2 on every port, then enable signing |
| **MAV-002** | high | No signed frame from the endpoint during the observation window | I.2(b), I.2(d) protection from unauthorised access, I.2(f) | Enable MAVLink 2 signing with per-vehicle keys and a provisioning process |
| **MAV-003** | medium | Some frames signed, some not | I.2(f) | Reject unsigned input beyond the minimum allow-list |
| **MAV-004** | info | Always reported: signing gives integrity, not confidentiality | I.2(e) confidentiality | Encrypted datalink or VPN where the risk assessment requires it |
| **MAV-005** | high | The vehicle answered mavaudit's **unsigned**, read-only `PARAM_REQUEST_READ` (by index 0). If every frame the vehicle sends is signed but it still answers, the report says so: a passive check alone would wrongly suggest the link is protected. | I.2(d), I.2(j) limit attack surface | Enable signing; make sure signing-exempt links (e.g. USB / channel 0) are physically trusted |
| **MAV-006** | high | `AUTOPILOT_VERSION` (requested unsigned) advertises `MAV_PROTOCOL_CAPABILITY_FTP` **and** unauthenticated peers are accepted | I.2(d), I.2(j) | Enable signing; disable or gate MAVLink FTP where not needed |
| **MAV-007** | info | Firmware version decoded from `AUTOPILOT_VERSION` | I.2(a) no known exploitable vulnerabilities, Part II(1) SBOM | Stay on a supported release; monitor advisories |

## Related advisories

mavaudit annotates findings with a small curated table (`mavaudit/advisories.py`). It is not a vulnerability scanner.

| Advisory | Attached to | Condition |
|---|---|---|
| [CVE-2026-1579 / CISA ICSA-26-090-02](https://www.cisa.gov/news-events/ics-advisories/icsa-26-090-02) | MAV-002 | PX4, no signed frames |
| [CVE-2026-32709 / GHSA-fh32-qxj9-x32f](https://github.com/PX4/PX4-Autopilot/security/advisories/GHSA-fh32-qxj9-x32f) | MAV-006 | PX4 below 1.17.0 with FTP reachable unauthenticated |
| [CVE-2020-10283](https://nvd.nist.gov/vuln/detail/CVE-2020-10283) | MAV-001 | MAVLink 1 present |

## What mavaudit sends

| Mode | Traffic sent by mavaudit |
|---|---|
| default (passive) | No MAVLink messages; mavaudit only listens. |
| `--active-probe` | 1× `PARAM_REQUEST_READ` (index 0) and 1× `COMMAND_LONG` / `MAV_CMD_REQUEST_MESSAGE` for `AUTOPILOT_VERSION`. Both are read-only. Only replies for index 0 from the probed vehicle count; the `COMMAND_ACK` result is recorded as corroboration. If the vehicle ignores the request, "FTP advertised" is reported as unknown. Not sent if the traffic came from outside the lab scope; on serial targets it requires `--authorized --scope-ref`. |

## Exit codes

| Code | Meaning |
|---|---|
| 0 | Scan completed (no `--fail-on` threshold reached) |
| 1 | No MAVLink traffic observed |
| 2 | Target refused by the scope guard |
| 3 | `--fail-on` threshold reached (useful as a CI gate) |
