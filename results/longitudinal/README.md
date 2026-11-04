# longitudinal

Attempted build-and-measure across seven releases on 2026-11-02. The per-release
directories hold what each attempt produced; [TABLE.md](TABLE.md) is the table.

**Four of the seven did not build.** `Copter-4.1.6`, `4.2.4`, `4.3.8` and `4.4.4`
failed to build in this toolchain, so nothing was measured for them; the table
records `build failed`, not a behaviour. `px4 v1.16.2` built but was not measured.

That leaves **two releases with measured behaviour**: `Copter-4.5.7` and
`Copter-4.6.3`. Both: signing off by default, signing works once provisioned, and
the console channel stays exempt after provisioning.

This is the reason the longitudinal paper says the *version-control* evidence spans
2016–2026 while the *measured* evidence spans two releases. A failed build is a
failure of this toolchain, not a property of the firmware, and nothing in this
directory should be read as one.

Not established here: why each build failed, whether the releases that failed would
behave like their neighbours, or anything about PX4 across versions.
