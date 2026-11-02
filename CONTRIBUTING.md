# Contributing

Thanks for helping improve the lab. Contributions in any of these areas are welcome:

- **New checks** for mavaudit. Each check needs a finding ID (`MAV-0xx`), a severity, a CRA Annex I mapping and a test against the reference vehicle (`mavaudit/sim/fake_vehicle.py`).
- **Reproduced measurements** on other PX4 or ArduPilot versions, sent as `results/<experiment>/` with the exact commit hash and command.
- **Corrections** to the literature review or the regulatory crosswalk. Please cite a primary source.

## Rules

1. **Defensive only.** Do not contribute exploit code, attack automation, RF transmission or jamming tooling.
2. Every active check must be read-only and must respect the scope guard (`mavaudit/safety.py`).
3. Run `python -m pytest -q` before opening a PR.
4. Mark CRA mappings as technical interpretation, not legal advice.

## Development

```bash
python -m pip install -e ".[dev]"
python -m pytest -q
```
