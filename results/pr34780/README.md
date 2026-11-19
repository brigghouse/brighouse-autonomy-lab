# Does ArduPilot PR #34780 close the channel-0 signing exemption?

ArduPilot Copter SITL, recorded 2026-11-19. Script: `scripts/pr34780.py`.
Data: `pr34780.json` (run 1) and `pr34780-run2.json` (run 2, same builds, same configurations).

## What was built

| Build | Source |
|---|---|
| `master` | ArduPilot `master` at `9d7be65` (2026-11-19) |
| `pr34780` | the same commit with the four commits of PR #34780 applied on top (PR head `3527020`; local commit `0769ceb` after `git am`) |

Both builds: `./waf configure --board sitl && ./waf copter`, gcc, no local changes.

## What the PR changes, and what SITL can and cannot test

[ArduPilot#34489](https://github.com/ArduPilot/ardupilot/issues/34489) reports that
`accept_unsigned_callback()` accepts every unsigned frame on `MAVLINK_COMM_0`, although
channel 0 is only the lowest-numbered serial port speaking MAVLink. [PR
#34780](https://github.com/ArduPilot/ardupilot/pull/34780) exempts channel 0 only when its
port reports `is_usb()`. In SITL the PR makes SERIAL0 stand in for USB
(`is_usb()` is `_portNumber == 0`), so that the documented "5760 behaves like USB, test
signing on 5762" workflow does not change.

So SITL can exercise the fix only where channel 0 is **not** SERIAL0. That happens when
SERIAL0 does not speak MAVLink: channel 0 is then SERIAL1. The PR description names this
case ("the exemption silently moves to the next MAVLink port, typically the telemetry
radio").

SITL **cannot** exercise the Linux HAL path (Bebop, Disco), where the PR reports no port
as USB. That needs a Linux board build and is not covered here.

## Configurations

| Config | SERIAL0 | channel 0 | channel 1 |
|---|---|---|---|
| A | MAVLink, TCP 5760 | SERIAL0 | SERIAL1, TCP 5762 |
| B | MAVLink, UDP | SERIAL0 | SERIAL1, TCP 5762 |
| E | `SERIAL0_PROTOCOL=-1` | SERIAL1, TCP 5762 | SERIAL2, TCP 5763 |
| F | `SERIAL0_PROTOCOL=-1` | SERIAL1, UDP | SERIAL2, TCP 5763 |

Each configuration: one unsigned read per channel before any key, then `SETUP_SIGNING`
over channel 0, then an unsigned and a signed `PARAM_REQUEST_READ` per channel.

## Result

Keyed vehicle, unsigned `PARAM_REQUEST_READ` on **channel 0**:

| Config | master | PR #34780 |
|---|---|---|
| A | answered | answered |
| B | answered | answered |
| E | **answered** | **rejected** |
| F | **answered** | **rejected** |

Channel 1 rejected the keyed unsigned read in every run, on both builds. Signed reads were
answered on every channel.

- **The fix works where SITL can test it.** On master, a SERIAL1 that has become channel 0
  answers unsigned reads over TCP and over UDP. With the PR it rejects them.
- **The documented SITL workflow is unchanged** (A, B): SERIAL0 stays trusted, whatever its
  transport. That is by design in the PR, and it also means that SITL alone cannot show
  the Linux case the issue was opened for.
- **Model agreement:** 48 of 48 cases in each run agree with the policy for that build
  (master: channel 0 trusted; PR: channel 0 trusted only when it is SERIAL0), 0
  inconclusive. Run 1 and run 2 are identical.

## Every rejection is observed, not a timeout

The probe is the one from `results/ch0-configs`. A negative counts as `rejected` only when
the vehicle's HEARTBEAT arrived during the same window (4 to 6 heartbeats in every
rejected case here) **and** a correctly signed read on the same link, sent immediately
after, was answered. In every rejected case of both runs the signed control was answered.
This also shows that key provisioning over channel 0 succeeded on the PR build, where
channel 0 is no longer exempt.

## Limits

- Simulation only, one vehicle type (Copter), one commit of master.
- Read-only probe (`PARAM_REQUEST_READ`); no command that moves the vehicle was sent.
- The Linux HAL change (`is_usb()` false for every port) and the ChibiOS hwdef flag are not
  exercised here.

## Reproduce

```bash
git clone https://github.com/ArduPilot/ardupilot.git ap-master
cd ap-master && git submodule update --init --recursive --depth 1
cd .. && cp -a ap-master ap-pr && cd ap-pr
git fetch origin pull/34780/head:pr34780 && git cherry-pick 566ed41 641ffcc 3290e3b 3527020
for d in ap-master ap-pr; do (cd ../$d && ./waf configure --board sitl && ./waf copter); done
python scripts/pr34780.py --master ../ap-master --pr ../ap-pr --out results/pr34780
```
