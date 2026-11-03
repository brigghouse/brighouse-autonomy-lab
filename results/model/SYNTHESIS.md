# Design-space synthesis: greedy-minimal liveness-preserving remediations

Generated from `mavaudit.model.synthesis` (`python -c 'from mavaudit.model.synthesis import analyse; ...'`).
For each measured/reference policy: the witnessed properties, whether it is functional
(liveness), and the **greedy-minimal** set of single-parameter edits that clears all safety
failures (P1-P3) while keeping the vehicle functional. Greedy is not guaranteed globally
minimal. Edits that are a no-op for a policy are never counted, and an edit is only added
when it strictly reduces the failure count. Where several edits are equally good at a step,
all are listed as *alternatives*. Iteration order is fixed, so the output is deterministic.

| Policy | Safety failures | Functional | Greedy-minimal fix | Alternatives (per step) | Residual | Functional after |
|---|---|---|---|---|---|---|
| `spec-strict` | P1, P2 | yes | close-tofu+oob | close-tofu+oob | none | yes |
| `px4-1.18` | P1, P2 | yes | close-tofu+oob | close-tofu+oob | none | yes |
| `px4-1.17` | P3 | yes | *none: no single edit reduces failures (adopt the full mechanism)* | — | P3 | yes |
| `ardupilot-4.7.2` | P1, P2 | yes | close-tofu+oob, drop-trusted-links | close-tofu+oob ; drop-trusted-links / no-unsigned-rekey | none | yes |

## Single-parameter edits (liveness-preserving only shown)

**`spec-strict`**
- `close-tofu+oob` removes P1, P2, P4, P6

**`px4-1.18`**
- `close-tofu+oob` removes P1, P2, P4, P6

**`px4-1.17`**
- `close-tofu+oob` introduces P2
- `drop-trusted-links` removes P5; introduces P1

**`ardupilot-4.7.2`**
- `close-tofu+oob` removes P1, P4, P6
- `drop-trusted-links` removes P5

