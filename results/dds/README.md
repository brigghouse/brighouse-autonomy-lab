# The second control plane: is it authenticated?

Recorded by `scripts/dds_probe.py` on 2026-11-03. **Passive**: we bind the agent's UDP port
and listen, decoding the DDS-XRCE session and submessage headers of whatever the flight
controller sends. We never answer, so no session is established and no topic is read or
written. This is detection, not exploitation.

| Build | Port | XRCE datagrams | Submessages | Unauthenticated agent discovery |
|---|---|---|---|---|
| PX4 v1.18.0-rc1 SITL | 8888 | 20 / 20 | all `GET_INFO` | **yes** |
| PX4 v1.17.0 SITL | 8888 | 20 / 20 | all `GET_INFO` | **yes** |
| ArduPilot Copter 4.7.2 SITL | 2019 | 0 | — | no (none offered) |

## What the PX4 result means

PX4's `uxrce_dds_client` is included in SITL and most firmware builds by default and is
started by the stock `rcS`. It emits a repeated `GET_INFO` submessage (id `0x02`) addressed
to `OBJECTID_AGENT` (`0xfffd`), in a session with `SESSION_ID_NONE_WITHOUT_CLIENT_KEY`, to
whichever process holds the configured agent port. No credential, key or challenge precedes
it, and micro XRCE-DDS in PX4 does not implement DDS-Security, so the client has no way to
authenticate the agent that answers either.

The point for conformance is not that this is a bug — PX4's own documentation states that
the DDS transport is unauthenticated and reaches uORB directly, and that the DDS network
must therefore be kept isolated. The point is that **a MAVLink signing key does not protect
this path**: `SETUP_SIGNING` provisions MAVLink links. A deployment that has "enabled
signing" and considers its command link protected may still expose a second plane that
reaches uORB. That is why the score has a separate criterion for it (v2, 8 points,
CRA Annex I 2(d)) rather than folding it into the MAVLink attack surface.

## What the ArduPilot result means, and what it does not

This ArduPilot SITL build offers nothing on port 2019 and does not expose a `DDS_ENABLE`
parameter, so `AP_DDS` is not compiled into it. That is a measurement of **this build**, not
a property of ArduPilot: in the source, `DDS_ENABLE` defaults to `1` and `DDS_UDP_PORT` to
`2019` where `AP_DDS` is compiled in, so a vendor build that includes it would need the same
probe. We score what we measured and say which build it was.

## Not measured

Whether a full agent could then read or write uORB topics (not attempted: it would require
answering) · DDS-Security · whether a remote, non-loopback peer can reach the port in a given
deployment, which is an integrator's network question, not a firmware property · ArduPilot
builds that do compile `AP_DDS`.
