# Security policy

## Reporting a vulnerability in mavaudit

Please report it privately through GitHub's **"Report a vulnerability"** button (Security tab → Advisories). Do not open a public issue. We aim to acknowledge reports within 5 working days.

## Vulnerabilities in third-party flight stacks or GCS

If you use this lab to find an issue in PX4, ArduPilot, QGroundControl, Mission Planner, MAVProxy or a vendor product, report it **to that project or vendor first**, through its published security policy, and follow coordinated disclosure. This repository does not publish undisclosed vulnerabilities, exploit code or attack procedures.

## Scope of this project

mavaudit is a **defensive configuration auditor**:

- It is passive by default. With `--active-probe` it sends two unsigned, read-only requests: one parameter read and one `AUTOPILOT_VERSION` request.
- It refuses non-loopback, non-private targets unless `--authorized --scope-ref <id>` is given. For listening targets (`udpin:`) it also checks the address the traffic came from before probing.
- It contains no RF code. On a serial port attached to a telemetry radio, however, the active probe would be transmitted, so `--active-probe` on serial targets requires `--authorized --scope-ref <id>`. All published lab work runs in software-in-the-loop simulation.

Only test systems you own, or systems you hold written authorisation to test.
