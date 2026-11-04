# The exceptions to signing: what is accepted unsigned even with a key active

Extracted from the source trees by `scripts/allowlists.py` on 2026-11-03, with the file and
line recorded for every entry so this record cannot drift from the code. This is
**source-derived** evidence, not a measurement of running firmware.

| Stack (rev) | Accepted unsigned regardless of key | Per-channel blanket exemption |
|---|---|---|
| ArduPilot 4.7.2 (`fb77356`) | `RADIO_STATUS`, `RADIO` | **yes** — all messages on channel 0 |
| PX4 v1.18.0-rc1 (`fca3df8`) | `HEARTBEAT`, `RADIO_STATUS`, `ADSB_VEHICLE`, `COLLISION` | no |
| PX4 v1.17.0 | *(no signing implementation in this release)* | n/a |

Two different designs. PX4 has the longer allowlist but no blanket exemption, and its source
comment says plainly that allowing `HEARTBEAT` permits spoofed phantom vehicles on a ground
station. ArduPilot has a shorter allowlist but exempts an entire channel — and
`results/ch0-configs/` shows that exemption follows the channel index, not the transport, so
it is the wider hole of the two on a board whose SERIAL0 is not USB.

## What this settles about Remote ID over MAVLink (G8)

Neither stack allowlists any `OPEN_DRONE_ID_*` message. So on a keyed, non-exempt link,
Remote ID messages carried over MAVLink are covered by signing like any other message, and
the exposure reduces to the two mechanisms we have already measured: the unkeyed default
state, and ArduPilot's channel-0 exemption. There is no third, Remote-ID-specific hole in
the MAVLink path.

**Correction (4 Nov 2026).** An earlier version of this note said the stock SITL build has
`AP_OPENDRONEID_ENABLED` defaulting to 0 and no `OPEN_DRONE_ID` strings in the binary, and
therefore that Remote ID handling could not be exercised here at all. **Both halves were
false, and the error was ours: we grepped for the wrong symbol.** The build gate does default
to 0 in `libraries/AP_OpenDroneID/AP_OpenDroneID_config.h:7`, which is what we read, but the
SITL board class overrides it — `Tools/ardupilotwaf/boards.py:813` calls
`cfg.define('AP_OPENDRONEID_ENABLED', 1)`, the generated `build/sitl/ap_config.h:13` carries
`#define AP_OPENDRONEID_ENABLED 1`, `build/sitl/libraries/AP_OpenDroneID/*.o` are compiled,
and the binary contains the five `DID_*` parameter names and the pre-arm string
`DID_ENABLE must be 1`. (ArduPilot `fb7735678960`.) So Remote ID handling **is** reachable on
stock SITL by setting `DID_ENABLE=1`, and `scripts/odid_probe.py` does exactly that. The
lesson we are keeping: a negative claim from a `grep` is only as good as the string, and a
default in a header is not the value in the build — read the generated config, not the
`#ifndef`.

One thing that override exposes, which we were not looking for: `AP_CheckFirmware.h:15`
defines `AP_CHECK_FIRMWARE_ENABLED` as `AP_OPENDRONEID_ENABLED`. Firmware-integrity checking
in ArduPilot is not an independent switch — it is enabled *by* enabling Remote ID. On this
build that means the check is compiled in while `AP_SIGNED_FIRMWARE` is 0
(`boards.py:814`), so the machinery is present and has nothing to verify against. A vendor
board shipping an ODID hwdef inherits the coupling in the other direction: it gets
firmware-check code whether or not it has set up signing keys. We have not measured what that
check does at runtime in either state; it is recorded here as a reading of the build, not as
a result.

What we still have **not** measured, and will not claim: anything about a vendor board's own
`hwdef.dat`, which would need its own run. And the broadcast side — the Bluetooth and Wi-Fi frames
an observer actually receives, where ASTM F3411 defines only the framing of an
Authentication Message and leaves the method to others (IETF DRIP fills that gap) — needs a
Remote ID module we do not have. Spoofing of that broadcast is documented against receivers
(CVE-2023-29156, CVE-2023-31191) and is out of our reach without hardware.

## What this settles about MAVLink 1 fallback (G7)

A MAVLink 1 frame cannot carry a signature. For PX4 it follows from the extracted source
that a v1 frame can only be accepted on a keyed link if its message id is one of the four
allowlisted ones, since `accept_unsigned` consults nothing else — a source-derived
conclusion, which we label as such because we did not exercise it: PX4 has no per-port
protocol-version setting we could flip without changing a parameter, and pymavlink
auto-upgrades a connection to MAVLink 2 on receiving a v2 frame, so an attempted v1 probe
against PX4 is not v1 at all. We found that out the hard way and discarded the run.

For ArduPilot it is measured: configuration D in `results/ch0-configs/` sets
`SERIAL1_PROTOCOL=1`, the probe's frames are recorded as `0xFE` (genuine MAVLink 1), and a
keyed port rejects the unsigned v1 read. The ArduPilot documentation's statement that
MAVLink 1 ports are "not protected" is, for this build and this message, stricter-sounding
than the behaviour.
