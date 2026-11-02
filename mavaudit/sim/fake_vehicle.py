"""Minimal fake MAVLink vehicle for tests and demos (no real autopilot needed).

Sends HEARTBEATs and answers PARAM_REQUEST_READ. Modes:
- unsigned:  MAVLink 2, no signing, answers everyone (typical default config)
- signed:    signs outgoing frames and rejects unsigned incoming messages
- v1:        MAVLink 1 framing

    python -m mavaudit.sim.fake_vehicle --mode unsigned --port 14550
"""

from __future__ import annotations

import argparse
import hashlib
import threading
import time

from pymavlink import mavutil
from pymavlink.dialects.v20 import ardupilotmega as mavlink2


def demo_key(passphrase: str = "brighouse-lab-demo") -> bytes:
    return hashlib.sha256(passphrase.encode()).digest()


class FakeVehicle:
    def __init__(self, port: int, mode: str = "unsigned", autopilot: str = "ardupilot", sysid: int = 1,
                 version: tuple[int, int, int] = (4, 7, 2)):
        self.mode = mode
        self.version = version
        self.sysid = sysid
        self.autopilot = (mavlink2.MAV_AUTOPILOT_ARDUPILOTMEGA if autopilot == "ardupilot"
                          else mavlink2.MAV_AUTOPILOT_PX4)
        self.param = "SYSID_THISMAV" if autopilot == "ardupilot" else "MAV_SYS_ID"
        self.conn = mavutil.mavlink_connection(f"udpout:127.0.0.1:{port}", source_system=sysid,
                                               source_component=1, dialect="ardupilotmega")
        self.conn.mav.robust_parsing = True
        if mode == "v1":
            self.conn.mav.WIRE_PROTOCOL_VERSION = "1.0"
        if mode == "signed":
            # Only RADIO_STATUS may be accepted unsigned (per the signing spec).
            self.conn.setup_signing(demo_key(), sign_outgoing=True,
                                    allow_unsigned_callback=lambda mav, msgid: msgid == mavlink2.MAVLINK_MSG_ID_RADIO_STATUS)
        self._stop = threading.Event()
        self.answered = 0

    def _send_heartbeat(self):
        self.conn.mav.heartbeat_send(mavlink2.MAV_TYPE_QUADROTOR, self.autopilot, 0, 0,
                                     mavlink2.MAV_STATE_STANDBY, force_mavlink1=(self.mode == "v1"))

    def run(self, duration: float | None = None):
        start = last_hb = time.time() - 1
        while not self._stop.is_set():
            now = time.time()
            if duration and now - start > duration:
                break
            if now - last_hb >= 0.2:
                self._send_heartbeat()
                last_hb = now
            try:
                msg = self.conn.recv_match(blocking=True, timeout=0.05)
            except Exception:
                msg = None  # e.g. rejected unsigned message in signed mode
            if msg is None:
                continue
            if msg.get_type() == "PARAM_REQUEST_READ":
                self.answered += 1
                self.conn.mav.param_value_send(self.param.encode(), float(self.sysid),
                                               mavlink2.MAV_PARAM_TYPE_INT32, 1, 0,
                                               force_mavlink1=(self.mode == "v1"))
            elif (msg.get_type() == "COMMAND_LONG" and msg.command == mavlink2.MAV_CMD_REQUEST_MESSAGE
                  and int(msg.param1) == mavlink2.MAVLINK_MSG_ID_AUTOPILOT_VERSION and self.mode != "v1"):
                self._send_autopilot_version()

    def _send_autopilot_version(self):
        caps = (mavlink2.MAV_PROTOCOL_CAPABILITY_MAVLINK2 | mavlink2.MAV_PROTOCOL_CAPABILITY_FTP
                | mavlink2.MAV_PROTOCOL_CAPABILITY_MISSION_INT)
        major, minor, patch = self.version
        sw = (major << 24) | (minor << 16) | (patch << 8) | 255  # 255 = FIRMWARE_VERSION_TYPE_OFFICIAL
        self.conn.mav.autopilot_version_send(caps, sw, 0, 0, 0, b"\x00" * 8, b"\x00" * 8, b"\x00" * 8,
                                             0, 0, 0, b"\x00" * 18)

    def start_background(self):
        t = threading.Thread(target=self.run, daemon=True)
        t.start()
        return t

    def stop(self):
        self._stop.set()


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--port", type=int, default=14550)
    p.add_argument("--mode", choices=["unsigned", "signed", "v1"], default="unsigned")
    p.add_argument("--autopilot", choices=["ardupilot", "px4"], default="ardupilot")
    p.add_argument("--duration", type=float, default=None)
    a = p.parse_args()
    print(f"Fake {a.autopilot} vehicle ({a.mode}) sending to udp 127.0.0.1:{a.port}. Ctrl+C to stop.")
    try:
        FakeVehicle(a.port, a.mode, a.autopilot).run(a.duration)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
