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
    assert not d.accepted and ("replay" in d.reason.lower() or "increasing" in d.reason.lower())


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


def test_conformance_predictions_match_recorded_observations():
    """Every model prediction equals the *observed* SITL outcome recorded in
    results/conformance/conformance-*.json.

    This is a RECORDED experiment: the SITL runs are not re-executed in CI. The test
    guards against the model drifting away from the committed observations. It
    deliberately reads the `observed` field (what the vehicle actually did), never a
    copy of the model's own `predicted` output, so it cannot be satisfied trivially.
    """
    import sys, os, json, glob
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
    from conformance import model_predict
    from mavaudit.model.configs import BY_NAME
    root = os.path.join(os.path.dirname(__file__), "..", "results", "conformance")
    files = sorted(glob.glob(os.path.join(root, "conformance-*.json")))
    assert files, "no recorded conformance results found"
    checked, discriminating = 0, 0
    for f in files:
        with open(f) as fh:
            d = json.load(fh)
        p = BY_NAME[d["policy"]]
        for c in d["cases"]:
            keyed = c["state"] == "keyed"
            trusted = c["link"] == "trusted"
            got = model_predict(p, trusted, bool(c["signed"]), keyed)
            assert got == c["observed"], (d["policy"], c, got)
            checked += 1
            # A case only discriminates when the vehicle could have rejected: keyed state.
            if keyed and c["observed"] is False:
                discriminating += 1
    assert checked == 24
    # Honest accounting: the unkeyed half is a tautology (nothing can reject). Only
    # the keyed rejections (px4-1.18 untrusted/unsigned x1, ardupilot untrusted/unsigned x1,
    # plus px4-1.18 trusted/unsigned) actually test the model's discriminating power.
    assert discriminating >= 3


def test_ch0_configs_recorded_transport_independence():
    """Recorded SITL runs (results/ch0-configs): the ch0 exemption follows the channel
    index, not the transport. B (ch0 over UDP) accepts unsigned; C (ch1 over UDP) rejects."""
    import json
    from pathlib import Path
    p = Path(__file__).resolve().parent.parent / "results/ch0-configs/ch0-configs.json"
    d = json.loads(p.read_text())
    by = {c["config"]: c for c in d["configs"]}
    def obs(cfg, link, signed=False):
        return [c["observed"] for c in by[cfg]["cases"]
                if c["state"] == "keyed" and c["link"] == link and c["signed"] == signed][0]
    assert obs("B-ch0udp-ch1tcp", "ch0") is True
    assert obs("C-ch0tcp-ch1udp", "ch1") is False
    assert obs("D-ch0tcp-ch1mav1", "ch1") is False
    assert all(c["agree"] for cfg in d["configs"] for c in cfg["cases"])
    assert sum(cfg["total"] for cfg in d["configs"]) == 23
    # The MAVLink 1 claim must rest on a measured wire version, not on a label: every
    # ch1 case of configuration D records 0xFE as the first byte actually sent.
    dcfg = by["D-ch0tcp-ch1mav1"]
    ch1 = [c for c in dcfg["cases"] if c["link"] == "ch1"]
    assert ch1 and all(c["wire_first_byte_sent"] == 0xFE and c["wire"] == 1 for c in ch1)
    # and every other configuration's probes were MAVLink 2.
    others = [c for k, cfg in by.items() if k != "D-ch0tcp-ch1mav1" for c in cfg["cases"]]
    assert all(c["wire_first_byte_sent"] == 0xFD for c in others)


def test_wire_version_parameter_discriminates_doc_from_implementation():
    """The model used to agree with configuration D for a reason it did not represent:
    it had no notion of wire version. With the parameter, the documentation's reading
    ("a MAVLink 1 port is not protected") and the implementation's behaviour are two
    distinct policies, and the recorded measurement picks one."""
    import json
    from pathlib import Path
    from mavaudit.model.configs import BY_NAME
    from mavaudit.model.semantics import READ, Frame, State, step

    st = State(key="K", clock=2_000_000)
    v1 = Frame("ch1", (9, 9), READ, signed=False, ts=2_000_050, link_id=1, wire=1)
    impl = step(BY_NAME["ardupilot-4.7.2"], st, v1)
    doc = step(BY_NAME["ardupilot-4.7.2-doc"], st, v1)
    assert impl.accepted is False and doc.accepted is True, "the policies must differ"

    # The recorded run decides between them: configuration D's keyed ch1 case, whose
    # frames are measured as 0xFE, was rejected.
    p = Path(__file__).resolve().parent.parent / "results/ch0-configs/ch0-configs.json"
    d = json.loads(p.read_text())
    cfg = next(c for c in d["configs"] if c["config"].startswith("D"))
    case = next(c for c in cfg["cases"]
                if c["state"] == "keyed" and c["link"] == "ch1")
    assert case["wire_first_byte_sent"] == 0xFE
    assert case["observed"] == impl.accepted      # implementation policy matches
    assert case["observed"] != doc.accepted       # documentation reading is refuted


def test_mavlink1_frame_cannot_be_signed():
    """Structural, not a policy choice: version 1 frames have no signature field."""
    import pytest
    from mavaudit.model.semantics import READ, Frame
    with pytest.raises(ValueError):
        Frame("ch1", (1, 1), READ, signed=True, wire=1)
    with pytest.raises(ValueError):
        Frame("ch1", (1, 1), READ, wire=3)
