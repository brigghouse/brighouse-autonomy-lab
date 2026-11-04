# Model-based conformance results

Each policy's predicted accept/reject decision (from `mavaudit.model`) is compared
with the live SITL build's observed behaviour over 8 read-only probe cases
(unkeyed/keyed x trusted/untrusted link x signed/unsigned read).

| Stack | Policy | Cases | Agreement |
|---|---|---|---|
| ardupilot-4.7.2 | `ardupilot-4.7.2` | 8/8 | 1.00 |
| px4-1.18 | `px4-1.18` | 8/8 | 1.00 |
| px4-1.17 | `px4-1.17` | 8/8 | 1.00 |

**What 8/8 does and does not mean.** An earlier version of this line read "all
documentation-derived policies are confirmed as measured policies", which is a stronger
claim than this run can carry and is contradicted by our own Table II in Paper 1. The
conformance run exercises the eight scenarios the harness defines, and every one agreed with
the model's prediction. Those eight scenarios all concern **acceptance of a read on a link**:
whether it is keyed, whether the link is trusted, whether the frame is signed, and which wire
version it used. They do not touch re-keying, armed-state behaviour, or replay, so a policy
scoring 8/8 here has had three of its six columns in Table II exercised, not six. On
ArduPilot in particular there is no re-key measurement of any kind
(`results/ardupilot-4.7.2/summary.json` records `tofu_unsigned_rekey` as `null`), so its TOFU
and re-key values remain documentation-derived however this table reads.

What the ArduPilot run does validate, and it is the finding the paper rests on, is R4:
keyed + trusted(ch0) + unsigned is accepted, keyed + untrusted + unsigned is rejected, both
predicted and observed. Since the channel-0 campaign was re-run with a positive control, the
rejection half of that is an observed refusal rather than a timeout -- see
`../ch0-configs/README.md`.
