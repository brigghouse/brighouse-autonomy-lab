"""Acceptance semantics of MAVLink 2 signing as a parameterised transition system.

Notation (mirrors the paper):
  V        the vehicle (receiver under study)
  K        V's current signing key, or None
  L        set of link identifiers; policy.trusted ⊆ L never require signatures
  S[s]     last accepted timestamp per stream s = (sysid, compid, link_id)
  frame    (link, src, msg, signed, key, ts, link_id)   -- key is the key used to sign
  Message kinds: CMD (state-changing), READ (read-only request), HB, RADIO, SETUP(key')

Decisions are functions of the policy, the state and the frame. Signature verification is
abstract: a frame "verifies" iff it was signed with V's key (no forgery; collisions ignored).
"""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from typing import FrozenSet, Optional, Tuple

WINDOW = 6_000_000  # 1 minute in 10 µs units (spec: reject if > 1 min behind local time)

CMD, READ, HB, RADIO, SETUP = "CMD", "READ", "HB", "RADIO", "SETUP"


@dataclass(frozen=True)
class Policy:
    name: str
    #: links on which unsigned frames are always accepted (e.g. ArduPilot MAVLINK_COMM_0 / USB)
    trusted: FrozenSet[str] = frozenset()
    #: message kinds accepted unsigned on any link while keyed (spec suggests RADIO_STATUS)
    allow_unsigned: FrozenSet[str] = frozenset({RADIO})
    #: when no key is provisioned, accept everything unsigned (both stacks do)
    open_when_unkeyed: bool = True
    #: SETUP_SIGNING accepted UNSIGNED when no key exists (trust-on-first-use)
    tofu: bool = True
    #: links on which SETUP_SIGNING is accepted at all (None = any link)
    setup_links: Optional[FrozenSet[str]] = None
    #: while keyed, an unsigned SETUP_SIGNING on a trusted link replaces the key (USB recovery)
    unsigned_rekey_on_trusted: bool = True
    #: while keyed, a correctly signed SETUP_SIGNING replaces the key (legitimate rotation)
    signed_rekey: bool = True
    #: SETUP_SIGNING refused while armed
    refuse_setup_armed: bool = False
    #: enforce strictly increasing timestamps per stream and the 1-minute window
    replay_check: bool = True
    #: does the vehicle sign its own outbound frames on link l? (telemetry may stay unsigned)
    sign_outgoing_on_trusted: bool = True
    #: key is installed out of band (factory), not over MAVLink: V starts keyed, no TOFU window
    oob_provision: bool = False


@dataclass(frozen=True)
class Frame:
    link: str
    src: Tuple[int, int]          # (sysid, compid) claimed by the sender
    kind: str                     # CMD | READ | HB | RADIO | SETUP
    signed: bool = False
    key: Optional[str] = None     # key used to sign (abstract label)
    ts: int = 0                   # signing timestamp
    link_id: int = 0
    payload: Optional[str] = None # for SETUP: the new key label


@dataclass(frozen=True)
class State:
    key: Optional[str] = None
    armed: bool = False
    #: last accepted timestamp per stream (sysid, compid, link_id)
    streams: Tuple[Tuple[Tuple[int, int, int], int], ...] = ()
    #: local signing clock
    clock: int = 0

    def last_ts(self, stream):
        for s, t in self.streams:
            if s == stream:
                return t
        return None

    def with_ts(self, stream, ts):
        items = [(s, t) for s, t in self.streams if s != stream] + [(stream, ts)]
        return replace(self, streams=tuple(sorted(items)))


@dataclass(frozen=True)
class Decision:
    accepted: bool
    reason: str
    state: State


def _fresh(policy: Policy, st: State, fr: Frame) -> Tuple[bool, str]:
    if not policy.replay_check:
        return True, "no replay check"
    stream = (fr.src[0], fr.src[1], fr.link_id)
    last = st.last_ts(stream)
    if last is not None:
        if fr.ts <= last:
            return False, "timestamp not increasing (replay/old)"
        return True, "fresh"
    # new stream: accept if at most one minute behind local clock
    if fr.ts + WINDOW < st.clock:
        return False, "new stream too old"
    return True, "fresh (new stream)"


def step(policy: Policy, st: State, fr: Frame) -> Decision:
    """One frame arrives at V. Returns the acceptance decision and the successor state."""
    # ---- SETUP_SIGNING: key management decisions -------------------------------------
    if fr.kind == SETUP:
        if policy.setup_links is not None and fr.link not in policy.setup_links:
            return Decision(False, "SETUP not accepted on this link", st)
        if policy.refuse_setup_armed and st.armed:
            return Decision(False, "SETUP refused while armed", st)
        if st.key is None:
            if policy.tofu:
                return Decision(True, "TOFU: first key accepted unsigned", replace(st, key=fr.payload))
            if fr.signed:
                return Decision(False, "cannot verify without key", st)
            return Decision(False, "no TOFU", st)
        # keyed
        if fr.signed and fr.key == st.key:
            ok, why = _fresh(policy, st, fr)
            if not ok:
                return Decision(False, why, st)
            if policy.signed_rekey:
                st2 = st.with_ts((fr.src[0], fr.src[1], fr.link_id), fr.ts)
                return Decision(True, "signed re-key", replace(st2, key=fr.payload))
            return Decision(False, "signed re-key disabled", st)
        if not fr.signed and fr.link in policy.trusted and policy.unsigned_rekey_on_trusted:
            return Decision(True, "unsigned re-key on trusted link", replace(st, key=fr.payload))
        return Decision(False, "unsigned/invalid SETUP while keyed", st)

    # ---- ordinary frames -----------------------------------------------------------
    if st.key is None:
        if policy.open_when_unkeyed:
            return Decision(True, "unkeyed: everything accepted", st)
        return Decision(False, "unkeyed: closed", st)
    if fr.link in policy.trusted:
        return Decision(True, "trusted link: unsigned accepted", st)
    if fr.signed:
        if fr.key != st.key:
            return Decision(False, "bad signature", st)
        ok, why = _fresh(policy, st, fr)
        if not ok:
            return Decision(False, why, st)
        return Decision(True, "valid signature", st.with_ts((fr.src[0], fr.src[1], fr.link_id), fr.ts))
    if fr.kind in policy.allow_unsigned:
        return Decision(True, "allow-listed kind accepted unsigned", st)
    return Decision(False, "unsigned frame rejected", st)
