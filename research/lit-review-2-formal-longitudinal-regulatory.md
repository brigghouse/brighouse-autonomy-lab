# Literature Review 2: Formal Verification, Longitudinal Measurement, Regulatory Crosswalks

**Programme:** Defensive MAVLink drone-link security (Brighouse Security Labs, Spain)
**Author of this review:** Ian Brighouse (compiled with tool-assisted search)
**Date:** 2026-11-02
**Scope:** Three research questions (Q1 formal/symbolic verification, Q2 longitudinal measurement of security defaults, Q3 regulatory-technical crosswalks), plus venue and IEEEtran notes.

**Verification method.** Every bibliographic entry below was checked on 2026-11-02 against at least one authoritative source: Crossref metadata (DOI resolution), OpenAlex (abstracts), arXiv abstract pages, Springer/USENIX/NDSS/ePrint landing pages, or the primary git history of ArduPilot and PX4 (partial clones, `git log`/`git tag --contains`). Items that could not be fully confirmed are tagged `[VERIFY]` with the reason. Nothing was invented; where a search returned nothing, that negative result is recorded as gap evidence.

**Searches run (for gap evidence).** WebSearch (extended mode) and WebFetch over arXiv, IEEE Xplore (via Crossref/OpenAlex, since Xplore blocks fetches), ACM DL, Springer, ScienceDirect, USENIX, NDSS, IACR ePrint, EUR-Lex, GitHub, Dronecode/ArduPilot forums. Query families: `MAVLink + {ProVerif, Tamarin, CryptoVerif, EasyCrypt, TLA+, Alloy, model checking, formal}`; `MAVLink signing + {formal, symbolic, SETUP_SIGNING, timestamp, link id, TOFU}`; `drone C2 + {formal verification, Scyther, AVISPA}`; `Remote ID / ASTM F3411 + formal`; `DJI + protocol analysis`; `SecOC / CAN / AUTOSAR + Tamarin`; `Bluetooth Just Works + formal`; `SSH / TOFU + formal`; `Matter commissioning + formal`; `model-based testing / conformance / automata learning + PX4 / ArduPilot / MAVLink`; `longitudinal + {security defaults, secure by default, TLS, Android permissions, firmware, Linux hardening, ROS, PX4, ArduPilot}`; `CRA Annex I + mapping`; `EN 18031 + research`; `2019/945 + cybersecurity`; `DO-326A + UAS`; `ISO 21434 / R155 + mapping`; `Trusted Drone label`; `COM(2026) 81 / Drone Security Package`.

---

## Q1. Formal / symbolic verification of MAVLink 2 signing and drone C2 key provisioning

### Q1(a) Verified references (most relevant first)

| # | Reference | What it does | Relevance to our gap |
|---|-----------|--------------|----------------------|
| 1 | T. Wray and Y. Wang, "PAVE-MAVLink: Formal Verification of MAVLink 2 for Secure UAV Communications," *MILCOM 2025*, Los Angeles, Oct. 2025. DOI 10.1109/MILCOM64451.2025.11310743. | LLM-generated nuXmv + ProVerif models of MAVLink 2; shows command injection without crypto; adds ChaCha20 encryption; validates in SITL and OTA. | **Closest prior work.** Per the abstract, the model covers MAVLink 2 *without* cryptographic protection and then a ChaCha20 *extension*; it does not claim to model the native signing scheme (sha256_48 tag, 48-bit timestamp, link id, SETUP_SIGNING). `[VERIFY: full text not accessible; confirm the native signing is absent from the model]` |
| 2 | B. Mak, J. Yang, J. Chen, P. Ratazzi, and Y. Wang, "Symbolic and Safety-Centric Formal Verification of MAVLink for Autonomous eVTOL Systems," *IEEE Networking Letters*, Dec. 2025. DOI 10.1109/LNET.2025.3610580. | Formal model of MAVLink behaviour under eVTOL constraints; claims "first work to formally analyze MAVLink in a safety-critical eVTOL setting"; proposes "formally guided cryptographic mitigation strategies." | Same Stevens group. Abstract frames MAVLink as lacking authentication; signing is not mentioned as modelled. `[VERIFY: full text]` |
| 3 | A. Amorim, M. Taylor, T. Kann, W. L. Harrison, G. T. Leavens, and L. Joneckis, "Enforcing MAVLink Safety & Security Properties via Refined Multiparty Session Types," *NASA Formal Methods (NFM 2025)*, LNCS, Springer, 2025. DOI 10.1007/978-3-031-93706-4_1. arXiv:2501.18874. | DATUM: refined multiparty session types to specify legal MAVLink message *sequences*; runtime enforcement; targets stealthy "valid message, wrong time" attacks. | Formal, MAVLink-specific, but about message ordering/semantics, not cryptographic authentication or key provisioning. |
| 4 | A. Amorim, P. Gazzillo, M. Taylor, and L. Joneckis, "From High-Level Types to Low-Level Monitors: Synthesizing Verified Runtime Checkers for MAVLink," *NFM 2026*, LNCS vol. 16622, Springer, 2026. DOI 10.1007/978-3-032-28079-4_5. arXiv:2604.03886. | Platum: Meta-F* checked DSL compiled to allocation-free C monitors; evaluated in ArduPilot SITL. | Shows a verified-artifact + SITL evaluation pipeline for MAVLink; still no signing/key model. |
| 5 | M. Alam, M. Alhashmi, M. Atrouz, A. Khader, R. A. Pashchapur, and A. Shoufan, "Authentication Protocols for UAV remote identification using public-key infrastructure," *Computers & Security*, vol. 171, art. 105075, Dec. 2026. DOI 10.1016/j.cose.2026.105075. | Two ASTM F3411-22a-compliant Broadcast Remote ID authentication designs; **Tamarin** proofs (Dolev-Yao) of key secrecy, integrity, token authenticity; injective agreement *not* provable (physical-source binding). | Direct template: Tamarin applied to an ASTM drone standard, with a prototype. Adjacent protocol (Remote ID), not C2. |
| 6 | N. Schiller, M. Chlosta, M. Schloegel, N. Bars, T. Eisenhofer, T. Scharnowski, F. Domke, L. Schönherr, and T. Holz, "Drone Security and the Mysterious Case of DJI's DroneID," *NDSS 2023*. DOI 10.14722/ndss.2023.24217. | Reverse-engineering of DJI OcuSync/DroneID; fuzzing of firmware; finds DroneID unencrypted/spoofable. | DJI adjacent protocol. Empirical, no symbolic model. |
| 7 | J. Wu, R. Wu, D. Xu, D. (J.) Tian, and A. Bianchi, "Formal Model-Driven Discovery of Bluetooth Protocol Design Vulnerabilities," *IEEE S&P 2022*. DOI 10.1109/SP46214.2022.9833777. | ProVerif model of BT Classic/BLE/Mesh incl. **Just Works**; 418 properties, 82 violations; Just Works violates both authenticity properties (MITM). | Template for modelling an "unauthenticated pairing" mode, analogous to SETUP_SIGNING over an untrusted link. |
| 8 | M. K. Jangid, Y. Zhang, and Z. Lin, "Extrapolating Formal Analysis to Uncover Attacks in Bluetooth Passkey Entry Pairing," *NDSS 2023*. DOI 10.14722/ndss.2023.23119. | Tamarin models of Numeric Comparison and Passkey Entry. | Template for Tamarin pairing models; Just Works not modelled. |
| 9 | S. Duttagupta, A. Kolozyan, G. Nicolas, D. Singelee, and B. Preneel, "What's the Matter? An In-Depth Security Analysis of the Matter Protocol," IACR ePrint 2025/1268 (to appear *IEEE S&P 2027*). | ProVerif analysis of Matter PASE/CASE/CASE-Resumption (device commissioning). | Closest "IoT key-provisioning/commissioning" formal analysis; shows what a provisioning analysis for drones should look like. `[VERIFY: S&P 2027 acceptance stated on ePrint page; confirm at publication]` |
| 10 | C. Bodei, M. De Vincenzi, and I. Matteucci, "Formal analysis of an AUTOSAR-based basic software module," *Int. J. Softw. Tools Technol. Transf.*, vol. 26, pp. 495-508, 2024. DOI 10.1007/s10009-024-00759-w. | Tamarin model of CINNAMON (confidentiality extension of AUTOSAR SecOC) on CAN. | Automotive analogue: MAC-authenticated bus messages with freshness values; closest to MAVLink's MAC+timestamp design. |
| 11 | D. Zelle, T. Lauser, D. Kern, and C. Krauß, "Analyzing and Securing SOME/IP Automotive Services with Formal and Practical Methods," *ARES 2021*. DOI 10.1145/3465481.3465748. | Tamarin + practical attacks on SOME/IP; proposes authenticated variant. | Pattern "formal model + practical validation" for an automotive C2-like protocol. |
| 12 | D. Jackson, C. Cremers, K. Cohn-Gordon, and R. Sasse, "Seems Legit: Automated Analysis of Subtle Attacks on Protocols that Use Signatures," *ACM CCS 2019*. DOI 10.1145/3319535.3339813. | Finer-grained symbolic models of signature schemes (key substitution, malleability, etc.) in Tamarin. | Methodological guidance for modelling a *truncated* MAC tag and non-standard primitives faithfully. |
| 13 | D. Basin, J. Dreier, L. Hirschi, S. Radomirović, R. Sasse, and V. Stettler, "A Formal Analysis of 5G Authentication," *ACM CCS 2018*. DOI 10.1145/3243734.3243846. | Tamarin model of 5G AKA derived from the 3GPP standard text; finds underspecification. | Template for "standard text to Tamarin model" with explicit assumptions; same style we need for mavlink.io signing spec. |
| 14 | C. Cremers, M. Horvat, J. Hoyland, S. Scott, and T. van der Merwe, "A Comprehensive Symbolic Analysis of TLS 1.3," *ACM CCS 2017*. DOI 10.1145/3133956.3134063. | Tamarin TLS 1.3 model incl. PSK/resumption modes. | Template for modelling pre-shared-key modes and multi-session state (analogous to per-stream timestamp state). |
| 15 | M. Barbosa, G. Barthe, K. Bhargavan, B. Blanchet, C. Cremers, K. Liao, and B. Parno, "SoK: Computer-Aided Cryptography," *IEEE S&P 2021*. DOI 10.1109/SP40001.2021.00008. | Survey of symbolic vs computational tools (ProVerif, Tamarin, CryptoVerif, EasyCrypt). | Tool selection justification. |

Supporting / adjacent (verified):

- MAVLink signing specification (primary source): "Message Signing (Authentication)," mavlink.io/en/guide/message_signing.html. Facts confirmed 2026-11-02: 13-byte trailer = link id (8 b) + timestamp (48 b, 10 µs units since 2015-01-01) + sha256_48(secret_key ‖ header ‖ payload ‖ CRC ‖ link id ‖ timestamp); 32-byte key; SETUP_SIGNING carries the key and "should only be sent over a secure link (USB/wired Ethernet)"; replay window 1 min; accept-unsigned rules "implementation specific."
- S. Card, A. Wiethuechter, R. Moskowitz, and A. Gurtov, "Drone Remote Identification Protocol (DRIP) Requirements and Terminology," RFC 9434, IETF, 2023. (DRIP authentication formats: draft-ietf-drip-auth, later published as an RFC `[VERIFY RFC number]`.)
- Y. Kwon, J. Yu, B. Cho, Y. Eun, and K. Park, "Empirical Analysis of MAVLink Protocol Vulnerability for Attacking Unmanned Aerial Vehicles," *IEEE Access*, vol. 6, 2018. DOI 10.1109/ACCESS.2018.2863237. (Empirical, not formal.)
- A. Allouch, O. Cheikhrouhou, A. Koubâa, M. Khalgui, and T. Abbes, "MAVSec: Securing the MAVLink Protocol for Ardupilot/PX4 Unmanned Aerial Systems," *IWCMC 2019*. DOI 10.1109/IWCMC.2019.8766667. (Encryption add-on; no formal model.)
- M. Hamza, M. Mohsin, M. Khalil, and S. K. A. Kazmi, "MAVLink Protocol: A Survey of Security Threats and Countermeasures," *ICoDT2 2024*. DOI 10.1109/ICoDT262145.2024.10740195. (Survey; lists no formal analysis of signing.)
- I. Hughes, A. Pupo, J. Wynd, Z. Thurlow, C. Ivancik, and Y. Wang, "Securing the Unprotected: Enhancing Heartbeat Messaging for MAVLink UAV Communications," *IEEE PACRIM 2024*. DOI 10.1109/PACRIM61180.2024.10690216.
- NIST, "FormalModelsOfOnboardingProtocols" (GitHub, usnistgov; archived 2026-06-12): ProVerif/AVISPA models of BRSKI, DPP, EAP-TLS onboarding. Companion to NIST SP 1800-36 `[VERIFY: no paper named in repo]`.
- Model-based testing / fuzzing of flight stacks (not conformance testing from a protocol model): H. Kim, M. O. Ozmen, A. Bianchi, Z. B. Celik, and D. Xu, "PGFUZZ: Policy-Guided Fuzzing for Robotic Vehicles," *NDSS 2021*, DOI 10.14722/ndss.2021.24096; T. Kim et al., "RVFuzzer: Finding Input Validation Bugs in Robotic Vehicles through Control-Guided Testing," *USENIX Security 2019* `[VERIFY author list]`; "ADGFUZZ: Assignment Dependency-Guided Fuzzing for Robotic Vehicles," *NDSS 2026* `[VERIFY authors]`; "UAVConfigFuzzer," NDSS Fuzzing Workshop 2026 `[VERIFY authors]`.

### Q1(b) Synthesis

Formal work on MAVLink exists but is thin and recent (2025-2026) and comes from two groups. The Stevens/AFRL group (Wray & Wang, MILCOM 2025; Mak et al., IEEE Netw. Lett. 2025) builds LLM-assisted nuXmv/ProVerif models of MAVLink 2 to show that the *unprotected* protocol admits command injection, then verifies an added ChaCha20 encryption layer; their framing treats MAVLink as "lacking standardized encryption and authentication" and does not engage with the signing mechanism that has shipped in the specification since 2016. The UCF/Boise/INL group (Amorim et al., NFM 2025/2026) uses refined multiparty session types and Meta-F* to enforce *legal message sequences* and compiles verified runtime monitors tested in ArduPilot SITL; this is about semantics and ordering, not cryptographic authentication or key management. Adjacent domains provide mature templates: Tamarin for ASTM F3411 Remote ID authentication (Alam et al., 2026), ProVerif/Tamarin for Bluetooth pairing including the unauthenticated Just Works mode (Wu et al., S&P 2022; Jangid et al., NDSS 2023), ProVerif for Matter device commissioning (Duttagupta et al., S&P 2027), Tamarin for AUTOSAR SecOC-style MAC+freshness on CAN (Bodei et al., 2024) and SOME/IP (Zelle et al., 2021), and the standards-to-model methodology of 5G AKA and TLS 1.3 (Basin et al., 2018; Cremers et al., 2017). Fuzzing of PX4/ArduPilot is well developed (RVFuzzer, PGFuzz, ADGFuzz), but all of it is property- or policy-guided input mutation, not test derivation from an explicit protocol model.

### Q1(c) The gap (with search evidence)

**Nobody has produced a symbolic (or computational) model of the MAVLink 2 signing scheme as specified: the sha256_48 truncated tag, the 48-bit per-(sysid, compid, linkid) monotonic timestamp with a one-minute replay window, the link-id channel binding, the implementation-specific accept-unsigned rules, and SETUP_SIGNING key provisioning with its trust-on-first-use character over an unauthenticated link.** Searches for `MAVLink` combined with `Tamarin`, `ProVerif`, `CryptoVerif`, `EasyCrypt`, `TLA+`, `Alloy`, `SETUP_SIGNING`, `trust on first use` returned only the two Stevens papers (which model the protocol without its native authentication and then verify an encryption add-on) and the session-type work (no cryptography). No Tamarin/ProVerif model of any drone C2 key-provisioning flow was found; the nearest analogues are Remote ID (broadcast, PKI-based, not C2) and Matter/Bluetooth commissioning. **Likewise, no model-based conformance testing of flight stacks exists:** searches for `model-based testing`, `conformance`, `automata learning`, `protocol state fuzzing`, `LearnLib` with `PX4`, `ArduPilot`, `MAVLink` returned only fuzzers (RVFuzzer, PGFuzz, ADGFuzz, UAVConfigFuzzer) and the Platum SITL evaluation; none derive test sequences from a protocol/signing model and check PX4 and ArduPilot implementations against it. Given that PX4 only merged signing in March 2026 (see Q2) and immediately needed a "align signing with MAVLink spec" fix, a model-derived conformance suite run against both stacks is both novel and timely.

---

## Q2. Longitudinal / historical measurement of security defaults in open-source robotic or embedded stacks

### Q2(a) Verified references

Methodological templates from other domains:

| # | Reference | Longitudinal design |
|---|-----------|---------------------|
| 1 | P. Kotzias, A. Razaghpanah, J. Amann, K. G. Paterson, N. Vallina-Rodriguez, and J. Caballero, "Coming of Age: A Longitudinal Study of TLS Deployment," *ACM IMC 2018*. DOI 10.1145/3278532.3278568. | 6-year passive measurement of TLS versions/ciphers; shows how defaults shift after disclosures. |
| 2 | X. Wei, L. Gomez, I. Neamtiu, and M. Faloutsos, "Permission Evolution in the Android Ecosystem," *ACSAC 2012*. DOI 10.1145/2420950.2420956. | Builds/examines successive Android releases to track permission defaults over time. |
| 3 | J. Walden, "The Impact of a Major Security Event on an Open Source Project: The Case of OpenSSL," *MSR 2020*. DOI 10.1145/3379597.3387465. | Before/after Heartbleed longitudinal analysis of OpenSSL code and process metrics. |
| 4 | F. Li and V. Paxson, "A Large-Scale Empirical Study of Security Patches," *ACM CCS 2017*. DOI 10.1145/3133956.3134072. | Multi-year study of patch latency across OSS projects. |
| 5 | R. Yu, F. Del Nin, Y. Zhang, S. Huang, P. Kaliyar, S. Zakto, M. Conti, G. Portokalidis, and J. Xu, "Building Embedded Systems Like It's 1996," *NDSS 2022*. DOI 10.14722/ndss.2022.24031. | Measures adoption of exploit mitigations in embedded firmware across vendors and years. `[VERIFY: full author list]` |
| 6 | N. Nino, R. Lu, W. Zhou, K. H. Lee, Z. Zhao, and L. Guan, "Unveiling IoT Security in Reality: A Firmware-Centric Journey," *USENIX Security 2024*. | 8,432 MCU firmware images; protections and mitigations rarely adopted (cross-sectional, not longitudinal). |
| 7 | Y. Wu et al., "Your Firmware Has Arrived: A Study of Firmware Update Vulnerabilities," *USENIX Security 2024*. `[VERIFY author list]` | Firmware-update security across devices. |
| 8 | A. Costin, J. Zaddach, A. Francillon, and D. Balzarotti, "A Large-Scale Analysis of the Security of Embedded Firmwares," *USENIX Security 2014*. `[VERIFY: no DOI; USENIX]` | Baseline large-scale firmware security measurement. |
| 9 | J. Ruohonen, "SoK: The design paradigm of safe and secure defaults," *J. Inf. Secur. Appl.*, 2025. DOI 10.1016/j.jisa.2025.103989. arXiv:2412.17329. | Systematic mapping of the "secure defaults" principle; notes IoT drove the post-2015 surge. |

Robotics / UAV specific:

| # | Reference | Content |
|---|-----------|---------|
| 10 | N. DeMarinis, S. Tellex, V. P. Kemerlis, G. Konidaris, and R. Fonseca, "Scanning the Internet for ROS: A View of Security in Robotics Research," *ICRA 2019*. DOI 10.1109/ICRA.2019.8794451. | Internet-wide scans 2017-2018 for exposed ROS masters. |
| 11 | W. Chen, S. Der, Y. Luo, F. Alshammari, and Q. A. Chen, "Understanding the Internet-Wide Vulnerability Landscape for ROS-based Robotic Vehicles," *VehicleSec 2024* (NDSS). DOI 10.14722/vehiclesec.2024.23018. | Repeats DeMarinis six years later: exposed hosts +60%; honeypots. Only robotics "longitudinal" security measurement found; measures *exposure*, not stack defaults. |
| 12 | D. Wang, S. Li, G. Xiao, Y. Liu, and Y. Sui, "An Exploratory Study of Autopilot Software Bugs in Unmanned Aerial Vehicles," *ESEC/FSE 2021*. DOI 10.1145/3468264.3468559. | 569 bugs mined from PX4 and ArduPilot histories; taxonomy; not security-default focused. |
| 13 | M. Taylor, J. Boubin, H. Chen, C. Stewart, and F. Qin, "A Study on Software Bugs in Unmanned Aircraft Systems," *ICUAS 2021*. DOI 10.1109/ICUAS51884.2021.9476844. | Bug study on PX4/ArduPilot issue trackers. |
| 14 | B. Breiling, B. Dieber, and P. Schartner, "Secure communication for the robot operating system," *IEEE SysCon 2017*. DOI 10.1109/SYSCON.2017.7934755. | Early ROS 1 security retrofit. |
| 15 | V. Mayoral-Vilches, R. White, G. Caiazza, and M. Arguedas, "SROS2: Usable Cyber Security Tools for ROS 2," *IROS 2022*. DOI 10.1109/IROS47612.2022.9982129. | ROS 2 security tooling; documents DDS-Security off-by-default. |
| 16 | S. Macenski, T. Foote, B. Gerkey, C. Lalancette, and W. Woodall, "Robot Operating System 2: Design, architecture, and uses in the wild," *Science Robotics*, vol. 7, 2022. DOI 10.1126/scirobotics.abm6074. | ROS 2 architecture incl. security design decisions. |

Primary-source milestones (verified from git history on 2026-11-02; cite as software/repository references):

**ArduPilot (github.com/ArduPilot/ardupilot):**
- 2016-01-12: `f6511e8337` "build: added mavlink2 build option" (Andrew Tridgell).
- **2016-01-21: `ed9a43ca46` "GCS_MAVLink: support for mavlink2 signing operations" (Andrew Tridgell)**, plus same-day commits adding SETUP_SIGNING handling to Plane/Copter/Rover/Tracker and a StorageManager region for signing keys.
- First stable release tags containing the signing commit: **ArduPlane 3.6.0 (2016-06-11)**, **ArduPlane 3.7.0 (2016-09-09)**, **Copter 3.4.0 (2016-10-31)**, **APMrover2 3.1.0 (2016-12-22)**. (Copter 3.3.x does not contain it.)
- 2016-09-16: `c64a020384` "GCS_MAVLink: default to MAVLink2 enabled"; **reverted 2016-10-21** (`d2e4b73eda`).
- 2018-07-18: `75c5fda222` "AP_SerialManager: make console do mavlink2 by default" (first in Plane 3.9.0).
- **2020-06-25: `211c20da38` "AP_SerialManager: default serial 1 and 2 protocols to MAVLink2"** (first in Copter 4.1.0 / Plane 4.1.0).
- Signing itself remains opt-in (no key by default; key must be provisioned via SETUP_SIGNING / GCS UI) through the current master. ArduPilot docs page "MAVLink2 Signing" (ardupilot.org) confirms USB is unaffected and MAVLink 1 ports are unprotected.
- 2019-01 issue #10298: "Setup signing works over mavlink 1 when it is not supposed to" (fixed by #10311) `[VERIFY merge date]`.

**PX4 (github.com/PX4/PX4-Autopilot):**
- 2020-07-30 forum thread "Mavlink Signing Support for PX4": no support; 2021-07-31 H. Kim points to branch `pr-mavlink_signing` (PR #17084 lineage) that was never merged.
- **2026-03-09: `358574f9f6` "feat(mavlink): mavlink signing support (#25284)"** (author yulianoifa-mobius); stores key as a file on the vehicle; bidirectional signing.
- 2026-03-12: `400bb253bd` "docs(mavlink): security hardening guide for production deployments (#26730)".
- **2026-04-12: `62b3c9a063` "fix(mavlink)!: align signing with MAVLink spec and fix performance regression (#26894)"** (breaking fix one month after merge; reviewer notes original doc wrongly claimed HMAC-SHA256).
- 2026-04-27 #27222 (don't write empty key file on shutdown); 2026-09-21 `f5586139e4` "feat(security): define security scope (#28571)" (Julian Oes; presents link encryption alongside signing); 2026-10-13 #29164 (signed frame fits send buffer); 2026-10-29 #28697 (signing races); 2026-10-31 #29488 (accept unsigned ADSB/COLLISION only on traffic-receiver links; PR text: "Signing first ships in 1.18").
- Release tags containing signing: v1.18.0-alpha1, -beta1, -beta2, **-rc1** (no final v1.18.0 tag as of 2026-11-02). Ten-year lag between ArduPilot (2016) and PX4 (2026).

Academic citations of these milestones: searches found **no** peer-reviewed paper citing the ArduPilot 2016 signing commit/release or the PX4 2026 merge as dated milestones. Kwon et al. (2018) and Hamza et al. (2024) mention MAVLink 2 signing generically; MAVSec (2019) states PX4/ArduPilot lack encryption; none give version history.

### Q2(b) Synthesis

Longitudinal "defaults" measurement is an established genre outside robotics: TLS deployment over six years (Kotzias et al.), Android permission defaults across releases (Wei et al.), OpenSSL before/after Heartbleed (Walden), patch latency across OSS (Li & Paxson), and adoption of exploit mitigations in embedded firmware across vendors and years (Yu et al.; Nino et al.; Costin et al.). Ruohonen's 2025 SoK systematises the "secure by default" principle and notes its IoT-driven rise after 2015 but does not measure any codebase. In robotics the only repeated measurement is Internet exposure of ROS masters (DeMarinis 2019, repeated by Chen et al. 2024), which measures deployments, not the defaults shipped by the stacks. Software-engineering studies of PX4/ArduPilot (Wang et al. FSE 2021; Taylor et al. ICUAS 2021) mine bug histories but ignore security configuration. The primary-source record (verified from git) is rich and unexploited: ArduPilot implemented signing in January 2016 and shipped it in Plane 3.6.0/Copter 3.4.0 that year, flipped MAVLink2 default on, reverted it, and only made it default on telemetry ports in 2020 (4.1); signing has never been on by default. PX4 had no signing until a March 2026 merge targeting v1.18, followed within weeks by a breaking spec-alignment fix and a series of race/buffer/allowlist fixes through October 2026.

### Q2(c) The gap (with search evidence)

**No study builds a sequence of PX4 and ArduPilot (or ROS/MAVLink library) releases over a decade and measures how security-relevant defaults evolved**: MAVLink 1 vs 2 default per port, signing availability and default state, accept-unsigned allowlists, key storage/persistence, timestamp persistence, USB/"secure channel" exemptions, parameter exposure of keys, and the time from upstream spec change to each stack's conformance. Searches for `longitudinal`/`evolution`/`across versions` combined with `PX4`, `ArduPilot`, `MAVLink`, `ROS`, `security defaults`, `secure by default` returned only exposure scans (ROS), bug taxonomies (FSE 2021, ICUAS 2021), and cross-sectional firmware studies. No paper cites the dated milestones above; the PX4 2026 signing history (merge, spec-alignment fix, v1.18 release-candidate status) has not yet appeared in any publication. A "ten-year secure-defaults timeline of open-source flight stacks," built by compiling tagged releases in SITL and probing behaviour with the Q1 conformance suite, would be the first such measurement in robotics and would directly feed the CRA "secure by default" evidence problem in Q3.

---

## Q3. Regulatory-technical crosswalks as research contributions

### Q3(a) Verified references

Academic crosswalks:

| # | Reference | Content |
|---|-----------|---------|
| 1 | J. Ruohonen, E.-Y. Kang, and Q. Ramadan, "An Alignment Between the CRA's Essential Requirements and the ATT&CK's Mitigations," *IEEE RE Workshops (REW) 2025*. DOI 10.1109/REW66121.2025.00033. arXiv:2505.13641. | Maps CRA Annex I essential requirements to MITRE ATT&CK mitigations; identifies gaps both ways. Only published Annex I-to-technical-framework mapping found. |
| 2 | J. Ruohonen, K. Hjerppe, and E.-Y. Kang, "A Mapping Analysis of Requirements Between the CRA and the GDPR," *IEEE REW 2025*. DOI 10.1109/REW66121.2025.00034. arXiv:2503.01816. | Legal-to-legal requirements mapping (CRA vs GDPR). |
| 3 | J. Ruohonen and P. Timmers, "Vulnerability Coordination under the Cyber Resilience Act," *Applied Cybersecurity & Internet Governance*, 2025. DOI 10.60097/ACIG/213350. arXiv:2412.06261. | CRA vulnerability-handling obligations. |
| 4 | J. Ruohonen, "SoK: The design paradigm of safe and secure defaults," *JISA*, 2025. DOI 10.1016/j.jisa.2025.103989. | Concept basis for "secure by default" (CRA Annex I Part I(2)(b)-style obligations). |
| 5 | A. Puliyski, A. Stefanova, and V. Serbezov, "The regulatory illusion of security in drone operations in the specific category: An analysis of the gaps between regulatory compliance and actual cyber resilience within the SORA," *Transportation Research Procedia*, vol. 91, pp. 91-98, 2025. DOI 10.1016/j.trpro.2025.10.013. | Scores a SORA-compliant delivery scenario (SAIL I-III) against five cyber-resilience criteria; argues compliance does not imply resilience. Closest drone regulation-vs-technical gap analysis; qualitative scoring, no protocol-level properties. |
| 6 | M. Huttunen, "Civil unmanned aircraft systems and security: The European approach," *J. Transp. Secur.*, 2019. DOI 10.1007/s12198-019-00203-0. | Legal analysis of 2019/945 and 2019/947 security provisions. |
| 7 | G. Costantino, M. De Vincenzi, and I. Matteucci, "A Comparative Analysis of UNECE WP.29 R155 and ISO/SAE 21434," *IEEE EuroS&PW 2022*. DOI 10.1109/EuroSPW55150.2022.00041. | Regulation-to-standard crosswalk applied to a TPMS case study (automotive template). |
| 8 | F. Siddiqui, A. Ahlbrecht, R. Khan, S. Tasdemir, H. Hui, B. Sonigara, S. Sezer, K. McLaughlin, and W. Dürr, "Cybersecurity Engineering: Bridging the Security Gaps in Avionics Architectures and DO-326A/ED-202A," *IEEE/AIAA DASC 2023*. DOI 10.1109/DASC58513.2023.10311187. `[VERIFY full author list]` | Maps DO-326A/ED-202A process to concrete avionics architecture controls. |
| 9 | C. Torens, "Safety Versus Security in Aviation, Comparing DO-178C with Security Standards," *AIAA SciTech 2020*. DOI 10.2514/6.2020-0242. | DO-178C vs DO-326A/ED-202A set comparison. |
| 10 | P. Emami-Naeini, Y. Agarwal, L. F. Cranor, and H. Hibshi, "Ask the Experts: What Should Be on an IoT Privacy and Security Label?," *IEEE S&P 2020*. DOI 10.1109/SP40000.2020.00043. | Evidence-based label design; template for a "Trusted Drone" label study. |
| 11 | F. Körner, "Current challenges of implementing ETSI EN 303 645 as a baseline security standard for consumer IoT security certification," TechRxiv, 2023. DOI 10.36227/techrxiv.24711672. `[VERIFY: preprint only]` | Practitioner view of conformance evidence for EN 303 645. |
| 12 | L. Jiang, H. Wen, H. Wu, and F. Zhu, "Research on Airworthiness Regulations and Standards for Aircraft Security," ACM ICNCC 2025. DOI 10.1145/3776942.3777003. `[VERIFY relevance: short survey]` | Survey of airworthiness security regs. |

Primary legal/standards sources (cite as official documents):

- Regulation (EU) 2024/2847 (Cyber Resilience Act), OJ L, 20 Nov 2024; Annex I Part I (product properties, incl. "secure by default configuration," protection against unauthorised access, integrity of data/commands, confidentiality) and Part II (vulnerability handling). Full application 11 Dec 2027 (confirmed by COM(2026) 81 wording "December 2027").
- Commission Delegated Regulation (EU) 2022/30 (RED Art. 3(3)(d)(e)(f)); harmonised standards EN 18031-1/-2/-3:2024 (listed in OJ Jan 2025 with restrictions) `[VERIFY OJ reference]`; applicability 1 Aug 2025.
- Commission Delegated Regulation (EU) 2019/945 (UAS and third-country operators) and Implementing Regulation (EU) 2019/947; class-marking Annex Part 1-17; direct remote identification requirements.
- Directive (EU) 2022/2555 (NIS2).
- ISO/SAE 21434:2021 (road vehicles cybersecurity engineering); UNECE R155.
- IEC 62443-4-2:2019 (component requirements) and 62443-4-1:2018 (secure development lifecycle).
- RTCA DO-326A / EUROCAE ED-202A (Airworthiness Security Process Specification), with DO-356A/ED-203A methods.
- ETSI EN 303 645 V2.1.1 (2020) / V3.1.3 (2024) consumer IoT baseline `[VERIFY edition]`; ETSI TR 103 621 guide.
- ASTM F3411-22a (Remote ID); RFC 9434 (DRIP requirements).
- **European Commission, "Action Plan on Drone and Counter-Drone Security," COM(2026) 81 final, Brussels, 11 Feb 2026** (EUR-Lex CELEX 52026DC0081). Verified content: Sec. 2.2.1 "EU Trusted Drone Label" relying on independent third-party verification, to be developed with Member States **by Q4 2026**, explicitly not duplicating existing EU cyber law; CRA will cover most drones from Dec 2027; "trusted chips" recommendation; coordinated Union-wide drone/counter-drone security risk assessment by Q3 2026 (toolbox); **Drone Security Package by Q3 2026** (registration and direct remote ID above 100 g; no take-off without operator ID); sovereign European C2 capacities with "state-of-the-art encryption" (Sec. 4.3); geofencing technical requirements in 2027.
- Council doc ST 6262/2026 INIT (transmission of COM(2026) 81).

Follow-ups since Feb 2026 (searched 2026-11-02):
- Trusted Drone Label: a Deloitte-led consortium ran a first expert workshop (reported Dronewatch Europe, 5 Feb 2026) with proposed criteria: resistance to hacking/takeover/spoofing, secure design and lifecycle, **end-to-end encrypted communications**, controlled software/firmware update behaviour, supply-chain transparency, EU data handling, GNSS jamming/spoofing resilience. No official criteria document, consultation, or Commission implementing text was found as of 2026-11-02 `[VERIFY: check DG DEFIS / digital-strategy pages for a Q4 2026 publication]`.
- Drone Security Package: **no legislative proposal located** on EUR-Lex or Commission transport/digital pages as of 2026-11-02; the Q3 2026 target appears to have slipped or the proposal is not yet published `[VERIFY: re-check EUR-Lex for amendments to 2019/945 and 2019/947]`.
- Non-binding CER guidelines on drone resilience (Q2 2026), D-TECT forum (Q2 2026), counter-drone performance Recommendation (Q4 2026): not independently located `[VERIFY]`.

### Q3(b) Synthesis

Regulatory-technical crosswalks are an accepted contribution type, but almost all published examples are standard-to-standard or regulation-to-framework at the *process* level: CRA to ATT&CK mitigations and CRA to GDPR (Ruohonen et al., 2025, both at RE workshops), R155 to ISO/SAE 21434 (Costantino et al., 2022), DO-326A/ED-202A to avionics architecture controls (Siddiqui et al., 2023; Torens, 2020), and SORA compliance to qualitative resilience criteria for drones (Puliyski et al., 2025). The drone-specific legal literature (Huttunen, 2019) predates the CRA and the RED delegated act. Evidence-oriented work on "secure by default" exists conceptually (Ruohonen SoK, 2025) and for labelling (Emami-Naeini et al., 2020; EN 303 645 practitioner reports), but the mapping stops at requirement text and does not reach down to measurable protocol properties. Policy is moving faster than the literature: the CRA applies fully in December 2027, EN 18031 has been applicable under the RED since August 2025, and COM(2026) 81 commits the Commission to an EU Trusted Drone Label (Q4 2026) and a Drone Security Package (Q3 2026) while early label criteria circulating via the Deloitte-led consortium already name "end-to-end encrypted communications" and "resistance to unauthorised takeover," properties that sit exactly at the MAVLink link layer.

### Q3(c) The gap (with search evidence)

**No work maps CRA Annex I (or EN 18031, 2019/945, DO-326A, IEC 62443-4-2) requirements to concrete, machine-checkable properties of a drone C2 protocol and then produces compliance evidence by executing checks against real flight stacks.** Searches for `Cyber Resilience Act Annex I` with `measurable`, `properties`, `metrics`, `evidence`, `protocol`; `EN 18031` with `research`, `evaluation`, `paper`; `2019/945` with `cybersecurity`, `MAVLink`, `C2`; and `secure by default` with `metric`, `score`, `compliance evidence` returned only the Ruohonen mappings (requirement-to-mitigation text), the SORA gap analysis (qualitative scoring of one scenario), practitioner guides, and certification-scheme overviews. Nothing connects Annex I Part I items such as "secure by default configuration," "protection from unauthorised access," and "integrity of commands" to specific MAVLink signing behaviours (default-off signing, accept-unsigned allowlists, key provisioning over untrusted links, timestamp persistence) or to the EN 18031-1 mechanism categories (ACM, AUM, SUM, SSM, SCM, RLM, NMM, TCM, CCK, GEC, CRY) `[VERIFY: mechanism list against the published EN 18031-1 text]`. No scoring framework for "secure by default compliance evidence" that takes measured defaults as input was found. A crosswalk that (i) tabulates each legal clause against a formally stated property from the Q1 model, (ii) instantiates it as a conformance test, and (iii) scores each historical release from Q2 would be the first drone-link instance of such a chain and would land before the CRA's December 2027 application and the Trusted Drone Label criteria.

---

## Venues and formatting

Where comparable work in this review was published: MILCOM (PAVE-MAVLink), IEEE Networking Letters (Mak et al.), NASA Formal Methods / LNCS (Amorim et al.), Computers & Security (Alam et al.), NDSS (DroneID, PGFuzz, Jangid, Yu, ADGFuzz), IEEE S&P (Wu, Barbosa, Emami-Naeini, Matter), USENIX Security (RVFuzzer, Nino, Wu, Costin), ACM CCS (Basin, Cremers, Jackson, Li & Paxson), ACM IMC (Kotzias), ACSAC (Wei), MSR (Walden), ICRA (DeMarinis), VehicleSec (Chen), ESEC/FSE (Wang), ICUAS (Taylor), IEEE Access (Kwon), IWCMC (MAVSec), EuroS&PW (Costantino), DASC (Siddiqui), REW (Ruohonen), JISA, Transportation Research Procedia, STTT, ARES, IROS, Science Robotics.

Target venue table (page limits checked 2026-11-02 where noted; others `[VERIFY]` against the current CFP):

| Venue | Type | Page limit (typical) | Notes |
|-------|------|----------------------|-------|
| NDSS 2027 | Conf. | **13 pages excl. references/appendices/ethics** (NDSS 2026 CFP, verified); US letter, 2-col, 10 pt Times; double-blind | Best fit for Q1+Q2 combined (protocol + measurement); VehicleSec co-located workshop for drone-specific work. |
| USENIX Security 2027 | Conf. | **13 pages main body excl. refs/appendices; camera-ready up to 20** (prelim. CFP, verified); cycles Aug 25 2026 / Jan 26 2027 | Strong for measurement + formal artifacts; artifact evaluation. |
| IEEE S&P | Conf. | 13 pages excl. refs `[VERIFY]`; rolling deadlines | Formal analyses of Bluetooth/Matter appeared here. |
| ACM CCS | Conf. | 12 pages excl. refs + appendix `[VERIFY]` | Tamarin standards analyses (5G, TLS 1.3). |
| ESORICS | Conf. | LNCS, ~20 pages incl. refs `[VERIFY]` | European venue; formal + applied mix; good for CRA angle. |
| ACSAC | Conf. | 12 pages excl. refs `[VERIFY]` | Applied security; measurement studies welcome. |
| IEEE/IFIP DSN | Conf. | 12 pages incl. refs `[VERIFY]` | Dependability + security; robotics track history. |
| IEEE TIFS | Journal | Regular papers ~13-14 pages, overlength charges `[VERIFY]` | Formal + measurement journal version. |
| IEEE IoT Journal | Journal | **No hard cap; mandatory overlength charge USD 175/page beyond 8** (author guidelines, verified) | Fit for regulatory crosswalk + IoT defaults. |
| IEEE Access | Journal | No fixed limit; APC-based `[VERIFY APC]` | Fast; Kwon et al. 2018 published here. |
| IEEE ICUAS | Conf. | 8 pages (up to 10 with charges) `[VERIFY]` | Drone community; Taylor et al. 2021. |
| IEEE Aerospace Conf. | Conf. | up to ~20 pages `[VERIFY]` | Long-form aerospace security. |
| RoMoCo (IEEE) | Conf. | ~6 pages `[VERIFY]` | Polish robotics venue; limited security audience. |
| NASA Formal Methods (NFM) | Conf. | LNCS ~15-18 pages `[VERIFY]` | Both Amorim MAVLink papers; natural home for the Tamarin model paper. |
| MILCOM | Conf. | 6 pages (+ overlength) `[VERIFY]` | Wray & Wang 2025. |
| IEEE REW / RE | Workshop | 6-8 pages `[VERIFY]` | Ruohonen's CRA crosswalks; fit for Q3. |

IEEEtran conventions (summary of the IEEE Editorial Style Manual and IEEEtran class):
- References numbered in order of first citation, in square brackets `[1]`, `[2], [5]`, ranges `[3]-[7]`; cite inline as "as shown in [4]" (not "ref. [4]"). BibTeX style `IEEEtran.bst`; class `\documentclass[conference]{IEEEtran}` or `[journal]`.
- Author names as initials + surname ("A. B. Author"), up to six authors then "et al."; article titles in quotes, journal/conference names in italics with standard abbreviations (*IEEE Trans. Inf. Forensics Security*, *Proc. NDSS*); volume, number, pages, month and year; include DOI where available.
- Figures: caption below, "Fig. 1." (abbreviated, period), captions sentence case; refer in text as "Fig. 1" (never "Figure 1" except at sentence start in some styles). Tables: caption above, "TABLE I" in Roman numerals, title in small caps; refer in text as "Table I".
- Equations numbered flush right "(1)"; units SI; abbreviations defined at first use; use `\IEEEauthorblockN/A` in conference mode; acknowledgments unnumbered section; keywords after abstract (`\begin{IEEEkeywords}`).

---

## BibTeX (verified entries only; `[VERIFY]` entries flagged in `note`)

```bibtex
@inproceedings{wray2025pave,
  author    = {Wray, Tom and Wang, Ying},
  title     = {{PAVE-MAVLink}: Formal Verification of {MAVLink} 2 for Secure {UAV} Communications},
  booktitle = {Proc. IEEE Military Communications Conference (MILCOM)},
  year      = {2025},
  address   = {Los Angeles, CA, USA},
  doi       = {10.1109/MILCOM64451.2025.11310743}
}

@article{mak2025evtol,
  author  = {Mak, Bing and Yang, Jingda and Chen, Juntao and Ratazzi, Paul and Wang, Ying},
  title   = {Symbolic and Safety-Centric Formal Verification of {MAVLink} for Autonomous {eVTOL} Systems},
  journal = {IEEE Networking Letters},
  year    = {2025},
  doi     = {10.1109/LNET.2025.3610580}
}

@inproceedings{amorim2025datum,
  author    = {Amorim, Arthur and Taylor, Max and Kann, Trevor and Harrison, William L. and Leavens, Gary T. and Joneckis, Lance},
  title     = {Enforcing {MAVLink} Safety \& Security Properties via Refined Multiparty Session Types},
  booktitle = {NASA Formal Methods (NFM 2025)},
  series    = {Lecture Notes in Computer Science},
  publisher = {Springer},
  year      = {2025},
  doi       = {10.1007/978-3-031-93706-4_1},
  note      = {arXiv:2501.18874}
}

@inproceedings{amorim2026platum,
  author    = {Amorim, Arthur and Gazzillo, Paul and Taylor, Max and Joneckis, Lance},
  title     = {From High-Level Types to Low-Level Monitors: Synthesizing Verified Runtime Checkers for {MAVLink}},
  booktitle = {NASA Formal Methods (NFM 2026)},
  series    = {Lecture Notes in Computer Science},
  volume    = {16622},
  publisher = {Springer},
  year      = {2026},
  doi       = {10.1007/978-3-032-28079-4_5},
  note      = {arXiv:2604.03886}
}

@article{alam2026remoteid,
  author  = {Alam, Mehbub and Alhashmi, Mariam and Atrouz, Mohammad and Khader, Abdulrahman and Pashchapur, Ravi Ashok and Shoufan, Abdulhadi},
  title   = {Authentication Protocols for {UAV} Remote Identification Using Public-Key Infrastructure},
  journal = {Computers \& Security},
  volume  = {171},
  pages   = {105075},
  year    = {2026},
  doi     = {10.1016/j.cose.2026.105075}
}

@inproceedings{schiller2023droneid,
  author    = {Schiller, Nico and Chlosta, Merlin and Schloegel, Moritz and Bars, Nils and Eisenhofer, Thorsten and Scharnowski, Tobias and Domke, Felix and Sch{\"o}nherr, Lea and Holz, Thorsten},
  title     = {Drone Security and the Mysterious Case of {DJI}'s {DroneID}},
  booktitle = {Proc. Network and Distributed System Security Symposium (NDSS)},
  year      = {2023},
  doi       = {10.14722/ndss.2023.24217}
}

@inproceedings{wu2022bluetooth,
  author    = {Wu, Jianliang and Wu, Ruoyu and Xu, Dongyan and Tian, Dave (Jing) and Bianchi, Antonio},
  title     = {Formal Model-Driven Discovery of {Bluetooth} Protocol Design Vulnerabilities},
  booktitle = {Proc. IEEE Symposium on Security and Privacy (S\&P)},
  year      = {2022},
  doi       = {10.1109/SP46214.2022.9833777}
}

@inproceedings{jangid2023passkey,
  author    = {Jangid, Mohit Kumar and Zhang, Yue and Lin, Zhiqiang},
  title     = {Extrapolating Formal Analysis to Uncover Attacks in {Bluetooth} Passkey Entry Pairing},
  booktitle = {Proc. Network and Distributed System Security Symposium (NDSS)},
  year      = {2023},
  doi       = {10.14722/ndss.2023.23119}
}

@misc{duttagupta2025matter,
  author       = {Duttagupta, Sayon and Kolozyan, Arman and Nicolas, Georgio and Singel{\'e}e, Dave and Preneel, Bart},
  title        = {What's the Matter? An In-Depth Security Analysis of the {Matter} Protocol},
  howpublished = {Cryptology ePrint Archive, Paper 2025/1268},
  year         = {2025},
  note         = {To appear, IEEE S\&P 2027 [VERIFY at publication]}
}

@article{bodei2024autosar,
  author  = {Bodei, Chiara and De Vincenzi, Marco and Matteucci, Ilaria},
  title   = {Formal Analysis of an {AUTOSAR}-Based Basic Software Module},
  journal = {International Journal on Software Tools for Technology Transfer},
  volume  = {26},
  pages   = {495--508},
  year    = {2024},
  doi     = {10.1007/s10009-024-00759-w}
}

@inproceedings{zelle2021someip,
  author    = {Zelle, Daniel and Lauser, Timm and Kern, Dustin and Krau{\ss}, Christoph},
  title     = {Analyzing and Securing {SOME/IP} Automotive Services with Formal and Practical Methods},
  booktitle = {Proc. 16th International Conference on Availability, Reliability and Security (ARES)},
  year      = {2021},
  doi       = {10.1145/3465481.3465748}
}

@inproceedings{jackson2019seemslegit,
  author    = {Jackson, Dennis and Cremers, Cas and Cohn-Gordon, Katriel and Sasse, Ralf},
  title     = {Seems Legit: Automated Analysis of Subtle Attacks on Protocols that Use Signatures},
  booktitle = {Proc. ACM SIGSAC Conference on Computer and Communications Security (CCS)},
  year      = {2019},
  doi       = {10.1145/3319535.3339813}
}

@inproceedings{basin2018fiveg,
  author    = {Basin, David and Dreier, Jannik and Hirschi, Lucca and Radomirovi{\'c}, Sa{\v{s}}a and Sasse, Ralf and Stettler, Vincent},
  title     = {A Formal Analysis of {5G} Authentication},
  booktitle = {Proc. ACM SIGSAC Conference on Computer and Communications Security (CCS)},
  year      = {2018},
  doi       = {10.1145/3243734.3243846}
}

@inproceedings{cremers2017tls13,
  author    = {Cremers, Cas and Horvat, Marko and Hoyland, Jonathan and Scott, Sam and van der Merwe, Thyla},
  title     = {A Comprehensive Symbolic Analysis of {TLS} 1.3},
  booktitle = {Proc. ACM SIGSAC Conference on Computer and Communications Security (CCS)},
  year      = {2017},
  doi       = {10.1145/3133956.3134063}
}

@inproceedings{barbosa2021sok,
  author    = {Barbosa, Manuel and Barthe, Gilles and Bhargavan, Karthikeyan and Blanchet, Bruno and Cremers, Cas and Liao, Kevin and Parno, Bryan},
  title     = {{SoK}: Computer-Aided Cryptography},
  booktitle = {Proc. IEEE Symposium on Security and Privacy (S\&P)},
  year      = {2021},
  doi       = {10.1109/SP40001.2021.00008}
}

@article{kwon2018mavlink,
  author  = {Kwon, Young-Min and Yu, Jaemin and Cho, Byeong-Moon and Eun, Yongsoon and Park, Kyung-Joon},
  title   = {Empirical Analysis of {MAVLink} Protocol Vulnerability for Attacking Unmanned Aerial Vehicles},
  journal = {IEEE Access},
  volume  = {6},
  year    = {2018},
  doi     = {10.1109/ACCESS.2018.2863237}
}

@inproceedings{allouch2019mavsec,
  author    = {Allouch, Azza and Cheikhrouhou, Omar and Koub{\^a}a, Anis and Khalgui, Mohamed and Abbes, Tarek},
  title     = {{MAVSec}: Securing the {MAVLink} Protocol for {Ardupilot}/{PX4} Unmanned Aerial Systems},
  booktitle = {Proc. 15th International Wireless Communications \& Mobile Computing Conference (IWCMC)},
  year      = {2019},
  doi       = {10.1109/IWCMC.2019.8766667}
}

@inproceedings{hamza2024mavlinksurvey,
  author    = {Hamza, Muhammad and Mohsin, Muhammad and Khalil, Muhammad and Kazmi, Syed Kazam Abbas},
  title     = {{MAVLink} Protocol: A Survey of Security Threats and Countermeasures},
  booktitle = {Proc. 4th International Conference on Digital Futures and Transformative Technologies (ICoDT2)},
  year      = {2024},
  doi       = {10.1109/ICoDT262145.2024.10740195}
}

@inproceedings{hughes2024heartbeat,
  author    = {Hughes, I. and Pupo, A. and Wynd, J. and Thurlow, Z. and Ivancik, C. and Wang, Ying},
  title     = {Securing the Unprotected: Enhancing Heartbeat Messaging for {MAVLink} {UAV} Communications},
  booktitle = {Proc. IEEE Pacific Rim Conference on Communications, Computers and Signal Processing (PACRIM)},
  year      = {2024},
  doi       = {10.1109/PACRIM61180.2024.10690216}
}

@inproceedings{kim2021pgfuzz,
  author    = {Kim, Hyungsub and Ozmen, Muslum Ozgur and Bianchi, Antonio and Celik, Z. Berkay and Xu, Dongyan},
  title     = {{PGFUZZ}: Policy-Guided Fuzzing for Robotic Vehicles},
  booktitle = {Proc. Network and Distributed System Security Symposium (NDSS)},
  year      = {2021},
  doi       = {10.14722/ndss.2021.24096}
}

@inproceedings{kim2019rvfuzzer,
  author    = {Kim, Taegyu and Kim, Chung Hwan and Rhee, Junghwan and Fei, Fan and Tu, Zhan and Walkup, Gregory and Zhang, Xiangyu and Deng, Xinyan and Xu, Dongyan},
  title     = {{RVFuzzer}: Finding Input Validation Bugs in Robotic Vehicles through Control-Guided Testing},
  booktitle = {Proc. 28th USENIX Security Symposium},
  year      = {2019},
  note      = {[VERIFY author list against USENIX page]}
}

@misc{rfc9434,
  author       = {Card, Stuart and Wiethuechter, Adam and Moskowitz, Robert and Gurtov, Andrei},
  title        = {Drone Remote Identification Protocol ({DRIP}) Requirements and Terminology},
  howpublished = {RFC 9434, IETF},
  year         = {2023}
}

@misc{mavlink_signing_spec,
  author       = {{MAVLink Developers}},
  title        = {Message Signing (Authentication)},
  howpublished = {\url{https://mavlink.io/en/guide/message_signing.html}},
  note         = {Accessed 2 Nov. 2026}
}

@inproceedings{kotzias2018tls,
  author    = {Kotzias, Platon and Razaghpanah, Abbas and Amann, Johanna and Paterson, Kenneth G. and Vallina-Rodriguez, Narseo and Caballero, Juan},
  title     = {Coming of Age: A Longitudinal Study of {TLS} Deployment},
  booktitle = {Proc. Internet Measurement Conference (IMC)},
  year      = {2018},
  doi       = {10.1145/3278532.3278568}
}

@inproceedings{wei2012permission,
  author    = {Wei, Xuetao and Gomez, Lorenzo and Neamtiu, Iulian and Faloutsos, Michalis},
  title     = {Permission Evolution in the {Android} Ecosystem},
  booktitle = {Proc. 28th Annual Computer Security Applications Conference (ACSAC)},
  year      = {2012},
  doi       = {10.1145/2420950.2420956}
}

@inproceedings{walden2020openssl,
  author    = {Walden, James},
  title     = {The Impact of a Major Security Event on an Open Source Project: The Case of {OpenSSL}},
  booktitle = {Proc. 17th International Conference on Mining Software Repositories (MSR)},
  year      = {2020},
  doi       = {10.1145/3379597.3387465}
}

@inproceedings{li2017patches,
  author    = {Li, Frank and Paxson, Vern},
  title     = {A Large-Scale Empirical Study of Security Patches},
  booktitle = {Proc. ACM SIGSAC Conference on Computer and Communications Security (CCS)},
  year      = {2017},
  doi       = {10.1145/3133956.3134072}
}

@inproceedings{yu2022embedded1996,
  author    = {Yu, Ruotong and Del Nin, Francesca and Zhang, Yuchen and Huang, Shan and Kaliyar, Pallavi and Zakto, Sarah and Conti, Mauro and Portokalidis, Georgios and Xu, Jun},
  title     = {Building Embedded Systems Like It's 1996},
  booktitle = {Proc. Network and Distributed System Security Symposium (NDSS)},
  year      = {2022},
  doi       = {10.14722/ndss.2022.24031},
  note      = {[VERIFY full author list]}
}

@inproceedings{nino2024firmware,
  author    = {Nino, Nicolas and Lu, Ruibo and Zhou, Wei and Lee, Kyu Hyung and Zhao, Ziming and Guan, Le},
  title     = {Unveiling {IoT} Security in Reality: A Firmware-Centric Journey},
  booktitle = {Proc. 33rd USENIX Security Symposium},
  year      = {2024}
}

@inproceedings{costin2014firmware,
  author    = {Costin, Andrei and Zaddach, Jonas and Francillon, Aur{\'e}lien and Balzarotti, Davide},
  title     = {A Large-Scale Analysis of the Security of Embedded Firmwares},
  booktitle = {Proc. 23rd USENIX Security Symposium},
  year      = {2014},
  note      = {[VERIFY: no DOI; USENIX]}
}

@article{ruohonen2025sok,
  author  = {Ruohonen, Jukka},
  title   = {{SoK}: The Design Paradigm of Safe and Secure Defaults},
  journal = {Journal of Information Security and Applications},
  year    = {2025},
  doi     = {10.1016/j.jisa.2025.103989},
  note    = {arXiv:2412.17329}
}

@inproceedings{demarinis2019ros,
  author    = {DeMarinis, Nicholas and Tellex, Stefanie and Kemerlis, Vasileios P. and Konidaris, George and Fonseca, Rodrigo},
  title     = {Scanning the {Internet} for {ROS}: A View of Security in Robotics Research},
  booktitle = {Proc. IEEE International Conference on Robotics and Automation (ICRA)},
  year      = {2019},
  doi       = {10.1109/ICRA.2019.8794451}
}

@inproceedings{chen2024rosvehicles,
  author    = {Chen, Wentao and Der, Sam and Luo, Yunpeng and Alshammari, Fayzah and Chen, Qi Alfred},
  title     = {Understanding the {Internet}-Wide Vulnerability Landscape for {ROS}-based Robotic Vehicles},
  booktitle = {Proc. Symposium on Vehicle Security and Privacy (VehicleSec)},
  year      = {2024},
  doi       = {10.14722/vehiclesec.2024.23018}
}

@inproceedings{wang2021autopilotbugs,
  author    = {Wang, Dinghua and Li, Shuqing and Xiao, Guanping and Liu, Yepang and Sui, Yulei},
  title     = {An Exploratory Study of Autopilot Software Bugs in Unmanned Aerial Vehicles},
  booktitle = {Proc. 29th ACM Joint European Software Engineering Conference and Symposium on the Foundations of Software Engineering (ESEC/FSE)},
  year      = {2021},
  doi       = {10.1145/3468264.3468559}
}

@inproceedings{taylor2021uasbugs,
  author    = {Taylor, Max and Boubin, Jayson and Chen, Haicheng and Stewart, Christopher and Qin, Feng},
  title     = {A Study on Software Bugs in Unmanned Aircraft Systems},
  booktitle = {Proc. International Conference on Unmanned Aircraft Systems (ICUAS)},
  year      = {2021},
  doi       = {10.1109/ICUAS51884.2021.9476844}
}

@inproceedings{breiling2017ros,
  author    = {Breiling, Benjamin and Dieber, Bernhard and Schartner, Peter},
  title     = {Secure Communication for the Robot Operating System},
  booktitle = {Proc. Annual IEEE International Systems Conference (SysCon)},
  year      = {2017},
  doi       = {10.1109/SYSCON.2017.7934755}
}

@inproceedings{mayoralvilches2022sros2,
  author    = {Mayoral-Vilches, V{\'i}ctor and White, Ruffin and Caiazza, Gianluca and Arguedas, Mikael},
  title     = {{SROS2}: Usable Cyber Security Tools for {ROS} 2},
  booktitle = {Proc. IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)},
  year      = {2022},
  doi       = {10.1109/IROS47612.2022.9982129}
}

@article{macenski2022ros2,
  author  = {Macenski, Steven and Foote, Tully and Gerkey, Brian and Lalancette, Chris and Woodall, William},
  title   = {Robot Operating System 2: Design, Architecture, and Uses in the Wild},
  journal = {Science Robotics},
  volume  = {7},
  number  = {66},
  year    = {2022},
  doi     = {10.1126/scirobotics.abm6074}
}

@misc{ardupilot_signing_commit,
  author       = {Tridgell, Andrew},
  title        = {{GCS\_MAVLink}: support for mavlink2 signing operations},
  howpublished = {ArduPilot git commit ed9a43ca46, 21 Jan. 2016; first stable releases ArduPlane 3.6.0 (11 Jun. 2016), Copter 3.4.0 (31 Oct. 2016), APMrover2 3.1.0 (22 Dec. 2016)},
  note         = {\url{https://github.com/ArduPilot/ardupilot}, verified from repository history 2 Nov. 2026}
}

@misc{ardupilot_mavlink2_default,
  author       = {{ArduPilot Developers}},
  title        = {{AP\_SerialManager}: default serial 1 and 2 protocols to {MAVLink2}},
  howpublished = {ArduPilot git commit 211c20da38, 25 Jun. 2020; first in Copter 4.1.0 / ArduPlane 4.1.0},
  note         = {Verified from repository history 2 Nov. 2026}
}

@misc{px4_signing_pr,
  author       = {{PX4 Developers}},
  title        = {feat(mavlink): mavlink signing support (\#25284)},
  howpublished = {PX4-Autopilot git commit 358574f9f6, 9 Mar. 2026; spec-alignment fix \#26894 (12 Apr. 2026); contained in v1.18.0-alpha1 through v1.18.0-rc1},
  note         = {\url{https://github.com/PX4/PX4-Autopilot}, verified from repository history 2 Nov. 2026}
}

@inproceedings{ruohonen2025attack,
  author    = {Ruohonen, Jukka and Kang, Eun-Young and Ramadan, Qusai},
  title     = {An Alignment Between the {CRA}'s Essential Requirements and the {ATT\&CK}'s Mitigations},
  booktitle = {Proc. IEEE 33rd International Requirements Engineering Conference Workshops (REW)},
  year      = {2025},
  doi       = {10.1109/REW66121.2025.00033},
  note      = {arXiv:2505.13641}
}

@inproceedings{ruohonen2025gdpr,
  author    = {Ruohonen, Jukka and Hjerppe, Kalle and Kang, Eun-Young},
  title     = {A Mapping Analysis of Requirements Between the {CRA} and the {GDPR}},
  booktitle = {Proc. IEEE 33rd International Requirements Engineering Conference Workshops (REW)},
  year      = {2025},
  doi       = {10.1109/REW66121.2025.00034},
  note      = {arXiv:2503.01816}
}

@article{ruohonen2025vulncoord,
  author  = {Ruohonen, Jukka and Timmers, Paul},
  title   = {Vulnerability Coordination under the {Cyber Resilience Act}},
  journal = {Applied Cybersecurity \& Internet Governance},
  year    = {2025},
  doi     = {10.60097/ACIG/213350},
  note    = {arXiv:2412.06261}
}

@article{puliyski2025sora,
  author  = {Puliyski, Anton and Stefanova, Alexandra and Serbezov, Vladimir},
  title   = {The Regulatory Illusion of Security in Drone Operations in the Specific Category: An Analysis of the Gaps Between Regulatory Compliance and Actual Cyber Resilience within the {SORA}},
  journal = {Transportation Research Procedia},
  volume  = {91},
  pages   = {91--98},
  year    = {2025},
  doi     = {10.1016/j.trpro.2025.10.013}
}

@article{huttunen2019uas,
  author  = {Huttunen, Mikko},
  title   = {Civil Unmanned Aircraft Systems and Security: The {European} Approach},
  journal = {Journal of Transportation Security},
  year    = {2019},
  doi     = {10.1007/s12198-019-00203-0}
}

@inproceedings{costantino2022r155,
  author    = {Costantino, Gianpiero and De Vincenzi, Marco and Matteucci, Ilaria},
  title     = {A Comparative Analysis of {UNECE WP.29 R155} and {ISO/SAE 21434}},
  booktitle = {Proc. IEEE European Symposium on Security and Privacy Workshops (EuroS\&PW)},
  year      = {2022},
  doi       = {10.1109/EuroSPW55150.2022.00041}
}

@inproceedings{siddiqui2023do326a,
  author    = {Siddiqui, Fahad and Ahlbrecht, Alexander and Khan, Rafiullah and Tasdemir, Sena and Hui, Henry and Sonigara, Balmukund and Sezer, Sakir and McLaughlin, Kieran and D{\"u}rr, Wanja},
  title     = {Cybersecurity Engineering: Bridging the Security Gaps in Avionics Architectures and {DO-326A/ED-202A}},
  booktitle = {Proc. IEEE/AIAA 42nd Digital Avionics Systems Conference (DASC)},
  year      = {2023},
  doi       = {10.1109/DASC58513.2023.10311187},
  note      = {[VERIFY full author list]}
}

@inproceedings{torens2020safetysecurity,
  author    = {Torens, Christoph},
  title     = {Safety Versus Security in Aviation, Comparing {DO-178C} with Security Standards},
  booktitle = {AIAA SciTech 2020 Forum},
  year      = {2020},
  doi       = {10.2514/6.2020-0242}
}

@inproceedings{emaminaeini2020label,
  author    = {Emami-Naeini, Pardis and Agarwal, Yuvraj and Cranor, Lorrie Faith and Hibshi, Hanan},
  title     = {Ask the Experts: What Should Be on an {IoT} Privacy and Security Label?},
  booktitle = {Proc. IEEE Symposium on Security and Privacy (S\&P)},
  year      = {2020},
  doi       = {10.1109/SP40000.2020.00043}
}

@misc{ec2026droneactionplan,
  author       = {{European Commission}},
  title        = {Action Plan on Drone and Counter-Drone Security},
  howpublished = {COM(2026) 81 final, Brussels, 11 Feb. 2026, CELEX 52026DC0081},
  year         = {2026}
}

@misc{eu2024cra,
  author       = {{European Parliament and Council}},
  title        = {Regulation ({EU}) 2024/2847 on Horizontal Cybersecurity Requirements for Products with Digital Elements ({Cyber Resilience Act})},
  howpublished = {Official Journal of the European Union, L, 20 Nov. 2024},
  year         = {2024}
}

@misc{eu2022red_da,
  author       = {{European Commission}},
  title        = {Commission Delegated Regulation ({EU}) 2022/30 Supplementing Directive 2014/53/EU (Radio Equipment Directive) as Regards the Application of the Essential Requirements in Article 3(3)(d), (e) and (f)},
  year         = {2022}
}

@misc{eu2019_945,
  author       = {{European Commission}},
  title        = {Commission Delegated Regulation ({EU}) 2019/945 on Unmanned Aircraft Systems and on Third-Country Operators of Unmanned Aircraft Systems},
  year         = {2019}
}

@misc{eu2022nis2,
  author       = {{European Parliament and Council}},
  title        = {Directive ({EU}) 2022/2555 on Measures for a High Common Level of Cybersecurity across the Union ({NIS2})},
  year         = {2022}
}
```

---

## Open verification items (consolidated)

1. PAVE-MAVLink (Wray & Wang 2025) and Mak et al. 2025: obtain full text to confirm that native MAVLink 2 signing (sha256_48 / SETUP_SIGNING) is not modelled. Abstracts indicate an unprotected baseline plus ChaCha20 extension.
2. Author lists flagged `[VERIFY]`: RVFuzzer (USENIX 2019), Yu et al. NDSS 2022, Siddiqui et al. DASC 2023, Wu et al. USENIX 2024, ADGFuzz NDSS 2026, UAVConfigFuzzer 2026.
3. Matter paper: S&P 2027 acceptance stated on the ePrint page; confirm at publication.
4. Drone Security Package (Q3 2026 target) and Trusted Drone Label criteria (Q4 2026 target): re-check EUR-Lex and DG DEFIS/DG MOVE pages; nothing located as of 2026-11-02.
5. EN 18031-1 mechanism-category list and OJ citation; EN 303 645 current edition.
6. Venue page limits marked `[VERIFY]` (S&P, CCS, ESORICS, ACSAC, DSN, TIFS, ICUAS, Aerospace, RoMoCo, NFM, MILCOM, REW).
7. ArduPilot issue #10298 fix (#10311) merge date.
