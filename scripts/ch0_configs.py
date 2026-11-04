"""Does ArduPilot's unsigned-accept exemption follow the *channel index* or the *link type*?

ArduPilot's `accept_unsigned_callback` (GCS_Signing.cpp) accepts any unsigned frame on
MAVLINK_COMM_0 on the assumption that channel 0 is USB. Upstream issue #34489 / PR #34780
(unmerged as of Nov 2026) note that on boards where SERIAL0 is not USB the exemption is
wrong. This script measures it in SITL by moving the *transport* of channel 0 and
channel 1 independently and observing whether an unsigned PARAM_REQUEST_READ is answered
while a signing key is active:

  A  ch0 = TCP, ch1 = TCP            baseline (same as results/conformance)
  B  ch0 = UDP, ch1 = TCP            channel 0 over a network transport
  C  ch0 = TCP, ch1 = UDP            channel 1 over the same network transport
  D  ch0 = TCP, ch1 = TCP MAVLink 1  SERIAL1_PROTOCOL=1: a MAVLink 1 port under a key

If the exemption follows the index, B accepts unsigned on ch0 and C rejects unsigned on
ch1 although both are UDP. D measures the documented "MAVLink 1 ports are not protected".

Read-only probes only (PARAM_REQUEST_READ) plus the reversible SETUP_SIGNING provisioning
step, against a local SITL that this script starts and stops itself.

    python scripts/ch0_configs.py --ardupilot ~/sitl/ardupilot --out results/ch0-configs
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import tempfile
import time
from pathlib import Path

import labkit
from conformance import _probe_read
from mavaudit.model.configs import BY_NAME
from mavaudit.model.semantics import READ, Frame, State, step

#: How long a probe waits for a reply before recording "not answered". A negative result
#: is therefore a *timeout*, not an observed rejection: the vehicle may have replied late.
#: Stated here because every "rejected" cell in the published table rests on it.
PROBE_TIMEOUT = 5.0

UDP0, UDP1 = 14600, 14601
TCP0, TCP1 = 5760, 5762

CONFIGS = {
    "A-ch0tcp-ch1tcp": {"serial0": None, "serial1": "tcp:2", "extra": {},
                        "ch0": f"tcp:127.0.0.1:{TCP0}", "ch1": f"tcp:127.0.0.1:{TCP1}"},
    "B-ch0udp-ch1tcp": {"serial0": f"udpclient:127.0.0.1:{UDP0}", "serial1": "tcp:2", "extra": {},
                        "ch0": f"udpin:127.0.0.1:{UDP0}", "ch1": f"tcp:127.0.0.1:{TCP1}"},
    "C-ch0tcp-ch1udp": {"serial0": None, "serial1": f"udpclient:127.0.0.1:{UDP1}", "extra": {},
                        "ch0": f"tcp:127.0.0.1:{TCP0}", "ch1": f"udpin:127.0.0.1:{UDP1}"},
    "D-ch0tcp-ch1mav1": {"serial0": None, "serial1": "tcp:2", "extra": {"SERIAL1_PROTOCOL": 1},
                         "ch0": f"tcp:127.0.0.1:{TCP0}", "ch1": f"tcp:127.0.0.1:{TCP1}", "ch1_v1": True},
}


def probe(cfg: dict, link: str, signed: bool, key) -> dict:
    """Read probe that measures three things instead of one, because the first version
    measured a *timeout* and called it a rejection.

    What it still measures: whether an unsigned (or signed) PARAM_REQUEST_READ is
    answered, and the wire version of the frame we actually sent. pymavlink's
    `auto_mavlink_version` silently upgrades a connection to MAVLink 2 (and sets
    MAVLINK20 process-wide) as soon as it receives a v2 frame, so a port configured for
    MAVLink 1 is the only case where a v1 probe survives the heartbeat. Returning the
    first byte of the frame we send (0xFE = v1, 0xFD = v2) keeps the record honest: an
    earlier version labelled the wire version from the configuration, not from the frame.

    What it now also measures, and the reason this function was rewritten: a silent link
    and a refusing autopilot look identical from here. Two controls separate them, both
    inside the same connection and the same moment as the negative result:

    1. **Liveness.** HEARTBEAT is broadcast and is allowlisted by both stacks, so it
       arrives whether or not our frame was accepted. If heartbeats from the vehicle keep
       arriving across the window in which our PARAM_VALUE does not, the peer was alive
       and did not answer. If they stop too, the link died and the case says nothing.
    2. **Positive control.** On the same link, immediately after, we send a *correctly
       signed* read. A policy that is rejecting our unsigned frame must accept that one.
       If the control is also unanswered, the probe or the link is at fault rather than
       the policy, whatever the negative result looked like.

    So the verdict is no longer a boolean. `accepted` means a reply arrived.
    `rejected` means no reply arrived *and* both controls passed. Anything else is
    `inconclusive`, with the reason recorded, and it is excluded from agreement counts
    rather than silently scored as a refusal. The control is skipped where it cannot
    apply (no key yet, or a MAVLink 1 port, which cannot carry a signature) and the case
    then rests on liveness alone, which is stated in the record.

    A MAVLink 1 frame cannot carry a signature, so `signed` is forced False there."""
    from pymavlink import mavutil
    want_v1 = bool(cfg.get(f"{link}_v1"))
    saved = os.environ.pop("MAVLINK20", None) if want_v1 else None
    if want_v1:
        mavutil.set_dialect("all")
    try:
        conn = mavutil.mavlink_connection(cfg[link], source_system=251, dialect="all")
        conn.wait_heartbeat(timeout=15)
        if signed and key is not None and not want_v1:
            conn.setup_signing(key, sign_outgoing=True,
                               allow_unsigned_callback=lambda m, i: True)
        wire = conn.mav.param_request_read_encode(1, 1, b"", 0).pack(conn.mav)[0]
        conn.mav.param_request_read_send(1, 1, b"", 0)

        # One loop watches for both the answer and the liveness evidence, so the
        # liveness claim is about the same window as the negative result and not a
        # separate check made afterwards.
        deadline = time.time() + PROBE_TIMEOUT
        answered, heartbeats = False, 0
        while time.time() < deadline:
            m = conn.recv_match(type=["PARAM_VALUE", "HEARTBEAT"], blocking=True, timeout=0.5)
            if m is None or m.get_srcSystem() != 1:
                continue
            if m.get_type() == "HEARTBEAT":
                heartbeats += 1
            elif int(getattr(m, "param_index", -2)) == 0:
                answered = True
                break

        control = _positive_control(conn, cfg, link, key, want_v1, signed)
        conn.close()

        if answered:
            verdict, reason = "accepted", None
        elif heartbeats == 0:
            verdict, reason = "inconclusive", ("no HEARTBEAT from the vehicle during the "
                                               "window, so the link cannot be shown to "
                                               "have been up when the read went unanswered")
        elif control["ran"] and not control["answered"]:
            verdict, reason = "inconclusive", ("a correctly signed read on the same link "
                                               "was also unanswered, so the probe or the "
                                               "link is implicated, not the policy")
        else:
            verdict, reason = "rejected", None

        return {"verdict": verdict, "answered": answered, "wire": wire,
                "heartbeats_during_window": heartbeats, "positive_control": control,
                "inconclusive_reason": reason,
                "timeout_s": PROBE_TIMEOUT}
    finally:
        if saved is not None:
            os.environ["MAVLINK20"] = saved
            mavutil.set_dialect("all")


def _positive_control(conn, cfg, link, key, want_v1, already_signed) -> dict:
    """Send a correctly signed read on the live connection and report whether it was
    answered. This is the control that turns a silence into a rejection, so its own
    limits are recorded rather than assumed: it cannot run before a key exists, and it
    cannot run on a MAVLink 1 port, which has no signature field at all."""
    if key is None:
        return {"ran": False, "answered": None,
                "skipped_because": "no key provisioned yet on this link"}
    if want_v1:
        return {"ran": False, "answered": None,
                "skipped_because": "MAVLink 1 frames cannot carry a signature"}
    try:
        if not already_signed:
            conn.setup_signing(key, sign_outgoing=True,
                               allow_unsigned_callback=lambda m, i: True)
        conn.mav.param_request_read_send(1, 1, b"", 0)
        deadline = time.time() + PROBE_TIMEOUT
        while time.time() < deadline:
            m = conn.recv_match(type="PARAM_VALUE", blocking=True, timeout=0.5)
            if m is not None and m.get_srcSystem() == 1 and int(getattr(m, "param_index", -2)) == 0:
                return {"ran": True, "answered": True,
                        "means": "the link and the probe both work; a silent negative on "
                                 "this link is the policy refusing, not a dead link"}
        return {"ran": True, "answered": False,
                "means": "a correctly signed read went unanswered too, so nothing on this "
                         "link can be attributed to the policy"}
    except Exception as e:  # a control that errors must not be read as a pass
        return {"ran": False, "answered": None, "skipped_because": f"control errored: {e!r}"}


def _case(r: dict, policy, cfg: dict, link: str, *, state: str,
          signed: bool, keyed: bool) -> dict:
    """One recorded case. `observed` stays a boolean for the cases that decided something,
    so the existing agreement arithmetic is unchanged, but the verdict and the evidence
    behind it travel with it -- including, when the case is a rejection, what made it a
    rejection rather than a timeout."""
    wire = 1 if r["wire"] == 0xFE else 2
    return {"state": state, "link": link, "transport": cfg[link].split(":")[0],
            "wire_first_byte_sent": r["wire"], "wire": wire, "signed": signed,
            "predicted": predict(policy, link, signed, keyed, wire=wire),
            "observed": r["answered"],
            "verdict": r["verdict"],
            "inconclusive_reason": r["inconclusive_reason"],
            "evidence_for_negative": {
                "heartbeats_during_window": r["heartbeats_during_window"],
                "positive_control": r["positive_control"],
                "timeout_s": r["timeout_s"],
                "note": ("a negative is recorded as a rejection only when the vehicle was "
                         "seen alive in the same window and a correctly signed read on the "
                         "same link was answered")}}


def predict(policy, link: str, signed: bool, keyed: bool, wire: int = 2) -> bool:
    """The prediction must be made for the frame we actually send, wire version included.
    An earlier version omitted `wire`, which silently made every prediction a version-2
    prediction: configuration D then "agreed" with both ardupilot-4.7.2 and its
    documentation variant, and the experiment could not discriminate between them at all.
    Found by an independent reviewer, not by us."""
    st = State(key="K" if keyed else None, clock=2_000_000)
    fr = Frame(link, (9, 9) if not signed else (1, 1), READ, signed=signed,
               key="K" if signed else None, ts=2_000_050, link_id=1, wire=wire)
    return step(policy, st, fr).accepted


def start_sitl(ap: Path, workdir: Path, cfg: dict) -> subprocess.Popen:
    defaults = [str(ap / "Tools/autotest/default_params/copter.parm")]
    if cfg["extra"]:
        extra = workdir / "extra.parm"
        extra.write_text("".join(f"{k} {v}\n" for k, v in cfg["extra"].items()))
        defaults.append(str(extra))
    cmd = [str(ap / "build/sitl/bin/arducopter"), "--model", "+", "--speedup", "1", "-I0", "-w",
           "--defaults", ",".join(defaults), "--serial1", cfg["serial1"]]
    if cfg["serial0"]:
        cmd += ["--serial0", cfg["serial0"]]
    log = open(workdir / "sitl.log", "w")
    proc = subprocess.Popen(cmd, cwd=workdir, stdout=log, stderr=subprocess.STDOUT)
    if cfg["ch0"].startswith("tcp:"):
        labkit.wait_tcp(TCP0)
    else:
        time.sleep(3)
    return proc


def run_config(name: str, cfg: dict, ap: Path, policy) -> dict:
    workdir = Path(tempfile.mkdtemp(prefix=f"ap-{name}-"))
    key = labkit.lab_key()
    proc = start_sitl(ap, workdir, cfg)
    cases = []
    try:
        # SITL boots once SERIAL0 has a peer; one unkeyed read on ch0 also settles that.
        for link in ("ch0", "ch1"):
            r = probe(cfg, link, False, None)
            cases.append(_case(r, policy, cfg, link, state="unkeyed", signed=False, keyed=False))
        labkit.provision_signing(cfg["ch0"], key)
        for link in ("ch0", "ch1"):
            for signed in ((False,) if cfg.get(f"{link}_v1") else (False, True)):
                r = probe(cfg, link, signed, key)
                cases.append(_case(r, policy, cfg, link, state="keyed", signed=signed, keyed=True))
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=10)
        except subprocess.TimeoutExpired:
            proc.kill()
    # An inconclusive case is neither agreement nor refutation. Counting it either way
    # would be the same mistake as reading an empty packet capture as a clean result.
    for c in cases:
        c["agree"] = (None if c["verdict"] == "inconclusive"
                      else c["predicted"] == c["observed"])
    decided = [c for c in cases if c["agree"] is not None]
    inconclusive = [c for c in cases if c["agree"] is None]
    return {"config": name, "serial0": cfg["serial0"] or "tcp:0 (default)", "serial1": cfg["serial1"],
            "extra_params": cfg["extra"], "cases": cases,
            "agree": sum(c["agree"] for c in decided), "total": len(decided),
            "inconclusive": len(inconclusive),
            "inconclusive_reasons": sorted({c["inconclusive_reason"] for c in inconclusive
                                            if c["inconclusive_reason"]}),
            "denominator_note": ("agree/total count only decided cases; inconclusive cases "
                                 "are reported separately and are not scored either way")}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--ardupilot", type=Path, required=True)
    p.add_argument("--policy", default="ardupilot-4.7.2")
    p.add_argument("--out", type=Path, default=labkit.REPO / "results/ch0-configs")
    p.add_argument("--only", nargs="*")
    a = p.parse_args()
    policy = BY_NAME[a.policy]
    a.out.mkdir(parents=True, exist_ok=True)
    results = {"stack": "ArduPilot Copter SITL", "source_rev": labkit.git_rev(a.ardupilot),
               "policy": a.policy, "started_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
               "configs": []}
    for name, cfg in CONFIGS.items():
        if a.only and name not in a.only:
            continue
        r = run_config(name, cfg, a.ardupilot, policy)
        results["configs"].append(r)
        print(name, f"{r['agree']}/{r['total']}",
              [(c["state"], c["link"], c["transport"], f"v{c['wire']}", c["signed"], c["observed"])
               for c in r["cases"]])
        (a.out / "ch0-configs.json").write_text(json.dumps(results, indent=2))
        time.sleep(2)


if __name__ == "__main__":
    main()
