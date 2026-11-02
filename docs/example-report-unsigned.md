# mavaudit report

- Target: `udpin:127.0.0.1:14560`
- Scope reference: lab / private network
- Generated (UTC): 2026-11-02T14:30:14+00:00
- Observation window: 3.0 s

## Endpoints

| sysid/compid | autopilot | frames | MAVLink 1 | MAVLink 2 | signed |
|---|---|---|---|---|---|
| 1/1 | ardupilot | 16 | 0 | 16 | 0 |

## Findings

### MAV-002 [HIGH] No signed MAVLink frames (1/1)

0/16 frames carry a MAVLink 2 signature. Commands and telemetry on this link have no cryptographic integrity or origin authentication.

- CRA: Annex I.I.2(b) secure by default; Annex I.I.2(d) protection from unauthorised access; Annex I.I.2(f) integrity of data and commands
- Recommendation: Enable MAVLink 2 message signing with a per-vehicle key and a key-provisioning process.

### MAV-004 [INFO] No link-layer confidentiality (1/1)

MAVLink signing provides integrity only; payloads (position, mission, parameters) are sent in clear unless the radio link is encrypted.

- CRA: Annex I.I.2(e) confidentiality
- Recommendation: Use an encrypted datalink (e.g. AES-capable radio) or a VPN/tunnel for IP links; assess per threat model.

### MAV-005 [HIGH] Vehicle answers unsigned requests (1/1)

An unsigned PARAM_REQUEST_READ for 'SYSID_THISMAV' was answered by system 1. Unsigned peers can at least read configuration.

- CRA: Annex I.I.2(d) protection from unauthorised access; Annex I.I.2(j) limit attack surface
- Recommendation: Enable signing on the vehicle so unsigned messages are rejected.

---

_CRA references map findings to Regulation (EU) 2024/2847 Annex I as a technical interpretation; they are not legal advice or a conformity assessment._
