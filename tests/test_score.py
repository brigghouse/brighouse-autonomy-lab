"""Tests for the secure-by-default score, checking its three axioms."""

import copy

import pytest

from mavaudit.score import CRITERIA, MAXW, score, score_summary_run


def base_report(**over):
    ep = {"autopilot": "px4", "frames": 100, "signed_frames": 0, "v1_frames": 0,
          "ftp_advertised": True, "firmware": "1.18.0 (type 192)"}
    ep.update(over.pop("ep", {}))
    r = {"target": "udpin:127.0.0.1:14550", "endpoints": [ep],
         "unsigned_probe": {"answered": True}}
    r.update(over)
    return r


def test_weights_sum_to_100():
    assert MAXW == 100 and sum(c.weight for c in CRITERIA) == 100


def test_ideal_scores_100():
    r = base_report(ep={"autopilot": "px4", "frames": 100, "signed_frames": 100,
                        "v1_frames": 0, "ftp_advertised": False, "firmware": "x"},
                    unsigned_probe={"answered": False})
    r["control_plane"] = {"unauthenticated": False, "detail": "model target"}
    s = score(r, policy="ideal-oob-provisioning", link_confidential=True)
    assert s["score"] == 100.0 and s["grade"] == "A"


def test_unmeasured_control_plane_is_a_lower_bound_not_a_pass():
    """A1 (provenance): a plane we never probed is not a plane we know to be clean."""
    ep = {"autopilot": "px4", "frames": 100, "signed_frames": 100,
          "v1_frames": 0, "ftp_advertised": False, "firmware": "x"}
    r = base_report(ep=dict(ep), unsigned_probe={"answered": False})
    unmeasured = score(r, policy="ideal-oob-provisioning", link_confidential=True)
    assert unmeasured["lower_bound"] is True
    assert unmeasured["unmeasured_criteria"] == ["control_plane"]
    cp = next(b for b in unmeasured["breakdown"] if b["criterion"] == "control_plane")
    assert cp["earned"] == 0.0 and "not measured" in cp["why"]

    clean = base_report(ep=dict(ep), unsigned_probe={"answered": False})
    clean["control_plane"] = {"unauthenticated": False, "detail": "probe found none"}
    dirty = base_report(ep=dict(ep), unsigned_probe={"answered": False})
    dirty["control_plane"] = {"unauthenticated": True, "detail": "XRCE GET_INFO observed"}
    a = score(clean, policy="ideal-oob-provisioning", link_confidential=True)
    b = score(dirty, policy="ideal-oob-provisioning", link_confidential=True)
    # A2 (monotonicity): an exposed second plane scores strictly lower than none.
    assert a["score"] > b["score"]
    assert "lower_bound" not in a and "lower_bound" not in b


def test_default_is_low():
    s = score(base_report(), policy="px4-1.18")
    assert s["score"] < 35 and s["grade"] == "E"


def test_axiom_provenance_every_criterion_cites_cra():
    s = score(base_report(), policy="px4-1.18")
    assert all(b["cra"] for b in s["breakdown"])


def test_axiom_monotonicity_fixing_a_finding_never_lowers_score():
    # Start from a weak report; improve one observable at a time; score must not decrease.
    r = base_report()
    prev = score(r, policy="px4-1.18")["score"]
    improvements = [
        {"ep": {"signed_frames": 100}},
        {"unsigned_probe": {"answered": False}},
        {"ep": {"signed_frames": 100, "ftp_advertised": False}},
        {"ep": {"signed_frames": 100, "ftp_advertised": False, "v1_frames": 0}},
    ]
    r2 = copy.deepcopy(r)
    for imp in improvements:
        for k, v in imp.items():
            if k == "ep":
                r2["endpoints"][0].update(v)
            else:
                r2[k] = v
        cur = score(r2, policy="px4-1.18")["score"]
        assert cur >= prev - 1e-9, (prev, cur)
        prev = cur


def test_r4_is_captured_numerically():
    # ArduPilot ch0 (signs everything but answers unsigned) must score BELOW a clean signed link.
    exempt = score_summary_run({"frames": 100, "signed_frames": 100, "v1_frames": 0,
                                "ftp_advertised": True, "unsigned_probe_answered": True,
                                "firmware": "4.7.2"}, "ardupilot-4.7.2")
    clean = score_summary_run({"frames": 100, "signed_frames": 100, "v1_frames": 0,
                               "ftp_advertised": False, "unsigned_probe_answered": False,
                               "firmware": "4.7.2"}, "ardupilot-4.7.2")
    assert exempt["score"] < clean["score"]


def test_empty_run_is_unscorable_not_secure():
    # A run that observed no frames and whose probe never answered must NOT get a grade
    # (absence of evidence is not evidence of security). Regression for the 42/D bug.
    s = score_summary_run({"frames": 0, "signed_frames": 0, "v1_frames": 0,
                           "ftp_advertised": None, "unsigned_probe_answered": None,
                           "firmware": "1.16.2"}, "px4-1.17")
    assert s["score"] is None and s["grade"] == "N/A" and s.get("insufficient_data")
    # and a real, running, insecure device must still be scored (and thus rank below nothing)
    insecure = score_summary_run({"frames": 100, "signed_frames": 0, "v1_frames": 0,
                                  "ftp_advertised": True, "unsigned_probe_answered": True,
                                  "firmware": "1.17.0"}, "px4-1.17")
    assert insecure["score"] is not None


def test_partial_credit_for_signed_fraction():
    half = score(base_report(ep={"signed_frames": 50}), policy="px4-1.18")["score"]
    none = score(base_report(ep={"signed_frames": 0}), policy="px4-1.18")["score"]
    full = score(base_report(ep={"signed_frames": 100}), policy="px4-1.18")["score"]
    assert none < half < full


def test_dds_probe_decodes_a_real_recorded_datagram():
    """The XRCE decoder is checked against a datagram actually captured from PX4 SITL
    (results/dds), not a hand-written one: session header, submessage id, target object."""
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
    from dds_probe import decode
    # Captured from PX4 v1.18.0-rc1 on 127.0.0.1:8888, 2026-11-03.
    d = decode(bytes.fromhex("8000000002010800000afffd02000000"))
    assert d["submessage"] == "GET_INFO"
    assert d["session_without_client_key"] is True
    assert d["targets_agent"] is True and d["target_object"] == "fffd"
    # Not XRCE at all -> None, so unrelated traffic is never counted as a finding.
    assert decode(b"\x00" * 8) is None
    assert decode(b"short") is None


def test_recorded_dds_runs_match_the_readme_claims():
    import json
    from pathlib import Path
    d = Path(__file__).resolve().parent.parent / "results/dds"
    recs = {f.stem: json.loads(f.read_text()) for f in d.glob("dds-*.json")}
    px4 = [r for r in recs.values() if r["stack"] == "px4"]
    ap = [r for r in recs.values() if r["stack"] == "ardupilot"]
    assert px4 and all(r["unauthenticated_agent_discovery"] for r in px4)
    assert all(r["submessage_counts"].get("GET_INFO", 0) > 0 for r in px4)
    assert ap and not any(r["unauthenticated_agent_discovery"] for r in ap)


def test_recorded_surface_runs_are_internally_consistent():
    """results/surface: every release answered a read-only FTP listing and a parameter
    read, and the static shell detection is recorded per build (not inferred)."""
    import json
    from pathlib import Path
    d = Path(__file__).resolve().parent.parent / "results/surface"
    recs = [json.loads(f.read_text()) for f in sorted(d.glob("surface-*.json"))]
    assert len(recs) >= 3
    for r in recs:
        assert r["advertised"]["ftp"] is True
        assert r["answered"]["param_read"] is True
        assert r["answered"]["ftp_list"]["result"] == "ack"
        assert r["static"]["checked"] is True
    px4 = [r for r in recs if r["stack"] == "px4"]
    ap = [r for r in recs if r["stack"] == "ardupilot"]
    # The shell asymmetry the README claims, asserted against the recorded data.
    assert all(r["static"]["hits"]["mavlink_shell"] is True for r in px4)
    assert all(r["static"]["hits"]["mavlink_shell"] is False for r in ap)
