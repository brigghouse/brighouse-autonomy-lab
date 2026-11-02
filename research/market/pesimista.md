# El Pesimista: ataque a las 13 ideas

**Fecha:** 2026-11-02
**Fundador:** solo, España/UE, perfil de pentesting (Brighouse Security Labs), investigación publicada, capital inferior a 5.000 €.
**Método:** cada ataque se apoya en los ficheros de investigación (defensa.md, neuro_bio.md, chips.md) o en búsquedas web nuevas con su URL. Lo que es opinión mía va marcado como **[INTERPRETACIÓN]**. No he leído optimista.md.

---

## 0. Tres hallazgos nuevos que cambian el tablero

1. **La idea 10 parte de un dato falso.** La fase 2 de CMMC **no** arranca el 10-11-2026. El Departamento de Guerra de EE. UU. la **suspendió el 13-07-2026** (https://www.wilmerhale.com/en/insights/client-alerts/20260720-pentagon-suspends-cmmc-phase-2-requirements-and-launches-review-of-cybersecurity-certification-program). La desviación de clase de septiembre lo llevó a los contratos: se aceptan autoevaluaciones de nivel 1 y 2. A 27-10-2026 la fase 2 sigue en pausa y no hay informe de la Task Force (https://secureframe.com/hub/cmmc/news-updates-2026.md). Los ficheros defensa.md e ideas.md están desactualizados en este punto.
2. **La ayuda SECURE no sirve para facturar este año.** Cierra el **11-12-2026**, dentro de 39 días. Después hay un hueco entre la solicitud y la firma del acuerdo, y **no se puede empezar el trabajo ni gastar antes de firmar**. No se publica el método de selección ni la fecha de pago. Con 11,5 M€ y 30 k€ por proyecto salen como mucho unos 383 proyectos para toda la UE/EEE (https://www.cyberresilienceact.eu/es/news/secure-second-open-call-1-october-2026-cra-sme-funding.html).
3. **El PSIRT del CRA tiene poco volumen y mucha responsabilidad.** En la Single Reporting Platform solo se notifican **vulnerabilidades explotadas activamente** (con "evidencia fiable" de explotación) e **incidentes graves**. Quien notifica es un "Assigned Representative" con cuenta EU Login personal y MFA, asociado al fabricante, y el fabricante sigue siendo el responsable (https://www.enisa.europa.eu/topics/product-security/single-reporting-platform-srp/frequently-asked-questions). Una pyme puede pasar meses sin un solo evento notificable. Así cuesta justificar una cuota mensual, pero si se escapa un plazo de 24 h el problema es tuyo **[INTERPRETACIÓN]**.

---

## Idea 1. PSIRT-as-a-Service para el CRA

**Defectos fatales o casi fatales**
- **Poca frecuencia y mucho riesgo.** Solo obliga a notificar lo explotado activamente y los incidentes graves (FAQ de ENISA, arriba). Para una pyme con pocos productos, el valor que percibe por mes es bajo.
- **Disponibilidad 24/7 en solitario.** El plazo de 24 h corre desde que el fabricante tiene conocimiento y no se pausa (https://www.cyberresilienceact.eu/news/cra-delegated-act-delaying-vulnerability-disclosure.html). Una sola persona no puede prometer un servicio 24/7 creíble, ni puede irse de vacaciones.
- **Responsabilidad y seguro.** La multa del CRA llega a 15 M€ o al 2,5 % de la facturación (chips.md). Si el cliente culpa al proveedor del PSIRT, la póliza de RC profesional tiene que cubrirlo. El coste de esa póliza está sin verificar (neuro_bio.md, sección 4).
- **El regulador no lo valora.** El fabricante sigue siendo el responsable. Para ENISA el PSIRT externo no aporta nada; solo vale como comodidad interna.

**Quién lo hace ya**
- **Plataformas:** Finite State redacta las notificaciones según los plazos del CRA y se coordina con el PSIRT del cliente (https://www.finitestate.io/cra). ONEKEY tiene un rol de "PSIRT Manager" y un caso de uso de respuesta a incidentes (https://www.onekey.com/compliance-wizard/).
- **Proveedores de chips, gratis:** Espressif publica avisos, un SBOM (esp-idf-sbom), un dashboard de CVE y, desde septiembre de 2026, un portal de notificación de vulnerabilidades (https://developer.espressif.com/blog/2026/09/esp32-cra-obligations-and-deadlines/). Le quita al PSIRT externo una parte del trabajo de vigilancia.
- **En España:** S2 Grupo tiene contenido comercial sobre la ley de ciberresiliencia (https://s2grupo.es/nueva-ley-de-ciberresiliencia-de-la-ue). Applus+ Laboratories (que integra a jtsec) vende un certificado de conformidad de ciberresiliencia y un "Cyber Resilience Mark" (https://www.appluslaboratories.com/global/en/news/new-applus+-cyber-resiliance-mark). Despachos de toda la UE (Jones Day, Crowell, Noerr) están captando el mismo cliente (chips.md; https://www.noerr.com/en/insights/cra-single-reporting-platform-launched-reporting-requirements-apply-with-immediate-effect).

**Comoditización.** Alta. La monitorización de CVE contra un SBOM la hace gratis OWASP Dependency-Track (https://owasp.org/www-project-dependency-track/). Lo único que queda por vender es redactar y enviar un formulario, y eso lo van a automatizar las plataformas **[INTERPRETACIÓN]**.

**Cómo fracasa en 12 meses.** Consigue 3 o 4 clientes a 300-800 €/mes, ninguno tiene un evento notificable y en la primera renovación preguntan para qué pagan. O al revés: hay un evento un sábado y lo atiende tarde.

**Criterio para abandonarla (60 días):** menos de 3 fabricantes dispuestos a firmar una cuota de al menos 500 €/mes **sin** un sprint previo regalado, o que la aseguradora no cubra la responsabilidad por los plazos del CRA a un precio razonable.

---

## Idea 2. Sprint "CRA Ready" más ayuda SECURE

**Defectos fatales o casi fatales**
- **El calendario de SECURE juega en contra.** Quedan 39 días hasta el cierre. El trabajo no puede empezar hasta que se firme el acuerdo y la fecha de resolución no está publicada (SECURE, arriba). Lo que se venda en noviembre y diciembre se factura, con suerte, en 2027.
- **Las plazas son pocas y no se sabe cómo se reparten.** Unos 383 proyectos como máximo en toda la UE/EEE y una sola propuesta por pyme. Si el cliente no gana la ayuda, el sprint pasa a costar el doble y la venta se cae.
- **Quedan dudas en la norma.** No se ha confirmado el estado de las normas armonizadas y a septiembre de 2026 no había ningún organismo notificado designado (chips.md). Un plan de cumplimiento escrito hoy puede quedarse viejo en 2027.

**Quién lo hace ya.** Cualquier consultora de GRC o de pentesting de la UE. En la propia página de SECURE las consultoras se anuncian para ayudar a solicitar la ayuda. En Alemania, Schutzwerk tiene una página dedicada a captar clientes de SECURE (https://www.schutzwerk.com/en/funding/eu-secure4sme/) y en Italia, CSQA (https://www.csqa.it/en-us/press/bando-secure”-per-l’adeguamento-normativo-al-cyber-resilience-act). En España están S2 Grupo, Applus+/jtsec y GlobalSuite (https://www.globalsuitesolutions.com/es/?p=112347), además de los despachos.

**Comoditización.** Media-alta. Un "gap assessment" de precio cerrado es una plantilla que hacen bien decenas de firmas. La diferencia de verdad es el pentest de firmware y hardware, que es lo que el fundador ya sabe hacer.

**Cómo fracasa en 12 meses.** Prepara 5 solicitudes de SECURE gratis o a éxito, gana 1 o 2 y cobra en el segundo trimestre de 2027. Entretanto, la consultora de pentesting ha descuidado a sus clientes de siempre.

**Criterio para abandonarla (60 días, es decir, a principios de enero de 2027):** menos de 2 sprints firmados y **pagados al menos al 50 % sin depender de SECURE**. Si el cliente solo compra cuando la ayuda paga la mitad, es que no tiene un dolor real.

---

## Idea 3. Paquete ciber-regulatorio para medtech y neurotech

**Defectos fatales o casi fatales**
- **La credibilidad de un solo fundador frente a la FDA o un organismo notificado.** El comprador asume un riesgo regulatorio de millones: un rechazo por ciberseguridad o, como en el caso Illumina, 9,8 M$ por la False Claims Act (neuro_bio.md). Elegirá a quien tenga historial. Blue Goat dice haber apoyado más de 275 solicitudes sin rechazos (dato autopromocional, neuro_bio.md).
- **No tiene historial en el sector regulado.** Necesita dominar ISO 14971, AAMI TIR57/SW96 y la IEC 81001-5-1 y presentar casos. Un pentester de TI generalista no los tiene.
- **Hay pocos clientes y no tienen dinero.** Las startups neuro españolas que se pueden nombrar son unas pocas (INBRAIN, Neuroelectrics, Bitbrain) y "tienen pocos fondos antes de su ronda" (neuro_bio.md). Los que tienen dinero, como Precision o Synchron, compran en EE. UU.
- **Responsabilidad.** Si un dossier contribuye a un rechazo o a un caso FCA, hace falta una RC profesional alta.

**Quién lo hace ya.** Blue Goat Cyber tiene una oferta específica para la UE con MDR premarket, postmarket y threat modeling (https://bluegoatcyber.com/eu/services/eu-mdr-premarket-cybersecurity). También TÜV SÜD (https://www.tuvsud.com/en/industries/medical-devices/cybersecurity), UL (https://www.ul.com/services/iec-81001-5-1-cybersecurity-compliance-medical-devices), Intertek (https://www.intertek.com/medical/connected-technologies/iec-81001-5-1-compliance/), Bureau Veritas (https://cybersecurity.bureauveritas.com/services/iot/medical-devices), DQS (https://www.dqsglobal.com/en/explore/blog/mdr-iec-81001-5-1), Pure Global (https://www.pureglobal.com/es/services/medical-device-cybersecurity), Complife (https://www.complifegroup.com/2026/02/10/cybersecurity-regulatory-mdr-ivdr/) y MedCrypt (neuro_bio.md).

**Comoditización.** Media. Los laboratorios grandes empaquetan la ciberseguridad con la certificación y él no puede certificar. Su ventaja posible está en el precio y en el idioma para startups españolas.

**Cómo fracasa en 12 meses.** Ciclos de venta de 4 a 9 meses ligados a las rondas de los clientes. Cierra 1 o 2 proyectos de 8-15 k€ y no tiene un flujo recurrente **[INTERPRETACIÓN]**.

**Criterio para abandonarla (60 días):** tras 20 conversaciones con fabricantes (incluidos los responsables de asuntos regulatorios), ninguno acepta una propuesta pagada, o todos piden casos previos de FDA o MDR que no tiene.

---

## Idea 4. Auditorías de seguridad y privacidad de neurodatos

**Defectos fatales o casi fatales**
- **El mercado es diminuto.** Los cascos EEG wearables suman unos 145,8 M$ en el mundo (neuro_bio.md). Si el mercado del hardware es tan pequeño, el del servicio de auditoría de privacidad de ese hardware lo es mucho más **[INTERPRETACIÓN]**.
- **La ley que lo exige está en otra parte.** Las obligaciones fuertes son de Colorado, California, Connecticut y Montana. En España no hay ley de neuroderechos: la Carta de Derechos Digitales es programática (neuro_bio.md). Un cliente estadounidense contratará a un despacho estadounidense.
- **Riesgo legal de la investigación como marketing.** Auditar el backend en la nube de un fabricante sin autorización puede ser ilegal. La divulgación responsable sobre el dispositivo propio es más segura, pero aun así puede traer amenazas legales **[INTERPRETACIÓN; conviene consultar a un abogado]**.

**Quién lo hace ya.** VeraSafe ofrece asesoría de cumplimiento para neurotecnología (https://verasafe.com/blog/mental-privacy-in-neurotech-and-the-growing-risk-for-organizations/). Secure Privacy publica guías de consentimiento de neurodatos bajo RGPD y CCPA (https://www.secureprivacy.ai/blog/neurodata-consent-eeg-brain-computer-interface-data-gdpr-ccpa). Los despachos que analizan estas leyes (Cooley, Goodwin, Constangy, MinterEllison) son los competidores naturales en la parte legal (https://constangy.com/constangy-cyber-advisor/colorado-amends-its-privacy-act-by-adding-protection-for-neural-data). La investigación académica sobre seguridad de BCI viene de 2019 (https://arxiv.org/pdf/1908.03536).

**Comoditización.** Una EIPD con un anexo de neurodatos la puede hacer cualquier DPO o despacho.

**Cómo fracasa en 12 meses.** Publica una buena investigación sobre un casco EEG, recibe aplausos en congresos y cero contratos, porque los fabricantes de consumo no tienen presupuesto de seguridad. Según la Neurorights Foundation, menos de la mitad cifra los datos (neuro_bio.md): eso indica justo que no les importa pagar por seguridad **[INTERPRETACIÓN]**.

**Criterio para abandonarla (60 días):** ningún fabricante de EEG de consumo de la UE o EE. UU. acepta una llamada de venta tras la publicación. O la publicación genera interés de prensa pero ninguna petición de presupuesto.

---

## Idea 5. Kit "Proveedor de Defensa" (ENS, NIS2 y HSEM)

**Defectos fatales o casi fatales**
- **La HSEM no se puede pedir por adelantado.** Exige una carta de expectativas firmada por el órgano de contratación o por la prima. Tarda unos 6 meses y la HPS hasta otros 6. Para RESERVADO se exigen 5 años de nacionalidad española (defensa.md, sección 4.1). El "kit" solo sirve a quien ya tiene un patrocinador, y quien lo tiene recibe la guía de la propia prima y de la DGAM, que no cobra tasas.
- **La NIS2 no está transpuesta en España.** Sigue en anteproyecto y la Comisión ha llevado a España ante el TJUE (defensa.md). La demanda "inminente" lleva así desde 2024.
- **La consultoría ENS está muy comoditizada.** Hay decenas de consultoras ENS para pymes (por ejemplo, https://asest.es/story/consultoria-ens-para-pymes/ y S2 Grupo, https://s2grupo.es/el-esquema-nacional-de-seguridad-ens). La certificación la emiten entidades acreditadas por ENAC (https://www.enac.es/documents/7020/15713/np-esquema-ens/e518dc60-5b66-4d54-81cb-a6f343c803e7) y el consultor no puede certificar.
- **El dinero no está donde se cree.** El 80,9 % del bloque de telecom y ciber de los PEM ya está adjudicado a primas (defensa.md).

**Quién lo hace ya.** Consultoras ENS e ISO 27001 de todo tamaño, las Big4, S2 Grupo (que además tiene un acuerdo con Indra desde noviembre de 2025, defensa.md) y consultoras nuevas de defensa e industria (https://www.vozpopuli.com/economia/empresas/ivan-redondo-lanza-una-nueva-consultora-en-industria-defensa-seguridad-y-energias-renovables.html).

**Comoditización.** Muy alta en ENS. La parte de HSEM es un trámite documental sin tasas.

**Cómo fracasa en 12 meses.** Vende proyectos de ENS a precio de mercado (bajo) a pymes industriales, compitiendo con cien consultoras. Las primas no le derivan clientes porque no tiene relación con ellas.

**Criterio para abandonarla (60 días):** ningún responsable de compras o de Participación Industrial de Indra, GMV, Oesía o Navantia acepta una reunión. O ninguna pyme con una carta de expectativas real aparece en el embudo.

---

## Idea 6. Pentesting de drones y sistemas autónomos

**Defectos fatales o casi fatales**
- **Las grandes construyen su equipo propio.** Las empresas con mucha financiación contratan dentro. Un ejemplo es Autonomous Teaming, que busca un "Drone Hacking & Cybersecurity Expert" (https://autonomous-teaming.jobs.personio.de/job/1975508) y un ingeniero de seguridad embebida y anti-spoofing para UAV (https://autonomous-teaming.jobs.personio.de/job/1971728). Helsing, Quantum o Tekever con cientos de millones (defensa.md) no van a confiar su C2 militar a un autónomo español sin habilitación.
- **Habilitaciones y control de exportación.** El trabajo sobre sistemas militares exige normalmente HPS o HSEM (con patrocinador, ver la idea 5). Los datos técnicos pueden estar sujetos a ITAR o al reglamento de doble uso (defensa.md, sección 4.2).
- **Hace falta equipo y laboratorio de RF.** Probar enlaces de datos y GNSS exige equipo de RF y un entorno de pruebas legal. Emitir o interferir sin licencia está regulado **[INTERPRETACIÓN]**.

**Quién lo hace ya.** Red Balloon Security tiene una oferta específica de UAS y estaciones de control (https://redballoonsecurity.com/industry-solutions/uas-hardening). También Dark Wolf con "UAS Cyber" (https://darkwolf.io/capability-details/), Resillion con pruebas de drones para una agencia de gobierno (https://www.resillion.com/case-studies/drone-testing/) y Bishop Fox, que trabajó para Parrot (https://images.bishopfox.com/prod-1437/Documents/Use-Cases/2022-Q3-CustomerStory-Parrot-1.pdf). Hay incluso formación comercial de "hack our drone" (https://ringzer0.training/hack-our-drone/). En España, Alias Robotics (EIC Accelerator 2024, 2,5 M€ de la UE) hace pentesting automatizado de robots (https://eic.ec.europa.eu/impact/alias-robotics_en). Su página no menciona drones, pero es el competidor natural si da el salto.

**Comoditización.** Baja en la parte militar, porque la barrera es la confianza. En drones civiles es media: es pentesting IoT con otra etiqueta.

**Cómo fracasa en 12 meses.** Ninguna empresa de drones de defensa le deja acercarse sin habilitación. Termina haciendo pentest IoT genérico a fabricantes civiles pequeños, que pagan poco.

**Criterio para abandonarla (60 días):** de 15 fabricantes europeos contactados (civiles y duales), ninguno acepta un piloto pagado de al menos 10 k€, o todos exigen habilitación o un equipo mayor.

---

## Idea 7. SaaS de inteligencia de licitaciones de defensa

**Defectos fatales o casi fatales**
- **La información es pública y gratuita.** TED, PLACSP, el portal Funding & Tenders y las páginas de convocatorias de EUDIS para pymes (https://eudis.europa.eu/eudis-tracks/sme-calls_en) lo publican todo.
- **El mercado útil es pequeño y paga poco.** Hablamos de unas 300-500 pymes objetivo en España (defensa.md). Muchas convocatorias son de consorcio y anuales: el EDF cerró en septiembre de 2026 y DIANA en julio (defensa.md). El cliente necesita la herramienta dos veces al año, así que la cancelará **[INTERPRETACIÓN]**.
- **No aprovecha su ventaja.** Nada de esto usa su perfil de ciberseguridad.

**Quién lo hace ya.** Tendios, una plataforma española de licitaciones con alertas, catalogada en datos.gob.es (https://datos.gob.es/es/empresas/tendios). Gobierto Contratación (https://contratos.gobierto.es/licitaciones/4802099). Artabro Tender (https://datos.gob.es/es/aplicaciones/artabro-tender). Las consultoras de subvenciones que el propio fundador usa como fuente: PNO Innovation (https://www.pnoinnovation.com/es/insights/el-eic-amplia-las-oportunidades-para-tecnologias-de-doble-uso-y-lanza-una-nueva-convocatoria-para-impulsar-la-innovacion-en-defensa/) y Hezelburcht (https://www.hezelburcht.com/en/news/european-defence-fund-edf-2026-open-for-applications-until-29-september/), que además redactan la propuesta y cobran a éxito. Y cualquier usuario de ChatGPT, porque montar alertas con IA ya es un tema de prensa generalista (https://emprendedores.es/ideas-de-negocio/chatgpt-contratacion-publica).

**Comoditización.** Extrema. Es un wrapper de un LLM sobre datos abiertos.

**Cómo fracasa en 12 meses.** Consigue 10-20 suscriptores a 50-150 €/mes y una rotación alta tras el cierre de cada convocatoria. No cubre ni su tiempo.

**Criterio para abandonarla (60 días):** menos de 10 pymes pagan una preventa anual de al menos 500 €. Si piden que además les escriba la propuesta, el negocio es una consultoría de subvenciones, no un SaaS.

---

## Idea 8. Migración post-cuántica (PQC)

**Defectos fatales o casi fatales**
- **El plazo de diciembre de 2026 es para los Estados, no para las empresas.** La hoja de ruta de la UE pide a los **Estados miembros** que inicien los inventarios a finales de 2026. Para las empresas, los plazos duros son 2030 y 2035 (chips.md). Para una pyme no hay urgencia hoy.
- **España no tiene hoja de ruta del CCN** (chips.md). No hay un regulador nacional que obligue todavía.
- **El comprador de verdad es grande.** Bancos (DORA), telecos y administraciones compran a IBM, a las Big4 o a vendedores especializados.

**Quién lo hace ya.** IBM Quantum Safe (Explorer, Advisor, Remediator), Keyfactor/InfoSec Global AgileSec, SandboxAQ AQtive Guard, CryptoNext COMPASS, Quantum Xchange (comprada por Keyfactor), PQStation, QryptoCyber, ISARA, Tychon y AppViewX. Hay herramientas open source: CBOMkit, donado a la Linux Foundation, y el estándar CycloneDX 1.6 CBOM (https://postquantum.com/post-quantum/cryptographic-inventory-vendors/). Incluso existe un escáner PQC gratuito en PyPI (https://pypi.org/project/cryptoscan-pqc/).

**Comoditización.** El inventario se está automatizando con herramientas gratuitas. La "hoja de ruta" es un documento que la consultora de turno añade a su catálogo.

**Cómo fracasa en 12 meses.** Las pymes dicen "en 2029 hablamos" y las grandes no compran a un autónomo. Solo la variante de auditoría de canal lateral de implementaciones PQC embebidas tiene un comprador técnico, pero ese mercado es el de la idea 12.

**Criterio para abandonarla (60 días):** ningún cliente sin obligación DORA, NIS2 o federal estadounidense acepta pagar un inventario. O el único interés que aparece es de bancos que exigen ISO 27001, seguros altos y homologación de proveedor.

---

## Idea 9. "Mini-Palantir" de vigilancia marítima con datos abiertos

**Defectos fatales o casi fatales**
- **El competidor es gratis y está financiado por filántropos.** Skylight (AI2, fundado por Paul G. Allen) es gratuito para gobiernos, organismos regionales de pesca y ONG cualificadas. Ya tiene un agente de IA, Shippy, que usa datos de Global Fishing Watch y SkyTruth y trabaja con UNODC (https://skylight.global/news/shippy-launch).
- **El cliente público europeo ya tiene la herramienta.** La EMSA ofrece Integrated Maritime Services con Automated Behaviour Monitoring: unos 18 millones de posiciones al día, encuentros en el mar, cambios bruscos de rumbo y velocidad, y entrada en zonas. Lo usan las autoridades de los Estados miembros (https://eu.vlex.com/vid/automated-behaviour-monitoring-abm-873420309).
- **El cliente privado lo compra a líderes con capital.** Windward fue comprada por FTV Capital y salió de la Bolsa de Londres (https://www.shipmanagementinternational.com/news/maritime-ai-company-windward-acquired-by-ftv-capital-delists-from-london-stock-exchange). Tiene un "Maritime Anomaly Detector" (https://windward.ai/maritime-anomaly-detector/).
- **Ventas lentas, regulación y ninguna ventaja propia.** Los clientes son autoridades portuarias, Salvamento y agencias, con ciclos de compra largos. Hay riesgo de control de exportación y de RGPD en el OSINT (defensa.md, sección 3). DIANA exige TRL 4 y acepta a un 5 % (defensa.md). Los datos satelitales "puros" no aprovechan la ventaja del fundador (chips.md, sección 2.6).

**Comoditización.** Total en la capa de datos (AIS y Sentinel son abiertos). La capa de análisis la regala Skylight.

**Cómo fracasa en 12 meses.** Gasta 6-9 meses en un prototipo, no supera DIANA ni EUDIS y no encuentra un cliente que pague por algo que Skylight o la EMSA le dan gratis. Además se ha comido el tiempo de la consultora.

**Criterio para abandonarla (60 días):** después de 10 entrevistas con usuarios finales (Salvamento Marítimo, Capitanías, Guardia Civil del Mar, aseguradoras P&I), ninguno nombra una carencia que no cubran Skylight, la EMSA o Windward, o ninguno tiene una partida presupuestaria.

---

## Idea 10. Preparación CMMC para proveedores europeos

**Defecto fatal: la premisa ya no existe.**
- La fase 2 (la certificación por un C3PAO) se **suspendió el 13-07-2026**. Se aceptan autoevaluaciones y los requisitos de terceros se van quitando de los contratos (https://www.wilmerhale.com/en/insights/client-alerts/20260720-pentagon-suspends-cmmc-phase-2-requirements-and-launches-review-of-cybersecurity-certification-program ; https://secureframe.com/hub/cmmc/news-updates-2026.md).
- Según el resumen interno citado por la prensa, el 76,6 % de los subcontratistas no había oído nada de sus primas sobre la pausa (Secureframe, arriba). El proveedor español de segundo nivel ni sabe que existe la norma.
- Hacerse C3PAO es inviable: todo el personal del proceso de evaluación necesita una investigación de antecedentes Tier 3 (SF-86) o una equivalencia que decide el DoD, y la organización pasa una revisión FOCI (https://www.law.cornell.edu/cfr/text/32/170.9). Las evaluaciones conjuntas en el extranjero las dirige DIBCAC con asesores gubernamentales del país socio (https://www.dcma.mil/Portals/31/Documents/DIBCAC/International-Joint-Assessments-Final(20251209).pdf).
- Lo que queda es la obligación DFARS 7012 / NIST 800-171 y el riesgo FCA de las autoevaluaciones. Como resume Wolf Theiss, el riesgo "migrates from regulation into the subcontract" (https://www.wolftheiss.com/insights/cmmc-phase-ii-suspended-what-changes-and-what-does-not-for-european-suppliers-to-the-us-defence-industrial-base/). Hay negocio de consultoría NIST 800-171, pero sin fecha que obligue a comprar.

**Quién lo hace ya.** Advania se presenta como la primera RPO de Europa (https://www.advania.se/en/news/advania-first-in-europe-cmmc). Secura (Países Bajos) ofrece readiness e implantación (https://www.secura.com/services/process/cmmc-compliance). También Protiviti (https://www.protiviti.com/sites/default/files/2026-10/whitepaper_cybersecurity_maturity_model_certification_cmmc_2.0_en.pdf), Kiteworks y cientos de RPO estadounidenses.

**Cómo fracasa en 12 meses.** Invierte en formación CCP/CCA y en marketing para un mercado en pausa indefinida. Si la fase 2 vuelve, lo hará para "una población más estrecha" (opción en estudio, según Secureframe).

**Criterio para abandonarla:** ya se cumple. Solo debería reabrirla si el DoW publica una fecha de reinicio de la fase 2 que incluya a proveedores extranjeros **y** si una prima española o europea le pide expresamente ayuda con NIST 800-171 para su cadena.

---

## Idea 11. SaaS de SBOM y gestión de vulnerabilidades para embebidos

**Defectos fatales o casi fatales**
- **Los competidores tienen capital y producto maduro.** ONEKEY analiza binarios de firmware sin código fuente y tiene un Compliance Wizard para CRA, IEC 62443-4-2 y EN 18031 (https://www.onekey.com/compliance-wizard/). Lo distribuye Advantech (https://alitek.advantech.com/products/ONEKEY--Automated-IoT-Security-Analysis/sub/97582f70-7d9c-4939-b5d1-d2eb2d03e1d6) y Gartner lo evalúa (https://www.gartner.com/reviews/product/onekey-platform). Finite State ofrece Living SBOM, VEX, borradores de notificación y expediente técnico (https://www.finitestate.io/cra). Cybellum está en marketplaces (https://platform.softwareone.com/product/cybellum/PCP-4157-5292).
- **La gama baja es gratis.** OWASP Dependency-Track (https://owasp.org/www-project-dependency-track/), Syft/Grype y el SBOM que regalan los fabricantes de chips (Espressif, arriba).
- **Le falta capital para construirlo.** Un SaaS de análisis de binarios con base de datos de vulnerabilidades y VEX es un producto de varios años de ingeniería. NEOTEC exige 20 k€ de capital social (neuro_bio.md, chips.md), cuatro veces su presupuesto.

**Comoditización.** Altísima. El SBOM es un formato estándar (SPDX o CycloneDX) que generan herramientas libres.

**Cómo fracasa en 12 meses.** Construye un MVP sobre Dependency-Track y el cliente le pregunta qué le aporta frente a ONEKEY o frente a la versión gratuita. No tiene respuesta, o la respuesta es "mi servicio", y entonces vuelve a la idea 1.

**Criterio para abandonarla (60 días):** menos de 5 cartas de intención de pago **por el software** (no por el servicio), o los clientes dicen que ya usan o han evaluado ONEKEY, Finite State, Cybellum o Dependency-Track.

---

## Idea 12. Laboratorio de canal lateral e inyección de fallos

**Defectos fatales o casi fatales**
- **Credibilidad y acreditación.** El cliente que paga de verdad (fabricantes de MCU, secure elements y pagos) necesita una evaluación reconocida: Common Criteria, SOGIS, EMVCo, LINCE o EUCC. Un laboratorio acreditado no es asumible al inicio (chips.md).
- **ChipWhisperer no basta.** Los clientes serios piden sondas EM, inyección de fallos por láser y plataformas comerciales. Estos laboratorios se montan entre socios industriales (por ejemplo, el laboratorio láser de AlphaNov y eShard: https://www.eshard.com/blog/alphanov-eshard-laser-fault-injection-lab).
- **El mercado se está concentrando en grandes.** Keysight compró Riscure, Cadence compró Secure-IC y Applus+ compró jtsec (chips.md).

**Quién lo hace ya.** Applus+ Laboratories (evaluaciones Common Criteria hasta EAL7 y SPA/SEMA, EMI y glitching, presentados ya en 2016: https://applus.com/global/en/news/applus+-presents-cost-effective-solutions-to-evaluate-cryptographic-module-security-against-current-threats). También Keysight/Riscure, eShard con DEKRA (https://www.dekra.com/en/dekra-eshard-collaboration/), Fraunhofer AISEC (https://www.aisec.fraunhofer.de/content/dam/aisec/Dokumente/Flyer/Fraunhofer_AISEC_HWS_Lab_pub.pdf), IOActive (https://www.ioactive.com/service/full-stack-security-assessments/side-channel-analysis/), Raelize y NewAE/lowRISC (chips.md). En España, Tarlogic con hardware y Bluetooth (chips.md).

**Comoditización.** Baja en el extremo alto, que sin embargo no puede alcanzar. Media en el extremo bajo: el glitching de un IoT barato lo enseñan ya en formaciones abiertas.

**Cómo fracasa en 12 meses.** Hace demos espectaculares en congresos, pero los fabricantes IoT pyme no pagan auditorías de canal lateral porque el CRA no las exige explícitamente. Y los fabricantes de chips eligen laboratorios acreditados.

**Criterio para abandonarla (60 días, como negocio independiente):** ningún fabricante paga al menos 10 k€ por una evaluación no acreditada. Puede quedarse como **diferenciador** dentro de los pentest de firmware de las ideas 2 y 3, no como empresa.

---

## Idea 13. Detección de drones con SDR barato

**Defectos fatales o casi fatales**
- **Compite contra empresas cotizadas que ya hacen exactamente eso con software.** DroneShield presentó en julio de 2026 RfAI-3, un motor de inteligencia RF de banda ancha pensado para drones basados en SDR. Tiene más de 22 M$ en contratos con un cliente militar europeo y 206 M$ de ingresos comprometidos para 2026 (https://www.defenceconnect.com.au/industry/18614-droneshield-reveals-new-rf-detection-solution-and-multi-million-european-contracts-in-trading-update). Dedrone es ya de Axon (defensa.md). En Europa están Sensofusion (45 M€), ARMMO con validación de la OTAN según prensa (defensa.md), Indra y los programas estatales.
- **La versión barata ya es open source.** Hay decodificadores de DJI DroneID por ingeniería inversa en GitHub (RUB-SysSec/DroneSecurity, proto17/dji_droneid) que corren en un AntSDR E200 (https://www.rtl-sdr.com/dji-droneid-detection-running-on-the-antsdr-e200-cpu/ ; https://www.jaredwatkins.com/research/drone-detection/open-source/). Si el producto es "SDR barato más DroneID", el núcleo ya es gratis.
- **El cliente es el Estado y la neutralización le está reservada.** En España, las Fuerzas y Cuerpos de Seguridad del Estado adquieren los equipos y existen sistemas estatales (SIGLO-CD) y programas de Defensa (SUCCAUL) (https://www.escudodigital.com/interior/seguridad-nacional-drones-amenaza-creciente-espana.html). El cliente privado (eventos, infraestructuras) solo puede detectar y necesita integradores certificados. Decodificar comunicaciones de terceros puede chocar con el secreto de las comunicaciones **[INTERPRETACIÓN, requiere opinión legal]**.
- **Necesita hardware, pruebas de campo, certificaciones y validación con amenazas reales.** El Programa Coincidente exige un demostrador con funcionalidad militar (defensa.md). Nada de esto cabe en 5.000 €. Los propios ficheros califican las ideas de hardware de "no accesibles" (defensa.md, sección 3).
- **Los drones de amenaza real evitan precisamente la detección por firma.** Por eso DroneShield ha tenido que pasar a detección de banda ancha.

**Comoditización.** La detección de drones comerciales DJI es ya una commodity. La de drones militares o caseros con SDR es una carrera de I+D que exige capital.

**Cómo fracasa en 12 meses.** Tiene un prototipo que detecta un DJI Mini en el jardín, ningún cliente lo certifica y ningún integrador lo distribuye frente a DroneShield o Dedrone. Pasa un año sin ingresos.

**Criterio para abandonarla (60 días):** si en 60 días no hay un integrador o una prima que firme una carta de intención para un piloto **pagado**, y un abogado que confirme por escrito que el modo de detección es legal para clientes privados en España, debe abandonarla. Ambas cosas son improbables **[INTERPRETACIÓN]**.

---

## Las 3 ideas más peligrosas

1. **Idea 13: detección de drones con SDR.** Combina todos los riesgos: hardware, pruebas de campo, regulación del espectro y de la neutralización, un cliente estatal con ciclos de años, y competidores cotizados con más de 200 M$ de ingresos comprometidos y producto basado en SDR (DroneShield RfAI-3). Además, la versión barata ya es open source. Es la más "Anduril" y por eso la más letal para alguien con 5.000 €.
2. **Idea 10: CMMC.** No es peligrosa por difícil, sino porque **su premisa es falsa a fecha de hoy**: la fase 2 está suspendida desde el 13-07-2026 sin fecha de reinicio. Invertir en formación y marketing CMMC es apostar por una decisión política de Washington.
3. **Idea 9: "Mini-Palantir" marítimo.** Consume meses de desarrollo para competir con Skylight, que es gratis, con la EMSA, que ya sirve a las autoridades de la UE, y con Windward, respaldada por capital privado. Tiene ciclos de venta públicos y riesgo de control de exportación y RGPD, y no aprovecha la ventaja del fundador.

Menciones para no hacer: la **idea 7** (SaaS de licitaciones; es un wrapper de LLM sobre datos públicos, con Tendios y las consultoras de subvenciones delante) y la **idea 11** (SaaS de SBOM; ONEKEY, Finite State y Dependency-Track gratis la aplastan).

## Las que mejor sobreviven al ataque

1. **Idea 2, con la idea 1 como extensión y no como producto independiente.** Sobrevive porque es pentest de firmware y producto con un informe orientado al CRA y a la EN 18031. Es lo que ya hace su consultora, con coste marginal casi cero, y la obligación es real y ya vigente. Condiciones: **no depender de SECURE** (por el calendario y la selección), venderla también sin la ayuda y ofrecer el PSIRT solo como anexo opcional, con un contrato que limite la responsabilidad y una póliza revisada.
2. **Idea 3: paquete ciber-regulatorio medtech.** Sobrevive porque el dolor es real (la FDA puede denegar la autorización solo por ciberseguridad, neuro_bio.md), los precios de referencia son altos (Blue Goat cobra desde 15 k$ solo por el pentest) y existe un hueco en español y en euros. Su debilidad es la credibilidad: necesita uno o dos casos y probablemente una alianza con una consultora de asuntos regulatorios que ya tenga clientes.
3. **Idea 12, solo como diferenciador técnico y no como empresa.** Las demos de canal lateral y glitching, incluidas las de implementaciones PQC embebidas, sirven para ganar los proyectos de las ideas 2 y 3 y para formación de pago (modelo Raelize). No sirven como laboratorio independiente.

**Advertencia final:** incluso las supervivientes son una consultora con otro nombre. Ninguna de las 13 da en 12 meses un negocio escalable sin capital. La versión honesta del plan es hacer crecer Brighouse Security Labs con un vertical CRA y medtech, no fundar "la Anduril española".
