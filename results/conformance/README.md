# Model-based conformance results

Each policy's predicted accept/reject decision (from `mavaudit.model`) is compared
with the live SITL build's observed behaviour over 8 read-only probe cases
(unkeyed/keyed x trusted/untrusted link x signed/unsigned read).

| Stack | Policy | Cases | Agreement |
|---|---|---|---|
| ardupilot-4.7.2 | `ardupilot-4.7.2` | 8/8 | 1.00 |
| px4-1.18 | `px4-1.18` | 8/8 | 1.00 |
| px4-1.17 | `px4-1.17` | 8/8 | 1.00 |

All documentation-derived policies are confirmed as **measured** policies.
The ArduPilot run validates R4: keyed+trusted(ch0)+unsigned is accepted (predicted and observed), while keyed+untrusted+unsigned is rejected.
