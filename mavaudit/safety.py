"""Target scope guard.

By default mavaudit only talks to loopback or private (RFC 1918 / link-local)
addresses, which covers SITL simulators and isolated bench networks. Anything
else requires an explicit authorisation flag plus a scope reference that is
written into the report, so every run is traceable to a signed engagement.
"""

from __future__ import annotations

import ipaddress
import re
from dataclasses import dataclass

_HOST_RE = re.compile(r"^(?:udpin|udpout|udp|tcp|tcpin):(?P<host>[^:]+):(?P<port>\d+)$")


class ScopeError(ValueError):
    """Raised when a target is outside the allowed scope."""


@dataclass(frozen=True)
class Target:
    connection: str
    host: str | None
    port: int | None
    kind: str  # "network" or "serial"


def parse_target(connection: str) -> Target:
    m = _HOST_RE.match(connection)
    if m:
        return Target(connection, m.group("host"), int(m.group("port")), "network")
    if connection.startswith("/dev/") or connection.upper().startswith("COM"):
        return Target(connection, None, None, "serial")
    raise ScopeError(f"Unrecognised connection string: {connection!r}")


def is_lab_address(host: str) -> bool:
    if host in ("localhost", "0.0.0.0"):
        return True
    try:
        ip = ipaddress.ip_address(host)
    except ValueError:
        return False  # hostnames other than localhost are not auto-trusted
    return ip.is_loopback or ip.is_private or ip.is_link_local


def check_scope(connection: str, authorized: bool = False, scope_ref: str | None = None,
                active: bool = False) -> Target:
    """Validate the target.

    Serial links are allowed for passive listening (wired bench). An active probe over a
    serial port may go out over a telemetry radio, so it needs explicit authorisation.
    For listening targets (udpin/tcpin/udp) the host is mavaudit's own bind address; the
    sending peer is checked separately by `check_peer` before any active probe.
    """
    target = parse_target(connection)
    if target.kind == "serial":
        if active and (not authorized or not scope_ref):
            raise ScopeError(
                "--active-probe on a serial port may be transmitted over a radio link. Re-run with "
                "--authorized --scope-ref <engagement-id> only if every vehicle that could receive "
                "it is covered by written authorisation."
            )
        return target
    assert target.host is not None
    if is_lab_address(target.host):
        return target
    if not authorized or not scope_ref:
        raise ScopeError(
            f"{target.host} is not a loopback/private lab address. Re-run with "
            "--authorized --scope-ref <engagement-id> only if you hold written "
            "authorisation from the system owner."
        )
    return target


def check_peer(peer_host: str | None, authorized: bool = False, scope_ref: str | None = None) -> bool:
    """Return True if an active probe may be sent to `peer_host` (the address traffic came from)."""
    if peer_host is None:
        return True  # outbound client connection: the target itself was already checked
    if is_lab_address(peer_host) and peer_host != "0.0.0.0":
        return True
    return bool(authorized and scope_ref)
