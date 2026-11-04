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
    # `evidence` is the field that matters: it is the raw string-match count with
    # generated MAVLink dialect headers excluded, which is what caught the
    # serial_control false positive. Asserting on the raw count would re-admit it.
    assert all(r["static"]["hits"]["mavlink_shell"]["evidence"] is True for r in px4)
    assert all(r["static"]["hits"]["mavlink_shell"]["evidence"] is False for r in ap)
    # ArduPilot's serial_control matches exist but live only in generated headers.
    for r in ap:
        sc = r["static"]["hits"]["serial_control"]
        assert sc["any_match"] is True and sc["excluding_generated_headers"] == 0
        assert sc["evidence"] is False
    # Repeatability must be measured and retained, not asserted in prose.
    for r in recs:
        rp = r["repeatability"]
        assert rp["live_runs"] >= 3
        assert rp["identical_across_runs"] is True
        assert len(rp["per_run"]) == rp["live_runs"]


def test_allowlists_extracted_from_source_match_the_readme():
    """results/allowlists: the exceptions to signing, with the claims the README makes
    about them asserted against the extracted data (not against prose)."""
    import json
    from pathlib import Path
    p = Path(__file__).resolve().parent.parent / "results/allowlists/allowlists.json"
    d = json.loads(p.read_text())
    ap = d["stacks"]["ardupilot"]
    px4 = d["stacks"]["px4"]
    assert {e["message"] for e in ap["allowlist"]["entries"]} == {"RADIO_STATUS", "RADIO"}
    assert {e["message"] for e in px4["allowlist"]["entries"]} == {
        "HEARTBEAT", "RADIO_STATUS", "ADSB_VEHICLE", "COLLISION"}
    # ArduPilot's blanket channel exemption exists; PX4's does not.
    assert ap["channel_exemption"]["present"] is True
    assert px4["channel_exemption"]["present"] is False
    # G8: neither stack allowlists Remote ID messages, so signing covers them.
    assert not any(v for v in d["open_drone_id_allowlisted"].values())
    # Every entry carries file/line provenance (A1).
    for st in (ap, px4):
        assert st["allowlist"]["file"]
        assert all(e["line"] > 0 for e in st["allowlist"]["entries"])


def test_protocol_ceiling_is_82_not_70():
    """A published metric must not confuse a measurement with a bound. An earlier draft
    claimed the MAVLink ceiling was 'near 70, grade C', quoting the best score measured
    (74) as though it were the maximum. The actual bound, with everything earnable under
    MAVLink 2 signing alone, is 82 (grade B); out-of-band keys take it to 94, and link
    encryption to 100."""
    perfect = {"target": None,
               "endpoints": [{"autopilot": "px4", "frames": 100, "signed_frames": 100,
                              "v1_frames": 0, "ftp_advertised": False, "firmware": "x"}],
               "unsigned_probe": {"answered": False},
               "control_plane": {"unauthenticated": False, "detail": "none offered"}}
    signing_only = score(dict(perfect), policy="px4-1.18", link_confidential=False)
    assert signing_only["score"] == 82.0 and signing_only["grade"] == "B"
    oob = score(dict(perfect), policy="ideal-oob-provisioning", link_confidential=False)
    assert oob["score"] == 94.0
    both = score(dict(perfect), policy="ideal-oob-provisioning", link_confidential=True)
    assert both["score"] == 100.0
    # The two unearnable criteria are exactly provisioning (12) and confidentiality (6).
    missing = {b["criterion"] for b in signing_only["breakdown"] if b["earned"] < b["weight"]}
    assert missing == {"provisioning", "confidentiality"}


def test_recorded_measurements_declare_their_repeatability_and_target():
    """Validity hygiene, asserted so it cannot quietly drop out of the write-ups:
    each campaign's README states how often it was repeated, and the surface campaign
    states that it measured a POSIX/SITL target rather than generalising to NuttX."""
    from pathlib import Path
    base = Path(__file__).resolve().parent.parent / "results"
    ch0 = (base / "ch0-configs/README.md").read_text()
    assert "Repeatability" in ch0 and "three times" in ch0
    # The hardware-carryover claim must be labelled source-derived, not measured.
    assert "source-derived argument, not a measurement" in ch0
    # Normalise whitespace: the prose is hard-wrapped, the claim is what matters.
    surface = " ".join((base / "surface/README.md").read_text().split())
    assert "SITL is not NuttX" in surface and "POSIX/SITL build" in surface
    dds = (base / "dds/README.md").read_text()
    assert "Repeatability" in dds


def test_every_recorded_rejection_carries_the_evidence_that_makes_it_one():
    """The defect this pins: the first version of the channel-0 experiment measured a
    timeout and recorded it as a rejection. A negative may only be called `rejected` when
    the vehicle was seen alive in the same window and, where it can run, a correctly
    signed read on the same link was answered. Anything else is `inconclusive` and must
    not be counted as agreement or refutation."""
    import json
    from pathlib import Path
    d = json.loads((Path(__file__).resolve().parent.parent
                    / "results/ch0-configs/ch0-configs.json").read_text())
    runs = d if isinstance(d, list) else d.get("configs", d.get("runs", [d]))
    assert runs
    rejections = 0
    for r in runs:
        cases = r["cases"]
        # The denominator may not quietly absorb inconclusive cases.
        decided = [c for c in cases if c["agree"] is not None]
        assert r["total"] == len(decided)
        assert r.get("inconclusive", 0) == len(cases) - len(decided)
        for c in cases:
            if c["verdict"] == "inconclusive":
                assert c["agree"] is None
                assert c["inconclusive_reason"]
                continue
            assert c["verdict"] in ("accepted", "rejected")
            if c["verdict"] != "rejected":
                continue
            rejections += 1
            e = c["evidence_for_negative"]
            # Liveness is mandatory for every rejection, without exception.
            assert e["heartbeats_during_window"] >= 1, (r["config"], c["link"])
            pc = e["positive_control"]
            if pc["ran"]:
                assert pc["answered"] is True, (r["config"], c["link"])
            else:
                # A control that cannot run must say why; silence is what we are fixing.
                assert pc.get("skipped_because")
    assert rejections >= 1, "a campaign with no rejections would make this test vacuous"
