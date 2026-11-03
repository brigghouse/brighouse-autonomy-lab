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

from .configs import ARDUPILOT_472, ARDUPILOT_472_DOC, PX4_117, PX4_118, SPEC_STRICT
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
    "no-v1-bypass": lambda p: replace(p, v1_bypasses_signing=False),
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
    base_policies = [SPEC_STRICT, PX4_118, PX4_117, ARDUPILOT_472, ARDUPILOT_472_DOC]
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
        # Greedy combination to clear all FAILURES (P1-P3). Two guards keep the
        # published set honest: (i) an edit that leaves the policy unchanged for this
        # stack (a no-op, e.g. enabling a check that is already on) is never counted;
        # (ii) an edit is appended only if it strictly reduces the failure count, so
        # the set carries no dead edits. Greedy is not guaranteed globally minimal;
        # the papers say "greedy-minimal", not "minimal".
        # (iii) iteration follows the declared EDITS order, never a hash-ordered set, so
        # the result is deterministic across runs; ties (several edits equally good at a
        # step) are recorded as alternatives instead of being silently broken.
        combo, alternatives = [], []
        cur = pol
        remaining = set(EDITS)
        cur_f = len(failures(present(cur, depth)))
        while cur_f and remaining:
            cands = []
            for ename in [e for e in EDITS if e in remaining]:
                cand = EDITS[ename](cur)
                if cand == cur:  # no-op for this policy
                    remaining.discard(ename)
                    continue
                cands.append((len(failures(present(cand, depth))), ename, cand))
            if not cands:
                break
            best_f = min(c[0] for c in cands)
            if best_f >= cur_f:  # no edit makes progress
                break
            tied = [c for c in cands if c[0] == best_f]
            chosen = tied[0]
            combo.append(chosen[1])
            alternatives.append([c[1] for c in tied])
            cur, cur_f = chosen[2], best_f
            remaining.discard(chosen[1])
        out[pol.name] = {
            "present": sorted(base),
            "failures": sorted(failures(base)),
            "functional": is_functional(pol, depth),
            "single_edits": edits,
            "min_edits_to_clear_failures": combo,
            "min_edits_alternatives": alternatives,  # per step: all equally-good edits
            "residual_failures_after_combo": sorted(failures(present(cur, depth))),
            "functional_after_combo": is_functional(cur, depth),
        }
    return out


if __name__ == "__main__":
    import json
    print(json.dumps(analyse(), indent=2))
