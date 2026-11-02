# El juez: veredicto final

**Fecha:** 2026-11-02
**Fundador:** Ian, solo, en España. Pentesting e investigación publicada (Brighouse Security Labs). Sabe vender. Tiene menos de 5.000 € de capital. Le apasionan la defensa, el deep tech y la biotecnología.
**Material leído:** ideas.md, optimista.md, pesimista.md, evaluador.md, defensa.md, neuro_bio.md, chips.md, más 9 verificaciones propias (marcadas **[JUEZ]**).
**Convenciones:** **[EST]** = estimación mía, no es un dato. **[VERIFICAR]** = confírmalo antes de actuar.

---

## 0. Resumen en cinco líneas

1. **Idea n.º 1:** un laboratorio de seguridad de producto conectado. Vende pentest de firmware y hardware a precio cerrado, con un informe de evidencias para el CRA y la EN 18031, y no depende de la ayuda SECURE. Es la idea 2, con la 1 (PSIRT) como anexo y la 12 (canal lateral) y la 8 (PQC) como módulos.
2. **Idea n.º 2:** el mismo laboratorio aplicado a **drones, robots y sistemas autónomos civiles o de doble uso** (la idea 6). Aquí **corrijo al evaluador**, que la ponía 6.ª. Es el puente hacia la ambición de defensa.
3. **Idea n.º 3:** el paquete ciberregulatorio para medtech y neurotech (la idea 3, con la 4 como investigación de marketing). Queda en reserva: se activa solo si falla la vertical de drones o si entra un cliente medtech por su cuenta.
4. **Queda descartado:** construir ahora la "Anduril española" (las ideas 13 y 9) con 5.000 €. El camino a la ambición es servicio → herramienta → producto con TRL 4 → EUDIS, DIANA y NEOTEC, con decisiones fechadas.
5. **El error más caro que hay que evitar:** crear ahora una SL con 20.000 € pensando en NEOTEC 2027. No llega a tiempo y la cuantía mínima del proyecto no encaja (sección 3.5).

---

## 1. Veredicto: TOP 3

### Cómo he juzgado (y en qué me aparto del evaluador)

El evaluador pondera con un objetivo implícito: "maximiza la viabilidad a 12 meses". Yo uso **dos filtros en secuencia**, porque Ian ha pedido dos cosas.

1. **Filtro de supervivencia (eliminatorio).** ¿Factura más de 10.000 € en 90 días con menos de 5.000 € de inversión, sin depender de una subvención con fecha de resolución desconocida?
2. **Filtro de ambición (para ordenar).** De las ideas que sobreviven, ¿cuál construye activos (datos, herramientas, credibilidad y clientes) que sirvan para un producto de defensa o deep tech en 2-3 años?

También penalizo la **dispersión** más que el evaluador. Un fundador solo no puede aprender a la vez la ISO 14971, la IEC 81001-5-1 y la FDA 524B (medtech) y los enlaces C2 y MAVLink (drones). Hay que elegir una vertical.

---

### n.º 1. "Brighouse Product Security Lab": evidencias CRA y EN 18031 para fabricantes de producto conectado

**Qué es:** pentest de producto (firmware, hardware, BLE/Wi-Fi, app y API de nube) a precio cerrado. El entregable está pensado como **evidencia técnica para la autoevaluación del CRA y la EN 18031 (RED)**. El PSIRT se ofrece como anexo opcional y el canal lateral y la PQC como módulos premium.

**Por qué gana:**
- **La obligación ya está vigente.**
  - Desde el 11-09-2026 hay que notificar a ENISA las vulnerabilidades explotadas, también en productos ya vendidos (https://www.jonesday.com/en/insights/2026/07/eu-cyber-resilience-act-24hour-reporting-duties-start-september-11-2026).
  - La RED/EN 18031 es obligatoria desde el 01-08-2025 (https://www.sgs.com/en-se/news/2025/06/red-cybersecurity-requirements-mandatory-on-1-august-2025).
  - La aplicación completa del CRA llega el **11-12-2027**, a 13 meses de hoy.
- **Coste marginal cero.** Ian ya sabe hacer el trabajo que más vale en el sprint.
- **Precios de referencia altos.**
  - Una firma de Dublín publica rangos de 15.000-30.000 € para un pentest manual completo (https://7asecurity.com/blog/2026/04/the-2026-guide-to-penetration-testing-pricing-and-scoping/).
  - Un sprint de 5.000-14.000 € es competitivo.
- **Oferta escasa en la parte alta.** A septiembre de 2026 no había ningún organismo notificado CRA designado (https://www.cyberresilienceact.eu/news/cra-notified-bodies-rules-apply-11-june-2026.html). Por eso los fabricantes necesitan evidencias propias sólidas.

**Quién ganó el debate:**
- **El pesimista gana en la estructura.**
  - No hay que depender de SECURE: el trabajo no puede empezar antes de firmar el acuerdo y no hay fecha de resolución (https://www.cyberresilienceact.eu/news/secure-second-open-call-1-october-2026-cra-sme-funding.html).
  - La selección es competitiva (https://www.secure4sme.eu/cascade-funding/second-open-call).
  - El PSIRT da poco volumen: solo se notifica lo explotado activamente y quien notifica es un representante del fabricante (https://www.enisa.europa.eu/topics/product-security/single-reporting-platform-srp/frequently-asked-questions). Por eso es un anexo y no un negocio propio.
- **El optimista gana en urgencia y precio.**
- **Coincido con el evaluador** en el primer puesto (7,35) y en la combinación B (7,50). **Le corrijo en un punto:** él trata SECURE como el acelerador de la idea. Yo la trato como un **extra**. Si un cliente la consigue, mejor; ninguna venta debe depender de ella.

**Lo que el pesimista tiene razón en recordar:** "es una consultora con otro nombre". Lo acepto para los primeros 12 meses. La sección 4 explica cómo deja de serlo.

---

### n.º 2. Seguridad de drones, robots y sistemas autónomos civiles o de doble uso (la idea 6 en su versión civil)

**Qué es:** el producto n.º 1 aplicado a una vertical concreta.
- **Alcance:** autopilotos, enlaces de datos y C2, estaciones de tierra (GCS), cadena de actualización OTA y API de flota.
- **Cliente:** fabricantes civiles o duales y proveedores de componentes. **No** las primas militares ni el C2 clasificado.
- **Base legal:** los drones y robots civiles entran en el CRA y en la RED, así que el argumento regulatorio es el mismo que en el n.º 1.

**Por qué la subo (aquí me aparto del evaluador, que la ponía 6.ª con 5,90):**
1. **Comparte la mayor parte del trabajo con el n.º 1 [EST].** El firmware, el BLE/RF, la app y la nube son lo mismo. Solo cambian MAVLink, el enlace C2 y el GNSS. El evaluador la puntuó como negocio independiente (rapidez 4, capital 6). Como vertical del n.º 1 casi no añade coste.
2. **Es la única vertical que alimenta la ambición que Ian ha declarado.**
   - La Comisión adoptó el Plan de Acción sobre seguridad de drones y antidrones el 11-02-2026, con certificación antidrón y *sandboxes* (https://www.medialaws.eu/the-commission-action-plan-on-drone-and-counter-drone-security/).
   - BCG estima una demanda antidrón en Europa de 5.000-7.000 M$ en 2029 (https://www.bcg.com/assets/2026/white-paper-countering-the-drone-threat-europes-cuas-opportunity.pdf).
3. **Medtech exige aprender un dominio regulatorio nuevo.** Drones exige aprender un protocolo nuevo. Para un pentester, lo segundo es semanas de trabajo y lo primero meses.

**Quién ganó el debate:**
- **El pesimista gana en los hechos.**
  - Las grandes contratan dentro (Autonomous Teaming busca un "Drone Hacking & Cybersecurity Expert": https://autonomous-teaming.jobs.personio.de/job/1975508).
  - El trabajo militar exige habilitación y conlleva riesgo ITAR o de doble uso.
  - Ya hay competencia especializada: Red Balloon (https://redballoonsecurity.com/industry-solutions/uas-hardening) y Bishop Fox con Parrot.
- **El optimista gana en la dirección:** es el camino más corto de servicio a producto de defensa.
- **Mi síntesis:** se acepta el ataque del pesimista **restringiendo el segmento**.
  - Pymes civiles y duales, proveedores de componentes (autopilotos, *datalinks*, *payloads*, software de GCS) y robots de servicio o industriales.
  - Primas y grandes, solo como **tercero independiente**, que tiene valor en *due diligence* y en evidencias de cumplimiento.
  - Nada clasificado ni con ITAR hasta tener un patrocinador y un abogado (sección 6).

**Condición:** entra a partir del día 30, como **una de las 3 verticales de la prospección** del n.º 1. No es un negocio aparte. Si el día 180 no hay al menos un cliente pagado de drones o robótica, se abandona (sección 5).

---

### n.º 3. Paquete ciberregulatorio para medtech y neurotech (la idea 3, con la 4 como investigación)

**Por qué es tercera y no segunda (el evaluador la ponía 2.ª con 6,60):**
- **Sus ventajas son reales.**
  - Tickets de 8-25 k€; Blue Goat cobra desde unos 15.000 $ solo por el pentest (https://bluegoatcyber.com/eu/services/medical-device-penetration-testing).
  - La FDA puede denegar una autorización solo por ciberseguridad (https://www.govinfo.gov/content/pkg/FR-2025-06-27/html/2025-11669.htm).
  - Es una pasión de Ian.
- **Pero el pesimista gana en lo que pesa con 5.000 €.**
  - Ciclos de venta de 4-9 meses ligados a rondas.
  - Falta de casos FDA o MDR.
  - Competencia de TÜV SÜD, UL, Intertek, Bureau Veritas y Blue Goat.
  - Pocas startups españolas con caja.
- **Y añade dispersión:** compite con el n.º 2 por las mismas horas de aprendizaje.

**Cuándo se activa:**
- Si falla la vertical de drones en el día 180.
- O de forma oportunista, si entra un fabricante medtech por la vía CRA. El CRA cubre los wearables EEG de bienestar que el MDR deja fuera (https://meddeviceguide.com/blog/eu-cyber-resilience-act-nis2-medical-devices-guide), así que el mismo sprint del n.º 1 sirve.
- Para la parte FDA y MDR, **siempre en alianza** con una consultora de asuntos regulatorios. Nunca en solitario.

**Quién ganó el debate:** empate en el valor y el **pesimista** en el calendario. Coincido con el evaluador en las puntuaciones; me aparto en el orden por la penalización por dispersión.

---

## 2. Ideas descartadas (una línea cada una)

- **1. PSIRT como negocio propio:** solo se notifica lo explotado activamente, lo notifica un representante del fabricante y un 24/7 en solitario no es creíble ni asegurable. Queda como **anexo** del n.º 1 (FAQ de ENISA, arriba).
- **4. Auditorías de neurodatos:** el mercado de cascos EEG ronda los 146 M$ y las leyes duras son estadounidenses. Sobrevive solo como **investigación pública** que alimenta el n.º 3.
- **5. Kit "Proveedor de Defensa":** la HSEM exige una carta de expectativas de un patrocinador, la consultoría ENS está comoditizada y el 80,9 % del bloque ciber de los PEM ya está adjudicado a primas.
- **7. SaaS de licitaciones:** es un wrapper de un LLM sobre datos públicos, con Tendios y las consultoras de subvenciones delante, y no usa la ventaja ciber.
- **8. PQC como negocio propio:** el plazo de finales de 2026 es para los Estados, no para las pymes, y el inventario se automatiza con CBOMkit. Queda como **módulo** del n.º 1.
- **9. "Mini-Palantir" marítimo:** Skylight es gratis, la EMSA ya ofrece ABM a las autoridades y Windward tiene capital privado. No usa la ventaja del fundador.
- **10. CMMC:** la fase 2 se suspendió el 13-07-2026 (https://www.wilmerhale.com/en/insights/client-alerts/20260720-pentagon-suspends-cmmc-phase-2-requirements-and-launches-review-of-cybersecurity-certification-program). No hay fecha que obligue a comprar.
- **11. SaaS de SBOM:** ONEKEY, Finite State, Cybellum y Dependency-Track (gratis) ya ocupan el espacio. Se reconsidera solo como herramienta interna del n.º 1.
- **12. Laboratorio de canal lateral como negocio propio:** sin acreditación (Common Criteria, EUCC) no llega al cliente que paga. Queda como **módulo diferenciador** y como formación.
- **13. Detección de drones con SDR:** DroneShield tiene RfAI-3 y más de 200 M$ de ingresos comprometidos (https://www.defenceconnect.com.au/industry/18614-droneshield-reveals-new-rf-detection-solution-and-multi-million-european-contracts-in-trading-update), el núcleo DroneID es open source y el cliente es el Estado. Se descarta **ahora**; la sección 4 la reabre solo con condiciones.

---

## 3. Plan para la idea n.º 1

### 3.1 La oferta (catálogo fijo, con precios publicados)

| Paquete | Contenido | Duración | Precio [EST] |
|---|---|---|---|
| **CRA Express** | Clasificación del producto (por defecto, clase I o II, crítico), análisis de brechas frente al anexo I y la EN 18031, modelo de amenazas y revisión de firmware estática | 4-5 días | **4.500 €** |
| **CRA Evidence Sprint** (producto estrella) | Express + pentest de hardware y firmware (UART/JTAG, extracción, arranque seguro, OTA), radio (BLE/Wi-Fi), app y API de nube, e informe de evidencias por requisito del anexo I con plan de remediación | 10-12 días | **8.500-11.000 €** |
| **Autonomous Systems Sprint** (vertical n.º 2) | Evidence Sprint + MAVLink/C2, GCS, *datalink*, integridad GNSS en banco cableado o jaula y cadena de actualización | 12-15 días | **12.000-18.000 €** |
| **Módulo Hardware+** | Canal lateral y *glitching* (ChipWhisperer) sobre arranque seguro y claves, y revisión de preparación PQC | +3-5 días | **+3.500-6.000 €** |
| **Anexo PSIRT-lite** | Política de divulgación coordinada (CVD), security.txt, monitorización de CVE frente al SBOM, triaje en horario laboral, borradores para la SRP. **Notifica el representante del cliente, no Ian.** Sin compromiso de disponibilidad 24/7 | Mensual | **450-900 €/mes** + *onboarding* de 1.500 € |
| **Retest** | Verificación de las correcciones | 1-2 días | 1.200-2.000 € |

**Reglas comerciales:**
- 50 % a la firma y 50 % a la entrega.
- SECURE nunca es condición. Si el cliente la solicita, Ian le ayuda con la memoria **gratis** y el proyecto, si se concede, se factura en 2027.
- El precio interno mínimo es de 750 €/día efectivo.

### 3.2 Plan de 30 días (del 2 de noviembre al 2 de diciembre de 2026)

| Semana | Acciones | Resultado medible |
|---|---|---|
| **S1 (2-8 nov)** | 1) Contratar la RC profesional (3.4). 2) Contrato tipo con limitación de responsabilidad, carta de autorización de pruebas y NDA (revisión de un abogado, sección 6). 3) Landing page "CRA Evidence Sprint" con los precios y una checklist gratuita "CRA + EN 18031 en 20 preguntas". 4) Lista de 150 cuentas objetivo (3.3) en una hoja o CRM gratuito. 5) Escribir a los clientes actuales de Brighouse que fabrican o integran producto. | Póliza firmada, landing publicada, 150 cuentas y 10 mensajes a la cartera actual |
| **S2 (9-15 nov)** | 1) Prospección: 15 mensajes personalizados al día (LinkedIn y correo) a CTOs y responsables de hardware o calidad, con el gancho "el 11-12-2027 no podrás poner el CE sin el anexo I; las notificaciones ya son obligatorias". 2) Publicar en LinkedIn el primer artículo técnico ("Los 7 fallos de firmware que suspenden el anexo I del CRA", sacado de hallazgos anonimizados). 3) Comprobar si está abierta la convocatoria EUDIS de primavera de 2027 (3.5). | ≥75 contactos y ≥8 respuestas |
| **S3 (16-22 nov)** | 1) Webinar gratuito de 45 minutos, "CRA para fabricantes: qué es obligatorio ya, qué en 2027 y cómo pedir SECURE antes del 11-12", con un clúster o asociación (3.3). 2) Llamadas de diagnóstico de 30 minutos. 3) Empezar la investigación pública n.º 1 (3.3) con dispositivos comprados. | ≥8 llamadas y ≥3 propuestas enviadas |
| **S4 (23 nov-2 dic)** | 1) Seguimiento y cierre. 2) Para quien lo quiera, memoria SECURE antes del 11-12 (gratis, como herramienta de cierre). 3) Primer contacto con 15 fabricantes de drones y robótica (vertical n.º 2). 4) Revisión de las métricas. | **≥1 sprint firmado con un 50 % cobrado sin SECURE**, ≥5 propuestas abiertas y ≥3 conversaciones con drones o robótica |

**Objetivo del día 30:** al menos 1 sprint firmado y cobrado al 50 %, un *pipeline* de al menos 40.000 € en propuestas y la póliza y el contrato en vigor.

### 3.3 Plan de 90 días (hasta el 31 de enero de 2027)

**Objetivos:**
- 4-6 sprints firmados, con **más de 25.000 € facturados** y más de 15.000 € cobrados.
- 1 anexo PSIRT-lite activo.
- 1 cliente de drones o robótica en negociación o firmado.
- 1 investigación publicada con divulgación responsable.
- Charla enviada a RootedCON 2027 (marzo, Madrid) [VERIFICAR el plazo del CFP].

**Los 20 tipos de cliente objetivo**, con empresas españolas o europeas como hipótesis de prospección. **[VERIFICAR el encaje y el contacto de cada una; no he confirmado que no tengan ya proveedor.]**

| # | Tipo de cliente | Ejemplos (hipótesis) |
|---|---|---|
| 1 | Videoporteros y control de accesos IP | Fermax (Valencia), Golmar (Barcelona) |
| 2 | Material eléctrico y domótica conectada | Simon, Orbis |
| 3 | Contadores, analizadores de red y eficiencia energética | Circutor (Terrassa) |
| 4 | Cargadores de vehículo eléctrico | Wallbox (Barcelona), Ingeteam |
| 5 | Inversores fotovoltaicos y almacenamiento | Power Electronics (Valencia), Ingeteam |
| 6 | SAI y electrónica de potencia conectada | Salicru |
| 7 | Automatización de red eléctrica y OT (protecciones, RTU) | ZIV Automation, Ormazabal (Velatia) |
| 8 | Sensores IoT industriales y agrícolas | Libelium (Zaragoza) |
| 9 | Telecomunicaciones, antenas y recepción con gestión remota | Televés (Santiago) |
| 10 | Radio profesional y comunicaciones críticas | Teltronic (Zaragoza) |
| 11 | Autopilotos y aviónica de UAS (vertical n.º 2) | UAV Navigation (Grupo Oesía), Embention (Alicante) |
| 12 | Fabricantes de UAS civiles y duales (vertical n.º 2) | FuVeX, Alpha Unmanned Systems, Quaternium (Valencia) |
| 13 | Ingeniería aeronáutica y UAS (vertical n.º 2) | Aertec Solutions, Arquimea |
| 14 | Robots móviles y de servicio (vertical n.º 2) | Robotnik (Valencia), PAL Robotics (Barcelona) |
| 15 | Neurotecnología y wearables EEG (vía CRA; puente al n.º 3) | Bitbrain (Zaragoza), Neuroelectrics (Barcelona) |
| 16 | Dispositivos sanitarios conectados de clase baja (vía CRA o RED) | Startups de Barcelona Health Hub y BioCat [identificar] |
| 17 | Fabricantes de cerraduras, alarmas y seguridad electrónica | Fabricantes nacionales de alarmas y CCTV [identificar en el directorio de TECNIFUEGO o AES] |
| 18 | Integradores y fabricantes de IoT industrial pyme sin equipo de seguridad | Miembros de clústeres regionales (GAIA en el País Vasco, clústeres TIC autonómicos) |
| 19 | Fabricantes de electrónica bajo contrato (EMS) y diseño, que revenden la evidencia a sus clientes | Casas de diseño electrónico de Barcelona, Valencia y el País Vasco [identificar] |
| 20 | Socios de canal: laboratorios sin capacidad de pentest de firmware que subcontratan, y consultoras GRC o despachos CRA sin técnicos | Laboratorios de ensayo RED, consultoras ISO, despachos con práctica CRA |

**Canales, por prioridad:**
1. **La cartera actual de Brighouse y sus referidos.** Es el canal más barato.
2. **Prospección directa** en LinkedIn y por correo, 15 mensajes al día. Sales Navigator solo durante 2 meses.
3. **Socios de canal** (tipo 20). Un laboratorio RED o una consultora GRC que derive el pentest de firmware vale por 10 clientes.
4. **Clústeres y asociaciones** para webinars: AMETIC, el clúster GAIA, la AEI Ciberseguridad y clústeres TIC regionales. Para drones, AERPAS (Asociación Española de RPAS) y el clúster aeroespacial andaluz Hélice [VERIFICAR nombres y contacto].
5. **Eventos:**
   - RootedCON (marzo de 2027, charla).
   - MWC (marzo de 2027, solo pasillo).
   - Embedded World (Núremberg, marzo de 2027, fabricantes).
   - FEINDEF 2027 (prevista para mayo de 2027 en Madrid) y UNVEX para la vertical de drones [VERIFICAR fechas].

**Investigación y contenido que publicar (en orden):**
1. **Semanas 2-8.** "CRA Readiness Report: 5 dispositivos IoT de consumo vendidos en España frente a la EN 18031". Solo con dispositivos comprados, sin tocar la nube del fabricante sin autorización, con divulgación coordinada y publicación después del plazo de corrección. Sirve de imán de clientes y de prueba de capacidad.
2. **Semanas 6-12 (vertical n.º 2).** Investigación de seguridad en un ecosistema abierto de autopiloto y GCS (PX4/ArduPilot, MAVLink, QGroundControl/Mission Planner), siempre en banco y sin emitir RF fuera de jaula o de cable. Cualquier hallazgo se comunica a los mantenedores. Es la tarjeta de visita ante ingenieros de UAS.
3. **Continuo.** Un artículo técnico cada 2 semanas, con hallazgos anonimizados de los sprints, y una checklist CRA gratuita como imán de clientes.
4. **Más adelante (opcional, para el n.º 3).** Investigación sobre la seguridad de 2 cascos EEG de consumo (coste de unos cientos de euros, según neuro_bio.md).

### 3.4 Forma jurídica y seguros

**Forma jurídica (de noviembre de 2026 a mediados de 2027): seguir como autónomo o con la estructura actual de Brighouse. No crear ahora una SL para NEOTEC.**

- **Si Ian ya es autónomo:** que siga así. Si es nuevo autónomo (sin alta en los 2 años anteriores), la tarifa plana es de unos 80 €/mes durante 12 meses (https://www.billeo.es/blog/tarifa-plana-autonomos-2026) [VERIFICAR la elegibilidad].
- **Si Brighouse ya es una SL con más de 3 años de antigüedad:** no sirve para NEOTEC, porque la empresa debe tener como máximo 3 años desde su inscripción. Hará falta una SL nueva para el producto (sección 4).

**Por qué no crear ahora una SL con 20.000 € para NEOTEC [JUEZ, verificado en la FAQ oficial de NEOTEC 2026]** (https://www.cdti.es/sites/default/files/2026-04/faq_neotec_2026_v1.0.pdf):
- El capital, o capital más **prima de emisión**, debe sumar 20.000 € **íntegramente desembolsados e inscritos antes de presentar** la solicitud.
- La empresa debe estar constituida **al menos 6 meses** y como máximo 3 años antes del cierre del plazo.
- El presupuesto subvencionable va de **175.000 € a 750.000 €**, con un 30 % de cofinanciación propia (al menos 52.500 €).
- El proyecto empieza el 1 de enero del año siguiente.
- **Consecuencia:** para NEOTEC 2027 (cierre previsiblemente en abril o mayo de 2027, igual que en 2026: https://www.cdti.es/en/noticias/cdti-innovacion-convocatoria-neotec-2026-subvencion-ebts-empresas-tecnologia [VERIFICAR la fecha de 2027]), la SL tendría que estar inscrita **ya, en noviembre de 2026**, y Ian debería tener un producto y unos 72.500 € entre capital y cofinanciación. No es realista.
- **Objetivo correcto: NEOTEC 2028.** Crear la SL de producto entre abril y octubre de 2027. Empezar con capital bajo (la Ley 18/2022 permite una SL de 1 € de capital, con reglas de reserva legal [VERIFICAR con un asesor]). Subir a 20.000 € (capital más prima) con aportaciones dinerarias de los ingresos de servicios antes de presentar en 2028.

**Seguros (contratar en la semana 1; es la mayor partida del presupuesto):**
1. **RC profesional** con cobertura de **daños patrimoniales puros**. Tiene que nombrar expresamente la actividad de pruebas de intrusión y auditoría técnica, porque muchas pólizas de "consultores" excluyen el acceso intencionado a sistemas. Hay que pedir que cubra la defensa jurídica y los daños a datos o equipos del cliente durante las pruebas. Referencia de producto: Hiscox Consultores (https://www.hiscox.es/documentos/IPID-Hiscox-Consultores-de-Negocio.pdf). Suma asegurada orientativa: 600.000 € a 1 M€. Prima orientativa: **600-1.500 €/año [EST, VERIFICAR con 2-3 corredores]**.
2. **Ciberriesgos propios** (su portátil y su laboratorio contienen firmware y secretos de clientes). Puede ir en el mismo paquete.
3. **Drones (vertical n.º 2):** si alguna prueba implica vuelo, hace falta un seguro de RC de operador de UAS y el registro como operador ante AESA [VERIFICAR las obligaciones vigentes]. Por defecto, **todas las pruebas se hacen en banco y sin vuelo**.
4. **En el contrato:** limitación de responsabilidad al importe de los honorarios, exclusión de daños indirectos, carta de autorización firmada por quien tiene autoridad sobre el sistema y cláusula de que **la notificación a ENISA la hace el fabricante**.

### 3.5 Financiación no dilutiva: ventanas reales

| Programa | Para quién | Ventana | Qué hacer |
|---|---|---|---|
| **SECURE, 2.ª convocatoria** (hasta 30 k€ al 50 %) | Para **sus clientes** (pymes fabricantes), no para Ian | **Cierra el 11-12-2026.** Resolución sin fecha; ejecución máxima de 180 días (https://www.secure4sme.eu/cascade-funding/second-open-call ; https://english.rvo.nl/funding-portal/secure-digital-europe-programme-cybersecurity) | Herramienta de cierre: escribir la memoria gratis para clientes que firmen. **Nunca** condición de venta |
| **EUDIS Business Accelerator** (bono de 120.000 €, más 50.000 € para los 3 mejores, sin ceder participaciones) | Startups de defensa o doble uso de la UE | **[JUEZ]** La página oficial anuncia 2 cohortes en 2027: primavera (empieza en marzo de 2027) y otoño (empieza en septiembre de 2027, con convocatoria de **abril a junio de 2027**). Para la de primavera indica "5 October - 16 November 2027", una fecha incoherente que probablemente sea 2026: **podría estar abierta ahora, hasta el 16-11-2026** (https://eudis.europa.eu/business-accelerator_en) | 1) **Esta semana**, comprobar en https://www.eudis-business-accelerator.eu/ si está abierta. Si lo está, presentar solo si se puede describir con honestidad un producto de doble uso (probabilidad baja). 2) **Objetivo real: la cohorte de otoño de 2027 (abril-junio de 2027)**, con el prototipo de la sección 4 y la SL constituida [VERIFICAR si exige persona jurídica] |
| **NATO DIANA** (hasta 400 k€: 100 k€ más 300 k€) | Empresa de un país OTAN, con la tecnología bajo su control y **TRL ≥ 4** | La convocatoria de 2027 fue del 2-06 al 3-07-2026, con ~5 % de aceptación (https://www.inventya.com/calls/nato-diana-2027-challenge-call). **La de 2028, previsiblemente de junio a julio de 2027** | Presentar en junio de 2027 solo si se supera la puerta 1 (sección 4). Reto probable: "resiliencia operativa en entornos disputados" |
| **CDTI NEOTEC** (hasta 250 k€ al 70 %) | SL de entre 6 meses y 3 años, con 20 k€ desembolsados | 2027: previsiblemente en abril o mayo (**no elegible de forma realista**). **2028: objetivo** | SL constituida entre abril y octubre de 2027 y capital a 20 k€ antes de la solicitud de 2028 |
| **ENISA, préstamos participativos** (Jóvenes Emprendedores / Emprendedores) | SL con fondos propios equivalentes | Abierto todo el año | Después de constituir la SL y tener ventas. Importes y requisitos [VERIFICAR en enisa.es] |
| **EDF 2027 y Programa Coincidente 2027** | Consorcios / empresa líder | EDF 2026 cerró el 29-09-2026 y la siguiente ronda se espera en 2027. Coincidente 2026 cerró el 27-07 (defensa.md) | Solo como **subcontratista o socio del paquete de ciberseguridad y pruebas** de un consorcio. Empezar a buscar socio en el primer semestre de 2027 |
| **INCIBE Emprende** (incubación y aceleración en ciberseguridad, a través de entidades regionales) | Startups de ciberseguridad | Convocatorias periódicas en varias comunidades (https://www.incibe.es/emprendimiento) | Solicitar en 2027 para la SL de producto: mentoría y red sin coste [VERIFICAR la convocatoria de 2027] |
| **EIC Accelerator** (admite doble uso) | Pyme con TRL ≥ 5 | Propuestas cortas en continuo | **No antes de 2028** |

### 3.6 Presupuesto (menos de 5.000 €)

| Partida | € [EST] |
|---|---|
| RC profesional + ciberriesgos (primer año) | 1.200 |
| Revisión del contrato tipo, la carta de autorización y la consulta sobre control de exportación (abogado, unas 3 h) | 500 |
| Asesor fiscal y laboral (consulta sobre la forma jurídica y NEOTEC) | 200 |
| Normas EN 18031-1/-2/-3 (UNE/CENELEC) | 300 |
| Laboratorio de hardware: ChipWhisperer-Husky o Lite, analizador lógico, adaptadores UART/JTAG/SWD, programador SPI, estación de soldadura y microscopio USB | 900 |
| Radio: HackRF One o equivalente + bolsa o caja de Faraday (**solo recepción y pruebas en jaula**) | 450 |
| Vertical de drones: controlador de vuelo Pixhawk o Holybro + radio de telemetría + kit de banco (**sin vuelo**) | 450 |
| Dispositivos IoT de consumo para la investigación n.º 1 (5 equipos) | 400 |
| Web y dominio, CRM gratuito, Sales Navigator 2 meses | 250 |
| Entrada a RootedCON y desplazamientos (2-3 viajes) | 350 |
| **Total** | **5.000** |

**Regla:** el laboratorio de drones se compra solo cuando haya al menos 2 conversaciones serias con fabricantes de UAS o robótica. Hasta entonces esos 450 € quedan de colchón.

---

## 4. Camino a la ambición: de laboratorio a empresa de producto de defensa en 2-3 años

**Tesis:** Anduril no empezó con armas, sino con ingenieros que conocían el problema del usuario y un producto de software sobre sensores. El equivalente honesto para Ian es este: **los datos y herramientas que salgan de decenas de pentests de drones y robots → un producto de ciberresiliencia para sistemas autónomos**. No la detección RF contra DroneShield, sino el **hueco que nadie cubre bien en Europa**: la seguridad dentro del sistema autónomo.

Precedentes:
- Alias Robotics recibió el EIC Accelerator 2024 con 2,5 M€ para ciberseguridad de robots (https://eic.ec.europa.eu/impact/alias-robotics_en).
- UAV Navigation creció con la entrada de Oesía como socio y canal (https://www.militaryaerospace.com/commercial-aerospace/article/14232309/grupo-oesia-invests-in-the-uav-sector-with-uav-navigation).
- El patrón común es servicio o piloto → validación en un acelerador (DIANA, EUDIS) → una prima como canal → capital tras la tracción (defensa.md §5).

**Candidatos a producto** (se elige uno en la puerta 1, según lo que repitan los clientes):
- **A. "C2 Link Guard":** detección de intrusiones y anomalías en el enlace MAVLink/C2 y en la GCS, más firma de comandos, como módulo de software para autopilotos y GCS.
- **B. "Autonomy Test Harness":** plataforma de pruebas de seguridad continua (fuzzing de MAVLink y DDS/ROS 2, *firmware diffing*, regresiones) que el fabricante ejecuta en su CI. Genera la evidencia del CRA de forma recurrente.
- **C (solo si A o B tienen tracción):** integridad GNSS y RF, detección de *spoofing* a bordo. Es el puente con la idea 13, pero con la tecnología dentro del dron propio.

### Hitos y puertas de decisión

| Fecha | Hito | Puerta de decisión |
|---|---|---|
| **Del día 0 al 6.º mes** (nov. 2026-abr. 2027) | 8-12 sprints, ≥2 clientes de drones o robótica, investigación de MAVLink publicada. Un 20 % del tiempo a herramientas internas reutilizables | **Puerta 1 (30-04-2027).** ¿Hay ≥40 k€ facturados, ≥2 clientes de drones o robótica pagados y ≥3 hallazgos que se repiten entre clientes y que un producto resolvería? **Sí →** crear la SL de producto (mayo de 2027), elegir A o B, prototipo TRL 4 en 8 semanas y presentar a EUDIS de otoño (abril-junio) y a DIANA 2028 (junio-julio). **No →** seguir como laboratorio (el camino de Tarlogic) y reevaluar en el 12.º mes |
| **Del 6.º al 12.º mes** (mayo-dic. 2027) | Prototipo en 1-2 pilotos (de pago o con cofinanciación), primera contratación (pentester junior pagado con los servicios), capital de la SL hacia 20 k€ y búsqueda de un socio de consorcio EDF o Coincidente | **Puerta 2 (11-12-2027, aplicación completa del CRA).** ¿Hay ≥120 k€ de facturación anual y (≥1 piloto de pago del producto o EUDIS/DIANA ganado)? **Sí →** NEOTEC 2028 (presupuesto ≥175 k€), préstamo ENISA e INCIBE Emprende. **No →** el producto queda como herramienta interna del laboratorio, sin buscar financiación de producto |
| **Del 12.º al 24.º mes** (2028) | Producto ≥20 % de los ingresos, ≥3 clientes de producto y una prima o un integrador como canal. Si un cliente prima lo patrocina, pedir HSEM y HPS (carta de expectativas) | **Puerta 3 (31-12-2028).** ¿Hay ≥150 k€ de ARR de producto o un cliente soberano o de una prima? **Sí →** ronda presemilla o semilla (fondos dual-use, coinversión de CDTI Innvierte, más adelante NATO Innovation Fund) y propuesta corta al EIC Accelerator. **No →** vender o licenciar la herramienta a un laboratorio (el patrón jtsec → Applus+) y quedarse como laboratorio rentable |
| **Del 24.º al 36.º mes** (2029) | Si se supera la puerta 3: equipo de 5-10 personas, contratos de defensa y opción C (integridad GNSS y RF). Solo entonces se reabre la detección de drones (idea 13) **como módulo sobre la plataforma propia**, no como producto RF independiente | Gate de la idea 13: ¿hay un integrador o una prima que pague un piloto **y** un informe jurídico favorable sobre detección pasiva para clientes privados? |

**Regla de oro:** durante los primeros 18 meses, **al menos el 70 % del tiempo debe ir a trabajo facturable**. El producto se financia con servicios y con subvenciones, nunca con deuda personal.

---

## 5. Criterios de abandono y métricas

### Criterios de abandono (con fecha)

| Fecha | Criterio | Si se cumple |
|---|---|---|
| **Día 30 (2-12-2026)** | 0 propuestas aceptadas y menos de 3 propuestas enviadas tras ≥150 contactos | Revisar el mensaje y el segmento (¿producto?, ¿precio?, ¿canal?). Todavía no se abandona |
| **Día 60 (2-01-2027)** | **Menos de 2 sprints firmados y cobrados al 50 % sin depender de SECURE** (criterio del pesimista, que adopto) | La tesis "el CRA obliga a comprar ya" ha fallado. Se pasa a pentest genérico de producto e IoT con Brighouse y se espera a 2027 |
| **Día 90 (31-01-2027)** | Menos de 15 k€ facturados, o tasa de cierre menor del 15 % sobre las propuestas | Se baja el precio de entrada (Express) o se cambia al n.º 3 (medtech) como vertical principal |
| **Día 180 (30-04-2027)** | 0 clientes pagados de drones o robótica tras ≥15 fabricantes contactados, o todos exigen habilitación o un equipo mayor | **Se abandona la vertical n.º 2** y se activa el n.º 3 (medtech con un socio regulatorio) |
| **En cualquier momento** | El seguro no cubre el pentest o el riesgo del CRA a un precio razonable (más de 3.000 €/año) | Se deja de vender el anexo PSIRT y se reduce el alcance a pruebas de banco |
| **12.º mes (nov. 2027)** | Menos de 80 k€ de facturación anual | No hay SL de producto ni NEOTEC. La empresa sigue siendo una consultora de una persona y se acepta como tal |
| **Gate de producto** | Menos de 3 cartas de intención **por el software** (no por el servicio) de fabricantes de UAS o robótica antes de dedicar más de 3 meses de ingeniería | No se construye el producto |

### Métricas (revisión semanal, en una hoja)

- **Embudo:** contactos al día (objetivo 15) → tasa de respuesta (≥8 %) → llamadas (≥5 por semana) → propuestas (≥2 por semana) → tasa de cierre (≥25 %).
- **Dinero:** facturado y cobrado acumulado, ticket medio (≥8 k€), tarifa efectiva por día (≥750 €), días de cobro y **cobertura del *pipeline*** (≥3 veces el objetivo del trimestre).
- **Calidad del dolor:** **porcentaje de ventas sin SECURE** (objetivo ≥80 %) y ciclo de venta en días (objetivo ≤30).
- **Recurrencia:** porcentaje de clientes de sprint que contratan el anexo o el retest (≥30 %).
- **Ambición:** clientes de drones o robótica pagados, hallazgos repetidos catalogados (los que alimentan el producto), horas a herramientas internas (≈20 %) y cartas de intención de producto.
- **Marca:** publicaciones al mes (≥2), clientes entrantes por publicación y charlas aceptadas.

---

## 6. Riesgos y lo que hay que verificar con un abogado o asesor

### Riesgos principales (en orden de gravedad)

1. **Penal y contractual: acceso no autorizado.** El art. 197 bis del Código Penal castiga el acceso ilícito a sistemas. Toda prueba necesita una autorización escrita de quien tiene poder de disposición sobre el sistema, también sobre la nube del fabricante. **En la investigación pública, no se toca la infraestructura de terceros.**
2. **Responsabilidad por el CRA.** Si el cliente se retrasa en una notificación de 24 h y culpa al proveedor, el riesgo es grande: hasta 15 M€ o el 2,5 % de la facturación. Por eso el anexo PSIRT deja por contrato la notificación en manos del representante del fabricante y no promete 24/7.
3. **Control de exportación y defensa (vertical n.º 2).**
   - El Reglamento (UE) 2021/821 de doble uso controla ciertos programas de intrusión y equipos de vigilancia de redes.
   - Los datos técnicos de sistemas militares pueden estar sujetos a ITAR o EAR si hay componentes de EE. UU.
   - El material de defensa en España está sujeto a la Ley 53/2007.
   - **No se acepta ningún trabajo militar ni clasificado sin un patrocinador, una HSEM o HPS y una opinión jurídica.**
4. **Radio y espectro.** Emitir, interferir o falsificar GNSS fuera de una jaula de Faraday o de un banco cableado está prohibido sin licencia. Las pruebas son de recepción, cableadas o en jaula. Si hay vuelo, se aplica la normativa de AESA sobre UAS.
5. **Concentración en una persona.** Enfermedad, vacaciones o un cliente grande que absorbe todo el tiempo. Mitigación: subcontratistas de confianza para picos y primera contratación cuando se supere la puerta 2.
6. **Regulatorio.** Las normas armonizadas del CRA y los organismos notificados están todavía pendientes, así que los informes deben citar la versión de la norma y la fecha.
7. **Competencia.** Applus+/jtsec, S2 Grupo, Tarlogic, GlobalSuite y los laboratorios TÜV, SGS y UL. Ian se diferencia por la profundidad técnica en firmware y hardware, por el precio de pyme y por la vertical autónoma.

### Lista de comprobación para el abogado o el asesor (antes del día 15)

**Abogado (mercantil, penal tecnológico y, para la vertical n.º 2, control de exportación):**
- [ ] Contrato tipo: limitación de responsabilidad al importe de los honorarios, exclusión de daños indirectos, propiedad de los hallazgos y derecho a publicar de forma anonimizada.
- [ ] Carta de autorización de pruebas: quién tiene que firmarla (sobre todo si hay nube de terceros, como AWS o Azure, o componentes de proveedores).
- [ ] Política de divulgación coordinada para la investigación pública: plazos, *safe harbour* y riesgo de reclamación del fabricante. ¿Se puede publicar el análisis de un dispositivo comprado sin permiso del fabricante?
- [ ] Cláusula del anexo PSIRT: deja claro que la obligación del art. 14 del CRA y la notificación corresponden al fabricante y a su representante. ¿Puede un tercero ser "Assigned Representative" en la SRP? (La FAQ de ENISA no lo aclara.)
- [ ] Vertical de drones: ¿qué pruebas sobre autopilotos o *datalinks* de uso dual entran en el Reglamento 2021/821 o en la Ley 53/2007? ¿Cuándo hace falta una licencia? ¿Qué hacer si el cliente usa componentes ITAR?
- [ ] Pruebas RF en banco y en jaula: confirmar que no exigen licencia de emisión.

**Asesor fiscal y laboral:**
- [ ] Elegibilidad para la tarifa plana (si es nuevo autónomo) o mantener la estructura actual.
- [ ] Si Brighouse es ya una SL: ¿puede una SL nueva de producto optar a NEOTEC si las mismas personas tienen otra empresa? ¿Hay riesgo de que CDTI lo vea como continuación de una actividad anterior?
- [ ] Calendario de la SL de producto: constitución entre abril y octubre de 2027 con capital bajo (Ley 18/2022), subida a 20 k€ (capital más prima de emisión) antes de NEOTEC 2028 y efectos de las aportaciones.
- [ ] IVA en servicios a clientes de la UE (inversión del sujeto pasivo) y facturación a clientes que pagan con SECURE.

**Corredor de seguros:**
- [ ] RC profesional que nombre expresamente "pruebas de intrusión y auditoría técnica de producto y firmware", sin exclusión por acceso intencionado, con cobertura de daños patrimoniales puros y suma asegurada de ≥600 k€. Comparar 2-3 ofertas.
- [ ] ¿Cubre la póliza las reclamaciones relacionadas con el CRA y con el anexo PSIRT? Si no las cubre, no se vende el anexo.
- [ ] Ciberriesgos propios (datos de clientes en el laboratorio).

---

## Fuentes nuevas verificadas por el juez [JUEZ]

- FAQ oficial de NEOTEC 2026 (capital más prima de 20 k€ desembolsado e inscrito antes de la solicitud, antigüedad de 6 meses a 3 años, presupuesto de 175-750 k€, proyectos desde el 1 de enero del año siguiente): https://www.cdti.es/sites/default/files/2026-04/faq_neotec_2026_v1.0.pdf
- Página oficial del EUDIS Business Accelerator (cohortes de primavera y otoño de 2027, convocatoria de otoño de abril a junio de 2027, bono de 120 k€ más 50 k€ para los 3 mejores; fecha de la convocatoria de primavera incoherente, comprobar): https://eudis.europa.eu/business-accelerator_en
- Cohorte 3 de EUDIS (cerró el 30-05-2026 y empezó en septiembre de 2026): https://starburst.aero/news/european-commission-opens-applications-for-cohort-3-of-the-eudis-business-accelerator/
- Tarifa plana de autónomos 2026 (80 €/mes): https://www.billeo.es/blog/tarifa-plana-autonomos-2026
- Referencia de un producto de RC profesional para consultores (Hiscox): https://www.hiscox.es/documentos/IPID-Hiscox-Consultores-de-Negocio.pdf
- INCIBE Emprende: https://www.incibe.es/emprendimiento
- No pude leer la página de precios de pentest en España de hard2bit (falló la descarga). Los precios del plan son estimaciones, contrastadas con la referencia de Dublín de 7asecurity.
