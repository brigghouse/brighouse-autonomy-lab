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


def test_oob_provisioning_is_functional_and_secure():
    from mavaudit.model.configs import IDEAL_OOB
    from mavaudit.model.synthesis import is_functional, present, failures
    assert is_functional(IDEAL_OOB)
    assert not failures(present(IDEAL_OOB))  # no security failures


def test_closing_tofu_without_oob_would_break_provisioning():
    # honesty check: closing TOFU but keeping over-the-wire provisioning makes the vehicle
    # unprovisionable (modelled: it cannot accept the legit first key), so it is NOT functional.
    from mavaudit.model.semantics import Policy
    from mavaudit.model.synthesis import is_functional
    broken = Policy(name="closed-no-oob", tofu=False, open_when_unkeyed=False, oob_provision=False)
    assert not is_functional(broken)


def test_synthesis_ardupilot_needs_two_fixes():
    from mavaudit.model.synthesis import analyse
    a = analyse()
    ap = a["ardupilot-4.7.2"]
    assert ap["functional"] and not ap["residual_failures_after_combo"]
    assert len(ap["min_edits_to_clear_failures"]) >= 2  # TOFU/key-exposure AND unsigned-rekey
    assert ap["functional_after_combo"]


def test_synthesis_px4_118_single_fix():
    from mavaudit.model.synthesis import analyse
    d = analyse()["px4-1.18"]
    assert d["min_edits_to_clear_failures"] == ["close-tofu+oob"]
    assert not d["residual_failures_after_combo"]


def test_conformance_predictions_match_measured_ground_truth():
    """The 8-case prediction vector per policy equals what the live SITL confirmed (8/8).
    Order: (keyed, trusted, signed) over {0,1}^3 as in scripts.conformance."""
    import sys, os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
    from conformance import model_predict
    from mavaudit.model.configs import BY_NAME
    # Ground truth from results/conformance (all stacks agreed 8/8 with these predictions):
    expected = {
        "ardupilot-4.7.2": {
            (False, True, False): True, (False, True, True): True,
            (False, False, False): True, (False, False, True): True,
            (True, True, False): True,  (True, True, True): True,     # ch0 answers unsigned (R4)
            (True, False, False): False, (True, False, True): True,
        },
        "px4-1.18": {
            (False, True, False): True, (False, True, True): True,
            (False, False, False): True, (False, False, True): True,
            (True, True, False): False, (True, True, True): True,     # no trusted link
            (True, False, False): False, (True, False, True): True,
        },
        "px4-1.17": {k: True for k in [(a, b, c) for a in (0, 1) for b in (0, 1) for c in (0, 1)]},
    }
    for pol, cases in expected.items():
        p = BY_NAME[pol]
        for (keyed, trusted, signed), exp in cases.items():
            got = model_predict(p, bool(trusted), bool(signed), bool(keyed))
            assert got == exp, (pol, keyed, trusted, signed, got, exp)
