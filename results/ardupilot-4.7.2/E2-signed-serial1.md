# mavaudit report

- Target: `tcp:127.0.0.1:5762`
- Scope reference: lab / private network
- Generated (UTC): 2026-11-02T16:31:01+00:00 by mavaudit 0.2.0
- Passive observation window: 15.0 s
- Active read-only probe: yes

## Endpoints

| sysid/compid | autopilot | firmware | frames | MAVLink 1 | MAVLink 2 | signed | FTP advertised |
|---|---|---|---|---|---|---|---|
| 1/1 | ardupilot | - | 25 | 0 | 25 | 25 | - |

## Findings

### MAV-004 [INFO] No link-layer confidentiality (1/1)

MAVLink signing provides integrity only; payloads (position, mission, parameters) are sent in clear unless the radio link is encrypted.

- CRA: Annex I.I.2(e) confidentiality
- Recommendation: Use an encrypted datalink (e.g. AES-capable radio) or a VPN/tunnel for IP links; assess per threat model.

---

_CRA references map findings to Regulation (EU) 2024/2847 Annex I as a technical interpretation; they are not legal advice or a conformity assessment._
