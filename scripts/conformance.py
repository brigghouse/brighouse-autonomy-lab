"""Model-based conformance testing: do the formal policies match the real stacks?

For a running SITL we derive READ-only and key-management test frames from the
acceptance semantics, send them, observe whether the vehicle responds, and compare
with the policy's predicted decision. Agreement turns a documentation-derived policy
(Table in the paper) into a measured one; a disagreement is a finding about either the
model or the implementation.

Only read-only probes (PARAM_REQUEST_READ) and reversible key-management steps
(SETUP_SIGNING) are used; no state-changing commands are sent. Local SITL only.

    python scripts/conformance.py ardupilot --target-trusted tcp:127.0.0.1:5760 \
        --target-untrusted tcp:127.0.0.1:5762 --policy ardupilot-4.7.2 --out results/conformance
    python scripts/conformance.py px4 --target-trusted udpin:127.0.0.1:14550 \
        --target-untrusted udpin:127.0.0.1:14540 --policy px4-1.18 --out ...
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import labkit  # noqa: E402
from pymavlink import mavutil  # noqa: E402

from mavaudit.model.configs import BY_NAME  # noqa: E402
from mavaudit.model.semantics import READ, SETUP, Frame, State, step  # noqa: E402


def _probe_read(conn, signed: bool, key: bytes | None, sysid=1, compid=1, timeout=3.0) -> bool:
    """Send one PARAM_REQUEST_READ (index 0); return True if answered. Read-only."""
    if signed and key is not None:
        conn.setup_signing(key, sign_outgoing=True, initial_timestamp=0)
    else:
        conn.signing.secret_key = None
        conn.signing.sign_outgoing = False
    conn.mav.param_request_read_send(sysid, compid, b"", 0)
    deadline = time.time() + timeout
    while time.time() < deadline:
        m = conn.recv_match(type=["PARAM_VALUE", "PARAM_ERROR"], blocking=True, timeout=0.5)
        if m is not None and m.get_srcSystem() == sysid and int(getattr(m, "param_index", -2)) == 0:
            return True
    return False


def model_predict(policy, link_trusted: bool, signed: bool, keyed: bool) -> bool:
    link = "ch0" if link_trusted else "ch1"
    st = State(key="K" if keyed else None, clock=2_000_000)
    fr = Frame(link, (9, 9) if not signed else (1, 1), READ, signed=signed,
               key="K" if signed else None, ts=2_000_050, link_id=1)
    return step(policy, st, fr).accepted


def run(stack: str, trusted: str, untrusted: str, policy_name: str, out: Path, duration_wait=3.0):
    policy = BY_NAME[policy_name]
    key = labkit.lab_key()
    cases, agree = [], 0

    def connect(target):
        c = mavutil.mavlink_connection(target, source_system=252, dialect="all")
        c.wait_heartbeat(timeout=20)
        return c

    # --- State 1: UNKEYED. Both links should answer both signed and unsigned reads ---
    for link_name, target, trustedlink in (("trusted", trusted, True), ("untrusted", untrusted, False)):
        c = connect(target)
        for signed in (False, True):
            obs = _probe_read(c, signed, key if signed else None, timeout=duration_wait)
            pred = model_predict(policy, trustedlink, signed, keyed=False)
            cases.append({"state": "unkeyed", "link": link_name, "signed": signed,
                          "predicted": pred, "observed": obs, "agree": pred == obs})
            agree += pred == obs
        c.close()

    # --- Provision the key over the trusted link (operator step) ---
    try:
        labkit.provision_signing(trusted, key)
        provisioned = True
    except Exception as e:  # noqa: BLE001
        provisioned = False
        cases.append({"provision_error": repr(e)})

    # --- State 2: KEYED. Unsigned reads: trusted link may still answer (R4); untrusted must not ---
    if provisioned:
        for link_name, target, trustedlink in (("trusted", trusted, True), ("untrusted", untrusted, False)):
            c = connect(target)
            for signed in (False, True):
                obs = _probe_read(c, signed, key if signed else None, timeout=duration_wait)
                pred = model_predict(policy, trustedlink, signed, keyed=True)
                cases.append({"state": "keyed", "link": link_name, "signed": signed,
                              "predicted": pred, "observed": obs, "agree": pred == obs})
                agree += pred == obs
            c.close()

    checked = [c for c in cases if "agree" in c]
    result = {
        "stack": stack, "policy": policy_name, "provisioned": provisioned,
        "cases_total": len(checked),
        "cases_agree": sum(c["agree"] for c in checked),
        "agreement": round(sum(c["agree"] for c in checked) / max(len(checked), 1), 3),
        "disagreements": [c for c in checked if not c["agree"]],
        "cases": cases,
    }
    out.mkdir(parents=True, exist_ok=True)
    (out / f"conformance-{policy_name}.json").write_text(json.dumps(result, indent=2))
    print(json.dumps({k: result[k] for k in ("stack", "policy", "provisioned", "cases_total",
                                             "cases_agree", "agreement")}, indent=2))
    if result["disagreements"]:
        print("DISAGREEMENTS:", json.dumps(result["disagreements"], indent=2))
    return result


def main():
    p = argparse.ArgumentParser()
    p.add_argument("stack", choices=["ardupilot", "px4"])
    p.add_argument("--target-trusted", required=True)
    p.add_argument("--target-untrusted", required=True)
    p.add_argument("--policy", required=True)
    p.add_argument("--out", type=Path, required=True)
    a = p.parse_args()
    run(a.stack, a.target_trusted, a.target_untrusted, a.policy, a.out)


if __name__ == "__main__":
    main()
