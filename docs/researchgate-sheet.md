# ResearchGate — qué subir y qué pegar en cada campo

**Generado por `scripts/researchgate_sheet.py` desde los `.tex`.** No lo edites a
mano: la versión anterior estaba escrita a mano y se quedó desfasada — seguía
llevando la reivindicación de primacía que el Paper 2 ya había retirado, así que el
abstract que ibas a pegar contradecía al PDF de debajo.

Cuatro preprints, en este orden.

**Tipo:** Preprint. **No** "Article" — no están revisados por pares, y marcarlos
como artículo es exactamente lo que nos quita la credibilidad que buscamos.

**Aviso real:** ResearchGate da DOI a los preprints, pero si luego quieres mandar
alguno a arXiv o a una conferencia, mira su política de preprints antes. La mayoría
de conferencias IEEE lo permiten; algunas revistas no.

---

## paper1-signing.pdf

**Título:**

> Signed but Unprotected: A Formal and Empirical Study of MAVLink 2 Message-Signing Defaults and Their Bearing on the EU Cyber Resilience Act

**Abstract:**

> MAVLink is the de facto command-and-control (C2) protocol of the open-source drone ecosystem. Since 2016 MAVLink 2 has offered optional per-frame message signing, yet whether a deployed aircraft is actually protected depends on a tangle of implementation choices—default state, allow-lists, link exemptions, and a trust-on-first-use key-provisioning step—that, to our knowledge, no prior work has stated precisely or measured end to end. We make three contributions. First, we give a compact parameterised acceptance semantics for MAVLink 2 signing: a transition system whose parameters capture the points at which PX4 and ArduPilot differ, together with a bounded symbolic adversary and six security properties. Bounded exploration yields short, human-readable attack witnesses and, crucially, distinguishes an idealised out-of-band provisioning policy—which satisfies every property—from the policies real stacks implement, which do not. Second, we build three flight stacks from source (ArduPilot Copter 4.7.2, PX4 v1.17.0, PX4 v1.18.0-rc1) and audit them in software-in-the-loop with mavaudit, a passive, key-less auditor we release. We find that all default links are unsigned, answer unauthenticated reads, and expose MAVLink FTP; that the current stable PX4 release contains no signing implementation at all; and that with signing enabled ArduPilot's primary channel signs every outbound frame while still accepting unsigned commands—so a purely passive observer would wrongly judge it protected. This channel-0 exemption is a documented upstream behaviour (ArduPilot issue \#34489, with a fix proposed but not yet merged ); our contribution is to measure it independently, to show that the model built from the implementation reproduces it, and to make explicit that the exemption follows the channel index rather than the link type (measured by moving the transport of each channel independently), which motivates an active, read-only probe. Third, we map each observed property to the essential requirements of EU Regulation 2024/2847 (the Cyber Resilience Act) and the command-link requirement of Delegated Regulation 2019/945. We claim no primacy for that mapping: Annex I crosswalks for drone products are already published as compliance guidance, including ones that name unauthenticated MAVLink as the control-link weakness to remediate, and the four-column crosswalk form itself is established practice. What differs here is the content of the cells. Those crosswalks map a requirement to an intended control; each row of ours is anchored to a measurement taken from a running autopilot, with the record published alongside it, including the rows where the measurement was inconclusive and earned nothing. All code, models, and data are released for reproduction.

**Keywords:**

> MAVLink, unmanned aerial vehicles, message signing, protocol security, formal methods, Cyber Resilience Act, secure by default.

---

## paper2-longitudinal.pdf

**Título:**

> A Decade of Defaults: How "Secure by Default" Evolved in the MAVLink Flight Stacks (ArduPilot and PX4, 2016–2026)

**Abstract:**

> "Secure by default" is now a legal requirement for connected products sold in the EU, yet we have little historical evidence on whether open-source embedded stacks have moved toward it. We present a decade of evidence on the command-link security defaults of the two dominant open-source drone flight stacks, ArduPilot and PX4. We claim no primacy for it, and we are explicit about which decade is which: the version-control evidence does span 2016–2026, whereas the measured evidence spans two releases. Calling the whole a decade-spanning measurement study would overstate it by an order of magnitude, so we do not. Four lines of evidence are combined: the projects' version-control history, a measured posture matrix from building and auditing releases in software-in-the-loop (which, we state plainly, covers only n=2 releases that both build and run on a current toolchain, ArduPilot 4.5.7 and 4.6.3; PX4 v1.16.2 builds but does not run under the harness), the buildability of each release on a current toolchain, and a measurement of what each runnable release answers to a peer that has presented no credential. Three findings are clear and mutually reinforcing. First, signing is never on by default: version control shows it was added to ArduPilot in 2016 and never defaulted, and absent from PX4 until 2026, and the releases we can still build confirm it. Second—and unexpectedly—the binding constraint on auditing old releases is reproducibility, not posture: pre-4.5 ArduPilot no longer builds on a current system through a layered cascade of Python and C++ toolchain breaks, and older PX4 builds but will not run under a uniform simulator harness. Third, the one clear advance—message signing arriving in the PX4 line—leaves a second, unauthenticated control plane (the uXRCE-DDS bridge to uORB) untouched in the same release, so a trend measured on one protocol alone would record progress and miss this. Both bear directly on the Cyber Resilience Act's expectation that products remain patchable and testable through their support period. All build recipes, raw records, failure reasons, and the analysis pipeline are released.

**Keywords:**

> longitudinal measurement, secure by default, MAVLink, drones, software evolution, Cyber Resilience Act.

---

## paper3-formal.pdf

**Título:**

> Acceptance Semantics for MAVLink 2 Signing: Bounded Symbolic Analysis and Model-Based Conformance Testing of Flight Stacks

**Abstract:**

> The MAVLink 2 message-signing specification fixes a frame format and a timestamp rule but delegates the decisive question—when is an unsigned or unexpected frame accepted?—to each implementation. The result is a family of subtly different receivers whose security cannot be compared by reading the specification. We give a precise, parameterised acceptance semantics for MAVLink 2 signing as a labelled transition system, in which the choices the specification leaves open become explicit policy parameters, and we equip it with a bounded symbolic adversary and six security properties with machine-checkable definitions. Bounded breadth-first exploration is sound (every reported violation is a concrete trace) and complete up to a depth bound relative to the adversary's restricted move set; it separates an idealised out-of-band provisioning policy, which satisfies every property while remaining functional, from the policies PX4 and ArduPilot implement, each of which violates a distinct subset. We then use the model generatively: a design-space search over single parameter edits, constrained to preserve a liveness (functionality) property, yields greedy-minimal remediations—and shows, for example, that the current ArduPilot policy requires two independent changes where PX4 v1.18 requires one. Finally, we introduce model-based conformance testing for flight stacks: read-only test frames derived from the semantics are executed against real software-in-the-loop builds, and the observed accept/reject decisions are compared with the model's predictions. In a recorded experiment across three stacks and four link configurations the model agrees with all 47 observed decisions, and one configuration resolves a disagreement between a stack's documentation and its behaviour in favour of the behaviour; we are explicit that the 20 unkeyed cases are tautological and that the signing-less PX4 v1.17 stack serves as a negative control, so the discriminating evidence rests on the 23 keyed cases, including seven observed rejections. One pair of configurations is a controlled experiment rather than a coincidence of agreement: moving the same transport between channel indices flips the decision exactly as the policy's trusted-link parameter predicts. All models, proofs-in-code, and harnesses are released.

**Keywords:**

> formal methods, protocol security, transition systems, bounded model checking, conformance testing, MAVLink, UAV security.

---

## paper4-score.pdf

**Título:**

> Scoring "Secure by Default": A Reproducible, CRA-Grounded Metric with a Drone Command-Link Instantiation

**Abstract:**

> The EU Cyber Resilience Act makes "secure by default" a legal requirement, but a requirement one cannot measure is a requirement one cannot audit. We propose a small, transparent metric that turns the observable security posture of a connected product's protocol endpoint into a 0–100 score with a letter grade, and we instantiate it on the MAVLink command links of two drone flight stacks. The metric is defined by three axioms—provenance (every criterion is computed from an observed finding or a model property, never from opinion), monotonicity (improving posture never lowers the score), and CRA-grounded weights (each criterion maps to an Annex I essential requirement and carries a fixed weight summing to 100)—and is released as executable code with a property-test suite that checks the axioms. Applied to our measured configurations, the score separates insecure defaults (grade E) from a provisioned but console-exempt link (grade D) and from a cleanly signed link (grade C), and ranks them below an idealised target (grade A), with grade B the ceiling for MAVLink 2 signing alone; the console-exemption penalty is captured numerically rather than described, and a criterion for a second, non-MAVLink control plane reorders two configurations that the MAVLink criteria alone rank equally. We argue that such a metric is the missing piece between a measurement tool and a conformity-evidence artefact, and we discuss its limits as a rubric rather than a canonical truth.

**Keywords:**

> secure by default, security metrics, Cyber Resilience Act, conformity evidence, MAVLink, measurement.

---

## Después de subir

Los DOIs que emita ResearchGate van a cuatro sitios, y los cuatro están
escritos esperando: la página de producto, el `README.md` del repo, el comentario
en el issue de ArduPilot, y los 4 mensajes de LinkedIn.

