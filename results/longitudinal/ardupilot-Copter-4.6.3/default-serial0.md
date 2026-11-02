# mavaudit report

- Target: `tcp:127.0.0.1:5760`
- Scope reference: lab / private network
- Generated (UTC): 2026-11-02T17:21:58+00:00 by mavaudit 0.2.0
- Passive observation window: 12.0 s
- Active read-only probe: yes

## Endpoints

| sysid/compid | autopilot | firmware | frames | MAVLink 1 | MAVLink 2 | signed | FTP advertised |
|---|---|---|---|---|---|---|---|
| 1/1 | ardupilot | 4.6.3 (type 255) | 24 | 0 | 24 | 0 | yes |

## Findings

### MAV-002 [HIGH] No signed MAVLink frames (1/1)

0/24 frames carry a MAVLink 2 signature. Commands and telemetry on this link have no cryptographic integrity or origin authentication.

- CRA: Annex I.I.2(b) secure by default; Annex I.I.2(d) protection from unauthorised access; Annex I.I.2(f) integrity of data and commands
- Recommendation: Enable MAVLink 2 message signing with a per-vehicle key and a key-provisioning process.

### MAV-006 [HIGH] MAVLink FTP advertised on an unsigned link (1/1)

The vehicle advertises MAV_PROTOCOL_CAPABILITY_FTP and this link accepts unauthenticated peers, so the file-transfer service is reachable without the signing key.

- CRA: Annex I.I.2(d) protection from unauthorised access; Annex I.I.2(j) limit attack surface
- Recommendation: Enable signing; disable or restrict MAVLink FTP in production builds where not needed.

### MAV-007 [INFO] Firmware version identified (1/1)

ardupilot firmware 4.6.3 (type 255). Track it against vendor advisories and the SBOM.

- CRA: Annex I.I.2(a) no known exploitable vulnerabilities; Annex I.II.1 SBOM
- Recommendation: Keep firmware on a supported release and monitor advisories (NVD, vendor GHSA).

### MAV-004 [INFO] No link-layer confidentiality (1/1)

MAVLink signing provides integrity only; payloads (position, mission, parameters) are sent in clear unless the radio link is encrypted.

- CRA: Annex I.I.2(e) confidentiality
- Recommendation: Use an encrypted datalink (e.g. AES-capable radio) or a VPN/tunnel for IP links; assess per threat model.

### MAV-005 [HIGH] Vehicle answers unsigned requests (1/1)

An unsigned PARAM_REQUEST_READ (index:0) was answered by system 1 with PARAM_VALUE. Unsigned peers are served by the parameter protocol, so they can at least read configuration.

- CRA: Annex I.I.2(d) protection from unauthorised access; Annex I.I.2(j) limit attack surface
- Recommendation: Enable signing on the vehicle so unsigned messages are rejected.

---

_CRA references map findings to Regulation (EU) 2024/2847 Annex I as a technical interpretation; they are not legal advice or a conformity assessment._
