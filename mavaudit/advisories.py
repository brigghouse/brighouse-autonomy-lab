"""Small, curated advisory table used to annotate findings.

Only entries verified against NVD / vendor advisories during the literature
review (research/literature-review.md, section 4) are included. This is NOT a
vulnerability scanner: matching is coarse and is meant to point the reader to
the advisory, not to assert exploitability.
"""

from __future__ import annotations

ADVISORIES = [
    {
        "id": "CVE-2026-1579",
        "ref": "https://www.cisa.gov/news-events/ics-advisories/icsa-26-090-02",
        "autopilot": "px4",
        "applies_when": "unsigned",
        "summary": "CISA ICSA-26-090-02: missing authentication for critical function in PX4 MAVLink "
                   "(CWE-306, CVSS v3 9.8). Remediation: enable MAVLink 2 signing on non-USB links.",
    },
    {
        "id": "CVE-2026-32709",
        "ref": "https://github.com/PX4/PX4-Autopilot/security/advisories/GHSA-fh32-qxj9-x32f",
        "autopilot": "px4",
        "applies_when": "ftp_unsigned",
        "fixed_in": (1, 17, 0),
        "summary": "PX4 MAVLink FTP path traversal reachable by unauthenticated peers; fixed in 1.17.0-rc2.",
    },
    {
        "id": "CVE-2020-10283",
        "ref": "https://nvd.nist.gov/vuln/detail/CVE-2020-10283",
        "autopilot": "any",
        "applies_when": "v1",
        "summary": "MAVLink v2 to v1 downgrade bypasses v2 authentication (CWE-288).",
    },
]


def decode_version(flight_sw_version: int) -> tuple[int, int, int, int]:
    """MAVLink AUTOPILOT_VERSION.flight_sw_version: major<<24 | minor<<16 | patch<<8 | type."""
    v = int(flight_sw_version)
    return (v >> 24) & 0xFF, (v >> 16) & 0xFF, (v >> 8) & 0xFF, v & 0xFF


OFFICIAL = 255  # FIRMWARE_VERSION_TYPE_OFFICIAL; lower values are dev/alpha/beta/rc builds


def matching(autopilot: str | None, condition: str, version: tuple[int, int, int] | None = None,
             version_type: int | None = None) -> list[dict]:
    out = []
    for adv in ADVISORIES:
        if adv["applies_when"] != condition:
            continue
        if adv["autopilot"] not in ("any", autopilot):
            continue
        fixed = adv.get("fixed_in")
        if fixed and version:
            v = tuple(version[:3])
            # A pre-release of the fixed version (e.g. 1.17.0-rc1) may predate the fix: keep it.
            if v > fixed or (v == fixed and version_type in (None, OFFICIAL)):
                continue
        out.append({k: adv[k] for k in ("id", "ref", "summary")})
    return out
