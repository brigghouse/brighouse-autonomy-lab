"""Design-space analysis: for each real policy, which single parameter change removes
which witnessed property? This turns the model into actionable guidance ("close the
first-use window AND drop the trusted link to fix P1,P2,P4,P6").

A property is "present" for a policy if witnessed in ANY scenario at the search depth.
We flip one Boolean/parameter at a time and recompute the present set.
"""

from __future__ import annotations

from dataclasses import replace
from itertools import product
from typing import Dict, List, Set

from .configs import ARDUPILOT_472, PX4_117, PX4_118, SPEC_STRICT
from .explore import SCENARIOS, World, explore, functional, legit_provision
from .semantics import State
from .semantics import HB, RADIO, Policy

PROPS = ("P1", "P2", "P3", "P4", "P5", "P6")

#: single-parameter edits we consider (name -> function producing the edited policy)
EDITS = {
    "close-tofu+oob": lambda p: replace(p, tofu=False, open_when_unkeyed=False, oob_provision=True),
    "drop-trusted-links": lambda p: replace(p, trusted=frozenset()),
    "no-unsigned-rekey": lambda p: replace(p, unsigned_rekey_on_trusted=False),
    "refuse-setup-armed": lambda p: replace(p, refuse_setup_armed=True),
    "strict-allowlist": lambda p: replace(p, allow_unsigned=frozenset({RADIO})),
    "enable-replay-check": lambda p: replace(p, replay_check=True),
}


def is_functional(policy: Policy, depth: int = 3) -> bool:
    """Can a legitimately provisioned vehicle still accept a legitimate signed command?"""
    clock = 1_000_000
    w = World(State(clock=clock), None, (), ())
    w = legit_provision(policy, w, "ch1", "ch0", clock)
    # a legit signed command on an ordinary (untrusted) link must be accepted
    return functional(policy, w, "ch1", clock + 20)


def present(policy: Policy, depth: int = 3) -> Set[str]:
    out: Set[str] = set()
    for name, a_link, p_link in SCENARIOS:
        res = explore(policy, name.split(",")[0], a_link, p_link, depth)
        out |= {k for k, v in res.items() if v is not None}
    return out


def failures(present_set: Set[str]) -> Set[str]:
    return present_set & {"P1", "P2", "P3"}


def analyse(depth: int = 3) -> Dict:
    base_policies = [SPEC_STRICT, PX4_118, PX4_117, ARDUPILOT_472]
    out = {}
    for pol in base_policies:
        base = present(pol, depth)
        edits = {}
        for ename, fn in EDITS.items():
            try:
                edited = present(fn(pol), depth)
            except Exception:  # noqa: BLE001
                continue
            removed = sorted(base - edited)
            added = sorted(edited - base)
            if removed or added:
                edits[ename] = {"removes": removed, "adds": added,
                                "still_functional": is_functional(fn(pol), depth)}
        # greedy minimal combination to clear all FAILURES (P1-P3)
        combo, cleared = [], failures(base)
        cur = pol
        remaining = set(EDITS)
        while failures(present(cur, depth)) and remaining:
            best = None
            for ename in list(remaining):
                cand = EDITS[ename](cur)
                f = failures(present(cand, depth))
                if best is None or len(f) < best[1]:
                    best = (ename, len(f), cand)
            combo.append(best[0])
            cur = best[2]
            remaining.discard(best[0])
            if best[1] == 0:
                break
        out[pol.name] = {
            "present": sorted(base),
            "failures": sorted(failures(base)),
            "functional": is_functional(pol, depth),
            "single_edits": edits,
            "min_edits_to_clear_failures": combo,
            "residual_failures_after_combo": sorted(failures(present(cur, depth))),
            "functional_after_combo": is_functional(cur, depth),
        }
    return out


if __name__ == "__main__":
    import json
    print(json.dumps(analyse(), indent=2))
