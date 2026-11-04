# Does the unsigned-accept exemption follow the channel index or the link type?

ArduPilot Copter 4.7.2 SITL (`fb77356`), recorded 2026-11-03. Script: `scripts/ch0_configs.py`.
Policy under test: `ardupilot-4.7.2` from `mavaudit/model/configs.py` (trusted = {ch0}).

`accept_unsigned_callback` in `GCS_Signing.cpp` accepts any unsigned frame on
`MAVLINK_COMM_0`, "assumed to be secure channel. This is USB on ChibiOS boards". Upstream
issue #34489 / PR #34780 (unmerged as of 3 Nov 2026) point out that SERIAL0 is not USB on
every board. We vary the *transport* of channel 0 and channel 1 independently and probe each
with an unsigned `PARAM_REQUEST_READ` while a signing key is active.

| Config | SERIAL0 (ch0) | SERIAL1 (ch1) | keyed, unsigned read on ch0 | keyed, unsigned read on ch1 | model |
|---|---|---|---|---|---|
| A | TCP | TCP | **answered** | rejected | 6/6 |
| B | **UDP** | TCP | **answered** | rejected | 6/6 |
| C | TCP | **UDP** | **answered** | rejected | 6/6 |
| D | TCP | TCP, `SERIAL1_PROTOCOL=1` (MAVLink 1 probe) | **answered** | rejected | 5/5 |

Reading:

- **B vs C isolate the variable.** The same UDP transport is accepted unsigned when it is
  channel 0 and rejected when it is channel 1. The exemption follows the channel index,
  not the link type. On a board whose SERIAL0 is a telemetry radio or a network port,
  that port accepts unsigned commands while every other port is protected.
- **D measures the "MAVLink 1 ports are not protected" statement** in the ArduPilot
  signing documentation. In SITL 4.7.2 a port configured as MAVLink 1 *rejects* an
  unsigned MAVLink 1 read while a key is active (the frame cannot carry a signature and
  the channel is not channel 0). The documentation's statement is, at least for this
  build, stricter-sounding than the behaviour; we report the measurement, not the text.
  Note: unsolicited `PARAM_VALUE` broadcasts (index 65535) still flow on that port; the
  probe only counts a reply to its own request (`param_index == 0`).
  The wire version is **measured, not assumed**: each case records the first byte of the
  frame the probe sent (`wire_first_byte_sent`), and configuration D's `ch1` cases record
  `0xFE`, a genuine MAVLink 1 frame. This matters because pymavlink's
  `auto_mavlink_version` silently upgrades a connection to MAVLink 2 as soon as it
  receives a v2 frame, so a probe intended as v1 is only v1 if the port itself speaks v1.
  An earlier version of this record labelled the wire version from the configuration
  rather than from the frame; it is now taken from the frame, and a test asserts it.
- All 23 observations agree with the formal policy, which already models ch0 as the
  trusted link irrespective of transport.

## Every negative in this campaign is now an observed rejection, not a timeout

The first version of this experiment measured a **timeout** and recorded it as a
rejection. A silent link and a refusing autopilot are indistinguishable from the probe's
side, so "no reply in 5 s" was carrying the weight of "the policy refused" with nothing
behind it. That affected every negative case here, and those negatives are what the
channel-0 finding rests on.

The probe now runs two controls inside the same connection and the same window as the
negative result:

- **Liveness.** `HEARTBEAT` is broadcast and allowlisted by both stacks, so it arrives
  whether or not our frame was accepted. Heartbeats still arriving while our
  `PARAM_VALUE` does not means the peer was alive and chose not to answer.
- **Positive control.** A correctly signed read on the same link, immediately after. A
  policy that is refusing our unsigned frame must answer that one. If the control is also
  unanswered, the probe or the link is implicated and the case says nothing about the
  policy.

A negative is recorded as `rejected` only when both controls pass; otherwise the case is
`inconclusive`, carries its reason, and is excluded from the agreement counts rather than
scored as a refusal. `agree`/`total` now count decided cases only, and `inconclusive` is
reported beside them.

**Outcome of the re-run: 23 cases, 4 rejections, 0 inconclusive.** The three configurations
whose channel 1 runs MAVLink 2 recorded 5-6 heartbeats in the window *and* a positive
control that was answered, so those refusals are observed. The published finding survived
the check; the method it rested on did not, and that is the part we fixed.

**One case is weaker than the other three, and it should not be quoted as if it were not.**
In configuration D channel 1 is a MAVLink 1 port, which has no signature field, so the
positive control cannot run there at all. That rejection rests on liveness alone: 5
heartbeats, no reply. It is a weaker form of the same claim, and the record says so in
`positive_control.skipped_because` rather than leaving the absence to be noticed.

A side effect worth stating, because it closes a gap we had listed as open: the positive
control is also the **verification that key provisioning actually took**. Previously
`provision_signing` was never checked, so a failed key installation would have produced
exactly the pattern we would have read as a strict policy. In all four configurations the
signed read on channel 0 was answered, which is that check.

## Repeatability

The four configurations were run three times end to end on 2026-11-03. All three runs are
identical, byte for byte, over the full tuple of (state, link, signed, observed, wire byte)
for every case. The firmware's decision here is deterministic, and we checked rather than
assumed it.

## Limits

SITL is not a ChibiOS board nor a Linux board. The claim that this carries to real hardware
rests on where the code lives, which we checked: `accept_unsigned_callback` is in
`libraries/GCS_MAVLink/GCS_Signing.cpp`, shared code, and no `AP_HAL_*` directory in the
tree contains an override for it; the channel assignment is likewise shared
(`chan = MAVLINK_COMM_0 + instance`, `GCS_Common.cpp:146`). So a ChibiOS or Linux board runs
the same decision path. That is a source-derived argument, not a measurement: we have not
flashed a board, and we do not claim to have.

Read-only probes only; the simulator is started and stopped by the script.
