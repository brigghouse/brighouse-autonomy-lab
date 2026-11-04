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

PX4's `uxrce_dds_client` is **not** "included in most firmware builds by default", which is
what an earlier version of this note claimed on the strength of a case-sensitive grep that
missed the configuration symbol entirely -- the same mistake we made about OpenDroneID the
same day. What the tree actually shows (PX4 `v1.18.0-rc1`): its Kconfig default is `n`
(`src/modules/uxrce_dds_client/Kconfig:3`), 73 of 286 `.px4board` configurations set
`CONFIG_MODULES_UXRCE_DDS_CLIENT=y` and 12 set it to `n`. More importantly, being compiled
in is not the same as listening: the only startup script in the tree that starts the client
is the **POSIX** one, `ROMFS/px4fmu_common/init.d-posix/rcS:326`, which runs
`uxrce_dds_client start -t udp -p 8888` with no parameter gating it -- unlike Zenoh two
lines below, which is behind `ZENOH_ENABLE`. The stock NuttX `init.d/rcS` contains zero
references to it.

So the honest shape of this finding is narrower than we had it and more useful: on a
**POSIX target** -- SITL, and a Linux companion computer such as ModalAI's VoXL2, whose own
start script also launches it -- the second control plane is up by default and ungated. On a
**stock NuttX flight board** the module may be in flash while nothing starts it. A customer
asking "do I have this plane?" gets a different answer depending on which of the two they
are running, and that is a question we can now answer from their build rather than guess.

This bounds our own score: the eight points PX4 loses on the control-plane criterion were
measured against a POSIX/SITL build, and they do not transfer unexamined to a NuttX board.

The client is
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

## Repeatability

The PX4 v1.18.0-rc1 measurement was repeated three times on 2026-11-03. The number of
datagrams captured varies with the listening window and the moment the client starts — 20,
17 and 18 over a 35-to-40 second window — because the client emits discovery periodically.
The finding does not vary: in all three runs every decoded datagram is a `GET_INFO`
submessage addressed to the agent in a session with no client key.

## Not measured

Whether a full agent could then read or write uORB topics (not attempted: it would require
answering) · DDS-Security · whether a remote, non-loopback peer can reach the port in a given
deployment, which is an integrator's network question, not a firmware property · ArduPilot
builds that do compile `AP_DDS`.
