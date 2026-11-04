# Surface served to an unauthenticated peer, per release

Recorded by `scripts/surface_probe.py`, on stock builds with default parameters, disarmed,
in SITL. Three records: `surface-ardupilot-4.7.2.json`, `surface-px4-v1.17.0.json`,
`surface-px4-v1.18.0-rc1.json`. Every probe is read-only, runs on loopback, and the script
refuses any target that is not local.

Three kinds of evidence, which are **not** equally strong, and which the records keep apart
because collapsing them is how a surface inventory starts overstating itself:

- **advertised** — the endpoint's `AUTOPILOT_VERSION` capability bits say the protocol
  exists. A claim by the vehicle, nothing more.
- **answered** — we asked and it replied, strictly read-only: one `PARAM_REQUEST_READ`, and
  an FTP `ListDirectory`, which reads a directory listing from our own simulator. The only
  category where we observed behaviour instead of inspecting or trusting.
- **static** — strings found by inspecting the build tree on disk, not by talking to it.
  The feature is compiled in; we did not exercise it.

| | ArduPilot 4.7.2 | PX4 v1.17.0 | PX4 v1.18.0-rc1 |
|---|---|---|---|
| FTP advertised | yes | yes | yes |
| **FTP directory listing answered** | **yes** | **yes** | **yes** |
| Parameter read answered | yes | yes | yes |
| Mission upload advertised | yes | yes | yes |
| Flight termination advertised | yes | yes | yes |
| `mavlink_shell` in build (static) | no — 0 matches | yes — 9 files, 9 outside generated headers | yes — 9 files, 9 outside generated headers |
| `SERIAL_CONTROL` in build (static) | **no evidence** — 13 matches, 0 outside generated headers | yes — 9 matches, 4 outside them | yes — 9 matches, 4 outside them |
| Secondary control plane (see `../dds/`) | **not established** — probe inconclusive | unauthenticated | unauthenticated |

## Reading

Every release we can run serves a **directory listing** of the flight controller's
filesystem to a peer that has presented no credential. "Advertised" would have been a
weaker claim; this is answered. Mission upload and flight termination are advertised on all
three, which is the normal ground-station capability set — and precisely the point: without
authentication there is no distinction between a ground station and anyone else.

The asymmetry worth noting is the shell. The PX4 builds contain `mavlink_shell`, the module
that serves an interactive shell over `SERIAL_CONTROL`; the ArduPilot build does not. This
is consistent with CVE-2026-1579 (unauthenticated shell access over MAVLink) being a PX4
advisory. We report it as **static** evidence: we did not open a shell, because opening one
is not a read-only probe.

Across the three releases the surface does not shrink. For the Cyber Resilience Act the
relevant observation is not that any single item is a vulnerability — most are documented
features — but that the shipped default serves all of them without authentication, and that
this has not changed between releases we can still run.

## Two claims in the table above that we had to withdraw

Neither was found by a reviewer reading our prose; both were found by making the probe
answer a harder question than it had been answering.

**`SERIAL_CONTROL` in ArduPilot was a grep artefact.** We had recorded it as present on 13
string matches. All 13 are in *generated MAVLink dialect headers*, which every stack carries
because they describe the protocol, not because the stack implements the message. The probe
now counts generated headers separately and reports `excluding_generated_headers` beside the
raw total; a hit only in those sets `evidence: false`. The headline shell asymmetry survived
this; the claim we had made next to it did not.

**"No secondary control plane in this build" was absence of evidence.** Our ArduPilot DDS
probe captured no datagrams, and we read that silence as the stack offering no second plane.
Zero datagrams cannot distinguish that from a probe that listened on the wrong port or
started too late. The probe now marks such a capture inconclusive, and the score that
depended on it is reported as a lower bound — see `../dds/README.md` and
`../scores/README.md`, where this reversed a published ordering of the two stacks.

**A third number is gone from the table rather than corrected.** We used to print the byte
count of the FTP listing (25 B, 101 B, 110 B) as if it were a per-release property. It is
the size field of a listing of whatever directory the simulator happened to be started in:
re-running the same probe from a different working directory returns 164 and 117 for the
same two builds. The field is still in the records, renamed `ack_size_field` and carrying
that caveat inline, because the *ack* is the finding. The size never was.

## Repeatability

Each live probe was run **three times** back to back against the same simulator process.
All three builds recorded `identical_across_runs: true`, with no field varying. The per-run
answers are retained in each record under `repeatability.per_run`, so the claim is checkable
rather than asserted — which is the point: an earlier version of this README stated a
repeatability we had not kept the artefacts for.

What that establishes is narrow, and the records say so: it measures probe determinism, not
reproducibility across a rebuild or on different hardware. The static section inspects a
fixed binary and is recorded once, because repeating it could not vary.

## A limit specific to this campaign: SITL is not NuttX

The MAVLink FTP implementation does not take the same path on every target, and the clearest
evidence is in the advisory for CVE-2026-32709 itself, which states that on POSIX targets —
Linux companion computers and SITL — the write-path validation function unconditionally
returns true, where NuttX has a guard. Our probe only *reads* a directory listing, so that
particular difference does not bear on what we measured. But it establishes that the FTP
code paths differ by target, and therefore that this measurement is of the **POSIX/SITL
build**. A NuttX board may answer differently, and a technical file should say which target
was measured rather than generalising from one. We did not have a NuttX target to compare.

## Limits

Three releases, two stacks: the releases that both build and run on a current toolchain (see
`../longitudinal/` for the ones that do not, and why). PX4 v1.13.3 is on disk but its build
never completed, so it is absent here for the same reason it is absent there. Nothing was
written: we did not test whether FTP can traverse paths or write files (CVE-2026-32709
covers that), did not open a shell, did not change a parameter, and did not test armed
behaviour.

Related: [../allowlists/README.md](../allowlists/README.md) — the exceptions to signing,
which decide whether these surfaces are reachable on a keyed link.
[../dds/README.md](../dds/README.md) — the second control plane, and why ArduPilot's row
above is unestablished rather than clean.
