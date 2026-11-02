"""Bounded exploration of the signing semantics under an abstract adversary.

Adversary A sits on one link `a_link` and can: inject any unsigned frame; replay any frame it
has observed on that link; sign with a key only if it has learned it (keys travel in clear
inside SETUP_SIGNING, so observing provisioning on its link leaks the key). A cannot forge.

Scenarios fix where A is and when it arrives relative to legitimate provisioning by the
ground station G on link `p_link`. For every policy and scenario, breadth-first search over A's
action sequences (bounded depth) looks for the shortest witness violating each property.

Properties (checked after legitimate provisioning unless stated):
  P1 command-integrity   : no A-originated CMD is accepted on a link outside policy.trusted
  P2 key-integrity       : A cannot change V's key
  P3 replay-resistance   : a replayed, previously accepted CMD is not accepted again
  P4 first-use-window    : (pre-provisioning) A can install its own key           [reported]
  P5 trusted-link        : A on a trusted link gets CMD accepted                  [by design]
  P6 key-exposure        : A observing the provisioning link later gets CMD accepted
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass, replace
from typing import Dict, List, Optional, Tuple

from .semantics import CMD, HB, RADIO, READ, SETUP, Frame, Policy, State, step

G_SRC, A_SRC = (255, 190), (254, 190)
V_SRC = (1, 1)
K_LEGIT, K_ADV = "K", "K_adv"


@dataclass(frozen=True)
class World:
    st: State
    a_key: Optional[str]                      # key learned by A, if any
    observed: Tuple[Frame, ...]               # frames A has seen on its link
    trace: Tuple[str, ...]


def legit_provision(policy: Policy, w: World, p_link: str, a_link: str, clock: int) -> World:
    """G installs K over p_link: unsigned when V is unkeyed (TOFU), signed otherwise."""
    signed = w.st.key is not None
    fr = Frame(p_link, G_SRC, SETUP, signed=signed, key=w.st.key if signed else None,
               ts=clock, link_id=1, payload=K_LEGIT)
    d = step(policy, replace(w.st, clock=clock), fr)
    observed = w.observed + ((fr,) if p_link == a_link else ())
    a_key = w.a_key
    if p_link == a_link and d.accepted:
        a_key = K_LEGIT  # SETUP_SIGNING carries the key in clear
    return World(d.state, a_key, observed, w.trace + (f"G:SETUP({'signed' if signed else 'unsigned'})@{p_link} -> {d.reason}",))


def legit_command(policy: Policy, w: World, link: str, a_link: str, clock: int) -> Tuple[World, Frame, bool]:
    fr = Frame(link, G_SRC, CMD, signed=w.st.key is not None, key=w.st.key, ts=clock, link_id=1)
    d = step(policy, replace(w.st, clock=clock), fr)
    observed = w.observed + ((fr,) if link == a_link else ())
    return World(d.state, w.a_key, observed, w.trace + (f"G:CMD@{link} -> {d.reason}",)), fr, d.accepted


def adversary_moves(w: World, a_link: str, clock: int) -> List[Tuple[str, Frame]]:
    moves = []
    for kind in (CMD, READ, HB, RADIO):
        moves.append((f"A:inject {kind} unsigned@{a_link}", Frame(a_link, A_SRC, kind, ts=clock, link_id=7)))
    moves.append((f"A:inject SETUP(K_adv) unsigned@{a_link}", Frame(a_link, A_SRC, SETUP, ts=clock, link_id=7, payload=K_ADV)))
    if w.a_key:
        moves.append((f"A:inject CMD signed({w.a_key})@{a_link}",
                      Frame(a_link, A_SRC, CMD, signed=True, key=w.a_key, ts=clock, link_id=7)))
        moves.append((f"A:inject SETUP(K_adv) signed({w.a_key})@{a_link}",
                      Frame(a_link, A_SRC, SETUP, signed=True, key=w.a_key, ts=clock, link_id=7, payload=K_ADV)))
    for i, fr in enumerate(w.observed):
        moves.append((f"A:replay obs[{i}]({fr.kind},{'signed' if fr.signed else 'unsigned'})@{a_link}",
                      replace(fr, link=a_link)))
    return moves


def _violations(policy: Policy, w: World, move: str, fr: Frame, d, key_before) -> List[str]:
    out = []
    if d.accepted and fr.kind == CMD and fr.src == A_SRC and fr.link not in policy.trusted:
        out.append("P1")
    if d.state.key != key_before and d.state.key == K_ADV:
        out.append("P2")
    if d.accepted and fr.kind == CMD and fr.src == G_SRC and "replay" in move:
        out.append("P3")
    if d.accepted and fr.kind == CMD and fr.src == A_SRC and fr.link in policy.trusted:
        out.append("P5")
    return out


def explore(policy: Policy, scenario: str, a_link: str, p_link: str, depth: int = 3) -> Dict[str, Optional[List[str]]]:
    """Return, per property, the shortest violating trace (None = no violation within depth)."""
    clock = 1_000_000
    w = World(State(clock=clock), None, (), ())
    found: Dict[str, Optional[List[str]]] = {p: None for p in ("P1", "P2", "P3", "P4", "P5", "P6")}

    if scenario == "pre-provisioning":
        # A acts before G ever provisions.
        for move, fr in adversary_moves(w, a_link, clock):
            d = step(policy, w.st, fr)
            if d.state.key == K_ADV and found["P4"] is None:
                found["P4"] = list(w.trace) + [f"{move} -> {d.reason}"]
        return found

    # Legitimate setup: provision, then one signed command the adversary may observe.
    w = legit_provision(policy, w, p_link, a_link, clock)
    clock += 10
    w, _, _ = legit_command(policy, w, p_link, a_link, clock)
    clock += 10
    if w.a_key and scenario == "on-provisioning-link":
        pass  # P6 is checked via P1 witnesses that use the learned key

    # BFS over adversary action sequences.
    queue = deque([w])
    seen = {(w.st, w.a_key, len(w.observed))}
    while queue:
        cur = queue.popleft()
        if len(cur.trace) - 2 >= depth:
            continue
        for move, fr in adversary_moves(cur, a_link, clock + 10 * len(cur.trace)):
            d = step(policy, replace(cur.st, clock=clock + 10 * len(cur.trace)), fr)
            trace = list(cur.trace) + [f"{move} -> {d.reason}"]
            for p in _violations(policy, cur, move, fr, d, cur.st.key):
                if found[p] is None:
                    found[p] = trace
                if p == "P1" and "signed(K)" in move and found["P6"] is None:
                    found["P6"] = trace
            nxt = World(d.state, cur.a_key, cur.observed, tuple(trace))
            sig = (nxt.st, nxt.a_key, len(nxt.observed))
            if sig not in seen:
                seen.add(sig)
                queue.append(nxt)
    return found


SCENARIOS = [
    ("pre-provisioning", "ch1", "ch1"),
    ("post-provisioning, A on untrusted link", "ch1", "ch0"),
    ("post-provisioning, A on trusted/console link", "ch0", "ch1"),
    ("on-provisioning-link", "ch1", "ch1"),
]


def run_all(policies, depth: int = 3):
    rows = []
    for pol in policies:
        for name, a_link, p_link in SCENARIOS:
            res = explore(pol, name.split(",")[0], a_link, p_link, depth)
            rows.append({"policy": pol.name, "scenario": name, "a_link": a_link, "p_link": p_link,
                         **{k: (v is not None) for k, v in res.items()},
                         "witnesses": {k: v for k, v in res.items() if v}})
    return rows
