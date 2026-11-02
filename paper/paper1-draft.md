---
title: "MAVLink Security in 2026: Message Signing in PX4 and ArduPilot and What the EU Cyber Resilience Act Means for Drone Manufacturers"
author: "Ian Brighouse, Brighouse Security Labs"
date: 2026-11-02
status: DRAFT v0.2. Results from SITL runs on 2026-11-02 (see results/). GCS interoperability (E5) is still pending.
---

# MAVLink Security in 2026: Message Signing in PX4 and ArduPilot and What the EU Cyber Resilience Act Means for Drone Manufacturers

**Ian Brighouse**, Brighouse Security Labs

> **Draft notes (remove before publication)**
> - `[cite:key]` refers to the BibTeX entries in `research/literature-review.md` §8.
> - `[VERIFY]` marks a claim that must be checked against the primary source. Legal text must be checked against the Official Journal PDF.
> - All numbers in §7 come from `results/*/summary.json`, produced by `scripts/run_*.py`. Do not edit them by hand.

## Abstract

MAVLink is the de facto command-and-control (C2) and telemetry protocol of the open-source drone ecosystem, used by PX4, ArduPilot and the ground control stations (GCS) built around them. Since 2016, MAVLink 2 has offered optional message signing, which authenticates frames and resists replay, but adoption has been left to integrators. In 2026 two developments made this gap pressing. First, a CISA advisory rated unauthenticated MAVLink in PX4 at CVSS 9.8 (CVE-2026-1579), and a cluster of 2026 CVEs showed that memory-safety bugs in MAVLink FTP, shell and log handlers are reachable by *any* peer when signing is off. Second, the EU Cyber Resilience Act (CRA) began applying its vulnerability-reporting duty on 11 September 2026, ahead of full application on 11 December 2027. We review the state of MAVLink signing in PX4, ArduPilot, QGroundControl, Mission Planner and MAVProxy as of November 2026. We map MAVLink security properties to CRA Annex I and to the C2-link requirement of Delegated Regulation (EU) 2019/945, and we release *mavaudit*, a passive, key-less auditor that measures signing posture and produces CRA-mapped evidence. Simulator measurements on ArduPilot Copter 4.7.2, PX4 v1.17.0 and PX4 v1.18.0-rc1 show three things. First, all six default links tested send no signed frames, answer unauthenticated parameter reads and advertise MAVLink FTP to unauthenticated peers. Second, the current PX4 stable release (v1.17.0) contains no signing implementation at all. Third, ArduPilot keeps accepting unsigned input on MAVLink channel 0 even while it signs everything it sends, so passive observation alone overstates protection. We conclude with a minimum security baseline for EU drone manufacturers building on open-source flight stacks.

## 1. Introduction

Open-source flight stacks underpin a large share of commercial and dual-use unmanned systems. Their common language, MAVLink, was designed for constrained radio links, and its original version carried no authentication `[cite:marty2014]`. Unauthenticated C2 has been shown, repeatedly and in public, to enable mission disruption and takeover `[cite:kwon2018]` `[cite:marty2014]`, and it is catalogued in NVD as protocol-level weaknesses CVE-2020-10281 to -10283.

MAVLink 2 introduced a signing mechanism that addresses the integrity and authentication part of the problem. Ten years later, three questions remain open in the literature (§7 of our review):

1. **Default posture.** How are current releases configured out of the box, and what does a manufacturer get if it changes nothing?
2. **Practical adoption.** What does enabling signing involve in each stack and GCS, and where are the exemptions?
3. **Regulatory meaning.** How does signing, or its absence, relate to the obligations EU manufacturers now face under the CRA and the UAS product rules?

**Contributions.**
- **C1.** An up-to-date (November 2026) review of MAVLink signing in PX4 (including the spec-aligned implementation in v1.18, at release-candidate stage when measured), ArduPilot and the main GCS (§3).
- **C2.** A synthesis of the 2020–2026 CVE landscape that links signing to the *reachability* of memory-safety bugs (§4).
- **C3.** A regulatory crosswalk from MAVLink security properties to CRA Annex I, Delegated Regulation 2019/945 and RED/EN 18031 (§5). To our knowledge no such crosswalk has been published.
- **C4.** *mavaudit*, an open, passive auditor with CRA-mapped output, and simulator measurements of default and hardened configurations (§6–7).

## 2. Background: MAVLink and message signing

**Framing.** MAVLink 1 frames start with `0xFE` and have a 6-byte header. MAVLink 2 frames start with `0xFD` and have a 10-byte header, 24-bit message IDs and incompatibility and compatibility flags. The only defined incompatibility flag, `0x01`, marks a signed frame. Both versions use a CRC with a per-message seed (`CRC_EXTRA`). The CRC detects mismatched message definitions, but it is not a security control.

**Signing.** A signed MAVLink 2 frame carries a 13-byte trailer: an 8-bit link ID, a 48-bit timestamp (in 10 µs units since 1 January 2015) and a 48-bit truncated SHA-256 over the 32-byte secret key, the header, the payload, the link ID and the timestamp. Receivers reject frames whose timestamps do not increase strictly per (system, component, link) stream, or that fall more than one minute behind local time.

**What signing does not provide.**
- **Confidentiality.** Payloads (position, missions, parameters) remain in plaintext.
- **Key distribution.** The key is pushed with `SETUP_SIGNING`, in cleartext, and the specification only advises using a secure link. There is no rotation, revocation or per-device identity.
- **Per-sender identity.** Any key holder can sign as any system or component ID.
- **A uniform policy for unsigned messages.** Acceptance of unsigned messages is implementation-defined.

These properties matter for the regulatory analysis in §5. Signing is evidence of *integrity and access control*, not of *confidentiality*.

## 3. Implementation status in 2026

| Stack | Signing support | Default | Notable exemptions and caveats |
|---|---|---|---|
| **PX4 v1.17.0** (latest stable) | **None in the release.** No signing code in the v1.17.0 MAVLink module and no `MAV_SIGN_CFG` parameter (source inspection and measurement, §7). The v1.18 notes mention "signing in v1.17", which probably refers to pre-release builds `[VERIFY with maintainers]` | n/a | Signing cannot be enabled on stable PX4 |
| **PX4 v1.18** (rc1 measured) | Spec-aligned (PR #26894); key on SD card | Off (no key → everything unsigned, everything accepted) | Unsigned allowlist: HEARTBEAT, RADIO_STATUS (+ADS-B on traffic links); **trust-on-first-use** provisioning on any link; key change refused while armed |
| **ArduPilot 4.7.2** | Via Mission Planner or MAVProxy `signing setup` | Off (measured, §7) | **MAVLink channel 0 always accepts unsigned input** ("assumed to be secure channel. This is USB on ChibiOS boards", `GCS_Signing.cpp`); RADIO_STATUS/RADIO allowed unsigned; MAVLink 1 ports unprotected |
| **QGroundControl** | Documented in master (Telemetry → MAVLink 2 Signing) | — | First stable release with signing not confirmed `[VERIFY]`; QGC issue #14250 (setup rejection not handled) |
| **Mission Planner** | Native key management and push | — | — |
| **MAVProxy** | `signing` module | — | Key sent in cleartext; docs mention SHA-512 vs spec SHA-256 `[VERIFY]` |

Sources: PX4 Message Signing and Security Hardening docs, PX4 v1.18 release notes, ArduPilot MAVLink2 Signing docs, MAVProxy signing module docs, QGC user guide and API docs (full URLs in the review).

**Observation.** In both major stacks signing is **opt-in**, and PX4 assigns link security explicitly to the *system integrator*. Under the CRA, that integrator is the manufacturer.

## 4. Threat and vulnerability landscape

We describe attack classes conceptually, following the published literature.

- **Protocol level.** NVD lists cleartext transmission (CVE-2020-10281), lack of authentication in MAVLink 1 (CVE-2020-10282) and downgrade from v2 to v1 (CVE-2020-10283). In 2026, CISA advisory ICSA-26-090-02 assigned CVE-2026-1579 (CWE-306, CVSS 9.8) to MAVLink in PX4 with signing off; the remediation is to enable signing on all non-USB links.
- **Implementation level.** From 2021 to 2026, PX4 accumulated CVEs in MAVLink-facing code: buffer overflows in message handlers, use-after-free in the MAVLink shell, path traversal in MAVLink FTP (CVE-2026-32709) and stack overflows in the log handler. ArduPilot recorded CVE-2026-38971 in `handle_serial_control()`.
- **Reachability argument.** With signing off, every one of these handlers is reachable by any peer that can inject frames: a radio in range, or a host on the same IP network for MAVLink-over-UDP. Signing does not fix memory-safety bugs, but it **restricts their reachability to key holders**. We test this as a yes/no conformance check in §7 (E-reach), without exploitation.
- **Beyond authentication.** Fuzzing work (RVFuzzer `[cite:kim2019rvfuzzer]`, PGFUZZ `[cite:kim2021pgfuzz]`, ADGFUZZ `[cite:wang2026adgfuzz]`) and stealthy-attack studies `[cite:dash2019]` show that *authenticated is not safe*: an authorised or compromised GCS can still send harmful but well-formed inputs. Signing is necessary but not sufficient.
- **GCS gap.** NVD returns no CVEs for QGroundControl or Mission Planner, and GCS-focused academic work is sparse `[cite:mansfield2013]`. We read this as a lack of scrutiny, not evidence of security.

## 5. Regulatory analysis

*This section is the author's technical interpretation, not legal advice.*

### 5.1 Is a MAVLink drone in scope of the CRA?

The CRA (Regulation (EU) 2024/2847) applies to products with digital elements that have a data connection. Article 2(3) excludes products **certified** under the EU aviation regulation 2018/1139. Open-category drones carrying a C-class marking under Delegated Regulation 2019/945 go through CE conformity assessment rather than certification, so they appear to be **in scope**, as does commercially distributed GCS software. Non-commercial open-source projects are outside scope, or are treated as open-source software stewards under Art. 24. A manufacturer that integrates PX4 or ArduPilot into a commercial product carries the **full Annex I obligations for the whole product**, including the integrated open-source code `[VERIFY against Commission guidance of 27-07-2026]`.

### 5.2 Product class

Flight control is not an Annex III category. Under Art. 7(1), embedding an RTOS or bootloader does not change the class of the host product, so a complete drone, flight controller or GCS is most plausibly a **default-class** product (self-assessment, Module A). Components sold on their own (an RTOS, a secure bootloader, a telemetry/mesh radio sold as a network interface, a security microcontroller) may be important class I. Some websites reproduce the 2022 proposal's Annex III, which listed "robot controllers"; the final text does not.

### 5.3 Timeline

The Art. 14 reporting of actively exploited vulnerabilities and severe incidents has applied **since 11 September 2026**, including to products already on the market. Full application starts on 11 December 2027. RED Delegated Regulation 2022/30 (with EN 18031) has applied to internet-capable radio equipment since 1 August 2025 and is repealed by 2026/339 with effect from 11 December 2027.

### 5.4 Crosswalk

| MAVLink observation | CRA Annex I, Part I, (2) | 2019/945 | Evidence a manufacturer can produce |
|---|---|---|---|
| No signed frames on the C2 link | (b) secure by default; (d) protection from unauthorised access; (f) integrity of commands | C2/C3: C2 link "protected against unauthorised access" `[VERIFY C3]` | mavaudit report showing 100 % signed frames; provisioning procedure |
| Vehicle answers unsigned requests | (d); (j) limit attack surface | as above | Unsigned probe not answered (MAV-005 absent) |
| MAVLink 1 enabled on radio ports | (b); (f) | as above | Port protocol configuration; no v1 frames observed |
| No link confidentiality | (e) confidentiality | — | Encrypted datalink or VPN, justified by the risk assessment |
| Shell or FTP services exposed | (j); (a) no known exploitable vulnerabilities | — | Services disabled or gated; SBOM + CVE monitoring |
| Unsigned firmware | (f) integrity of programs | — | Secure-boot configuration (PX4 ed25519 / ArduPilot signed bootloader) |
| No vulnerability-handling process | Part II (5)–(6); Art. 14 | — | CVD policy, `security.txt`, ENISA reporting runbook |

## 6. Methodology: mavaudit and the SITL testbed

**mavaudit** (released in this repository, v0.2.0) is a passive auditor that **never needs the signing key**. It classifies every frame it observes from the raw header bytes: MAVLink 1 (`0xFE`), unsigned MAVLink 2, or signed MAVLink 2 (incompatibility flag `0x01`). It identifies the autopilot from HEARTBEAT.

With `--active-probe` it sends two **unsigned, read-only** requests:
- a `PARAM_REQUEST_READ` by index 0, so it does not depend on parameter names that change between releases (ArduPilot 4.7 renamed `SYSID_THISMAV` to `MAV_SYSID`);
- a `MAV_CMD_REQUEST_MESSAGE` for `AUTOPILOT_VERSION`, which gives the firmware version and capability flags.

Findings MAV-001 to MAV-007 (`docs/findings.md`) map to the crosswalk in §5.4. A scope guard limits targets to loopback and private addresses. The tool is validated against a Python reference vehicle in unsigned, signed and MAVLink 1 modes (10 automated tests in CI).

**Testbed.** One headless Ubuntu 24.04 VM (2 vCPU, 7 GB). We built from source:
- ArduPilot Copter 4.7.2 (`fb7735678960`, the upstream `ArduCopter-stable` tag at run time);
- PX4 v1.17.0 (`d6f12ad1c4f7`, the latest stable release);
- PX4 v1.18.0-rc1 (`fca3df865af3`).

PX4 runs with its SIH physics, so no Gazebo is needed. There is no RF emission and no third-party system; `scripts/setup_sitl.sh` reproduces the build.

**Procedure** (`scripts/run_ardupilot.py`, `scripts/run_px4.py`):
1. Start a fresh simulator with its parameters wiped.
2. Audit each link for 15 s with the active probe.
3. Provision a lab key the way an operator would: an unsigned `SETUP_SIGNING` over the local link.
4. Audit again.
5. Verify signatures with the key.
6. On PX4, check that an unsigned attempt to replace the key is rejected (the documented trust-on-first-use rule).

Links audited: ArduPilot SERIAL0 (MAVLink channel 0) and SERIAL1; PX4 "GCS" (udp 14550) and "Onboard" (udp 14540).

## 7. Results

Full table: `results/README.md`. Raw reports and logs are in each `results/<run>/` folder.

| Stack | Link | Default: signed frames | Default: unsigned read answered | After provisioning: signed frames | After provisioning: unsigned read answered | Signatures verified with key |
|---|---|---|---|---|---|---|
| ArduPilot 4.7.2 | SERIAL0 (chan 0) | 0/35 | yes | 27/27 | **yes** | 9/9 |
| ArduPilot 4.7.2 | SERIAL1 | 0/31 | yes | 24/24 | no | 9/9 |
| PX4 v1.17.0 | GCS | 0/7321 | yes | 0/7309 | yes | 0/2906 |
| PX4 v1.17.0 | Onboard | 0/8023 | yes | 0/8058 | yes | 0/3194 |
| PX4 v1.18.0-rc1 | GCS | 0/7355 | yes | 7371/7371 | no | 2911/2911 |
| PX4 v1.18.0-rc1 | Onboard | 0/8470 | yes | 8486/8486 | no | 3222/3222 |

Frame counts differ between stacks because ArduPilot SITL streams telemetry only when a GCS requests it, while PX4 streams by default. "Signatures verified" counts only frames that pymavlink could decode; frames with message IDs missing from its dialect are skipped and reported in the summaries.

**R1: insecure by default, everywhere.** On all 6 default links: 0 signed frames, unauthenticated parameter reads answered, and MAVLink FTP advertised (`MAV_PROTOCOL_CAPABILITY_FTP`) to an unauthenticated peer. A manufacturer that ships either stack unchanged ships a C2 link with no integrity or access control (findings MAV-002, -005 and -006 on every default run).

**R2: stable PX4 cannot sign.** In v1.17.0 the provisioning step had no effect: no key file, 0 valid signatures, unsigned reads still answered. Source inspection agrees: the v1.17.0 MAVLink module has no signing implementation and no `MAV_SIGN_CFG` parameter. The CISA remediation for CVE-2026-1579 (enable signing) is therefore only available from the v1.18 line. This corrects a claim from our own literature review.

**R3: PX4 v1.18 signing works as documented.** After unsigned first-use provisioning:
- a 40-byte key file appeared;
- 100 % of outbound frames were signed on both links, and every decodable frame verified with the key;
- unsigned reads, and the `AUTOPILOT_VERSION` request, went unanswered;
- a later **unsigned** attempt to install a different key was rejected and the original key stayed valid.

The trust-on-first-use window before the first key is installed remains a provisioning risk (§8).

**R4: ArduPilot's channel-0 exemption hides from passive observers.** With a key installed, SERIAL1 signs everything and ignores unsigned input. SERIAL0 also signs **every frame it sends (27/27), yet still answers unsigned requests**. This is by design: `accept_unsigned_callback` accepts all unsigned traffic on MAVLINK_COMM_0, which is assumed to be a secure channel (USB on ChibiOS boards). An auditor that only watches traffic would conclude this link is protected. That is why mavaudit's MAV-005 relies on an active read-only probe and states the discrepancy explicitly. Integrators must make sure that whatever ends up as MAVLink channel 0 is physically trusted.

**Not yet measured.** E5 (GCS × stack interoperability and the provisioning UX in QGroundControl, Mission Planner and MAVProxy), replay behaviour across reboots, and ArduPilot versions other than 4.7.2.

## 8. Recommendations: a minimum baseline for EU drone manufacturers

1. **Ship with signing enabled, or with an unavoidable first-run provisioning step.** Under the CRA's "secure by default" requirement, an opt-in control that customers rarely enable is hard to defend.
2. **Pick a stack version that can sign.** For PX4, that means the v1.18 line (R2). On ArduPilot, treat MAVLink channel 0 as an unauthenticated link and make sure it is only ever a physically trusted port (R4).
3. **Provision keys in production, over a trusted channel.** This avoids trust-on-first-use. Use per-vehicle keys generated by a CSPRNG and document rotation, revocation and lost-key recovery.
4. **Disable MAVLink 1 on every radio port.**
5. **Add link confidentiality** (an AEAD radio or VPN) where the risk assessment requires it, and say why in the technical file.
6. **Gate or disable high-risk services** (the `SERIAL_CONTROL` shell, MAVLink FTP) in production builds.
7. **Use secure boot and signed firmware.**
8. **Run fuzzing and policy checks in CI.** Authentication does not stop harmful but legal inputs.
9. **Operate vulnerability handling now.** Maintain an SBOM (PX4 v1.18 generates SPDX), a CVD policy and an Art. 14 ENISA reporting runbook. The reporting duty is already live.
10. **Audit actively as well as passively.** A link that signs everything it sends may still accept unsigned input (R4). Run a read-only active probe such as `mavaudit --active-probe --fail-on high` in CI against SITL builds of your configuration.

## 9. Limitations and ethics

The study covers simulation only; vendor firmware and hardware radios may behave differently. Legal analysis reflects publicly available texts and secondary sources as of November 2026. No third-party systems were tested. Any previously unknown issue found is reported privately to the maintainers before publication.

## 10. Conclusion

MAVLink signing works when it is turned on. In our measurements PX4 v1.18.0-rc1 and ArduPilot 4.7.2 telemetry ports enforce it exactly as documented. But it is off by default in every stack we tested. It is **absent from the current stable PX4 release**. And on ArduPilot it is bypassed by design on channel 0, which a passive observer cannot see. For EU manufacturers, the CRA turns this integrator responsibility into a legal obligation, with reporting duties already live. A reproducible audit that combines passive observation with a read-only active probe, such as mavaudit, is a cheap first piece of evidence, and the lab in this repository lets anyone reproduce ours in about 30 minutes.

## References

See `research/literature-review.md` §8 (verified BibTeX). Before submission, convert this draft to LaTeX/IEEEtran and resolve every `[cite:…]`.

## Availability

mavaudit and the experiment scripts: `[repository URL, once published]`. Paper DOI: `[Zenodo DOI]`.
