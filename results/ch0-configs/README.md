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
- All 23 observations agree with the formal policy, which already models ch0 as the
  trusted link irrespective of transport.

Limits: SITL is not a ChibiOS board nor a Linux board; what we measure is the firmware's
channel logic, which is shared across HALs. We have not measured a physical USB port.
Read-only probes only; the simulator is started and stopped by the script.
