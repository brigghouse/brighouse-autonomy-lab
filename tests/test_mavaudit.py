import socket
import time

import pytest

from mavaudit import cli
from mavaudit.safety import ScopeError, check_scope
from mavaudit.sim.fake_vehicle import FakeVehicle


def free_port() -> int:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()
    return port


def run_scan(tmp_path, mode, active=True, autopilot="ardupilot"):
    port = free_port()
    vehicle = FakeVehicle(port, mode=mode, autopilot=autopilot)
    vehicle.start_background()
    out = tmp_path / f"report_{mode}"
    try:
        args = ["scan", "--target", f"udpin:127.0.0.1:{port}", "--duration", "2", "--out", str(out)]
        if active:
            args.append("--active-probe")
        rc = cli.main(args)
    finally:
        vehicle.stop()
        time.sleep(0.1)
    import json
    report = json.loads(out.with_suffix(".json").read_text())
    return rc, report


def ids(report):
    return {f["id"] for f in report["findings"]}


def test_scope_allows_lab_and_blocks_public():
    assert check_scope("udpin:127.0.0.1:14550").host == "127.0.0.1"
    assert check_scope("udpout:192.168.1.20:14550").host == "192.168.1.20"
    with pytest.raises(ScopeError):
        check_scope("udpout:8.8.8.8:14550")
    assert check_scope("udpout:8.8.8.8:14550", authorized=True, scope_ref="ENG-001").host == "8.8.8.8"


def test_unsigned_vehicle_flags_high(tmp_path):
    rc, report = run_scan(tmp_path, "unsigned")
    assert rc == 0
    assert {"MAV-002", "MAV-004", "MAV-005"} <= ids(report)
    assert report["unsigned_probe"]["answered"] is True
    ep = next(e for e in report["endpoints"] if e["sysid"] == 1)
    assert ep["autopilot"] == "ardupilot" and ep["signed_frames"] == 0
    assert ep["v2_frames"] > 0 and ep["v1_frames"] == 0
    assert "MAV-001" not in ids(report)


def test_signed_vehicle_rejects_unsigned_probe(tmp_path):
    rc, report = run_scan(tmp_path, "signed")
    assert rc == 0
    assert "MAV-002" not in ids(report)
    assert "MAV-005" not in ids(report)
    assert report["unsigned_probe"]["answered"] is False
    ep = next(e for e in report["endpoints"] if e["sysid"] == 1)
    assert ep["signed_frames"] == ep["frames"] > 0


def test_mavlink1_vehicle(tmp_path):
    rc, report = run_scan(tmp_path, "v1", active=False)
    assert "MAV-001" in ids(report)
    ep = next(e for e in report["endpoints"] if e["sysid"] == 1)
    assert ep["v1_frames"] > 0


def test_px4_probe_param(tmp_path):
    rc, report = run_scan(tmp_path, "unsigned", autopilot="px4")
    assert report["unsigned_probe"]["param"] == "index:0"
    assert report["unsigned_probe"]["response"] == "PARAM_VALUE"


def run_scan_vehicle(tmp_path, vehicle_kwargs, extra=()):
    port = free_port()
    vehicle = FakeVehicle(port, **vehicle_kwargs)
    vehicle.start_background()
    out = tmp_path / "report"
    try:
        rc = cli.main(["scan", "--target", f"udpin:127.0.0.1:{port}", "--duration", "2",
                       "--active-probe", "--out", str(out), *extra])
    finally:
        vehicle.stop()
        time.sleep(0.1)
    import json
    return rc, json.loads(out.with_suffix(".json").read_text())


def test_firmware_and_ftp_on_unsigned_px4(tmp_path):
    rc, report = run_scan_vehicle(tmp_path, {"mode": "unsigned", "autopilot": "px4", "version": (1, 16, 0)})
    ep = next(e for e in report["endpoints"] if e["sysid"] == 1)
    assert ep["firmware_tuple"] == [1, 16, 0]
    assert ep["ftp_advertised"] is True
    f6 = next(f for f in report["findings"] if f["id"] == "MAV-006")
    assert any(a["id"] == "CVE-2026-32709" for a in f6["advisories"])
    f2 = next(f for f in report["findings"] if f["id"] == "MAV-002")
    assert any(a["id"] == "CVE-2026-1579" for a in f2["advisories"])
    assert "MAV-007" in ids(report)


def test_fixed_px4_version_drops_ftp_advisory(tmp_path):
    rc, report = run_scan_vehicle(tmp_path, {"mode": "unsigned", "autopilot": "px4", "version": (1, 17, 0)})
    f6 = next(f for f in report["findings"] if f["id"] == "MAV-006")
    assert f6["advisories"] == []


def test_signed_vehicle_hides_version_and_ftp(tmp_path):
    rc, report = run_scan_vehicle(tmp_path, {"mode": "signed"})
    assert "MAV-006" not in ids(report) and "MAV-007" not in ids(report)


def test_fail_on_high_exit_code(tmp_path):
    rc, _ = run_scan_vehicle(tmp_path, {"mode": "unsigned"}, extra=("--fail-on", "high"))
    assert rc == 3
    rc, _ = run_scan_vehicle(tmp_path, {"mode": "signed"}, extra=("--fail-on", "high"))
    assert rc == 0


def test_version_decoding():
    from mavaudit.advisories import decode_version
    assert decode_version((4 << 24) | (7 << 16) | (2 << 8) | 255) == (4, 7, 2, 255)


def test_signed_exempt_link_is_caught_by_active_probe(tmp_path):
    """Link signs everything it sends but accepts unsigned input (ArduPilot channel 0 pattern)."""
    rc, report = run_scan_vehicle(tmp_path, {"mode": "signed-exempt"})
    ep = next(e for e in report["endpoints"] if e["sysid"] == 1)
    assert ep["signed_frames"] == ep["frames"] > 0
    assert "MAV-002" not in ids(report)          # passive view: looks protected
    f5 = next(f for f in report["findings"] if f["id"] == "MAV-005")
    assert "passive check alone would wrongly suggest" in f5["detail"]
    assert "MAV-006" in ids(report)              # FTP reachable without the key
    assert report["unsigned_probe"]["command_ack_result"] == 0


def test_param_error_counts_as_answer(tmp_path):
    rc, report = run_scan_vehicle(tmp_path, {"mode": "unsigned", "param_error": True})
    assert report["unsigned_probe"]["answered"] is True
    assert report["unsigned_probe"]["response"] == "PARAM_ERROR"


def test_ftp_unknown_when_version_not_received(tmp_path):
    rc, report = run_scan_vehicle(tmp_path, {"mode": "signed"})
    ep = next(e for e in report["endpoints"] if e["sysid"] == 1)
    assert ep["ftp_advertised"] is None


def test_release_candidate_of_fixed_version_keeps_advisory(tmp_path):
    rc, report = run_scan_vehicle(tmp_path, {"mode": "unsigned", "autopilot": "px4",
                                             "version": (1, 17, 0), "version_type": 192})
    f6 = next(f for f in report["findings"] if f["id"] == "MAV-006")
    assert any(a["id"] == "CVE-2026-32709" for a in f6["advisories"])


def test_scope_serial_and_listen_addresses():
    from mavaudit.safety import check_peer
    assert check_scope("/dev/ttyUSB0").kind == "serial"                      # passive serial ok
    with pytest.raises(ScopeError):
        check_scope("/dev/ttyUSB0", active=True)                            # active over radio: refuse
    assert check_scope("/dev/ttyUSB0", authorized=True, scope_ref="ENG-1", active=True).kind == "serial"
    with pytest.raises(ScopeError):
        check_scope("udpin:drone.example.com:14550")                        # hostnames not trusted
    assert check_peer("127.0.0.1") and check_peer("10.0.0.5") and check_peer(None)
    assert not check_peer("8.8.8.8")
    assert check_peer("8.8.8.8", authorized=True, scope_ref="ENG-1")
