# Literature review: MAVLink security in 2026

**Working title:** "MAVLink security in 2026: the state of message signing in PX4 and ArduPilot, and what the EU Cyber Resilience Act means for drone makers"
**Author:** Ian Brighouse, Brighouse Security Labs
**Research cut-off:** 2026-11-02
**Scope:** Defensive, survey-level. Attack classes are described only at the conceptual level used in the published literature. There are no procedures or exploit code.

> **How sources were verified.** Bibliographic data for academic papers comes from Crossref, the publisher, arXiv or the institutional repository. CVE data comes from the NVD API 2.0, queried on 2026-11-02. Project behaviour comes from the projects' own documentation, and for PX4 from the doc sources in the PX4-Autopilot repository on `main`. Legal text comes from EUR-Lex, with article text checked against public mirrors of the CRA (EUR-Lex HTML could not be retrieved from this environment). Before you quote legal text in the paper, re-check it against the Official Journal PDF. Items marked **[VERIFY]** could only be partly confirmed.

---

## 1. MAVLink protocol basics

### 1.1 MAVLink 1 vs MAVLink 2
- **Framing** ([MAVLink serialization guide](https://mavlink.io/en/guide/serialization.html)):
  - MAVLink 1 uses start marker `0xFE`, a 6-byte header, 8-bit message IDs (0-255) and fixed-length payloads. The maximum packet is 263 bytes.
  - MAVLink 2 uses start marker `0xFD`, a 10-byte header, 24-bit message IDs, and *incompatibility* and *compatibility* flags. It truncates zero-filled trailing payload bytes and can carry an optional 13-byte signature. The maximum packet is 280 bytes when signed.
- **Checksum and CRC_EXTRA.** Both versions use CRC-16/MCRF4XX with a per-message `CRC_EXTRA` seed. This guards against mismatched message definitions. It is **not** a security control, since anyone can compute it.
- **Flags.** The only incompatibility flag defined is `0x01` (`MAVLINK_IFLAG_SIGNED`). A receiver that does not understand an incompatibility flag must drop the packet.
- **Backwards compatibility.** MAVLink 2 is described as "a backward-compatible update", and the C library still handles MAVLink 1 ([MAVLink 2 guide](https://mavlink.io/en/guide/mavlink_2.html)). This coexistence is why NVD records a **protocol-downgrade** weakness class. CVE-2020-10283 says a peer may be steered towards MAVLink 1, which has no authentication (see §4).

### 1.2 MAVLink 2 message signing ([spec](https://mavlink.io/en/guide/message_signing.html))
**What it provides**
- Authentication and integrity of each frame. The signature is the first 48 bits of SHA-256 over a 32-byte secret key, the packet header and payload, the link ID and the timestamp.
- A 13-byte trailer: an 8-bit link ID, a 48-bit timestamp counted in 10 µs units since 2015-01-01 GMT, and the 48-bit signature.
- Replay resistance. Timestamps must increase strictly for each (SystemID, ComponentID, LinkID) stream. A receiver discards a packet that is older than the last one on that stream, or more than 1 minute (6,000,000 units) behind its local time. The link timestamp must never be updated from a packet that is signed incorrectly. Implementations should persist the timestamp at least about once a minute.

**What it does not provide**
- **Confidentiality.** Payloads stay in plaintext. Telemetry, missions and parameters can be read by anyone on the link.
- **Key distribution.** The spec only says the 32-byte key can come from a SHA-256 passphrase or a random generator. It is to be shared via `SETUP_SIGNING` over a secure link such as USB or wired Ethernet. That message "should never be broadcast" and must not be forwarded, and the key must not appear on public protocols or in logs. There is no rotation, revocation or per-device identity.
- **Source identity within the trust domain.** Every holder of the shared symmetric key can sign as any system or component ID. PX4's documentation says this explicitly.
- **Uniform acceptance of unsigned traffic.** The rules are left to each implementation. They may depend on parameters, transport, message type or flags. Suggested cases include secure channels, always accepting `RADIO_STATUS`, an unsigned mode, and "accept unsigned until the first signed packet". The spec only requires that packets failing these rules be rejected.

**Points for the paper:**
1. Signing is opt-in and implementation-defined at the edges: provisioning, allowlists, and USB exemptions.
2. The timestamp-based replay window depends on the clocks being sane and the timestamp being persisted. PX4 notes that most vehicles lose power abruptly, so the timestamp stored on disk usually stays at its value from the last provisioning.
3. The 48-bit truncated tag and the lack of encryption are design choices for constrained links.

---

## 2. Implementation status, 2025–2026

### 2.1 PX4
- **History.**
  - An early proof of concept, PX4/Firmware PR #7530 ("First stab at Mavlink signing", opened July 2017), used a hard-coded key. It was **closed without merging** in March 2021 ([PR #7530](https://github.com/PX4/Firmware/pull/7530)).
  - PX4 v1.17 shipped a signing implementation configured by a non-standard parameter, `MAV_SIGN_CFG`. In that version `SETUP_SIGNING` was accepted only over USB, as implied by the v1.18 notes.
- **v1.18 (in beta at the cut-off date): spec-compliant signing.** PR [#26894](https://github.com/PX4/PX4-Autopilot/pull/26894) is "fix(mavlink)!: align signing with MAVLink spec and fix performance regression", authored by mrpollo and opened 27 March 2026. The v1.18 release notes record the change as breaking ([v1.18 release notes](https://docs.px4.io/main/en/releases/1.18.html)):
  - Signing is active only when a valid key file is present on the SD card (`/mavlink/mavlink-signing-key.bin`, 40 bytes, mode 0600).
  - `SETUP_SIGNING` is accepted on **any** link but rejected while the vehicle is armed.
  - Signing can be disabled with a *signed* all-zero key.
  - `MAV_SIGN_CFG` was removed, and signing has zero overhead when inactive.
  - Integrators upgrading from v1.17 must re-provision their keys.
  - A PX4 forum reply of 5 Aug 2026 confirms that signing is "only from v1.18 onwards" for the spec-compliant flow ([discuss.px4.io](https://discuss.px4.io/t/px4-mavlink2-signing/49306)).
- **Current behaviour** ([PX4 Message Signing](https://docs.px4.io/main/en/mavlink/message_signing.html)):
  - **Default is off.** With no key, "all messages are sent unsigned and all incoming messages are accepted."
  - With a key, signing is enforced on **all links including USB**, and unsigned or invalid frames are not forwarded to other links.
  - **Unsigned allowlist:** `HEARTBEAT` (0) and `RADIO_STATUS` (109) on all links. `ADSB_VEHICLE` (246) and `COLLISION` (247) are allowed only on links in `ADS-B/Traffic (uAvionix)` mode.
  - **Provisioning is trust-on-first-use.** "When no key is provisioned, `SETUP_SIGNING` is accepted unsigned on any link." The hardening guide warns that a key installed by a third party locks out the legitimate GCS, and recovery requires physical access.
  - The key is not exposed through parameters. The SD card is the main physical attack surface. A lost key can only be recovered physically, by removing the SD card or reflashing over SWD/JTAG.
  - PX4 states that its implementation "has not been" audited, although the protocol was audited when drafted.
- **Hardening guidance.** "MAVLink Security Hardening for Production Deployments" ([PX4 docs](https://docs.px4.io/main/en/mavlink/security_hardening.html)) states that "by default, all MAVLink messages are unauthenticated and unencrypted". It lists the capabilities exposed on an unsecured link: shell via `SERIAL_CONTROL`, FTP file access, parameter and mission changes, arm/disarm, and flight termination. It assigns link security to the **system integrator**. This framing matters for the CRA discussion in §5.
- **CISA.** Advisory ICSA-26-090-02 (31 Mar 2026) covers CVE-2026-1579, CWE-306, CVSS v3 9.8, with the product listed as PX4 v1.16.0 SITL. Its remediation is to enable MAVLink 2 signing on all non-USB links and to follow the hardening guide ([CISA](https://www.cisa.gov/news-events/ics-advisories/icsa-26-090-02); [CSAF JSON](https://github.com/cisagov/CSAF/blob/develop/csaf_files/OT/white/2026/icsa-26-090-02.json); Spanish mirror at [INCIBE-CERT](https://www.incibe.es/en/incibe-cert/early-warning/vulnerabilities/cve-2026-1579)).

### 2.2 ArduPilot
- **Configuration through Mission Planner** ([ArduPilot MAVLink2 Signing](https://ardupilot.org/copter/docs/common-MAVLink2-signing.html)):
  - Set the serial port protocol to MAVLink2. "Communication with any serial port using MAVLink 1 is not protected."
  - Then use SETUP > Advanced > "Mavlink Signing". ADD creates a passkey, USE pushes it to the autopilot, and Disable Signing removes it.
- **Acceptance behaviour:**
  - "USB connections are unaffected". This is deliberate, so a user can recover from an unknown key.
  - Serial MAVLink2 links only respond to *commands* signed with the active key, but "telemetry downlink data is unaffected".
  - Signing "merely controls if the autopilot will respond to MAVLink commands or not". It provides no encryption.
  - The page does not state a default. It presents signing as something the user turns on, which implies it is off until configured. **[VERIFY in SITL]**
- **MAVProxy `signing` module** ([MAVProxy docs](https://ardupilot.org/mavproxy/docs/modules/signing.html)):
  - `signing setup KEY` sets the key on both MAVProxy and the vehicle. The docs warn the key "is sent in plaintext to the vehicle, so ensure this setup is done over a secure link."
  - `signing remove`, `signing disable` and `signing key` cover the other operations. `disable` affects only MAVProxy, and the vehicle still expects signed packets.
  - The MAVProxy page says it attaches a "SHA-512 hash" of the key, but the MAVLink spec defines SHA-256. Treat this as a documentation inconsistency. **[VERIFY]**
- **Tamper-proof firmware.** ArduPilot supports signed bootloaders and signed firmware ([ArduPilot secure firmware](https://ardupilot.org/dev/docs/secure-firmware.html)).

### 2.3 QGroundControl
- The QGC user guide (master) documents a **MAVLink 2 Signing** section under Application Settings > Telemetry ([QGC docs](https://docs.qgroundcontrol.com/master/en/qgc-user-guide/settings_view/telemetry.html)):
  - Keys are named passphrases, and only the hash is stored.
  - Enabling sends `SETUP_SIGNING` to the vehicle. Disabling sends an all-zero key.
  - QGC auto-detects a matching stored key when signed packets arrive.
  - The guide warns that keys "should only be sent to the vehicle over secure (wired or encrypted) links."
- The QGC API documentation exposes a `MAVLinkSigning` namespace ([API docs](https://api.qgroundcontrol.com/master/namespaceMAVLinkSigning.html)). It includes key handling, verification, and unsigned-acceptance policies (`Strict`, `Pending`).
- **Maturity caveats:**
  - The PX4 PR #26894 tests used a "QGroundControl daily build".
  - The PR author found that QGC did not check for `SETUP_SIGNING` rejection, which can cause loss of communication. This is tracked as QGC issue #14250.
  - The "What's new since v5.1" page does not mention signing ([QGC what's new](https://docs.qgroundcontrol.com/master/en/qgc-user-guide/getting_started/whats_new.html)).
  - I could not confirm which *stable* QGC release first ships signing. **[VERIFY]**

### 2.4 Mission Planner
Mission Planner supports signing natively. It stores keys on the PC and can push them to the autopilot (see §2.2).

### 2.5 Default configurations shipped by vendors
- I found **no published, systematic measurement** of signing defaults on commercial airframes or flight controllers.
- The upstream defaults are documented:
  - PX4 has signing off without a key.
  - ArduPilot has signing off until configured, and USB stays exempt.
- PX4's documentation explicitly places enabling signing on the integrator.
- This is a gap for empirical work (§7).

---

## 3. Academic and industry literature

### 3.1 Foundational MAVLink security analyses
- **Marty (2014), AFIT MSc thesis.** Presents three proofs of concept against confidentiality, integrity and availability on unprotected MAVLink (ArduPilot Mega 2.5 with Mission Planner and MAVProxy). Also proposes a way to measure the cost of securing MAVLink in latency, power and exploit success. [ref: marty2014]
- **Domin, Symeonidis & Marin (2016).** Fuzzes MAVLink 1 against a flight stack and identifies robustness and security issues. Listed in the repository as an e-print or working paper; I could not confirm the venue. [ref: domin2016] **[VERIFY venue]**
- **Kwon et al. (2018), IEEE Access.** An empirical analysis that uses a MAVLink weakness to interrupt an ongoing mission. It is a canonical citation for the availability impact of unauthenticated command channels. [ref: kwon2018]
- **Allouch et al. (2019), IWCMC (MAVSec).** Adds encryption to MAVLink in ArduPilot and compares AES-CBC, AES-CTR, RC4 and ChaCha20 on memory and CPU. ChaCha20 performed best. [ref: allouch2019]

### 3.2 Encryption and protocol-hardening proposals
- **Sabuwala & Daruwala (2022), IEEE IBSSC.** Encrypts MAVLink. [ref: sabuwala2022]
- **Dixit et al. (2025), arXiv (MAVShield).** A new lightweight cipher, benchmarked against AES-CTR, ChaCha20, Speck-CTR and Rabbit on a real testbed. Note for the paper: a home-grown cipher validated only with statistical tests (NIST/Diehard) should be treated cautiously compared with standard AEAD constructions. [ref: dixit2025]
- **Amorim et al. (2025), arXiv.** Refined multiparty session types that enforce *safe sequences* of MAVLink messages. Aimed at "stealthy" attacks built from individually legal messages. [ref: amorim2025]

### 3.3 Fuzzing and input validation in flight stacks
These works show that **authenticated is not the same as safe**: a legitimate or compromised GCS can still send harmful but well-formed inputs.
- **Kim T. et al. (2019), USENIX Security (RVFuzzer).** Control-guided fuzzing of control parameters. Found 89 input-validation bugs, 87 of them zero-day, in two popular flight stacks. [ref: kim2019rvfuzzer]
- **Kim H. et al. (2021), NDSS (PGFUZZ).** Policy-guided fuzzing for logic bugs in robotic vehicles. [ref: kim2021pgfuzz]
- **Wang et al. (2026), NDSS (ADGFUZZ).** Assignment-dependency-guided fuzzing. [ref: wang2026adgfuzz]
- **Zhou et al. (2026), International Fuzzing Workshop (UAVConfigFuzzer).** Detects incorrect configurations. [ref: zhou2026uavconfigfuzzer]
- **Dash et al. (2019), ACSAC.** Stealthy attacks that evade control-based intrusion detection in robotic vehicles. [ref: dash2019]
- **Konapalli et al. (2025), arXiv.** Reverse-engineers ArduPilot's architecture and control models for a control-aware security analysis. [ref: konapalli2025]

### 3.4 Surveys, 2020–2025
- **Yaacoub et al. (2020), Internet of Things (Elsevier).** Drone attacks, limitations and recommendations. [ref: yaacoub2020]
- **Nassi et al. (2021), IEEE S&P (SoK).** Security and privacy of commercial drones. [ref: nassi2021]
- **Tsao, Girdler & Vassilakis (2022), Ad Hoc Networks.** UAV communications and FANET threats. [ref: tsao2022]
- **Mekdad et al. (2023), Computer Networks.** Survey of UAV security and privacy issues. [ref: mekdad2023]
- **Hamza et al. (2024), ICoDT2.** "MAVLink Protocol: A Survey of Security Threats and Countermeasures", the most MAVLink-specific recent survey. [ref: hamza2024]

### 3.5 Ground control stations
- **Mansfield et al. (2013), IEEE HST.** A threat model for smart-device GCS. This is one of the few academic works focused on the GCS. [ref: mansfield2013]
- I found **no peer-reviewed vulnerability study focused on QGroundControl or Mission Planner** for 2024–2026. NVD keyword searches for "QGroundControl" and "Mission Planner" returned no CVEs on 2026-11-02. This is itself a finding and a research gap (§7).

### 3.6 Adjacent (non-MAVLink) drone security
- **Schiller et al. (2023), NDSS.** DJI DroneID and firmware analysis. Useful context that proprietary ecosystems face the same classes of issue. [ref: schiller2023]

---

## 4. CVEs and advisories

All entries below are from NVD as of 2026-11-02. "Class" is my one-line summary of the NVD description and CWE. Entries marked "Awaiting Analysis" or "Deferred" have not been fully analysed by NVD.

### 4.1 Protocol level (MAVLink)
| ID | Year | Component | Class |
|---|---|---|---|
| CVE-2020-10281 | 2020 | MAVLink protocol | Cleartext transmission (CWE-319). No confidentiality on the medium. |
| CVE-2020-10282 | 2020 | MAVLink v1 | No authentication or authorisation (CWE-306), which enables spoofing and person-in-the-middle attacks. |
| CVE-2020-10283 | 2020 | MAVLink v2 negotiation | Downgrade to v1 bypasses v2 authentication (CWE-288). |
| CVE-2026-1579 | 2026 | MAVLink as deployed in PX4 (CISA ICSA-26-090-02) | Missing authentication for a critical function (CWE-306, CVSS 9.8). Without signing, any peer can send any message, including `SERIAL_CONTROL` shell access. |

### 4.2 PX4-Autopilot (selection relevant to the MAVLink and GCS attack surface)
| ID | Year | Component | Class |
|---|---|---|---|
| CVE-2021-34125 | 2021 (published 2023) | PX4 ≤1.11.3 / Yuneec Mantis Q, NuttX shell | Information disclosure through shell commands |
| CVE-2021-46896 | 2021 (published 2023) | MAVLink handler, msgid 332 | Buffer overflow leading to DoS |
| CVE-2023-46256 | 2023 | Parser (`parserbuf_index`) | Heap buffer overflow |
| CVE-2023-47625 | 2023 | CRSF RC parser | Global buffer overflow |
| CVE-2024-24254 / -24255 | 2024 | Geofence and mission feasibility checker | Race condition leading to unintended mission |
| CVE-2024-29460, CVE-2024-30800 | 2024 | Mission block / geofence | Logic flaws affecting the flight path and geofence |
| CVE-2024-30799 | 2024 | Breach return point | Buffer overflow |
| CVE-2024-38951 | 2024 | MAVLink message handling (v1.12.3) | Buffer overflow leading to DoS |
| CVE-2024-38952 | 2024 | Logger topic name | Buffer overflow |
| CVE-2024-40427 | 2024 (published 2025) | Stack buffer overflow | Memory safety |
| CVE-2025-5640 | 2025 | `MavlinkReceiver::handle_message_trajectory_representation_waypoints` | Stack overflow |
| CVE-2025-9020 | 2025 | `handle_message_serial_control` (MAVLink shell) | Use-after-free |
| CVE-2025-15150 | 2025 | `MavlinkLogHandler` | Stack overflow |
| CVE-2026-26741 / -26742 | 2026 | Mode switching / re-arm grace period | Missing authorisation and protection-mechanism failures (safety logic) |
| CVE-2026-32705 / -32706 / -32707 / -32708 | 2026 | BST probe, CRSF parser, tattu_can, Zenoh uORB subscriber | Unbounded copies and overflows from peripheral or bus input |
| CVE-2026-32709 | 2026 | MAVLink FTP | Unauthenticated path traversal (CWE-22). Fixed in 1.17.0-rc2 ([GHSA-fh32-qxj9-x32f](https://github.com/PX4/PX4-Autopilot/security/advisories/GHSA-fh32-qxj9-x32f)). |
| CVE-2026-32713 | 2026 | MAVLink FTP session validation | Logic error (`&&` vs `\|\|`) |
| CVE-2026-32724 | 2026 | `MavlinkShell::available()` | Use-after-free race |
| CVE-2026-32743 | 2026 | `MavlinkLogHandler` (log request) | Stack overflow |
| CVE-2026-84698, -86096, -86097, -86713, -86714, -102808, -102809 | 2026 | Shell or system commands (sd_bench, temperature calibration, param, load_mon, netman, sd_stress, file2) | Memory safety issues reachable once shell access exists. These are "Awaiting Analysis". |

*Observation for the paper:* the 2026 cluster shows that several high-impact paths (MAVLink FTP, shell, log handler) are reachable by **any** MAVLink peer when signing is off. This links §2 to §4: signing reduces the *reachability* of memory-safety bugs to holders of the key.

### 4.3 ArduPilot
| ID | Year | Component | Class |
|---|---|---|---|
| CVE-2022-28711 | 2022 | APWeb (`cgi.c` unescape) | Memory corruption from crafted HTTP request |
| CVE-2024-48519 | 2024 (published 2026) | Rover, ADIS1647x IMU driver | Buffer overflow leading to DoS (local) |
| CVE-2026-38971 | 2026 | `GCS_MAVLINK::handle_serial_control()` (through Plane-4.6.3) | Out-of-bounds read. Fix in [PR #32587](https://github.com/ArduPilot/ardupilot/pull/32587). |

### 4.4 GCS and libraries
- **QGroundControl, Mission Planner, pymavlink, MAVSDK and MAVProxy:** no NVD CVEs were returned by keyword search on 2026-11-02.
- I could not enumerate the repository-level GitHub Security Advisories for these projects from this environment. **[VERIFY manually at `github.com/<org>/<repo>/security/advisories`]**
- **Related, not MAVLink stack:** CVE-2024-33844 (Parrot ANAFI USA). Missing validation of `MAV_MISSION_TYPE` in `MISSION_COUNT` handling cuts the controller link.

---

## 5. Regulation

### 5.1 CRA (Regulation (EU) 2024/2847) scope for drones and GCS
- **General scope (Art. 2(1)).** The CRA covers "products with digital elements made available on the market" whose intended or reasonably foreseeable use includes a direct or indirect data connection to a device or network. A drone with a telemetry or C2 link, a flight controller, and GCS software sold commercially all fit this definition on its face.
- **Exclusions relevant to aviation:**
  - Art. 2(3): the CRA "does not apply to products with digital elements that have been **certified** in accordance with Regulation (EU) 2018/1139" ([CRA Art. 2 mirror](https://cyber-resilience-act.com/cra/chapter-1/article-2/); [official text](https://eur-lex.europa.eu/eli/reg/2024/2847/oj/eng)).
  - Art. 2(2) excludes medical devices (2017/745, 2017/746) and motor vehicles (2019/2144).
  - Art. 2(4) excludes marine equipment (2014/90/EU).
  - Art. 2(7) excludes products developed exclusively for national security or defence.
- **Analysis for the paper** (author's interpretation, to be framed as such):
  - The exclusion turns on **certification** under 2018/1139: type certificates and similar, typical of the *certified* UAS category.
  - Open-category drones carrying a C-class marking under Delegated Regulation (EU) 2019/945 go through product conformity assessment and CE marking. They are not certified, so they are **plausibly within CRA scope**.
  - Standalone GCS software and firmware made available commercially are also plausibly in scope.
  - A compliance-vendor guide reaches the same reading ([CVD Portal guide](https://cvdportal.com/guides/drone-uav-manufacturers); vendor material, not authoritative). Cite it only as an illustration of industry interpretation.
  - The Commission's non-binding CRA application guidance, published 27 July 2026, should be checked for any aviation-specific statement ([Commission](https://digital-strategy.ec.europa.eu/en/library/commission-publishes-new-guidance-support-timely-cyber-resilience-act-implementation)). **[VERIFY]**
- **Art. 2(5).** The CRA's application may be limited or excluded for products covered by sectoral rules that achieve the same or a higher level of protection, through a Commission delegated act. I found no such act for UAS.
- **Open source:**
  - Non-commercial FOSS is outside scope. The Commission guidance clarifies that free software is out of scope "provided it is not marketed as part of a commercial activity" ([summary](https://www.opensourceforu.com/2026/07/eu-clarifies-cra-rules-for-non-commercial-open-source/)).
  - *Open-source software stewards* have light obligations under Art. 24: a documented cybersecurity policy, cooperation with market surveillance, and partial Art. 14 reporting ([Art. 24](https://www.springlex.eu/en/packages/cra/cra-regulation/article-24/)).
  - Upstream PX4 and ArduPilot are likely FOSS or steward-type cases. **Drone makers that integrate them into commercial products are the "manufacturers"** and carry the full Annex I obligations for the whole product, including the integrated FOSS.

### 5.2 Interplay with Delegated Regulation (EU) 2019/945 (UAS product rules)
- 2019/945 defines classes C0 to C6. Annex Part 3 (class C2), point (8), requires that the UA, "unless tethered", be "equipped with a command and control link protected against unauthorised access to the command and control functions" ([2019/945 Annex Part 3, legislation.gov.uk reproduction of EU text](https://www.legislation.gov.uk/eur/2019/945/annex/part/3)). A secondary source lists the same requirement for C3 ([summary](https://eudroneport.com/blog/drone-product-requirements-2019-945/)). **[VERIFY C3 point against the OJ]**
- That requirement is **outcome-only**. It names no mechanism, standard or test.
  - MAVLink 2 signing is one candidate technical means for MAVLink-based C2/C3 products.
  - Signing alone may not satisfy a strict reading, because USB is exempt in ArduPilot, PX4 provisioning is trust-on-first-use, and PX4 allowlists some messages.
- Remote ID: classes C1 to C3 require direct remote identification. The texts I reviewed set no cybersecurity requirement for Remote ID integrity.
- **Overlap question for the paper.** Where a C-class drone is in CRA scope, the manufacturer may face two regimes for the same C2 link: the 2019/945 outcome requirement and the CRA Annex I essential requirements. CRA conformity evidence (threat model, secure defaults, vulnerability handling) could help demonstrate the 2019/945 "protected against unauthorised access" property. There is no formal presumption linking the two.

### 5.3 Interplay with RED Delegated Regulation (EU) 2022/30 and EN 18031
- DA 2022/30 activates RED Art. 3(3)(d), (e) and (f) for in-scope radio equipment. These cover network harm, personal data and privacy, and fraud. It has applied from **1 August 2025** ([Reed Smith](https://www.reedsmith.com/our-insights/blogs/viewpoints/102ktki/red-eu-cybersecurity-obligations-for-iot-products-from-august-2025/)).
- The key scope trigger is **internet capability**. A drone or GCS that is internet-connected (for example over Wi-Fi or LTE) is a candidate. A pure point-to-point sub-GHz telemetry radio is less clearly in scope. **[VERIFY per product]**
- **Harmonised standards.** EN 18031-1/-2/-3:2024 were cited with restrictions by Commission Implementing Decision (EU) 2025/138 of 28 January 2025. For example, there is no presumption of conformity where users may skip setting a password (AUM-5-1, AUM-5-2) ([summary](https://www.ezurio.com/resources/blog/understanding-eu-commission-implementation-of-decision-eu-2025-138-new-harmonized-standards-and-restrictions)).
- **Repeal.** Delegated Regulation (EU) **2026/339** of 16 February 2026, published in the OJ on 29 April 2026, repeals DA 2022/30 **with effect from 11 December 2027**, when the CRA applies in full, to avoid overlap ([TÜV](https://www.tuv.com/regulations-and-standards/en/eu-commission-delegated-regulation-eu-2026-339-of-february-16-2026-repealing-delegated-regulation-eu-2022-30.html); [Lovguiden](https://www.lovguiden.dk/en/det-offentlige/eur-lex-eu-tidende/2026-04-29-eu-ophaever-cybersikkerhedskrav-for-radioudstyr-fra-december-2027); [EUR-Lex](https://eur-lex.europa.eu/eli/reg_del/2026/339/oj/eng)).
- **Practical consequence.** Between 1 Aug 2025 and 11 Dec 2027, internet-capable radio drones and GCS hardware fall under RED DA and EN 18031. After that, they fall under the CRA alone. EN 18031 work can be reused as early CRA evidence.

### 5.4 Key CRA dates (Art. 71(2))
| Date | What applies |
|---|---|
| 10 Dec 2024 | Entry into force |
| 11 Jun 2026 | Chapter IV (notification of conformity assessment bodies, Arts. 35–51) |
| **11 Sep 2026** | **Art. 14 reporting** of actively exploited vulnerabilities and severe incidents. This also covers products already on the market. |
| **11 Dec 2027** | **Full application** |

Source: Art. 71(2) "This Regulation shall apply from 11 December 2027. However, Article 14 shall apply from 11 September 2026 and Chapter IV … from 11 June 2026" ([Art. 71 mirror](https://www.european-cyber-resilience-act.com/Cyber_Resilience_Act_Article_71.html)).
*Note for the paper:* as of the cut-off date, the Art. 14 reporting duty is **already live**. A drone maker that learns of active exploitation of a vulnerability like CVE-2026-1579 in its product must notify through the ENISA single reporting platform.

### 5.5 Product class: default, important class I or II, or critical?
- **Art. 7(1).** A product is "important" if its **core functionality** matches an Annex III category. Integrating such a component does not by itself make the host product important ([Art. 7 mirror](https://www.european-cyber-resilience-act.com/Cyber_Resilience_Act_Article_7.html)).
- **Final Annex III:**
  - **Class I** includes boot managers (8), physical and virtual network interfaces (10), operating systems (11), routers, modems and switches (12), and microprocessors and microcontrollers with security-related functionalities (13, 14).
  - **Class II** includes hypervisors and container runtimes, firewalls and IDS/IPS, and tamper-resistant microprocessors and microcontrollers ([Annex III mirror](https://cyber-resilience-act.com/cra/annex-iii/)).
  - *Caution:* some websites reproduce the 2022 *proposal* Annex III, which listed "robot controllers" and IACS. These are **not** in the final text.
- **Implementing Regulation (EU) 2025/2392** (OJ 1.12.2025) gives technical descriptions ([EUR-Lex](https://eur-lex.europa.eu/eli/reg_impl/2025/2392/oj/eng); [mirror of Annex I](https://www.springlex.eu/en/packages/cra/tdpc-regulation/annex-1/)):
  - "Operating systems" expressly include "real-time operating systems, general-purpose and special-purpose operating systems."
  - "Boot managers" include "single-stage and multi-stage boot loaders."
- **Reasoned mapping** (author's interpretation):
  - **Complete drone, or flight controller with PX4 or ArduPilot:** the core function is flight control, which is not an Annex III category, so it is **default** (self-assessment, Module A). This holds even though it embeds an RTOS (NuttX, ChibiOS) and a bootloader.
  - **GCS software (QGC or Mission Planner derivatives):** the core function is vehicle command and monitoring. This most plausibly falls in the **default** class. One could argue it is a "network management system" (Class I item 6) for swarm or fleet GCS that manage networked nodes. That reading is weak and should be flagged as contested.
  - **Products sold standalone whose core functionality matches Annex III:**
    - an RTOS sold as a product: Class I, operating system;
    - a secure bootloader sold separately: Class I, boot manager;
    - a telemetry or mesh radio module sold as a network interface or router: Class I, network interface or router;
    - an MCU with security features: Class I.
  - **Annex IV (critical: HSM-style devices, smart meter gateways, smartcards/secure elements):** not expected to apply to typical drone products.
  - **Internet-connected toy drones:** a vendor guide argues that toy drones covered by Directive 2009/48/EC with location-tracking features may fall under Class I item 18 ([CVD Portal](https://cvdportal.com/guides/drone-uav-manufacturers)). This is plausible because the item covers "internet-connected toys … with … location tracking features".

### 5.6 EU Action Plan on Drone and Counter-Drone Security (11 Feb 2026)
- COM(2026) 81 final ([Commission news](https://commission.europa.eu/news-and-media/news/new-plan-counter-drone-threats-2026-02-11_en); [library](https://digital-strategy.ec.europa.eu/en/library/action-plan-drone-and-counter-drone-security); [analysis](https://www.medialaws.eu/the-commission-action-plan-on-drone-and-counter-drone-security/)).
- It focuses on civil internal security, organised around preparedness, detection, response and defence readiness.
- It announces a **Drone Security Package** to "adapt the existing regulatory framework for airborne drones to the evolving security threats". It proposes extending registration and identification to **all drones above 100 g** and envisions an **"EU Trusted Drone"** scheme to identify secure equipment ([The Register](https://www.theregister.com/2026/02/11/eu_drone_action_plan/)).
- Per MediaLaws, the plan does **not** say whether a cybersecurity certification scheme under the Cybersecurity Act (2019/881) will follow. The sources I reviewed do not mention the CRA.
- **Relevance:** a future "Trusted Drone" label and revised UAS rules could specify C2-link security more concretely than 2019/945 does today. This is a natural place for the paper to argue for MAVLink signing or AEAD-link baselines.

---

## 6. Defensive recommendations from the literature and vendor guidance

1. **Authenticate the C2 link.**
   - Enable MAVLink 2 signing on every vehicle, GCS and companion computer (PX4 hardening guide; CISA ICSA-26-090-02; ArduPilot docs).
   - Disable or physically restrict MAVLink 1 on radio ports, given ArduPilot's "MAVLink 1 is not protected" and CVE-2020-10283.
2. **Provision keys before first exposure, over a trusted channel.**
   - The MAVLink spec, PX4, MAVProxy and QGC all warn that `SETUP_SIGNING` carries the key in cleartext.
   - PX4 trust-on-first-use means factory or production provisioning is preferable.
   - Generate keys from a CSPRNG rather than weak passphrases (spec).
3. **Add confidentiality where it is needed.**
   - Signing does not encrypt. Use link-layer AEAD (encrypted radios, VPN or IPsec) as PX4 recommends.
   - In research, MAVSec (Allouch 2019) found ChaCha20 efficient on autopilot-class hardware.
   - Prefer standard, reviewed AEAD over novel ciphers (compare Dixit 2025).
4. **Minimise exposed MAVLink services.**
   - Do not expose MAVLink UDP/TCP to untrusted networks, and segment networks (PX4 hardening guide).
   - Restrict high-risk services such as the `SERIAL_CONTROL` shell and MAVLink FTP. The 2026 CVE cluster in §4 shows why.
5. **Key management lifecycle.**
   - There is no automatic rotation or per-device identity, so the integrator must define rotation, revocation and lost-key procedures. PX4 supports physical recovery only.
   - Protect the SD card and debug ports, since the PX4 key sits on the SD card.
6. **Firmware integrity.** Use secure or signed boot: the PX4 ed25519 bootloader ([PX4 secure boot](https://docs.px4.io/main/en/advanced_config/bootloader_secure_boot.html)) or ArduPilot signed bootloader and firmware. This aligns with the CRA Annex I expectations on integrity and secure updates.
7. **Input validation and robustness testing.**
   - Authentication does not stop harmful legal inputs from an authorised or compromised GCS (RVFuzzer, PGFUZZ, ADGFUZZ, Dash 2019, Amorim 2025).
   - Integrate fuzzing and policy checks into CI.
8. **Vulnerability handling and SBOM for CRA readiness.**
   - PX4 v1.18 generates an SPDX 2.3 SBOM per build ([v1.18 notes](https://docs.px4.io/main/en/releases/1.18.html)).
   - Manufacturers need a coordinated vulnerability disclosure (CVD) process and an Art. 14 reporting process, which has been live since 11 Sep 2026.

---

## 7. Gaps: open questions for simulator-based study (SITL, no flight hardware)

These are research questions only, framed as measurements of defensive posture.

1. **Default acceptance.** Across PX4 SITL (v1.16, v1.17, v1.18 beta, main) and ArduPilot SITL (Copter, Plane, Rover, current stable), what fraction of default configurations accept unsigned MAVLink 2 and MAVLink 1 commands on each link type (UDP, simulated serial, USB-equivalent)?
2. **Allowlist and exemption surface.** Which message IDs are accepted unsigned when signing is active in each stack? This covers PX4's documented allowlist, ArduPilot's USB exemption and its "telemetry unaffected" behaviour. Do the observed behaviours match the documentation?
3. **Provisioning semantics.** How does each stack handle `SETUP_SIGNING` while unprovisioned, provisioned, armed and disarmed, and over which links? How does each GCS (QGC stable vs daily, Mission Planner, MAVProxy) handle rejection? QGC issue #14250 suggests a robustness gap.
4. **Replay-window robustness.** How do the stacks behave across reboot when the timestamp persists infrequently (PX4 notes on-disk timestamps are often stale), and under GCS clock skew? Measure whether behaviour conforms to the 1-minute rule.
5. **GCS interoperability matrix.** Do signed sessions interoperate across PX4 or ArduPilot × QGC, Mission Planner, MAVProxy or MAVSDK, including routers such as mavlink-router or MAVProxy forwarding? Where are signatures stripped or re-signed?
6. **Version negotiation.** Do current stacks still permit falling back to MAVLink 1 on ports configured for MAVLink 2 when signing is enabled? This is a conformance check related to CVE-2020-10283.
7. **Performance cost.** Measure the CPU, latency and bandwidth overhead of signing in SITL, and if possible on reference hardware. Compare with published encryption overheads (MAVSec, MAVShield). PX4 claims zero overhead when signing is inactive, which can be confirmed.
8. **Reachability reduction.** For the 2026 PX4 CVEs (FTP, shell, log handler), confirm in a patched-vs-unpatched SITL matrix whether enabling signing blocks reachability from an unkeyed peer. This should be a yes/no conformance test, not exploitation.
9. **Vendor defaults (outside SITL).** No public dataset exists on signing defaults in commercial C-class drones. A survey of manufacturers' documentation and Declarations of Conformity under 2019/945 (C2/C3 point (8)) would fill this.
10. **Regulatory mapping.** How do MAVLink signing and link encryption map to CRA Annex I essential requirements, EN 18031-1 mechanisms and the 2019/945 C2 point (8)? No published crosswalk exists.
11. **GCS security research gap.** There are no QGC or Mission Planner CVEs in NVD, and the GCS-focused academic work is old (Mansfield 2013). A defensive review of GCS signing UX, key storage at rest and plugin surfaces is missing.
12. **Open-source steward status.** How do Dronecode/PX4 and ArduPilot position themselves under CRA Art. 24, and what does that mean for downstream manufacturers' due diligence (Art. 13(5))?

---

## 8. References (verified; BibTeX)

```bibtex
@mastersthesis{marty2014,
  author = {Marty, Joseph A.},
  title  = {Vulnerability Analysis of the {MAVLink} Protocol for Command and Control of Unmanned Aircraft},
  school = {Air Force Institute of Technology},
  type   = {{MSc} thesis},
  year   = {2014},
  month  = mar,
  note   = {Advisor: Barry E. Mullins. Theses and Dissertations 613},
  url    = {https://scholar.afit.edu/etd/613}
}

@misc{domin2016,
  author = {Domin, Karel and Symeonidis, Iraklis and Marin, Eduard},
  title  = {Security Analysis of the Drone Communication Protocol: Fuzzing the {MAVLink} Protocol},
  year   = {2016},
  note   = {E-print/working paper; venue not confirmed},
  url    = {https://orbilu.uni.lu/handle/10993/37613}
}

@article{kwon2018,
  author  = {Kwon, Young-Min and Yu, Jaemin and Cho, Byeong-Moon and Eun, Yongsoon and Park, Kyung-Joon},
  title   = {Empirical Analysis of {MAVLink} Protocol Vulnerability for Attacking Unmanned Aerial Vehicles},
  journal = {IEEE Access},
  volume  = {6},
  pages   = {43203--43212},
  year    = {2018},
  doi     = {10.1109/ACCESS.2018.2863237}
}

@inproceedings{allouch2019,
  author    = {Allouch, Azza and Cheikhrouhou, Omar and Koubaa, Anis and Khalgui, Mohamed and Abbes, Tarek},
  title     = {{MAVSec}: Securing the {MAVLink} Protocol for {Ardupilot/PX4} Unmanned Aerial Systems},
  booktitle = {2019 15th International Wireless Communications \& Mobile Computing Conference (IWCMC)},
  pages     = {621--628},
  year      = {2019},
  doi       = {10.1109/IWCMC.2019.8766667},
  note      = {Preprint: arXiv:1905.00265}
}

@inproceedings{sabuwala2022,
  author    = {Sabuwala, Noshin and Daruwala, Rohin D.},
  title     = {Securing Unmanned Aerial Vehicles by Encrypting {MAVLink} Protocol},
  booktitle = {2022 IEEE Bombay Section Signature Conference (IBSSC)},
  pages     = {1--6},
  year      = {2022},
  doi       = {10.1109/IBSSC56953.2022.10037546}
}

@misc{dixit2025,
  author = {Dixit, Bhavya and A., Ananthapadmanabhan and Thahsin, Adheeba and Pathak, Saketh and Kasbekar, Gaurav S. and Maity, Arnab},
  title  = {A Novel Cipher for Enhancing {MAVLink} Security: Design, Security Analysis, and Performance Evaluation Using a Drone Testbed},
  year   = {2025},
  eprint = {2504.20626},
  archivePrefix = {arXiv},
  doi    = {10.48550/arXiv.2504.20626}
}

@misc{amorim2025,
  author = {Amorim, Arthur and Taylor, Max and Kann, Trevor and Harrison, William L. and Leavens, Gary T. and Joneckis, Lance},
  title  = {Enforcing {MAVLink} Safety \& Security Properties Via Refined Multiparty Session Types},
  year   = {2025},
  eprint = {2501.18874},
  archivePrefix = {arXiv},
  url    = {https://arxiv.org/abs/2501.18874}
}

@misc{konapalli2025,
  author = {Konapalli, Yasaswini and Ben Othmane, Lotfi and Tunc, Cihan and Benchellal, Feras and Mudagere, Likhita},
  title  = {Reverse Engineering and Control-Aware Security Analysis of the {ArduPilot} {UAV} Framework},
  year   = {2025},
  eprint = {2512.01164},
  archivePrefix = {arXiv},
  url    = {https://arxiv.org/abs/2512.01164}
}

@inproceedings{kim2019rvfuzzer,
  author    = {Kim, Taegyu and Kim, Chung Hwan and Rhee, Junghwan and Fei, Fan and Tu, Zhan and Walkup, Gregory and Zhang, Xiangyu and Deng, Xinyan and Xu, Dongyan},
  title     = {{RVFuzzer}: Finding Input Validation Bugs in Robotic Vehicles through Control-Guided Testing},
  booktitle = {28th USENIX Security Symposium (USENIX Security 19)},
  pages     = {425--442},
  year      = {2019},
  url       = {https://www.usenix.org/conference/usenixsecurity19/presentation/kim}
}

@inproceedings{kim2021pgfuzz,
  author    = {Kim, Hyungsub and Ozmen, Muslum Ozgur and Bianchi, Antonio and Celik, Z. Berkay and Xu, Dongyan},
  title     = {{PGFUZZ}: Policy-Guided Fuzzing for Robotic Vehicles},
  booktitle = {Network and Distributed System Security Symposium (NDSS)},
  year      = {2021},
  doi       = {10.14722/ndss.2021.24096}
}

@inproceedings{wang2026adgfuzz,
  author    = {Wang, Yuncheng and Zheng, Yaowen and Liu, Puzhuo and Fang, Dongliang and Cheng, Jiaxing and Shi, Dingyi and Sun, Limin},
  title     = {{ADGFUZZ}: Assignment Dependency-Guided Fuzzing for Robotic Vehicles},
  booktitle = {Network and Distributed System Security Symposium (NDSS)},
  year      = {2026},
  doi       = {10.14722/ndss.2026.231014}
}

@inproceedings{zhou2026uavconfigfuzzer,
  author    = {Zhou, Yingnan and Liu, Yuhao and Zhang, Hanfeng and Jia, Yan and Xu, Sihan and Jiang, Zhiyuan and Liu, Zheli},
  title     = {{UAVConfigFuzzer}: Detecting Incorrect Configurations in Unmanned Aerial Vehicles via Setpoint Estimation Guided Fuzzing (Registered Report)},
  booktitle = {International Fuzzing Workshop (FUZZING)},
  year      = {2026},
  doi       = {10.14722/fuzzing.2026.23009}
}

@inproceedings{dash2019,
  author    = {Dash, Pritam and Karimibiuki, Mehdi and Pattabiraman, Karthik},
  title     = {Out of Control: Stealthy Attacks Against Robotic Vehicles Protected by Control-Based Techniques},
  booktitle = {Proceedings of the 35th Annual Computer Security Applications Conference (ACSAC)},
  pages     = {660--672},
  year      = {2019},
  doi       = {10.1145/3359789.3359847}
}

@article{yaacoub2020,
  author  = {Yaacoub, Jean-Paul and Noura, Hassan and Salman, Ola and Chehab, Ali},
  title   = {Security Analysis of Drones Systems: Attacks, Limitations, and Recommendations},
  journal = {Internet of Things},
  volume  = {11},
  pages   = {100218},
  year    = {2020},
  doi     = {10.1016/j.iot.2020.100218}
}

@inproceedings{nassi2021,
  author    = {Nassi, Ben and Bitton, Ron and Masuoka, Ryusuke and Shabtai, Asaf and Elovici, Yuval},
  title     = {{SoK}: Security and Privacy in the Age of Commercial Drones},
  booktitle = {2021 IEEE Symposium on Security and Privacy (SP)},
  pages     = {1434--1451},
  year      = {2021},
  doi       = {10.1109/SP40001.2021.00005}
}

@article{tsao2022,
  author  = {Tsao, Kai-Yun and Girdler, Thomas and Vassilakis, Vassilios G.},
  title   = {A Survey of Cyber Security Threats and Solutions for {UAV} Communications and Flying Ad-Hoc Networks},
  journal = {Ad Hoc Networks},
  volume  = {133},
  pages   = {102894},
  year    = {2022},
  doi     = {10.1016/j.adhoc.2022.102894}
}

@article{mekdad2023,
  author  = {Mekdad, Yassine and Aris, Ahmet and Babun, Leonardo and El Fergougui, Abdeslam and Conti, Mauro and Lazzeretti, Riccardo and Uluagac, A. Selcuk},
  title   = {A Survey on Security and Privacy Issues of {UAVs}},
  journal = {Computer Networks},
  volume  = {224},
  pages   = {109626},
  year    = {2023},
  doi     = {10.1016/j.comnet.2023.109626}
}

@inproceedings{hamza2024,
  author    = {Hamza, Muhammad Ameer and Mohsin, Mujahid and Khalil, Mohsin and Kazmi, Syed M. Kazam Abbas},
  title     = {{MAVLink} Protocol: A Survey of Security Threats and Countermeasures},
  booktitle = {2024 4th International Conference on Digital Futures and Transformative Technologies (ICoDT2)},
  pages     = {1--8},
  year      = {2024},
  doi       = {10.1109/ICoDT262145.2024.10740195}
}

@inproceedings{mansfield2013,
  author    = {Mansfield, Katrina and Eveleigh, Timothy and Holzer, Thomas H. and Sarkani, Shahryar},
  title     = {Unmanned Aerial Vehicle Smart Device Ground Control Station Cyber Security Threat Model},
  booktitle = {2013 IEEE International Conference on Technologies for Homeland Security (HST)},
  pages     = {722--728},
  year      = {2013},
  doi       = {10.1109/THS.2013.6699093}
}

@inproceedings{schiller2023,
  author    = {Schiller, Nico and Chlosta, Merlin and Schloegel, Moritz and Bars, Nils and Eisenhofer, Thorsten and Scharnowski, Tobias and Domke, Felix and Sch{\"o}nherr, Lea and Holz, Thorsten},
  title     = {Drone Security and the Mysterious Case of {DJI}'s {DroneID}},
  booktitle = {Network and Distributed System Security Symposium (NDSS)},
  year      = {2023},
  doi       = {10.14722/ndss.2023.24217}
}

% ---- Specifications, project documentation, advisories ----
@misc{mavlink_signing,
  author = {{MAVLink Development Team}},
  title  = {Message Signing (Authentication)},
  howpublished = {MAVLink Developer Guide},
  url    = {https://mavlink.io/en/guide/message_signing.html},
  note   = {Accessed 2026-11-02}
}

@misc{mavlink_serialization,
  author = {{MAVLink Development Team}},
  title  = {Packet Serialization},
  url    = {https://mavlink.io/en/guide/serialization.html},
  note   = {Accessed 2026-11-02}
}

@misc{px4_signing,
  author = {{PX4 Development Team}},
  title  = {{MAVLink} Message Signing},
  howpublished = {PX4 User Guide (main)},
  url    = {https://docs.px4.io/main/en/mavlink/message_signing.html},
  note   = {Accessed 2026-11-02}
}

@misc{px4_hardening,
  author = {{PX4 Development Team}},
  title  = {{MAVLink} Security Hardening for Production Deployments},
  url    = {https://docs.px4.io/main/en/mavlink/security_hardening.html},
  note   = {Accessed 2026-11-02}
}

@misc{px4_pr26894,
  author = {{PX4 Development Team}},
  title  = {fix(mavlink)!: align signing with {MAVLink} spec and fix performance regression ({PR} \#26894)},
  year   = {2026},
  url    = {https://github.com/PX4/PX4-Autopilot/pull/26894}
}

@misc{px4_v118,
  author = {{PX4 Development Team}},
  title  = {{PX4-Autopilot} v1.18.0 Release Notes (beta)},
  url    = {https://docs.px4.io/main/en/releases/1.18.html},
  note   = {Accessed 2026-11-02}
}

@misc{ardupilot_signing,
  author = {{ArduPilot Dev Team}},
  title  = {{MAVLink2} Signing},
  url    = {https://ardupilot.org/copter/docs/common-MAVLink2-signing.html},
  note   = {Accessed 2026-11-02}
}

@misc{mavproxy_signing,
  author = {{ArduPilot Dev Team}},
  title  = {{MAVProxy}: Packet Signing},
  url    = {https://ardupilot.org/mavproxy/docs/modules/signing.html},
  note   = {Accessed 2026-11-02}
}

@misc{qgc_telemetry,
  author = {{QGroundControl Developers}},
  title  = {Telemetry Settings ({MAVLink} 2 Signing)},
  url    = {https://docs.qgroundcontrol.com/master/en/qgc-user-guide/settings_view/telemetry.html},
  note   = {Accessed 2026-11-02}
}

@misc{cisa_icsa2609002,
  author = {{CISA}},
  title  = {{ICS} Advisory {ICSA-26-090-02}: {PX4} Autopilot ({CVE-2026-1579})},
  year   = {2026},
  url    = {https://www.cisa.gov/news-events/ics-advisories/icsa-26-090-02}
}

@misc{nvd_cve20201028x,
  author = {{NIST NVD}},
  title  = {{CVE-2020-10281}, {CVE-2020-10282}, {CVE-2020-10283} ({MAVLink})},
  year   = {2020},
  url    = {https://nvd.nist.gov/vuln/detail/CVE-2020-10283}
}

% ---- EU law ----
@misc{cra2024,
  author = {{European Parliament and Council of the EU}},
  title  = {Regulation ({EU}) 2024/2847 on horizontal cybersecurity requirements for products with digital elements (Cyber Resilience Act)},
  year   = {2024},
  howpublished = {OJ L, 2024/2847, 20.11.2024},
  url    = {https://eur-lex.europa.eu/eli/reg/2024/2847/oj/eng}
}

@misc{cra_impl2025_2392,
  author = {{European Commission}},
  title  = {Commission Implementing Regulation ({EU}) 2025/2392 on the technical description of the categories of important and critical products with digital elements},
  year   = {2025},
  howpublished = {OJ L, 2025/2392, 1.12.2025},
  url    = {https://eur-lex.europa.eu/eli/reg_impl/2025/2392/oj/eng}
}

@misc{uas2019_945,
  author = {{European Commission}},
  title  = {Commission Delegated Regulation ({EU}) 2019/945 on unmanned aircraft systems and on third-country operators of unmanned aircraft systems},
  year   = {2019},
  url    = {https://eur-lex.europa.eu/eli/reg_del/2019/945/oj}
}

@misc{red2022_30,
  author = {{European Commission}},
  title  = {Commission Delegated Regulation ({EU}) 2022/30 supplementing Directive 2014/53/{EU} with regard to Article 3(3)(d), (e) and (f)},
  year   = {2022},
  url    = {https://eur-lex.europa.eu/eli/reg_del/2022/30/oj}
}

@misc{red2026_339,
  author = {{European Commission}},
  title  = {Commission Delegated Regulation ({EU}) 2026/339 repealing Delegated Regulation ({EU}) 2022/30},
  year   = {2026},
  url    = {https://eur-lex.europa.eu/eli/reg_del/2026/339/oj/eng}
}

@misc{droneplan2026,
  author = {{European Commission}},
  title  = {Action Plan on Drone and Counter Drone Security, {COM}(2026) 81 final},
  year   = {2026},
  month  = feb,
  url    = {https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:52026DC0081}
}
```

### Items deliberately excluded
- Papers whose bibliographic details I could not confirm. One is a 2025 Authorea preprint on post-quantum MAVLink: its DOI was found but its content was not reviewed, so it is omitted.
- Venue and pages for Domin et al. (2016) are not given, because they were not confirmed.
