"""A transparent, reproducible secure-by-default score for a MAVLink C2 link.

The score is a rubric, not a claim of canonical truth. It is designed to satisfy three
axioms so that it is defensible as conformance evidence:

  A1 Provenance.   Every criterion is computed from an observable (a mavaudit finding or a
                   model property), never from opinion; the breakdown cites the observable.
  A2 Monotonicity. Removing a finding (improving posture) never lowers the score.
  A3 CRA-grounded weights. Each criterion maps to a CRA Annex I, Part I(2) requirement and
                   carries a fixed weight; weights sum to 100.

The input is a mavaudit report dict (for the link under test) plus, optionally, the
provisioning model policy name (for the one criterion a single audit cannot observe: the
trust-on-first-use window). Output is a 0-100 score with a per-criterion breakdown.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from .model.configs import BY_NAME


@dataclass(frozen=True)
class Criterion:
    key: str
    weight: int
    cra: str
    describe: str


# Weights reflect CRA Annex I emphasis: integrity/access control of the command channel
# dominate; confidentiality and maintenance are real but lighter for a C2 link.
CRITERIA = [
    Criterion("integrity", 28, "I.2(f)", "command/telemetry frames are signed"),
    Criterion("access_control", 24, "I.2(d)", "unsigned requests are rejected"),
    Criterion("attack_surface", 16, "I.2(j)", "no unauthenticated file-transfer/service exposure"),
    Criterion("no_legacy", 10, "I.2(b)", "no unprotected MAVLink 1 on the link"),
    Criterion("provisioning", 12, "I.2(d)", "no trust-on-first-use key window (out-of-band keys)"),
    Criterion("confidentiality", 6, "I.2(e)", "link payloads are confidential"),
    Criterion("maintenance", 4, "II.1", "firmware identifiable for SBOM/advisory tracking"),
]
MAXW = sum(c.weight for c in CRITERIA)
assert MAXW == 100


def _endpoint(report: dict) -> dict:
    eps = [e for e in report.get("endpoints", []) if e.get("autopilot") in ("ardupilot", "px4")]
    return eps[0] if eps else (report.get("endpoints", [{}]) or [{}])[0]


def score(report: dict, policy: Optional[str] = None, link_confidential: bool = False) -> dict:
    """Compute the score for one audited link. `report` is a mavaudit report dict."""
    ep = _endpoint(report)
    probe = report.get("unsigned_probe") or {}
    raw_frames = int(ep.get("frames", 0) or 0)
    # A1 (provenance): absence of evidence is not evidence of security. A run that
    # observed no frames and whose probe never answered is unscorable, not a good score.
    if raw_frames == 0 and not bool(probe.get("answered")):
        return {"score": None, "max": MAXW, "grade": "N/A", "insufficient_data": True,
                "reason": "no frames observed and probe did not complete; run is unscorable",
                "link": report.get("target"), "policy": policy, "breakdown": []}
    frames = max(raw_frames, 1)
    signed_frac = ep.get("signed_frames", 0) / frames
    unsigned_answered = bool(probe.get("answered"))
    ftp = ep.get("ftp_advertised")
    v1 = ep.get("v1_frames", 0) > 0
    firmware = ep.get("firmware")

    # Each criterion returns a fraction in [0,1] of its weight earned (A1: from observables).
    met = {
        "integrity": signed_frac,                                   # partial credit = signed fraction
        "access_control": 0.0 if unsigned_answered else 1.0,
        "attack_surface": 1.0 if ftp is False else (0.0 if ftp else 0.5),  # None(unknown)->0.5
        "no_legacy": 0.0 if v1 else 1.0,
        "provisioning": _provisioning_credit(policy),
        "confidentiality": 1.0 if link_confidential else 0.0,
        "maintenance": 1.0 if firmware else 0.0,
    }
    breakdown = []
    total = 0.0
    for c in CRITERIA:
        earned = round(c.weight * met[c.key], 2)
        total += earned
        breakdown.append({"criterion": c.key, "cra": c.cra, "weight": c.weight,
                          "fraction": round(met[c.key], 3), "earned": earned, "describe": c.describe})
    return {"score": round(total, 1), "max": MAXW, "grade": _grade(total),
            "link": report.get("target"), "policy": policy, "breakdown": breakdown}


def _provisioning_credit(policy: Optional[str]) -> float:
    """Full credit for out-of-band provisioning; none for a trust-on-first-use window.
    Unknown policy -> neutral 0.5 (audit alone cannot observe the first-use window)."""
    if policy is None:
        return 0.5
    p = BY_NAME.get(policy)
    if p is None:
        return 0.5
    if p.oob_provision:
        return 1.0
    if p.tofu:
        return 0.0
    return 0.5


def _grade(total: float) -> str:
    return ("A" if total >= 90 else "B" if total >= 75 else "C" if total >= 55
            else "D" if total >= 35 else "E")


def score_summary_run(summary_run: dict, policy: Optional[str] = None,
                      link_confidential: bool = False) -> dict:
    """Score from a longitudinal/summary 'run' dict (no full report).  A2-safe."""
    if int(summary_run.get("frames", 0) or 0) == 0 and not summary_run.get("unsigned_probe_answered"):
        return {"score": None, "max": MAXW, "grade": "N/A", "insufficient_data": True,
                "reason": "no frames observed and probe did not complete; run is unscorable",
                "link": summary_run.get("firmware"), "policy": policy, "breakdown": []}
    frames = max(summary_run.get("frames", 0), 1)
    fake_report = {
        "target": None,
        "endpoints": [{
            "autopilot": "ardupilot" if (summary_run.get("firmware") or "").count(".") else "px4",
            "frames": frames,
            "signed_frames": summary_run.get("signed_frames", 0),
            "v1_frames": summary_run.get("v1_frames", 0),
            "ftp_advertised": summary_run.get("ftp_advertised"),
            "firmware": summary_run.get("firmware"),
        }],
        "unsigned_probe": {"answered": summary_run.get("unsigned_probe_answered")},
    }
    return score(fake_report, policy, link_confidential)
