# Which directory is which run

Every directory under `results/` is the output of one named campaign, and the name says
which. The convention is `<stack>-<version>` for a release campaign (`ardupilot-4.7.2`,
`px4-1.17.0`, `px4-1.18.0-rc1`) and a campaign name for everything else (`ch0-configs`,
`dds`, `surface`, `allowlists`, `conformance`, `model`, `scores`, `longitudinal`).

**A directory named after a stack without its version is not a campaign.** On 4 Nov 2026 a
`results/ardupilot/` appeared here and was committed: it was the accidental output of a
2-second simulator start used to bring SITL up for another probe, 38 frames, no README, and
sitting beside the real `results/ardupilot-4.7.2/` campaign where anyone browsing the
repository would have read it as evidence. It has been removed. Recording it here rather
than deleting it quietly, because the whole point of this directory is that a reader can
tell what was measured and when.

Each campaign directory carries its own `README.md` stating what was measured, how often it
was repeated, and what the campaign does not establish. Where a README is missing the raw
JSON still carries `started_utc` and `source_rev`; treat the JSON as the record and the
README as the reading of it.
