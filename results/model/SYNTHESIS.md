# Design-space synthesis: minimal liveness-preserving remediations

Generated from `mavaudit.model.synthesis`. For each measured/reference policy: the
witnessed properties, whether it is functional (liveness), and the minimal set of
single-parameter edits that clears all safety failures (P1-P3) while keeping the
vehicle functional.

| Policy | Safety failures | Functional | Minimal fix | Residual | Functional after |
|---|---|---|---|---|---|
| `spec-strict` | P1, P2 | yes | close-tofu+oob | none | yes |
| `px4-1.18` | P1, P2 | yes | close-tofu+oob | none | yes |
| `px4-1.17` | P3 | yes | refuse-setup-armed, enable-replay-check, strict-allowlist, no-unsigned-rekey, close-tofu+oob, drop-trusted-links | none | yes |
| `ardupilot-4.7.2` | P1, P2 | yes | close-tofu+oob, drop-trusted-links | none | yes |

## Single-parameter edits (liveness-preserving only shown)

**`spec-strict`**
- `close-tofu+oob` removes P1, P2, P4, P6

**`px4-1.18`**
- `close-tofu+oob` removes P1, P2, P4, P6

**`px4-1.17`**
- `drop-trusted-links` removes P5; introduces P1

**`ardupilot-4.7.2`**
- `close-tofu+oob` removes P1, P4, P6
- `drop-trusted-links` removes P5

