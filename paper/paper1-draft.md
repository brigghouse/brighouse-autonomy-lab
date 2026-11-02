---
title: "MAVLink Security in 2026: Message Signing in PX4 and ArduPilot and What the EU Cyber Resilience Act Means for Drone Manufacturers"
author: "Ian Brighouse, Brighouse Security Labs"
date: 2026-11-02
status: DRAFT v0.1. Results sections are placeholders until experiments E1–E5 are run.
---

# MAVLink Security in 2026: Message Signing in PX4 and ArduPilot and What the EU Cyber Resilience Act Means for Drone Manufacturers

**Ian Brighouse**, Brighouse Security Labs

> **Draft notes (remove before publication)**
> - `[cite:key]` refers to the BibTeX entries in `research/literature-review.md` §8.
> - `[VERIFY]` marks a claim that must be checked against the primary source. Legal text must be checked against the Official Journal PDF.
> - `[RESULT]` marks a value that comes from our own SITL experiments (`research/experiment-plan.md`). Do not fill these in by hand.

## Abstract

MAVLink is the de facto command-and-control (C2) and telemetry protocol of the open-source drone ecosystem, used by PX4, ArduPilot and the ground control stations (GCS) built around them. Since 2016, MAVLink 2 has offered optional message signing, which authenticates frames and resists replay, but adoption has been left to integrators. In 2026 two developments made this gap pressing. First, a CISA advisory rated unauthenticated MAVLink in PX4 at CVSS 9.8 (CVE-2026-1579), and a cluster of 2026 CVEs showed that memory-safety bugs in MAVLink FTP, shell and log handlers are reachable by *any* peer when signing is off. Second, the EU Cyber Resilience Act (CRA) began applying its vulnerability-reporting duty on 11 September 2026, ahead of full application on 11 December 2027. We review the state of MAVLink signing in PX4, ArduPilot, QGroundControl, Mission Planner and MAVProxy as of November 2026. We map MAVLink security properties to CRA Annex I and to the C2-link requirement of Delegated Regulation (EU) 2019/945, and we release *mavaudit*, a passive, key-less auditor that measures signing posture and produces CRA-mapped evidence. Simulator measurements across default and hardened configurations show `[RESULT]`. We conclude with a minimum security baseline for EU drone manufacturers building on open-source flight stacks.

## 1. Introduction

Open-source flight stacks underpin a large share of commercial and dual-use unmanned systems. Their common language, MAVLink, was designed for constrained radio links, and its original version carried no authentication `[cite:marty2014]`. Unauthenticated C2 has been shown, repeatedly and in public, to enable mission disruption and takeover `[cite:kwon2018]` `[cite:marty2014]`, and it is catalogued in NVD as protocol-level weaknesses CVE-2020-10281 to -10283.

MAVLink 2 introduced a signing mechanism that addresses the integrity and authentication part of the problem. Ten years later, three questions remain open in the literature (§7 of our review):

1. **Default posture.** How are current releases configured out of the box, and what does a manufacturer get if it changes nothing?
2. **Practical adoption.** What does enabling signing involve in each stack and GCS, and where are the exemptions?
3. **Regulatory meaning.** How does signing, or its absence, relate to the obligations EU manufacturers now face under the CRA and the UAS product rules?

**Contributions.**
- **C1.** An up-to-date (November 2026) review of MAVLink signing in PX4 (including the spec-aligned implementation in v1.18 `[VERIFY: release status]`), ArduPilot and the main GCS (§3).
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
| **PX4 ≤ v1.17** | Non-standard (`MAV_SIGN_CFG`); `SETUP_SIGNING` only over USB `[VERIFY]` | Off | Replaced in v1.18 |
| **PX4 v1.18** (beta at cut-off) | Spec-aligned (PR #26894); key on SD card | Off (no key → everything unsigned, everything accepted) | Unsigned allowlist: HEARTBEAT, RADIO_STATUS (+ADS-B on traffic links); **trust-on-first-use** provisioning on any link; key change refused while armed |
| **ArduPilot** | Via Mission Planner or MAVProxy `signing setup` | Off until configured `[VERIFY in SITL]` | **USB exempt**; downlink telemetry stays unsigned; MAVLink 1 ports unprotected |
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

**mavaudit** (released in this repository) is a passive auditor that **never needs the signing key**. It classifies every observed frame as MAVLink 1 (`0xFE`), unsigned MAVLink 2, or signed MAVLink 2 (incompatibility flag `0x01`), and it identifies the autopilot from HEARTBEAT messages. An optional active check sends **one unsigned, read-only** `PARAM_REQUEST_READ` (for a harmless system-ID parameter) and records whether it is answered. Findings MAV-001 to MAV-005 are mapped to the crosswalk in §5.4. A scope guard restricts targets to loopback and private addresses unless an authorisation reference is supplied. The tool is validated against a Python reference vehicle that runs in unsigned, signed and MAVLink 1 modes (5 automated tests).

**Testbed.** ArduPilot SITL (current Copter stable) and PX4 SITL (v1.16 or v1.17 stable and v1.18 beta), with QGroundControl, Mission Planner and MAVProxy. All work is local simulation: no RF emission, no third-party systems.

**Experiments** (`research/experiment-plan.md`):

| ID | Configuration | Question |
|---|---|---|
| E1 | ArduPilot default | RQ1: default signing posture |
| E2 | ArduPilot with signing | RQ2: unsigned rejection and exemptions |
| E3 | PX4 default | RQ1 |
| E4 | PX4 v1.18 with signing | RQ2, including the allowlist |
| E5 | GCS × stack interoperability | RQ3: provisioning UX and failure handling |
| E-reach | Signed vs unsigned × unkeyed peer | Reachability reduction (yes/no, no exploitation) |

## 7. Results

`[RESULT]` Table: per configuration, the frames observed, the % signed, whether MAVLink 1 was present, the unsigned-probe outcome, and the mavaudit findings.

`[RESULT]` Provisioning observations per GCS (steps, failure modes, whether the key ever transits an unsecured link).

`[RESULT]` Performance overhead of signing in SITL (optional).

## 8. Recommendations: a minimum baseline for EU drone manufacturers

1. **Ship with signing enabled, or with an unavoidable first-run provisioning step.** Under the CRA's "secure by default" requirement, an opt-in control that customers rarely enable is hard to defend.
2. **Provision keys in production, over a trusted channel.** This avoids trust-on-first-use. Use per-vehicle keys generated by a CSPRNG and document rotation, revocation and lost-key recovery.
3. **Disable MAVLink 1 on every radio port.**
4. **Add link confidentiality** (an AEAD radio or VPN) where the risk assessment requires it, and say why in the technical file.
5. **Gate or disable high-risk services** (the `SERIAL_CONTROL` shell, MAVLink FTP) in production builds.
6. **Use secure boot and signed firmware.**
7. **Run fuzzing and policy checks in CI.** Authentication does not stop harmful but legal inputs.
8. **Operate vulnerability handling now.** Maintain an SBOM (PX4 v1.18 generates SPDX), a CVD policy and an Art. 14 ENISA reporting runbook. The reporting duty is already live.

## 9. Limitations and ethics

The study covers simulation only; vendor firmware and hardware radios may behave differently. Legal analysis reflects publicly available texts and secondary sources as of November 2026. No third-party systems were tested. Any previously unknown issue found is reported privately to the maintainers before publication.

## 10. Conclusion

`[After results]` MAVLink signing has matured, and in 2026 both major stacks support spec-aligned signing. Yet it stays off by default, it is integrator-owned, and the GCS side remains thinly studied. For EU manufacturers, the CRA turns that integrator responsibility into a legal obligation with live reporting duties. mavaudit provides a low-cost, reproducible way to produce the first piece of evidence.

## References

See `research/literature-review.md` §8 (verified BibTeX). Before submission, convert this draft to LaTeX/IEEEtran and resolve every `[cite:…]`.

## Availability

mavaudit and the experiment scripts: `[repository URL, once published]`. Paper DOI: `[Zenodo DOI]`.
