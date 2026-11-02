# Chips, semiconductores y deep tech adyacente: oportunidades de bajo capital para un fundador solo (España/UE)

**Fecha del análisis:** 2 de noviembre de 2026
**Perfil:** fundador en solitario, formación en informática y ciberseguridad (consultora de pentesting, investigación publicada), sabe vender, capital inferior a 5.000 €.
**Convención:** cada cifra lleva su fuente. **[INCIERTO]** marca un dato no verificado o con fuentes débiles. **[INTERPRETACIÓN]** marca una conclusión propia, no un dato.

---

## Resumen ejecutivo

1. Fabricar o diseñar chips propios no es viable con menos de 5.000 €, salvo prototipos educativos (Tiny Tapeout). El dinero público español y europeo va a empresas con decenas o cientos de empleados (Openchip ~300, Semidynamics, Qilimanjaro).
2. La oportunidad real está en el **cumplimiento regulatorio de seguridad de producto**. El **Cyber Resilience Act (CRA)** obliga desde el **11-sep-2026** a notificar vulnerabilidades explotadas e incidentes graves en 24 h, 72 h y 14 días, y se aplica por completo el **11-dic-2027**. Además, la UE financia hasta **30.000 € por pyme** (50 % de cofinanciación) para pagar trabajos de cumplimiento del CRA, incluidas auditorías y pentesting.
3. La **migración a criptografía postcuántica (PQC)** tiene ya fechas firmes. La UE pide inventarios nacionales para el 31-dic-2026, casos de alto riesgo migrados para 2030 y riesgo medio para 2035. NIST IR 8547 final (27-oct-2026) declara RSA/ECC obsoletos tras 2030 y prohibidos tras 2035.
4. Recomendación **[INTERPRETACIÓN]**: un servicio "CRA + PQC readiness" para fabricantes pyme de dispositivos conectados, con gestión de vulnerabilidades y PSIRT externalizado, inventario criptográfico (CBOM) y pentesting de firmware y hardware. Se apalanca en la consultora actual, no necesita capital y tiene fechas legales que fuerzan la compra.

---

## 1. Mercado y financiación

### 1.1 EU Chips Act (1.0) y Chips Act 2.0

| Dato | Valor | Fuente |
|---|---|---|
| Inversión pública y privada movilizada por el Chips Act 1.0 | >52.000 M€ | https://aeneas-office.org/2026/06/03/european-commission-unveils-proposed-chips-act-2-0/ |
| Resultados del 1.0 | 5 líneas piloto, red de centros de competencia; plataforma de diseño en la nube "prevista para otoño de 2026" | https://sciencebusiness.net/industry/chips-act-20-hits-right-notes-what-about-budget |
| Objetivo del 20 % de cuota mundial en 2030 | El Tribunal de Cuentas Europeo lo considera improbable; Intel canceló Magdeburgo (30.000 M€) | https://sciencebusiness.net/industry/chips-act-20-hits-right-notes-what-about-budget |
| Presentación del Chips Act 2.0 | 3-jun-2026, dentro del "Technology Sovereignty Package" | https://aeneas-office.org/2026/06/03/european-commission-unveils-proposed-chips-act-2-0/ ; https://digital-strategy.ec.europa.eu/en/library/proposal-chips-act-20 |
| Medidas del 2.0 | Compra pública innovadora, "demand accelerators/forum", "Grand Challenges" tipo DARPA, proyectos First-of-a-Kind, sello "Semiconductor Regions of Excellence", plataforma B2B de cadena de suministro, más capacidad de diseño avanzado | https://aeneas-office.org/2026/06/03/european-commission-unveils-proposed-chips-act-2-0/ ; https://sciencebusiness.net/industry/chips-act-20-hits-right-notes-what-about-budget |
| Presupuesto del 2.0 | **Sin cifra**; depende del MFF 2028-2034 | https://sciencebusiness.net/industry/chips-act-20-hits-right-notes-what-about-budget ; https://www.digitaleurope.org/news/chips-act-2-0-ambition-requires-funding/ |
| Calendario legislativo | La Comisión espera de 12 a 18 meses de negociación, es decir, adopción hacia finales de 2027 o 2028 **[INCIERTO]** | https://sciencebusiness.net/industry/chips-act-20-hits-right-notes-what-about-budget |
| Mercado global de semiconductores en 2030 (proyección de la CE) | 1,37 billones € | https://aeneas-office.org/2026/06/03/european-commission-unveils-proposed-chips-act-2-0/ |

**Lectura:** el 2.0 no incluye medidas específicas de seguridad de chips ni de startups pequeñas, más allá de la compra pública ([sciencebusiness](https://sciencebusiness.net/industry/chips-act-20-hits-right-notes-what-about-budget)). Durante 2027 no habrá dinero nuevo relevante para un fundador solo.

### 1.2 PERTE Chip (12.250 M€): qué se ha ejecutado de verdad

| Fecha | Dato | Fuente |
|---|---|---|
| dic-2023 | Solo 50,4 M€ adjudicados ("ejecución casi nula" según el PP) | https://forbes.es/ultima-hora/406720/pp-exige-impulsar-el-perte-chip-por-su-ejecucion-casi-nula-y-un-plan-formativo-de-semiconductores-en-espana/ |
| dic-2025 | La industria (Aesemi) estima que se han empleado ~1.000 M€ de 12.250 M€; el PERTE "termina en junio de 2026" y el sector pide prórroga | https://rtvc.es/congreso-chipnation-gran-canaria-4-diciembre-2025/ |
| 2-oct-2026 | El ministro Carlos Cuerpo admite en el Congreso que se han movilizado **2.248 M€ de 12.250 M€ (recorte del 82 %)**. El eje de fábricas (9.350 M€) va al ~10 % de ejecución; los otros tres ejes entre el 60 % y el 70 % | https://www.que.es/2026/10/02/gobierno-recorta-plan-chips-fondos-europeos/ |
| Reorientación | Hacia proyectos menos intensivos en capital (p. ej., fotónica en Vigo) | https://www.que.es/2026/10/02/gobierno-recorta-plan-chips-fondos-europeos/ |
| Ecosistema | ~200 empresas de semiconductores en España, 14 en Canarias | https://rtvc.es/congreso-chipnation-gran-canaria-4-diciembre-2025/ |
| Programa UNICO Chips JU I+D (RD 269/2026, BOE 2-abr-2026) | Hasta 12,35 M€ para cofinanciar entidades españolas seleccionadas en convocatorias Chips JU (36 beneficiarios, 14 proyectos); tope del 70 % de costes; actividades hasta el 31-dic-2030 | https://www.boe.es/diario_boe/txt.php?id=BOE-A-2026-7447 |

**[INCIERTO]** No he encontrado un documento oficial con el desglose de lo pagado (frente a lo comprometido o adjudicado) a octubre de 2026. La cifra de 2.248 M€ procede de declaraciones del ministro recogidas por prensa.

### 1.3 Startups españolas de chips (financiación 2025-2026)

| Empresa | Qué hace | Financiación reciente | Fuente |
|---|---|---|---|
| **Openchip** (Barcelona) | Chips RISC-V para IA y HPC, fabless; fundada en 2021 por GTD y el BSC; ~300 empleados | SETT: **115,77 M€** (jun-2026) vía el instrumento Next Tech (PRTR). Antes, préstamos de la Generalitat (10 M€, ampliados a 35 M€) | https://startups.one.gob.es/news/note/spain-s-sett-backs-openchip-with-115-8m-to-build-europe-s-chip-autonomy ; https://en.ara.cat/economy/the-government-raises-the-loan-to-openchip-to-35m-to-maintain-the-catalan-microprocessor-project_1_5763469.html |
| **Substrate AI** | IA/chips | SETT 19,1 M€ dentro de una ronda de 39 M€ | https://startups.one.gob.es/news/note/spain-s-sett-backs-openchip-with-115-8m-to-build-europe-s-chip-autonomy |
| **Semidynamics** (Barcelona) | IP RISC-V y chips de inferencia de IA "memory-centric" | Inversión estratégica de **SK hynix** (8-abr-2026, importe no revelado); 45 M€ acumulados en financiación no dilutiva europea y española | https://www.prnewswire.com/es/comunicados-de-prensa/semidynamics-consigue-una-inversion-para-impulsar-chips-de-inferencia-de-ia-centrados-en-la-memoria-302736983.html |
| **Qilimanjaro Quantum Tech** (Barcelona) | Computación cuántica (fluxonium, multimodal) | Serie A, primer cierre de **19,6 M€** (14-oct-2026): Indra/IndraMind 10 M€ y SETT 9,6 M€; cierre previsto en el 4T 2026 | https://thequantuminsider.com/2026/10/14/qilimanjaro-quantum-tech-announces-nearly-e20-million-first-close-of-series-a-led-by-indra-group/ |
| Celestia Chip, Wooptix (Canarias) | Spin-offs de centros canarios | n/d | https://rtvc.es/congreso-chipnation-gran-canaria-4-diciembre-2025/ |

**Lectura [INTERPRETACIÓN]:** el capital público español (SETT) va a apuestas de decenas o centenares de millones con equipos grandes. No es un camino para un fundador solo, aunque estas empresas sí pueden ser **clientes** de servicios de seguridad, por ejemplo para auditar IP RISC-V o el firmware de arranque seguro.

### 1.4 Ecosistema RISC-V y financiación de diseño europeo

| Dato | Valor | Fuente |
|---|---|---|
| SoC RISC-V previstos en 2031 (SHD Group) | ~35.900 M unidades; ~318.000 M$ de ingresos; IP de CPU ~1.900 M$ | https://riscv.org/blog/shd-forecast-2026/ |
| Aceleradores de IA RISC-V en 2031 | ~9.060 M de unidades, ~222.000 M$ (~70 % de los ingresos) | https://riscv.org/blog/shd-forecast-2026/ |
| Cuota en automoción (hasta 2031) | Del 2,2 % al 3,9 % | https://riscv.org/blog/shd-forecast-2026/ |
| Top 2025 de financiación de semis en Europa (tech.eu) | NXP 1.000 M€ (préstamo del BEI), FMC 100 M€, Axelera AI 61,6 M€ (subvención), Paragraf 55 M$, Corintis 49 M$, Swave 33 M€... | https://tech.eu/2026/06/29/semiconductors-10-companies-that-raised-the-most-in-2025/ |
| Axelera AI | >250 M$ en 2025-2026 (anunciada como la mayor ronda de semis de la UE) | https://www.design-reuse.com/news/202530200-axelera-raises-250m-in-largest-eu-semi-round-ever/ |

**[INCIERTO]** No hay una cifra agregada fiable de la financiación de startups de chiplets en la UE. Las rondas grandes son de aceleradores de IA (Axelera, Vsora), no de chiplets puros.

---

## 2. Puntos de entrada de bajo capital (evaluados para el perfil)

Escala: **Capital** (lo que cuesta empezar) / **Encaje** (con un perfil de ciberseguridad) / **Urgencia** (fecha legal que obliga a comprar).

### 2.1 Cumplimiento del CRA para fabricantes de dispositivos conectados (máxima prioridad)

**Fechas y obligaciones verificadas**

| Hito | Fecha | Fuente |
|---|---|---|
| Entra en vigor el Reglamento (UE) 2024/2847 | dic-2024 | https://www.cyberresilienceact.eu/news/cra-notified-bodies-rules-apply-11-june-2026.html |
| Reglas de organismos notificados (Cap. IV, arts. 35-51) | **11-jun-2026**. A 8-sep-2026 **no había ningún organismo notificado designado en NANDO** | https://www.cyberresilienceact.eu/news/cra-notified-bodies-rules-apply-11-june-2026.html |
| Obligaciones de notificación (art. 14) | **11-sep-2026**. Se abre la Single Reporting Platform (SRP) de ENISA | https://www.jonesday.com/en/insights/2026/07/eu-cyber-resilience-act-24hour-reporting-duties-start-september-11-2026 ; https://helpnetsecurity.com/2026/09/14/enisa-cra-single-reporting-platform |
| Plazos de notificación | Alerta temprana en **24 h**; notificación en **72 h**; informe final **14 días** después de que exista la corrección (vulnerabilidades explotadas) o **1 mes** después (incidentes graves). Se notifica simultáneamente a ENISA y al CSIRT coordinador. Hay que informar a los usuarios afectados | https://www.jonesday.com/en/insights/2026/07/eu-cyber-resilience-act-24hour-reporting-duties-start-september-11-2026 |
| Alcance de la notificación | **Todos** los productos con elementos digitales, **incluidos los ya comercializados** antes del 11-dic-2027. No es retroactiva para explotaciones conocidas antes del 11-sep-2026 | https://www.jonesday.com/en/insights/2026/07/eu-cyber-resilience-act-24hour-reporting-duties-start-september-11-2026 |
| Guía de la Comisión sobre notificación | 27-jul-2026 (no vinculante) | https://www.jonesday.com/en/insights/2026/07/eu-cyber-resilience-act-24hour-reporting-duties-start-september-11-2026 |
| Objetivo de organismos notificados "suficientes" | 11-dic-2026 (art. 35(2)) | https://www.cyberresilienceact.eu/news/cra-notified-bodies-rules-apply-11-june-2026.html |
| **Aplicación completa** | **11-dic-2027** | https://www.jonesday.com/en/insights/2026/07/eu-cyber-resilience-act-24hour-reporting-duties-start-september-11-2026 |
| Multas | Hasta 15 M€ o el 2,5 % de la facturación mundial | https://www.jonesday.com/en/insights/2026/07/eu-cyber-resilience-act-24hour-reporting-duties-start-september-11-2026 |
| Categorías | Por defecto: autoevaluación (Módulo A). Importante Clase I: autoevaluación solo si se aplican normas armonizadas o certificación. Clase II: tercero obligatorio. Críticos: posible certificado europeo | https://www.cyberresilienceact.eu/news/cra-notified-bodies-rules-apply-11-june-2026.html |

**Autoridades en España [INCIERTO, fuente privada]:** la vigilancia del mercado correspondería al Ministerio de Consumo (productos de consumo) y a MINTUR (industriales). INCIBE actuaría como apoyo técnico y el CCN/OCC como base de la evaluación de conformidad. No consta una designación formal (fuente del 4-oct-2026): https://cdn.presencis.com/regulations/cra/national/es

**Tamaño y coste del problema para el cliente**

- Impacto agregado estimado por la CE (2022): ~29.000 M€ de costes de cumplimiento. Estimaciones de consultoras: de 20.000 € (producto simple, autoevaluación) a más de 500.000 € (complejo, con tercero). Un sensor IoT simple: hasta 80.000 € iniciales y hasta 90.000 €/año. Calculadora de cyberresilienceact.eu: 78.300 € más 13.500 €/año para un producto básico. Fuente (artículo de opinión, cifras de consultoras): https://circleid.com/posts/eu-cyber-resilience-act-costs-and-economic-impact **[INCIERTO: estimaciones no oficiales]**
- Encuesta de ENISA a pymes sobre el CRA, publicada el 24-jun-2026 (no pude leer las cifras del PDF): https://www.enisa.europa.eu/node/19417

**Dinero para que el cliente pague (clave comercial)**

- **Proyecto SECURE, 2.ª convocatoria abierta:** 11,5 M€ en total; **hasta 30.000 € por pyme al 50 %**. Abre el 1-oct-2026 y **cierra el 11-dic-2026**. Costes elegibles: auditorías, apoyo a la certificación, redacción de políticas, **pruebas de vulnerabilidades y pentesting**, gestión de incidentes, cadena de suministro, formación y servicios profesionales: https://www.cyberresilienceact.eu/es/news/secure-second-open-call-1-october-2026-cra-sme-funding.html
  - **[INTERPRETACIÓN]** Es una herramienta de venta inmediata: ayudar a pymes clientes a solicitarla antes del 11-dic-2026, con el fundador como proveedor del servicio.

**Regulación adyacente ya obligatoria:** desde el **1-ago-2025**, el acto delegado de la Directiva de Equipos Radioeléctricos (RED) exige ciberseguridad en equipos de radio conectados (normas EN 18031-1/-2/-3). Cuando se aplican sus restricciones, interviene un organismo notificado: https://www.sgs.com/en-se/news/2025/06/red-cybersecurity-requirements-mandatory-on-1-august-2025

**Servicios concretos que puede vender un fundador solo [INTERPRETACIÓN]:**
1. **"CRA gap assessment"** de precio fijo para fabricantes pyme (IoT, OT, electrónica de consumo, software embebido): clasificación del producto (por defecto, Clase I o II), análisis de requisitos del Anexo I y plan de acción.
2. **PSIRT / gestión de vulnerabilidades como servicio:** política de divulgación coordinada, SBOM, triaje y redacción de las notificaciones de 24 h, 72 h y 14 días en la SRP. Es **recurrente** (mensual) y ya obligatorio.
3. **Pentesting de firmware y producto** como evidencia técnica del expediente.
4. Plantillas o SaaS ligero (por ejemplo, un generador de documentación técnica CRA o un flujo de notificación) como segunda fase productizada.

### 2.2 Migración a criptografía postcuántica (PQC)

| Hito | Fecha | Fuente |
|---|---|---|
| Normas NIST FIPS 203 (ML-KEM), 204 (ML-DSA), 205 (SLH-DSA) | ago-2024; HQC elegido en marzo de 2025 como KEM alternativo (FIPS en desarrollo) | https://labs.cloudsecurityalliance.org/research/csa-research-note-nist-ir8547-pqc-transition-20261030-csa-st/ |
| **NIST IR 8547 final** | **27-oct-2026**: algoritmos de clave pública vulnerables (RSA, ECDSA, EdDSA, DH/ECDH) **obsoletos tras 2030 y prohibidos tras 2035, sea cual sea el tamaño de clave** (el borrador solo aplicaba 2030 a 112 bits). ML-KEM-768 recomendado por defecto | https://labs.cloudsecurityalliance.org/research/csa-research-note-nist-ir8547-pqc-transition-20261030-csa-st/ **[verificar con NIST directamente: la fuente es una nota de CSA]** |
| EE. UU. (efecto en proveedores europeos que venden allí) | EO 14412 / OMB M-26-15: PQC para intercambio de claves antes del 31-dic-2030 y firmas antes del 31-dic-2031; regla FAR propuesta hacia el 19-dic-2026 | https://labs.cloudsecurityalliance.org/research/csa-research-note-nist-ir8547-pqc-transition-20261030-csa-st/ **[INCIERTO]** |
| **Hoja de ruta coordinada UE (NIS CG)** | Publicada en junio de 2025 | https://pqshield.com/eu-pqc-workstream-publishes-a-coordinated-implementation-roadmap-for-the-transition-to-post-quantum-cryptography/ |
| UE: **31-dic-2026** | Los Estados miembros inician la transición: inventarios y mapas de dependencias criptográficas (incluida la cadena de suministro), concienciación, implicación de la industria | https://pqshield.com/eu-pqc-workstream-publishes-a-coordinated-implementation-roadmap-for-the-transition-to-post-quantum-cryptography/ |
| UE: **31-dic-2030** | Casos de **alto riesgo** migrados; "quantum-vulnerable public key mechanisms shall not be used stand-alone after the end of 2030" | https://pqshield.com/eu-pqc-workstream-publishes-a-coordinated-implementation-roadmap-for-the-transition-to-post-quantum-cryptography/ |
| UE: **31-dic-2035** | Casos de **riesgo medio** y tantos sistemas como sea posible | https://pqshield.com/eu-pqc-workstream-publishes-a-coordinated-implementation-roadmap-for-the-transition-to-post-quantum-cryptography/ |
| Recomendación de la CE sobre PQC | abr-2024 | https://www.esmartcity.es/2024/04/15/comision-europea-publica-recomendacion-transicion-hacia-criptografia-poscuantica-europa |
| Mercado de servicios PQC (ABI Research) | ~255 M$ a nivel global a finales de 2025; los servicios (descubrimiento, inventario, estrategia) dominan la fase inicial; mercado de "miles de millones" en 2030 | https://www.abiresearch.com/press/new-algorithmic-standards-and-migration-policy-timelines-propel-post-quantum-cryptography-toward-billion-dollar-market-by-2030 |
| España | **[INCIERTO]** No he encontrado una hoja de ruta nacional PQC publicada por el CCN a fecha de hoy; la UE la exige para finales de 2026, así que su publicación es probable en las próximas semanas o meses | (búsqueda sin resultados oficiales) |

**Servicios de bajo capital [INTERPRETACIÓN]:**
- **Inventario criptográfico / CBOM** (qué algoritmos, librerías, certificados y HSM usa el cliente), análisis de riesgo "harvest-now-decrypt-later" y plan de cripto-agilidad. Es exactamente la fase que, según ABI, concentra el gasto inicial.
- **Auditoría de implementaciones PQC en embebido** (canales laterales en ML-KEM/ML-DSA sobre microcontroladores). Encaja con la investigación publicada del fundador. La herramienta de partida (ChipWhisperer) cuesta del orden de cientos a pocos miles de dólares **[INCIERTO: confirmar precios en newae.com]**.
- **Combinar con el CRA:** el Anexo I exige proteger la confidencialidad con mecanismos "state of the art". Vender "CRA + preparación PQC" en el mismo informe es un argumento natural, ya que los productos de 2027 seguirán en el mercado después de 2030 **[INTERPRETACIÓN]**.

### 2.3 Seguridad de hardware: firmware, auditorías embebidas, canales laterales y fault injection

- La demanda existe y consolida: Keysight compró Riscure (2024): https://securitydelta.nl/news/overview/riscure-acquired-by-keysight-technologies ; Cadence compra Secure-IC (anunciado el 21-ene-2025): https://us.design-reuse.com/news/57317/cadence-secure-ic-acquisition.html ; Applus+ compró jtsec (2022): https://www.appluslaboratories.com/global/en/about-us/inbrief/applus-jtsec
- **Capital:** empezar por la **revisión de firmware** (extracción, reversing, arranque seguro, actualizaciones OTA) cuesta casi cero. El banco de canal lateral y glitching es asequible con herramientas abiertas (ChipWhisperer, NewAE). Un laboratorio acreditado (Common Criteria, LINCE, EUCC) **no** es asumible al inicio: requiere acreditación ENAC/CCN y personal.
- **Encaje:** muy alto. **Urgencia:** media-alta, impulsada por el CRA, el RED (EN 18031) y la IEC 62443-4.
- **Garantía de cadena de suministro / troyanos hardware:** como negocio para un fundador solo es **poco viable** **[INTERPRETACIÓN]**: requiere microscopía y desprocesado (equipos de 6 cifras) y los clientes son defensa o gobierno. Una variante viable es la revisión documental de la cadena de suministro y el SBOM/HBOM dentro del CRA.

### 2.4 EDA abierto y diseño de IP RISC-V (open PDK)

| Opción | Coste | Fuente |
|---|---|---|
| Tiny Tapeout (SKY130, IHP SG13G2, GF180) | Precio orientativo: **~70 € por tile y ~300 € por devkit** (declaración del fundador, may-2025, "por determinar"); el precio actual depende del tamaño, el shuttle y si el diseño es analógico. Ver la calculadora en app.tinytapeout.com | https://www.eenewseurope.com/en/tiny-tapeout-sees-industrial-boost-as-it-recovers-from-efabless-closure/ ; https://tinytapeout.com/ **[INCIERTO: precio vigente]** |
| Uso industrial de Tiny Tapeout | Industria = 38 % del programa (frente al 14 % en 2023) | https://www.eenewseurope.com/en/tiny-tapeout-sees-industrial-boost-as-it-recovers-from-efabless-closure/ |
| Cierre de eFabless | mar-2025; ChipFoundry.io sube de 10.000 $ a 15.000 $ por 100 chips | https://www.eenewseurope.com/en/tiny-tapeout-sees-industrial-boost-as-it-recovers-from-efabless-closure/ |
| wafer.space (GF180) | **7.000 $ por 1.000 chips** | https://tinytapeout.com/news/wafer-space-partnership/ |
| Shuttles 2026 | TTSKY26a agotado; TTSKY26b con tapeout el 11-may-2026; abiertos SKY26d y GF26c | https://tinytapeout.com/news/ttsky26b-opens/ ; https://tinytapeout.com/ |

**Lectura [INTERPRETACIÓN]:** sirve para **I+D y marketing técnico**, por ejemplo un demostrador abierto de contramedidas contra canal lateral o un núcleo PQC en silicio que sirva de prueba de credibilidad. No sirve como negocio: el mercado de IP lo dominan empresas con certificación y soporte.

### 2.5 Software de edge AI

- Mercado en crecimiento (aceleradores de IA RISC-V ~9.060 M de unidades en 2031: https://riscv.org/blog/shd-forecast-2026/), pero muy competido y sin ventaja específica para el perfil. **[INTERPRETACIÓN]** Nicho viable: **seguridad de modelos en el edge** (extracción de modelos por canal lateral, integridad del firmware de NPUs), como extensión del servicio de hardware.

### 2.6 Espacio y datos satelitales

- **EU Space Act** (propuesta del 25-jun-2025): exige a los operadores espaciales gestión de riesgos, evaluación de ciberseguridad, cifrado, notificación de incidentes y **pruebas de penetración dirigidas por amenazas (TLPT)**. Se aplica también a proveedores no UE. Aplicación prevista el **12-ene-2030** (borrador): https://www.skadden.com/insights/publications/2025/07/the-eus-new-cybersecurity-law-for-the-space-sector **[INCIERTO: texto en negociación]**
- **[INTERPRETACIÓN]** La ciberseguridad de segmento terreno y de satélites pequeños es un nicho a 3 o 4 años vista para el perfil, compatible con ESA BIC. Los servicios de datos satelitales puros (Copernicus) no aprovechan la ventaja del fundador.

---

## 3. Financiación no dilutiva

| Instrumento | Importe / condiciones | Encaje | Fuente |
|---|---|---|---|
| **SECURE (CRA para pymes)** | Hasta 30.000 € al 50 %; cierra el 11-dic-2026 | Para **clientes** del fundador (y quizá para el propio fundador como pyme) | https://www.cyberresilienceact.eu/es/news/secure-second-open-call-1-october-2026-cra-sme-funding.html |
| **CDTI Neotec 2026** | 20,38 M€ en total; hasta 250.000 € (325.000 € si se contratan doctores), cubre el 70 % (85 %); empresa de <3 años, **capital social mínimo de 20.000 €**; plazo 14-abr a 14-may-2026 (cerrado; próxima convocatoria previsiblemente en primavera de 2027 **[INCIERTO]**) | Alto si se crea una SL tecnológica con producto (p. ej., una herramienta de CRA o PQC). **Ojo:** el capital mínimo de 20.000 € supera el presupuesto actual | https://www.cdti.es/en/noticias/cdti-innovacion-convocatoria-neotec-2026-subvencion-ebts-empresas-tecnologia |
| **Chips JU (convocatorias 2026)** | ~300 M€; temas entre 5 y 70 M€; consorcios internacionales; plazos de sep-2026 (cerrados) | Bajo para un fundador solo; solo como socio pequeño en un consorcio | https://www.hezelburcht.com/en/news/chips-ju-2026-launched-new-calls-for-europes-nano-electronic-chip-technologies/ ; https://www.chips-ju.europa.eu/Open-and-Upcoming-Calls |
| UNICO Chips JU I+D | Cofinanciación nacional de los seleccionados por Chips JU (12,35 M€) | Solo si se entra en un consorcio | https://www.boe.es/diario_boe/txt.php?id=BOE-A-2026-7447 |
| **Centros de competencia en España** | **MicroNanoSpain** (coordina AESEMI; CSIC, BSC, UPM, UPV, UPC; 3 M€ nacionales con el mismo importe de la CE) y **PIXSpain** (fotónica, 1 M€) | Gratis o de bajo coste: formación, acceso a plataformas de diseño y salas blancas; "Venture Builder" próximamente. No hace falta ser socio | https://micronanospain.org/ ; https://digital.gob.es/content/dam/portal-mtdfp/comunicacion/comunicacion_setid/2025/10/2025-10-28/20251028_NdP_adjudicacionesCHIPSJUdocx.pdf |
| **EU Chips Design Platform** | Coordina imec (12 socios); acceso en la nube a EDA comercial, IP, ruta a silicio y programa para startups; incorporación de pymes "a partir de principios de 2026", con despliegue "en otoño de 2026" según otra fuente | Medio (útil si se diseña IP de seguridad) | https://www.design-reuse.com/news/202501727-imec-coordinates-eu-chips-design-platform/ ; https://sciencebusiness.net/industry/chips-act-20-hits-right-notes-what-about-budget |
| **ESA BIC** (Madrid, Barcelona, Castilla y León, Castellón...) | Madrid: hasta 50.000 € en 2 años más incubación; otras sedes anuncian 60.000 € **[INCIERTO]** | Medio (si se pivota a ciberseguridad espacial) | https://www.madrimasd.org/emprendedores/esa-bic-comunidad-madrid/beneficios-los-participantes?lan=en ; https://capital-riesgo.es/es/articles/esa-bic-barcelona-abre-una-nueva-convocatoria-para-seleccionar-e-incubar-startups-del-sector-espacial/ |
| Talento | Déficit de más de 75.000 trabajadores en semis en la UE en 2030 (ECSA) | Formación pagada como línea de ingreso | https://www.eenewseurope.com/en/semiconductor-talent-gap-semi-europe-brussels/ |

---

## 4. Barreras y qué evitar

| Barrera | Dato | Fuente |
|---|---|---|
| Coste de tapeout | MPW a 180 nm: 5.000-15.000 $; 28 nm MPW: 50.000-150.000 $ (máscaras completas de 1 a 3 M$); 7 nm de 5 a 10 M$ en máscaras y más de 30 M$ en total; 3-5 nm más de 30-100 M$ | https://siliconanalysts.com/analysis/fabless-startup-tapeout-cost-guide |
| Talento | >75.000 personas de déficit en la UE en 2030; solo el 28 % de los graduados STEM en campos relevantes | https://www.eenewseurope.com/en/semiconductor-talent-gap-semi-europe-brussels/ |
| Plazos | Chips Act 2.0: de 12 a 18 meses de negociación; PERTE con ejecución del 18 % | https://sciencebusiness.net/industry/chips-act-20-hits-right-notes-what-about-budget ; https://www.que.es/2026/10/02/gobierno-recorta-plan-chips-fondos-europeos/ |
| Organismos notificados CRA | Ninguno designado a sep-2026, lo que genera un cuello de botella para las Clases I y II | https://www.cyberresilienceact.eu/news/cra-notified-bodies-rules-apply-11-june-2026.html |
| Normas armonizadas CRA | **[INCIERTO]** Estado de publicación no confirmado en las fuentes consultadas | — |

**Evitar [INTERPRETACIÓN]:**
- Diseñar silicio propio para vender (requiere 6 o 7 cifras y ciclos de 18 a 36 meses).
- Competir en IP RISC-V genérica o en aceleradores de IA (Openchip, Semidynamics y Axelera tienen cientos de millones).
- Intentar ser **laboratorio acreditado** u **organismo notificado** desde el primer día (ENAC, CCN, seguros, personal). Mejor colaborar o subcontratar con ellos.
- Depender de subvenciones como fuente principal: PERTE y Chips JU son lentos, van a consorcios y exigen cofinanciación.
- Vender "PQC" en abstracto: hay que venderlo atado a un plazo y a un regulador concreto (CRA, NIS2, DORA, contratos con EE. UU.).

---

## 5. Casos de estudio (empresas pequeñas de seguridad hardware, criptografía o diseño)

| Empresa | Origen | Modelo | Resultado | Fuente | Nota |
|---|---|---|---|---|---|
| **NewAE Technology** (Canadá) | 2013; Colin O'Flynn durante su doctorado, con su pareja; ChipWhisperer nace de la tesis | Hardware abierto (canal lateral y fault injection) más formación; "ventas casi inmediatas"; campaña en Kickstarter (Hackaday) | 6 empleados al venderse; comprada por **lowRISC** en jun-2022 | https://entrevestor.com/blog/newae-sold-to-britains-lowrisc ; https://www.newae.com/about ; https://hackaday.com/2015/page/381/ | **[INCIERTO]** Que fuera 100 % bootstrapped no está confirmado explícitamente |
| **jtsec Beyond IT Security** (Granada) | 2017, Javier Tallón | Laboratorio de evaluación (Common Criteria, LINCE, ETSI EN 303 645, IEC 62443-4) más herramienta CCToolBox | Más de 50 profesionales; integrada en **Applus+ Laboratories** en 2022 | https://www.appluslaboratories.com/global/en/about-us/inbrief/applus-jtsec | El caso español más cercano al perfil; no hay datos públicos de inversión externa **[INCIERTO: bootstrapped]** |
| **Tarlogic Security** (Galicia/Madrid) | Sep-2011, hermanos Tarascó, 2 personas | Pentesting, más IoT/Bluetooth/hardware hacking, más producto (BlueTrust, Acrylic WiFi) | ~100 empleados a los 10 años | https://www.tarlogic.com/news/10-years-of-tarlogic-security/ | El artículo sugiere voluntad de "control total" pero no confirma que fuera bootstrapped **[INCIERTO]** |
| **Raelize** (Róterdam) | Cristofaro Mune y Niek Timmers (investigadores en fault injection) | Consultoría, pruebas y **formación** de seguridad de dispositivos (revisiones de bootloader ROM y SoC) | Empresa pequeña, con formación en Ringzer0, hardwear.io y Recon | https://raelize.com/ ; https://ringzer0.training/fault-injection-characterization/ | Modelo replicable: investigación publicada, luego formación y consultoría. Tamaño y fecha de fundación no publicados **[INCIERTO]** |
| **Cryptography Research Inc.** (EE. UU.) | 1995; Paul Kocher (descubridor del DPA) | Consultoría más **licencias de patentes** de contramedidas DPA | Comprada por Rambus por **342,5 M$** (6-jun-2011) | https://en.wikipedia.org/wiki/Cryptography_Research | Muestra el techo del modelo de investigación a IP |
| (Contraste) Riscure y Secure-IC | Laboratorios y IP de seguridad | Escala media | Compradas por Keysight (2024) y Cadence (2025) | https://securitydelta.nl/news/overview/riscure-acquired-by-keysight-technologies ; https://us.design-reuse.com/news/57317/cadence-secure-ic-acquisition.html | Confirma el apetito de compra de la industria de EDA y test por la seguridad hardware |

**Patrón común [INTERPRETACIÓN]:** investigación pública, después formación o herramientas, después consultoría o servicio recurrente, y finalmente producto o laboratorio. Salida habitual: adquisición por un laboratorio de certificación (Applus+, SGS, TÜV) o una empresa de EDA o test (Keysight, Cadence, Rambus).

---

## 6. Huecos concretos para un fundador solo con perfil de ciberseguridad

Ordenados por relación entre urgencia y capital necesario **[INTERPRETACIÓN sobre los datos anteriores]**:

1. **"PSIRT-as-a-Service" CRA para pymes fabricantes** (urgencia **ya vigente** desde el 11-sep-2026). Las notificaciones de 24 h y 72 h a ENISA aplican también a productos ya vendidos; una pyme sin equipo de seguridad no puede cubrir ese turno. Modelo: cuota mensual (política de divulgación coordinada, monitorización de CVE frente al SBOM, triaje, redacción y envío a la SRP). Fuentes: Jones Day y ENISA SRP (arriba).
2. **"CRA Readiness Sprint" de precio cerrado más gestión de la ayuda SECURE** (venta en noviembre y diciembre de 2026). Se ofrece la evaluación y se ayuda al cliente a pedir los 30.000 € al 50 % antes del **11-dic-2026**.
3. **Pentesting de producto IoT/OT con informe orientado al CRA y a EN 18031**: el RED ya obliga desde agosto de 2025 y el CRA desde diciembre de 2027. Faltan organismos notificados, así que los fabricantes necesitan evidencias de autoevaluación sólidas.
4. **Inventario criptográfico y hoja de ruta PQC** para proveedores de infraestructura crítica, sector financiero (DORA) y proveedores que venden a EE. UU. Los plazos de 2030 y 2035 son ya firmes en la UE y en NIST IR 8547.
5. **Auditoría de implementaciones PQC en embebido (canal lateral y fault injection)**: nicho técnico de alto valor para fabricantes de MCU, HSM y secure elements, y para startups como Openchip o Semidynamics. Arranque con ChipWhisperer (bajo coste).
6. **Formación de pago** (CRA para ingenieros de producto; hardware hacking; PQC para desarrolladores): monetiza la investigación publicada y aprovecha el déficit de talento (más de 75.000 personas).
7. **Medio plazo (2028-2030):** ciberseguridad para operadores espaciales (EU Space Act, TLPT) vía ESA BIC; y asociarse como subcontratista técnico con un futuro organismo notificado CRA español.

**Riesgos del plan:** competencia de las Big4 y de laboratorios (Applus+, SGS, TÜV) en clientes grandes, así que conviene centrarse en pymes; posibles retrasos o cambios por actos delegados del CRA y normas armonizadas aún no confirmadas; responsabilidad profesional, por lo que hace falta un seguro de RC profesional.

---

## Notas metodológicas

- Varias fuentes son despachos o consultoras (Jones Day, Skadden, CSA, cyberresilienceact.eu, presencis). Para obligaciones legales, conviene contrastar con el Reglamento (UE) 2024/2847 en EUR-Lex y con NIST IR 8547 en csrc.nist.gov.
- Las cifras del PERTE de 2025-2026 proceden de prensa (rtvc.es, que.es) que recoge declaraciones del sector y del ministro; no hay un informe oficial de pagos consultado.
- No se ha verificado el precio vigente por tile de Tiny Tapeout ni el estado de las normas armonizadas del CRA.
