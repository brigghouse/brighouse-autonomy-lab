# Command-Link Check — example report

This is a **worked example** of the free check, run on a stock ArduPilot build so that
anyone can reproduce it. A real check mirrors the customer's own firmware version and
parameter file; nothing else changes about the method.

- **Subject:** ArduPilot Copter 4.7.2 (`fb77356`), built from source, default parameters
- **Method:** software-in-the-loop. The probes are read-only (`PARAM_REQUEST_READ`, a
  capability request, an FTP directory listing). Two things are not reads, and we say so:
  the capability request is a `COMMAND_LONG`, and the rows below that show signing enabled
  required us to **install a signing key** on the simulator first, which is a write that
  changes persistent state. Both happen only on our own simulator, never on your aircraft.
- **Dates:** posture runs 2026-11-02; channel configurations and surface probes 2026-11-03/04 · **Tool:** `mavaudit` (open source, this repository)
- **What this is not:** a certification, a penetration test, or a statement about a
  physical aircraft. It measures the firmware's command-link posture as shipped.

## Result

| Configuration | Score | Grade |
|---|---|---|
| Default, primary link (SERIAL0) | **14 / 100** | **E** |
| Signing enabled, primary link (SERIAL0) | 42 / 100 | D |
| Signing enabled, telemetry link (SERIAL1) | 66 / 100 | C |

Read the three rows together: enabling signing is necessary but, on the primary link,
not sufficient. See *Ceiling* below for how high this can go at all.

## Findings

**F1 — The default link accepts unauthenticated commands.** (CRA Annex I 2(d))
With default parameters, an unsigned `PARAM_REQUEST_READ` from an unknown sender is
answered: that part is measured. The vehicle also *advertises* parameter writing, mission
upload and flight termination, which we did not exercise — a capability bit is an offer, not
a demonstration. What the measurement establishes is that the firmware has no way to tell a
legitimate ground station from any other sender, which is why the distinction between
advertised and exploited comes down to who is within range.
*Reproduce:* `python -m mavaudit scan --target tcp:127.0.0.1:5760 --active-probe --out /tmp/check`
(`--active-probe` is what asks the question; without it the unsigned read is never sent)
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
| No unauthenticated file transfer | 2(j) | 0 / 8 |
| No unauthenticated second control plane | 2(d) | 0 / 8 — **not established** |
| No MAVLink 1 frames emitted on this link | 2(b) | 10 / 10 |
| Out-of-band key provisioning | 2(d) | 0 / 12 |
| Payload confidentiality | 2(e) | 0 / 6 |
| Firmware identifiable (SBOM/advisories) | II.1 | 4 / 4 |

The weights are ours, fixed in advance, and documented in `mavaudit/score.py`. They are
not an official scale: the score is a rubric for comparing configurations, not a verdict.
The criteria set is versioned (this is v2); scores from different versions are not
comparable, and the version is reported with every result.

The second-control-plane criterion earns nothing here, and the reason matters. We probed
the port ArduPilot would use and captured no traffic, and the build does not answer for a
`DDS_ENABLE` parameter — both consistent with the subsystem not being compiled in. But
silence is not a measurement: it cannot distinguish a stack that offers nothing from a probe
that listened in the wrong place. So the criterion is unearned and this score is a **lower
bound**. On a PX4 build the same criterion scores zero for a different and firmer reason:
its uXRCE-DDS bridge was *observed* offering unauthenticated agent discovery, and a MAVLink
signing key does not reach it.

## Ceiling

MAVLink 2 signing authenticates frames; it does not encrypt them. A link configured as well
as signing alone allows — every frame signed, unsigned input rejected, file transfer closed,
no second plane, firmware identifiable — scores **82, a grade B**, and no higher. The
remaining 18 points are not in the protocol's gift:

- **12** for key provisioning, earnable only by distributing keys out of band in production.
  The in-band `SETUP_SIGNING` flow both stacks implement *is* the trust-on-first-use window
  this criterion penalises.
- **6** for confidentiality, which MAVLink 2 does not do at all. It needs an encrypted radio
  or a VPN underneath.

With out-of-band keys the ceiling is 94; only with link encryption as well is 100 reachable.
So the honest version is: **grade B is what signing alone can buy you, and the step to A is a
production practice and a radio, not a protocol fix.** We would rather tell you that now
than sell you a path to an A that does not exist.

## What we did not test

Radio hardware and its link-layer security · Remote ID broadcast over Bluetooth/Wi-Fi ·
DroneCAN/Cyphal peripheral bus · the companion computer's own interfaces (note that a
PX4 uXRCE-DDS bridge is unauthenticated by design and MAVLink signing does not protect
it) · bootloader and firmware-signature configuration · anything on physical hardware.

Two limits bear directly on what you just read, so they belong here and not in a footnote:

- **This is a POSIX/SITL build, and the MAVLink FTP code path differs by target.** The
  advisory for CVE-2026-32709 states that on POSIX targets — Linux companion computers and
  simulation — a write-path check that NuttX performs is skipped. Our probe only reads, so
  that difference does not bear on this result, but the FTP row describes the target we
  measured and should not be generalised to a NuttX flight controller.
- **The channel-0 result reaches hardware by argument, not by measurement**, as said above.

Each of these is in scope for the paid engagement where it is measurable; where it needs
hardware we say so rather than guessing.

## Next step

If this is useful, the paid engagement produces the **CRA technical file** for your own
self-assessment: your firmware and your parameters under test, each finding mapped to the
Annex I requirement it answers, the raw data and scripts so you can repeat every test,
and an explicit statement of what was not covered.

Method and evidence behind this report: four IEEE-format preprints in `papers/`, the
formal model in `mavaudit/model/`, and the recorded runs in `results/`.
