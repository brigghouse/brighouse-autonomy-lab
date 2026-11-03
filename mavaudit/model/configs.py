"""Policy instances. Each encodes documented behaviour (cited in the paper) or a
reference point. Values marked `measured` were confirmed against SITL by
scripts/conformance.py; the rest are documentation-derived hypotheses that the
conformance run tests.
"""

from __future__ import annotations

from .semantics import HB, RADIO, Policy

LINKS = frozenset({"ch0", "ch1"})

#: The MAVLink spec text leaves acceptance of unsigned traffic to implementations; this is
#: the strictest reading: no trusted link, only RADIO_STATUS unsigned, TOFU required for
#: the very first key (the spec provides no other key-distribution mechanism).
SPEC_STRICT = Policy(
    name="spec-strict",
    trusted=frozenset(),
    allow_unsigned=frozenset({RADIO}),
    tofu=True,
    unsigned_rekey_on_trusted=False,
)

#: An idealised policy with an out-of-band first key (no TOFU window at all).
IDEAL_OOB = Policy(
    name="ideal-oob-provisioning",
    trusted=frozenset(),
    allow_unsigned=frozenset({RADIO}),
    open_when_unkeyed=False,
    tofu=False,
    oob_provision=True,
    unsigned_rekey_on_trusted=False,
)

#: PX4 v1.18 (docs: message_signing.md; PR #26894). HEARTBEAT and RADIO_STATUS are
#: accepted unsigned on all links; SETUP on any link, refused while armed; no trusted link.
PX4_118 = Policy(
    name="px4-1.18",
    trusted=frozenset(),
    allow_unsigned=frozenset({HB, RADIO}),
    tofu=True,
    setup_links=None,
    unsigned_rekey_on_trusted=False,
    refuse_setup_armed=True,
)

#: PX4 v1.17.0 stable: no signing implementation at all (measured).
PX4_117 = Policy(
    name="px4-1.17",
    trusted=LINKS,                   # everything behaves like an always-trusted link
    open_when_unkeyed=True,
    tofu=False,                      # SETUP_SIGNING has no effect
)

#: ArduPilot 4.7.2 (GCS_Signing.cpp): MAVLINK_COMM_0 always accepts unsigned; RADIO_STATUS
#: and RADIO allow-listed; USB exemption is the documented recovery path.
ARDUPILOT_472 = Policy(
    name="ardupilot-4.7.2",
    trusted=frozenset({"ch0"}),
    allow_unsigned=frozenset({RADIO}),
    tofu=True,
    setup_links=None,
    unsigned_rekey_on_trusted=True,
)

#: The same policy as read from ArduPilot's *documentation* rather than its source: the
#: signing page states that a serial port speaking MAVLink 1 "is not protected". If that
#: were the behaviour, a keyed non-trusted port would accept MAVLink 1 commands. We keep
#: this as a separate policy so the two readings are distinguishable and a measurement can
#: decide between them; configuration D in results/ch0-configs refutes it for 4.7.2.
ARDUPILOT_472_DOC = Policy(
    name="ardupilot-4.7.2-doc",
    trusted=frozenset({"ch0"}),
    allow_unsigned=frozenset({RADIO}),
    tofu=True,
    setup_links=None,
    unsigned_rekey_on_trusted=True,
    v1_bypasses_signing=True,
)

ALL = [SPEC_STRICT, IDEAL_OOB, PX4_118, PX4_117, ARDUPILOT_472, ARDUPILOT_472_DOC]
BY_NAME = {p.name: p for p in ALL}
