# Command-Link Check — example report

This is a **worked example** of the free check, run on a stock ArduPilot build so that
anyone can reproduce it. A real check mirrors the customer's own firmware version and
parameter file; nothing else changes about the method.

- **Subject:** ArduPilot Copter 4.7.2 (`fb77356`), built from source, default parameters
- **Method:** software-in-the-loop, read-only probes only (`PARAM_REQUEST_READ`,
  `AUTOPILOT_VERSION`). No commands, no writes, no hardware touched.
- **Date:** 2026-11-03 · **Tool:** `mavaudit` (open source, this repository)
- **What this is not:** a certification, a penetration test, or a statement about a
  physical aircraft. It measures the firmware's command-link posture as shipped.

## Result

| Configuration | Score | Grade |
|---|---|---|
| Default, primary link (SERIAL0) | **14 / 100** | **E** |
| Signing enabled, primary link (SERIAL0) | 42 / 100 | D |
| Signing enabled, telemetry link (SERIAL1) | 70 / 100 | C |

Read the three rows together: enabling signing is necessary but, on the primary link,
not sufficient. 70/C is close to the practical ceiling for MAVLink (see *Ceiling*, below).

## Findings

**F1 — The default link accepts unauthenticated commands.** (CRA Annex I 2(d))
With default parameters, an unsigned `PARAM_REQUEST_READ` from an unknown sender is
answered. Any peer that can reach the link can also read and write parameters, upload
missions, arm, or trigger flight termination, because MAVLink does not distinguish a
legitimate ground station from any other sender.
*Reproduce:* `python -m mavaudit tcp:127.0.0.1:5760 --out /tmp/check`
*Fix:* provision a signing key (`SETUP_SIGNING`) over a trusted connection.

**F2 — With signing enabled, the primary channel still accepts unsigned commands.**
(CRA Annex I 2(d), and the reason the score stops at 42/D)
The firmware exempts channel 0 from signature checks, on the assumption that channel 0 is
USB. We measured that the exemption follows the **channel index, not the transport**: the
same network transport is accepted unsigned on channel 0 and rejected on channel 1
(`results/ch0-configs/`). Consequently, **if your radio or network port is wired to
SERIAL0, that port accepts unsigned commands while every other port is protected.**
This behaviour is tracked upstream as ArduPilot issue #34489; a fix (PR #34780) is
proposed but unmerged as of November 2026.
*Fix:* keep SERIAL0 for USB and move the radio to SERIAL1+, or carry the upstream patch.
*Check this first:* it is a wiring and parameter question, and costs nothing to correct.

**F3 — Unauthenticated file transfer is advertised.** (CRA Annex I 2(j))
The link advertises MAVLink FTP without authentication. Note also CVE-2026-32709
(unauthenticated path traversal in PX4's FTP implementation, fixed in 1.17.0-rc2) as an
illustration of what this surface costs when it goes wrong.
*Fix:* disable FTP on operational links, or require signing before FTP is served.

**F4 — Key provisioning is trust-on-first-use.** (CRA Annex I 2(d))
When no key is installed, the first `SETUP_SIGNING` to arrive sets the key — from any
peer, on any link. Whoever gets there first owns the aircraft.
*Fix:* provision out of band during production, never in the field.

## Score breakdown (default configuration)

| Criterion | CRA Annex I | Earned |
|---|---|---|
| Frames signed | 2(f) | 0 / 28 |
| Unsigned requests rejected | 2(d) | 0 / 24 |
| No unauthenticated service exposure | 2(j) | 0 / 16 |
| No unprotected MAVLink 1 | 2(b) | 10 / 10 |
| Out-of-band key provisioning | 2(d) | 0 / 12 |
| Payload confidentiality | 2(e) | 0 / 6 |
| Firmware identifiable (SBOM/advisories) | II.1 | 4 / 4 |

The weights are ours, fixed in advance, and documented in `mavaudit/score.py`. They are
not an official scale: the score is a rubric for comparing configurations, not a verdict.

## Ceiling

MAVLink 2 signing authenticates frames; it does not encrypt them, and a short list of
messages is always accepted unsigned. So payload confidentiality and part of the attack
surface cannot be earned at the protocol level. **A grade C may be as good as MAVLink
gets**; above that needs link-layer security (an encrypted radio, a VPN) underneath.
We would rather tell you that now than sell you a path to an A that does not exist.

## What we did not test

Radio hardware and its link-layer security · Remote ID broadcast over Bluetooth/Wi-Fi ·
DroneCAN/Cyphal peripheral bus · the companion computer's own interfaces (note that a
PX4 uXRCE-DDS bridge is unauthenticated by design and MAVLink signing does not protect
it) · bootloader and firmware-signature configuration · anything on physical hardware.

Each of these is in scope for the paid engagement where it is measurable; where it needs
hardware we say so rather than guessing.

## Next step

If this is useful, the paid engagement produces the **CRA technical file** for your own
self-assessment: your firmware and your parameters under test, each finding mapped to the
Annex I requirement it answers, the raw data and scripts so you can repeat every test,
and an explicit statement of what was not covered.

Method and evidence behind this report: four IEEE-format preprints in `papers/`, the
formal model in `mavaudit/model/`, and the recorded runs in `results/`.
