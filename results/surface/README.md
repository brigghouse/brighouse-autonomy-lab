# Surface served to an unauthenticated peer, per release

Recorded by `scripts/surface_probe.py` on 2026-11-03, on stock builds with default
parameters, disarmed, in SITL. Three kinds of evidence, which are **not** equally strong:

- **advertised** — the endpoint's `AUTOPILOT_VERSION` capability bits say the protocol exists.
- **answered** — we asked and it replied, strictly read-only: one `PARAM_REQUEST_READ`, and
  an FTP `ListDirectory`, which reads a directory listing from our own simulator.
- **static** — found by inspecting the build tree on disk, not by talking to it.

| | ArduPilot 4.7.2 | PX4 v1.17.0 | PX4 v1.18.0-rc1 |
|---|---|---|---|
| FTP advertised | yes | yes | yes |
| **FTP directory listing answered** | **yes** (25 B) | **yes** (101 B) | **yes** (110 B) |
| Parameter read answered | yes | yes | yes |
| Mission upload advertised | yes | yes | yes |
| Flight termination advertised | yes | yes | yes |
| `mavlink_shell` in build (static) | no | yes | yes |
| `SERIAL_CONTROL` in build (static) | yes | yes | yes |
| Secondary control plane (see `results/dds/`) | none in this build | unauthenticated | unauthenticated |

## Reading

Every release we can run serves a **directory listing** of the flight controller's
filesystem to a peer that has presented no credential. "Advertised" would have been a
weaker claim; this is answered. Mission upload and flight termination are advertised on
all three, which is the normal ground-station capability set — and precisely the point:
without authentication there is no distinction between a ground station and anyone else.

The asymmetry worth noting is the shell. The PX4 builds contain `mavlink_shell`, the module
that serves an interactive shell over `SERIAL_CONTROL`; the ArduPilot build does not. This
is consistent with CVE-2026-1579 (unauthenticated shell access over MAVLink) being a PX4
advisory. We report it as **static** evidence: we did not open a shell, because opening one
is not a read-only probe.

Across the three releases the surface does not shrink. For the Cyber Resilience Act the
relevant observation is not that any single item is a vulnerability — most are documented
features — but that the shipped default serves all of them without authentication, and that
this has not changed between releases we can still run.

## Repeatability

The ArduPilot run was repeated three times on 2026-11-03 with identical results (FTP
listing answered, 25 bytes of entries; parameter read answered).

## A limit specific to this campaign: SITL is not NuttX

The MAVLink FTP implementation does not take the same path on every target, and the clearest
evidence is in the advisory for CVE-2026-32709 itself, which states that on POSIX targets —
Linux companion computers and SITL — the write-path validation function unconditionally
returns true, where NuttX has a guard. Our probe only *reads* a directory listing, so that
particular difference does not bear on what we measured. But it establishes that the FTP
code paths differ by target, and therefore that **this measurement is of the POSIX/SITL
build**. A NuttX board may answer differently, and a technical file should say which target
was measured rather than generalising from one. We did not have a NuttX target to compare.

## Limits

Three releases, two stacks: the releases that both build and run on a current toolchain (see
`results/longitudinal/` for the ones that do not, and why). PX4 v1.13.3 is on disk but its
build never completed, so it is absent here for the same reason it is absent there. Nothing
was written: we did not test whether FTP can traverse paths or write files
(CVE-2026-32709 covers that), did not open a shell, did not change a parameter, and did not
test armed behaviour.
