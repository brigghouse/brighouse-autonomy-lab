"""Tests for the acceptance-semantics model."""

from mavaudit.model.configs import ARDUPILOT_472, IDEAL_OOB, PX4_117, PX4_118, SPEC_STRICT
from mavaudit.model.explore import explore, run_all
from mavaudit.model.semantics import (CMD, RADIO, READ, SETUP, Frame, Policy, State, step)


def test_unkeyed_accepts_everything():
    d = step(PX4_118, State(), Frame("ch1", (2, 2), CMD))
    assert d.accepted and d.state.key is None


def test_tofu_installs_first_key_unsigned():
    d = step(PX4_118, State(), Frame("ch1", (2, 2), SETUP, payload="K"))
    assert d.accepted and d.state.key == "K"


def test_keyed_rejects_unsigned_command_off_trusted():
    st = State(key="K", clock=1_000_000)
    d = step(PX4_118, st, Frame("ch1", (9, 9), CMD))
    assert not d.accepted and "rejected" in d.reason


def test_keyed_accepts_valid_signature_and_advances_timestamp():
    st = State(key="K", clock=1_000_000)
    fr = Frame("ch1", (1, 1), CMD, signed=True, key="K", ts=1_000_050, link_id=1)
    d = step(PX4_118, st, fr)
    assert d.accepted
    assert d.state.last_ts((1, 1, 1)) == 1_000_050


def test_replay_rejected_by_timestamp():
    st = State(key="K", clock=1_000_000).with_ts((1, 1, 1), 1_000_050)
    d = step(PX4_118, st, Frame("ch1", (1, 1), CMD, signed=True, key="K", ts=1_000_050, link_id=1))
    assert not d.accepted and "replay" in d.reason.lower() or "increasing" in d.reason


def test_bad_signature_rejected():
    st = State(key="K", clock=1_000_000)
    d = step(PX4_118, st, Frame("ch1", (9, 9), CMD, signed=True, key="K_adv", ts=1_000_050, link_id=1))
    assert not d.accepted and d.reason == "bad signature"


def test_ardupilot_trusted_link_accepts_unsigned():
    st = State(key="K", clock=1_000_000)
    assert step(ARDUPILOT_472, st, Frame("ch0", (9, 9), CMD)).accepted         # trusted
    assert not step(ARDUPILOT_472, st, Frame("ch1", (9, 9), CMD)).accepted     # untrusted


def test_px4_118_refuses_setup_while_armed():
    st = State(key="K", armed=True, clock=1_000_000)
    d = step(PX4_118, st, Frame("ch1", (1, 1), SETUP, signed=True, key="K", ts=1_000_050, link_id=1, payload="K2"))
    assert not d.accepted and "armed" in d.reason


def test_px4_117_has_no_protection():
    # modelled as everything-trusted: unsigned commands always accepted, SETUP never helps
    st = State(key=None)
    assert step(PX4_117, st, Frame("ch1", (9, 9), CMD)).accepted
    d = step(PX4_117, st, Frame("ch1", (2, 2), SETUP, payload="K"))
    assert d.state.key is None  # no TOFU: provisioning has no effect


def test_ideal_oob_is_clean_everywhere():
    rows = [r for r in run_all([IDEAL_OOB], depth=3)]
    assert all(not any(r[p] for p in ("P1", "P2", "P3", "P4", "P5", "P6")) for r in rows)


def test_tofu_policies_have_first_use_window():
    for pol in (SPEC_STRICT, PX4_118, ARDUPILOT_472):
        res = explore(pol, "pre-provisioning", "ch1", "ch1", depth=3)
        assert res["P4"] is not None, pol.name


def test_key_exposure_on_provisioning_link():
    # SETUP_SIGNING carries the key in clear: an adversary on the provisioning link forges later.
    for pol in (SPEC_STRICT, PX4_118, ARDUPILOT_472):
        res = explore(pol, "on-provisioning-link", "ch1", "ch1", depth=3)
        assert res["P1"] is not None and res["P6"] is not None, pol.name


def test_ardupilot_unsigned_rekey_on_trusted_link():
    res = explore(ARDUPILOT_472, "post-provisioning, A on trusted", "ch0", "ch1", depth=3)
    assert res["P2"] is not None  # adversary on ch0 replaces the key unsigned


def test_custom_policy_without_tofu_closes_window():
    pol = Policy(name="no-tofu", tofu=False, open_when_unkeyed=False)
    assert explore(pol, "pre-provisioning", "ch1", "ch1", depth=3)["P4"] is None
