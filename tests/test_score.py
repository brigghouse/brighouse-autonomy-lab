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
    s = score(r, policy="ideal-oob-provisioning", link_confidential=True)
    assert s["score"] == 100.0 and s["grade"] == "A"


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


def test_partial_credit_for_signed_fraction():
    half = score(base_report(ep={"signed_frames": 50}), policy="px4-1.18")["score"]
    none = score(base_report(ep={"signed_frames": 0}), policy="px4-1.18")["score"]
    full = score(base_report(ep={"signed_frames": 100}), policy="px4-1.18")["score"]
    assert none < half < full
