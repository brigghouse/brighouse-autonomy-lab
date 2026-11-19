# The Linux case of issue #34489, on the Linux HAL: master vs PR #34780

ArduPilot Copter built for the generic Linux board (`./waf configure --board linux`) and
run on an x86-64 host, recorded 2026-11-19. Script: `scripts/linux_hal_ch0.py`.
Data: `linux-hal-ch0.json` (run 1), `linux-hal-ch0-run2.json` (run 2), `vehicle-state.json`.

## Why this campaign exists

[Issue #34489](https://github.com/ArduPilot/ardupilot/issues/34489) was opened for Linux
boards: on the Parrot Bebop the documented start-up command puts the Wi-Fi UDP link on
SERIAL0, which is MAVLink channel 0, so signing does not protect it. `results/pr34780/`
tested the proposed fix in SITL, but SITL cannot show this case: with the PR, SITL keeps
SERIAL0 as its stand-in for USB. Here the Linux HAL itself runs, where the PR reports no
port as USB.

## Builds

| Build | Source |
|---|---|
| `master` | ArduPilot `master` at `9d7be65` (2026-11-19), `--board linux` |
| `pr34780` | the same commit plus the four commits of PR #34780 (PR head `3527020`), `--board linux` |

## The vehicle is stalled, and why that does not matter for this question

There is no sensor hardware, so the vehicle stops in its configuration-error loop. Both
builds report it (`vehicle-state.json`, 20 s window):

> Config Error: Baro: unable to initialise driver
> Config Error: fix problem then reboot

That loop keeps servicing MAVLink: `AP_BoardConfig::throw_error()`
(`libraries/AP_BoardConfig/AP_BoardConfig.cpp:550`) loops forever and calls
`gcs().update_receive()` and `gcs().update_send()` on every pass (lines 583-584). The
vehicle sends HEARTBEAT, answers `PARAM_REQUEST_READ` and handles `SETUP_SIGNING`.

The signing decision does not depend on vehicle state. It is taken while each frame is
parsed, in the MAVLink library (`mavlink_helpers.h:989-990` and `1015-1016`), which calls
ArduPilot's `accept_unsigned_callback()` (`GCS_Signing.cpp:116`), the function the PR
changes. A stalled vehicle therefore exercises the same acceptance path as a flying one.
What it does not exercise is listed under Limits.

## Configurations

| Config | SERIAL0 = channel 0 | SERIAL1 = channel 1 |
|---|---|---|
| L1 | UDP (as on the Bebop) | TCP |
| L2 | TCP | UDP |

Before every run the vehicle's state directory (`/var/lib/ardupilot`, parameters and the
signing key) is wiped, so no key carries over between builds. Each run: one unsigned read
per channel before any key, `SETUP_SIGNING` over channel 0, then an unsigned and a signed
`PARAM_REQUEST_READ` per channel.

## Result

Keyed vehicle, unsigned `PARAM_REQUEST_READ`:

| Config | master, ch0 | master, ch1 | PR, ch0 | PR, ch1 |
|---|---|---|---|---|
| L1 (ch0 UDP) | **answered** | rejected | **rejected** | rejected |
| L2 (ch0 TCP) | **answered** | rejected | **rejected** | rejected |

- **On master the Bebop situation is reproduced on the Linux HAL:** the UDP link on
  SERIAL0 answers unsigned reads while a key is active, and so does a TCP link in the same
  position. The exemption follows the channel index on Linux as it does in SITL.
- **With PR #34780 the exemption is gone on Linux:** channel 0 rejects unsigned reads over
  UDP and over TCP, like every other port.
- Signed reads were answered on every channel. 24/24 cases agree with the per-build policy
  in each run (master: `ardupilot-4.7.2`, channel 0 trusted; PR:
  `ardupilot-pr34780-ch0-not-usb`, no trusted link), 0 inconclusive. Run 1 and run 2 are
  identical.
- Every rejection is observed, not a timeout: 10 to 17 heartbeats arrived in the same
  window, and a correctly signed read on the same link was answered right after.

## What this means for a Linux-board user

With the PR, a Linux board with signing enabled has **no** unsigned recovery port: a lost
key is recovered by disabling signing per channel (`MAVn_OPTIONS`) or resetting
parameters, as the PR description says. That is the intended trade-off of the fix, stated
here so it is not mistaken for a regression.

## Limits

- Generic `linux` board on x86-64, not a Bebop or Disco image, and no hardware in the loop.
  The ArduPilot code path is the Linux HAL's; the board-specific start-up scripts are not.
- The vehicle is in its configuration-error loop (no sensors). Commands that need a
  healthy vehicle (arming, mode changes) are not tested; the probe is a read-only
  `PARAM_REQUEST_READ`.
- One commit of master, Copter only.

## Reproduce (as root, on a disposable host or container)

```bash
# two checkouts of the same master commit, the second with the PR's commits applied
for d in ap-master-linux ap-pr-linux; do (cd $d && ./waf configure --board linux && ./waf copter); done
python scripts/linux_hal_ch0.py --master ap-master-linux --pr ap-pr-linux --out results/linux-hal-ch0
```
