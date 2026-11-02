# El optimista: el mejor caso honesto para cada una de las 13 ideas

**Fecha:** 2026-11-02
**Rol:** defender el mejor escenario *defendible* de cada idea. No invento datos: cada afirmación sale de `defensa.md`, `neuro_bio.md` y `chips.md` (misma carpeta) o de búsquedas nuevas, con su URL.
**Perfil del fundador:** solo, España/UE, pentesting y ciberseguridad (Brighouse Security Labs), investigación publicada, sabe vender y tiene menos de 5.000 € de capital. Le interesan lo militar, la tecnología, la neurotecnología y la biotecnología.

**Convención:**
- **[EST]** marca una estimación propia (precios, plazos de venta, número de clientes). No es un dato.
- **[NUEVO]** marca una fuente que encontré en esta ronda de búsquedas y que no aparece en los ficheros de investigación.

**Aviso de honestidad que cambia una idea:** la fase 2 de CMMC **no** arranca el 10-11-2026, como dicen `ideas.md` y `defensa.md`. Quedó suspendida en julio de 2026 (lo detallo en la idea 10). Ser optimista no consiste en ocultar esto, sino en buscar el ángulo que sobrevive.

---

## Datos transversales que sostienen casi todo el optimismo

1. **La regulación obliga a comprar, y algunas fechas ya han pasado.**
   - CRA: las notificaciones a ENISA son obligatorias desde el **11-09-2026**, también para productos ya comercializados, con plazos de 24 h, 72 h y 14 días. La aplicación completa llega el **11-12-2027**, con multas de hasta 15 M€ o el 2,5 % de la facturación (chips.md §2.1; https://www.jonesday.com/en/insights/2026/07/eu-cyber-resilience-act-24hour-reporting-duties-start-september-11-2026).
   - A 8-09-2026 **no había ningún organismo notificado CRA designado** (https://www.cyberresilienceact.eu/news/cra-notified-bodies-rules-apply-11-june-2026.html). Hay cuello de botella y escasez de oferta.
2. **Hay dinero para que el cliente pague.** La ayuda SECURE da hasta 30.000 € por pyme al 50 %, cubre expresamente el pentesting y **cierra el 11-12-2026** (https://www.cyberresilienceact.eu/es/news/secure-second-open-call-1-october-2026-cra-sme-funding.html).
3. **Falta talento.** Al 91 % de las pymes medtech le cuesta contratar perfiles regulatorios (https://medtecheurope.org/wp-content/uploads/2025/01/mte-ivdr-mdr-survey-report-highlights-final.pdf). En semiconductores faltarán más de 75.000 personas en la UE en 2030 (chips.md §3).
4. **El capital de defensa existe, aunque no vaya al fundador.**
   - VC europeo en defensa, seguridad y resiliencia en 2025: 8.700 M$, un 55 % más que en 2024 (https://www.nif.fund/news/dealroom-and-nato-innovation-fund-european-defence-security-resilience-startups-smash-record-with-8-7b-raised-in-2025/).
   - Helsing levantó 1.800 M$ y Quantum Systems 1.200 M$ en julio de 2026 (defensa.md §1.2).
   - Esas empresas son **clientes** con caja.
5. **Los patrones de salida existen.**
   - Cryptography Research fue comprada por 342,5 M$, Riscure por Keysight y Secure-IC por Cadence. jtsec (Granada) acabó en Applus+ (chips.md §5).
   - Tarlogic pasó de 2 a unas 100 personas en 10 años (https://www.tarlogic.com/news/10-years-of-tarlogic-security/).
   - CounterCraft (San Sebastián) ganó un contrato *sole source* del gobierno de EE. UU. con techo de más de 26 M$ (defensa.md §5).
   - El camino "servicios → producto → cliente soberano" ya lo han recorrido españoles.

---

## 1. PSIRT-as-a-Service para el CRA

**Tesis del mejor caso.**
- Desde el 11-09-2026, cualquier fabricante que venda en la UE un producto con elementos digitales debe poder emitir una alerta a ENISA en 24 h. Eso exige un turno de vigilancia que una pyme de 20 personas no tiene.
- Es una obligación legal **continua**, no un proyecto puntual. Por eso encaja de forma natural con una cuota mensual, con alta retención y bajo coste de servir una vez estandarizado el triaje.
- Es el "SOC" del producto: quien gestiona el PSIRT de un fabricante se convierte en su proveedor de seguridad por defecto, y de ahí salen pentests, SBOM y marcado CE.

**Por qué ahora.**
- Las notificaciones son obligatorias desde el **11-09-2026** e incluyen los productos ya vendidos. La Single Reporting Platform de ENISA está abierta (https://helpnetsecurity.com/2026/09/14/enisa-cra-single-reporting-platform).
- La Comisión publicó su guía de notificación el 27-07-2026 (chips.md §2.1).
- En España no consta todavía una autoridad de vigilancia designada formalmente (https://cdn.presencis.com/regulations/cra/national/es). Quien llegue antes educa al mercado.

**Camino a los primeros 10.000 €.** **[EST]**
- Convertir clientes de la idea 2 (sprint CRA) en abonados. Un *onboarding* de PSIRT a 2.000-3.000 € (política CVD, security.txt, inventario SBOM y procedimiento SRP) más una cuota de 500-1.500 €/mes.
- Con 3 o 4 fabricantes pyme en noviembre y diciembre se llega a 10 k€ entre *onboardings* y primeras cuotas.

**Camino a 100.000 € de ARR.** **[EST]**
- 10-12 clientes a ~800 €/mes de media. Es alcanzable en 12-18 meses si la idea 2 actúa de embudo y si se automatiza la monitorización de CVE frente al SBOM (lo que lleva a la idea 11).

**Potencial.**
- La aplicación completa del CRA (11-12-2027) multiplica el mercado: hay que hacer marcado CE con el anexo I.
- La CE estimó unos 29.000 M€ de costes agregados de cumplimiento (https://circleid.com/posts/eu-cyber-resilience-act-costs-and-economic-impact, cifra no oficial).
- El mejor caso es convertirse en el "PSIRT europeo de las pymes": primero una plataforma de cumplimiento continuo, después un socio técnico de un organismo notificado español (chips.md §6.7) y una salida hacia un laboratorio (Applus+, SGS, TÜV) o una empresa de herramientas.

**Ventaja del fundador.**
- Un pentester sabe triar si una vulnerabilidad es explotable, y eso es lo que decide si hay que notificar en 24 h.
- La investigación publicada le da credibilidad ante los CSIRT.
- Coste de arranque casi cero sobre la consultora que ya tiene.

---

## 2. Sprint "CRA Ready" a precio cerrado + solicitud de la ayuda SECURE

**Tesis del mejor caso.**
- Es la idea con **la urgencia comercial más alta del documento**. El cliente tiene una obligación que ya está vigente y una ayuda que le paga la mitad, y esa ayuda caduca en 5-6 semanas.
- Un sprint de precio cerrado (diagnóstico, clasificación del producto, análisis de brechas del anexo I, pentest y plan) se vende en una reunión, porque el cliente puede pedir hasta 30.000 € al 50 % para pagarlo.
- Es la puerta de entrada a las ideas 1, 11 y 12.

**Por qué ahora.**
- SECURE abrió el 1-10-2026 y **cierra el 11-12-2026**. Cubre auditorías, pentesting, políticas y gestión de incidentes (https://www.cyberresilienceact.eu/es/news/secure-second-open-call-1-october-2026-cra-sme-funding.html).
- RED/EN 18031 es obligatoria desde el 01-08-2025 (https://www.sgs.com/en-se/news/2025/06/red-cybersecurity-requirements-mandatory-on-1-august-2025).
- Muchos fabricantes ya incumplen algo, y eso es un buen argumento de venta.

**Camino a los primeros 10.000 €.** **[EST]**
- 2 sprints de 5.000-8.000 € (o 1 de 12-15 k€) vendidos en noviembre de 2026 a fabricantes IoT u OT pyme. El cliente paga en la práctica la mitad gracias a SECURE.
- Canal: la cartera actual de Brighouse, clústeres industriales y asociaciones (por ejemplo AMETIC o clústeres TIC regionales) con un webinar del tipo "SECURE: 30 k€ para tu CRA, cierra el 11 de diciembre".
- Es **el camino más corto a 10 k€ de las 13 ideas**.

**Camino a 100.000 € de ARR.**
- El sprint en sí no es recurrente, pero puede generar unos 100 k€ de facturación anual con 10-12 sprints al año **[EST]**.
- La parte recurrente llega convirtiendo un 30-50 % de esos clientes en abonados de PSIRT (idea 1) **[EST]**.

**Potencial.** La metodología del sprint se convierte en producto (plantillas y herramienta de autoevaluación, idea 11) y en formación de pago (chips.md §6.6). Es el caso jtsec: un laboratorio de evaluación que acabó dentro de Applus+.

**Ventaja del fundador.** Sabe vender, ya tiene la consultora, y el pentest (la parte de más valor del sprint) es su oficio. Además, SECURE es para pymes, el segmento que las Big4 desatienden (chips.md §6, riesgos).

---

## 3. Paquete ciber-regulatorio para medtech y neurotech

**Tesis del mejor caso.**
- La FDA puede **denegar una autorización solo por ciberseguridad** (sección 524B) y el MDR reformado hace explícita la ciberseguridad y la notificación a ENISA.
- Las startups medtech y BCI tienen dinero recién levantado pero no tienen ese perfil en plantilla.
- Un paquete cerrado (modelo de amenazas, SBOM, pentest de BLE, firmware y app, plan CVD, plan postmercado y mapeo a IEC 81001-5-1) resuelve un bloqueo que retrasa la llegada al mercado. Por eso el comprador no regatea igual que en TI.

**Por qué ahora.**
- La guía final de la FDA sobre la 524B se publicó en **junio de 2025** (https://www.govinfo.gov/content/pkg/FR-2025-06-27/html/2025-11669.htm).
- La reforma del MDR/IVDR (COM(2025) 1023, 16-12-2025) añade el art. 87a de notificación a ENISA y CSIRT.
- Team-NB pidió en febrero de 2026 basar la norma armonizada en IEC 81001-5-1 (neuro_bio.md §2.2).
- La financiación de BCI superó los **1.000 M$ en 2026** (https://www.remio.ai/es/post/pitchbook-bci-funding-tops-1-billion-but-clinical-proof-still-lags-es).

**Camino a los primeros 10.000 €.** **[EST]**
- Un único cliente. Blue Goat cobra desde unos 15.000 $ solo por el pentest (https://bluegoatcyber.com/blog/medical-device-cybersecurity-cost). Un paquete UE en español de 8-25 k€ es competitivo (estimación de neuro_bio.md §6.1).
- Objetivo: startups del ecosistema de Barcelona (INBRAIN, Neuroelectrics, Barcelona Health Hub, BioCat) o Bitbrain en Zaragoza, priorizando las recién financiadas.

**Camino a 100.000 € de ARR.** **[EST]**
- 5-6 paquetes al año, más retenes de mantenimiento postmercado (vigilancia del SBOM y gestión CVD) a 500-1.000 €/mes por dispositivo.
- La 524B exige un plan de mantenimiento durante toda la vida del producto, así que la recurrencia viene de la propia norma.

**Potencial.**
- MedCrypt empezó con un seed pequeño, levantó una Serie B de 25 M$ y dice trabajar con 7 de los 10 mayores fabricantes de productos sanitarios (https://medcitynews.com/2022/11/medical-device-security-startup-reels-in-25m-as-cyber-threats-escalate/).
- El mercado de ciberseguridad de dispositivos médicos se estima en 8.990 M$ en 2026 y 18.280 M$ en 2031 (Mordor, cifra de consultora; neuro_bio.md §1.5).
- Mejor caso: "el MedCrypt europeo", con producto de monitorización postmercado vendido a fabricantes.

**Ventaja del fundador.** Combina su interés en neurotecnología con su oficio. La investigación publicada de la idea 4 le sirve de marketing para esta. El precedente de Illumina (9,8 M$ bajo la False Claims Act) le da un argumento de venta muy concreto (https://www.justice.gov/opa/pr/illumina-inc-pay-98m-resolve-false-claims-act-allegations-arising-cybersecurity).

---

## 4. Auditorías de seguridad y privacidad de neurodatos

**Tesis del mejor caso.**
- Los neurodatos se están convirtiendo en una categoría regulada propia: leyes en Colorado, California, Connecticut y Montana, prohibición del AI Act de inferir emociones en el trabajo y en centros educativos, y la recomendación de la UNESCO.
- Casi nadie está preparado: de 30 empresas analizadas, **menos de la mitad cifraba** los datos de usuario (https://www.statnews.com/2024/04/17/neural-data-privacy-emotiv-eeg-muse-headband-neurorights/).
- Quien publique la primera investigación seria de vulnerabilidades en cascos EEG de consumo se convierte en la referencia de una categoría que nace ahora. Esa autoridad no se puede comprar con capital.

**Por qué ahora.**
- Montana SB 163 está vigente desde el 01-10-2025 y exige un programa de seguridad completo. Connecticut firmó su ley el 24-06-2025 (https://www.neurorightsfoundation.org/advocacy/united-states).
- El art. 5.1.f del AI Act aplica desde el 02-02-2025 (neuro_bio.md §2.1). La UNESCO adoptó su recomendación el 12-11-2025.
- El CRA alcanza a los wearables EEG de bienestar que el MDR deja fuera (https://meddeviceguide.com/blog/eu-cyber-resilience-act-nis2-medical-devices-guide).

**Camino a los primeros 10.000 €.** **[EST]**
1. Publicar la investigación (BLE, app y nube de 2 o 3 cascos comerciales, con divulgación responsable). Coste: unos cientos de euros en hardware (neuro_bio.md §6.4).
2. Presentarla en RootedCON o en un evento similar.
3. Vender 2 "Neural Data Readiness Assessments" a 4-6 k€ a empresas EEG que venden en EE. UU. y la UE (Neurable, NextSense, Somnee y similares; rondas en neuro_bio.md §1.2).

**Camino a 100.000 € de ARR.** **[EST]**
- El mercado de cascos EEG es pequeño (145,8 M$ en 2024, neuro_bio.md §1.2), así que a solas tiene un techo bajo.
- El mejor caso es usar esta idea como **motor de captación** de la 3 y de la 1. El ARR viene de convertir las auditorías en retenes de cumplimiento (CRA + leyes estatales) y de licenciar una herramienta de puntuación.

**Potencial.**
- Si las interfaces cerebro-ordenador de consumo llegan al mercado de masas (Merge Labs levantó 252 M$ de seed en enero de 2026; neuro_bio.md §1.1), harán falta estándares de seguridad de neurodatos.
- Mejor caso: ser el autor del estándar o del esquema de certificación de "neuroseguridad", como Paul Kocher con el DPA y su posterior negocio de licencias.

**Ventaja del fundador.** Es la idea que mejor junta pasión (neurotecnología) y oficio (investigación de vulnerabilidades). Es la que tiene más potencial de marca personal.

---

## 5. Kit "Proveedor de Defensa" (ENS/NIS2 + expediente HSEM)

**Tesis del mejor caso.**
- España ha disparado su gasto: **35.419 M€ en 2026**, un +146 % real entre 2020 y 2025 (defensa.md §1.3).
- Los Planes de Participación Industrial **obligan** a las primas a incorporar pymes en todos los PEM. IN+DEF quiere sumar más de 500 pymes a la base industrial de defensa.
- Esas pymes industriales (mecanizado, electrónica, software) no saben qué es una JSSP ni cómo pasar una auditoría ENS. El cuello de botella es de trámites, no de capital, y se resuelve con consultoría empaquetada.

**Por qué ahora.**
- IN+DEF se lanzó el 30-03-2026.
- La Comisión llevó a España ante el TJUE el **08-07-2026** por no transponer NIS2 (https://nisd2.eu/es/wiki/timelines-and-status/nis2-status-spain). La ley española llegará y creará una ola de demanda.
- El bloque de telecom y ciber de los PEM (3.262,76 M€) ya está en ejecución.

**Camino a los primeros 10.000 €.** **[EST]**
- 2-3 paquetes de 3-5 k€ (defensa.md §6.1 propone 3-15 k€ por proyecto) a pymes que ya son subcontratistas de una prima y han recibido un cuestionario de seguridad.
- Canal: departamentos de Participación Industrial de Indra, GMV y Oesía, jornadas IN+DEF y FEINDEF.

**Camino a 100.000 € de ARR.** **[EST]**
- Más de 20 clientes con un mantenimiento anual de cumplimiento (ENS + NIS2 + revisión de primas) de 4-5 k€.
- Cuando entre en vigor la ley NIS2 española, el mercado se amplía mucho más allá de defensa.

**Potencial.**
- Es el camino de S2 Grupo: servicios ciber, después producto y después cliente soberano. Hoy factura unos 37 M€ y la SEPI negocia entrar en su capital (defensa.md §5).
- El kit es la cabeza de playa para estar dentro de la cadena de las primas. Desde ahí se puede pedir la HSEM con su patrocinio y entrar en trabajo clasificado.

**Ventaja del fundador.** Sabe vender y conoce ENS/NIS2. Al ser una persona sin capital extranjero, el expediente de seguridad es sencillo. Lo que le falta (patrocinio de una prima) es justo lo que consigue el primer cliente.

---

## 6. Pentesting de drones y sistemas autónomos

**Tesis del mejor caso.**
- Los fabricantes europeos de drones son las empresas de defensa **con más caja de Europa**: Helsing 1.800 M$, Quantum Systems 1.200 M$, Tekever 580 M$, Stark 500 M€ (defensa.md §1.2).
- Venden a ejércitos que se enfrentan a guerra electrónica real, y su enlace de datos, su estación de tierra y su cadena de actualización de firmware son superficie de ataque.
- Tienen dinero, urgencia y poca capacidad ofensiva propia. Un especialista que demuestre romper un enlace C2 cobra tarifas de nicho.
- Es un servicio defensivo sobre el producto del cliente, no diseño de armas.

**Por qué ahora.**
- La Comisión adoptó el **Plan de Acción sobre seguridad de drones y antidrones el 11-02-2026** (COM(2026) 81). Prevé un esquema de certificación para sistemas antidrón, *sandboxes* regulatorios y una Iniciativa Europea de Defensa contra Drones, financiada con Horizon Europe y el EDF **[NUEVO]** (https://www.medialaws.eu/the-commission-action-plan-on-drone-and-counter-drone-security/).
- Los drones civiles también entran en el CRA y en RED.

**Camino a los primeros 10.000 €.** **[EST]**
- Un pentest de un dron o de una estación de control para una startup mediana europea o española, a 10-20 k€ (el pentest médico de referencia ya parte de 15 k$).
- Paso previo de coste casi nulo: publicar investigación sobre un dron comercial o un autopiloto abierto (PX4/ArduPilot, MAVLink) para tener pruebas que enseñar.

**Camino a 100.000 € de ARR.** **[EST]**
- 3-4 fabricantes con un retén anual de 25-35 k€ (pentest por versión de firmware + gestión de vulnerabilidades).
- Con ~80 plataformas antidrón en Europa (35 programas) y decenas de fabricantes de UAS, hay demanda suficiente.

**Potencial.**
- Precedente: Alias Robotics, ciberseguridad de robots (defensa.md §3).
- El paso a producto es un sistema de detección de anomalías en el enlace C2 o un "firewall" de MAVLink con TRL 4. Eso abre **EUDIS (120 k€)** y **DIANA (hasta 400 k€)**. DIANA 2027 incluye el reto de "resiliencia operativa en entornos disputados" (defensa.md §2).
- Es la idea con **el camino más corto de servicio a ambición "Anduril"**: quien sabe atacar drones acaba construyendo la seguridad que va dentro de ellos.

**Ventaja del fundador.** Pentesting más interés militar. La investigación publicada es la tarjeta de visita que funciona con ingenieros de defensa. España tiene UAV Navigation y su entrada en FCAS a través de Oesía (defensa.md §5) como posibles clientes y canal.

---

## 7. SaaS de inteligencia de licitaciones de defensa

**Tesis del mejor caso.**
- La información está fragmentada: PLACSP, TED, EDF, EUDIS, DIANA, Coincidente, Llamadas a la Innovación y portales de compras de las primas.
- Las 500 o más pymes que IN+DEF quiere incorporar no saben ni por dónde empezar. Un agente de IA que cruce convocatorias con el perfil de cada pyme es barato de construir y fácil de vender por suscripción.
- El modelo ya está validado en EE. UU.: **GovDash levantó una Serie B de 30 M$** en enero de 2026 para ayudar a ganar contratos públicos con IA **[NUEVO]** (https://www.axios.com/pro/fintech-deals/2026/01/15/govdash-30m-government-contracts ; https://www.govdash.com/blog/press-govdash-raises-30m-series-b-to-help-companies-win-and-manage-government-contracts-with-ai).

**Por qué ahora.**
- El EDF batió su récord en 2026 con 612 propuestas (+49 %) y tiene 60 M€ en convocatorias no temáticas para pymes (defensa.md §2).
- El EIC admite ahora tecnología dual.
- IN+DEF y los PEM generan un flujo constante de oportunidades.

**Camino a los primeros 10.000 €.** **[EST]**
- Empezar como **servicio** (un boletín curado más alertas a medida a 150-300 €/mes) para 10-15 pymes del entorno de las ideas 5 y 2.
- Alternativa: 2-3 "diagnósticos de financiación" a 2-3 k€ que identifiquen convocatorias concretas.

**Camino a 100.000 € de ARR.** **[EST]**
- Unas 40 suscripciones a ~200 €/mes. O una licencia a una asociación sectorial (TEDAE) o a una cámara de comercio que lo ofrezca a sus socios.

**Potencial.** Gestionar el flujo de oportunidades de la base industrial de defensa es una posición estratégica: se pueden añadir redacción de propuestas, búsqueda de socios para consorcios EDF y datos de mercado. Es un "Govini europeo" a pequeña escala.

**Ventaja del fundador.** Sabe vender y conoce el ecosistema. Es una herramienta que **él mismo necesita** para las ideas 5, 6 y 9, así que la construye como subproducto. Como ingeniero, puede montar el agente con muy poco capital.

---

## 8. Migración postcuántica (PQC)

**Tesis del mejor caso.**
- Las fechas ya son firmes. La hoja de ruta UE pide inventarios para el **31-12-2026**, migración de los casos de alto riesgo en 2030 y de riesgo medio en 2035 (https://pqshield.com/eu-pqc-workstream-publishes-a-coordinated-implementation-roadmap-for-the-transition-to-post-quantum-cryptography/).
- NIST IR 8547, en su versión final del 27-10-2026, declara RSA y ECC obsoletos tras 2030 y prohibidos tras 2035 (chips.md §2.2).
- El primer gasto es el **inventario criptográfico**, que es justo un trabajo de auditoría técnica.
- El VC confirma la categoría: **QIZ Security levantó 17 M$ de seed en julio de 2026** (Bessemer, Merlin, Evolution Equity) con una plataforma de descubrimiento criptográfico y hojas de ruta de remediación **[NUEVO]** (https://quantumcomputingreport.com/qiz-security-raises-17m-seed-round-to-scale-enterprise-cryptographic-posture-platforms/amp/).

**Por qué ahora.**
- NIST IR 8547 se publicó hace 6 días.
- El plazo de inventarios de la UE vence en 2 meses.
- El CCN todavía no ha publicado su hoja de ruta (chips.md §2.2), y cuando lo haga generará demanda en el sector público y en sus proveedores.
- ABI estima un mercado de servicios PQC de ~255 M$ a finales de 2025, con miles de millones previstos para 2030, y la fase inicial de inventario domina el gasto (https://www.abiresearch.com/press/new-algorithmic-standards-and-migration-policy-timelines-propel-post-quantum-cryptography-toward-billion-dollar-market-by-2030).

**Camino a los primeros 10.000 €.** **[EST]**
- Vender PQC **pegada a un plazo concreto** (chips.md §4 advierte que no hay que venderla en abstracto): "Informe CRA + preparación PQC" para clientes de la idea 2, o un inventario CBOM a 5-8 k€ para una entidad financiera mediana bajo DORA o un proveedor de infraestructura crítica.
- Con 2 inventarios se llega a 10 k€.

**Camino a 100.000 € de ARR.** **[EST]** 
- Herramienta propia de inventario (un escáner de código, binarios y certificados que genere un CBOM) en modelo de suscripción, más servicios de hoja de ruta.
- Unos 10 clientes con monitorización continua de cripto-agilidad a 8-10 k€/año.

**Potencial.**
- La transición dura hasta 2035, así que es un mercado de 9 años con fechas que obligan a comprar.
- La rama embebida (auditoría de canal lateral de ML-KEM y ML-DSA en microcontroladores, que se une a la idea 12) es un nicho de alto valor con salida natural hacia empresas como PQShield, Rambus o Keysight.

**Ventaja del fundador.** Mezcla auditoría y criptografía aplicada. Puede publicar investigación sobre implementaciones PQC en embebido (encaja con su perfil investigador). Además, PQC se puede añadir como capa a todos los clientes CRA.

---

## 9. "Mini-Palantir" de vigilancia marítima con datos abiertos

**Tesis del mejor caso.**
- La seguridad marítima europea pasó en dos años de nicho a prioridad: sabotaje de cables en el Báltico, flota fantasma rusa y *spoofing* de AIS.
- La UE anunció **casi 1.000 M€ para proteger cables submarinos**, incluido un mecanismo de vigilancia con datos compartidos (febrero de 2025) **[NUEVO]** (https://www.bairdmaritime.com/security/naval/european-union-to-spend-nearly-a-billion-euros-to-protect-undersea-cables).
- La OTAN lanzó patrullas en el Báltico tras sospechas de sabotaje **[NUEVO]** (https://www.omanobserver.om/article/1164843/world/europe/nato-launches-baltic-sea-patrols-after-suspected-cable-sabotage).
- Detectar anomalías fusionando AIS, Sentinel-1 (SAR) y datos abiertos es software puro. Los datos Copernicus son gratuitos y el fundador puede construir un demostrador sin capital.

**Por qué ahora.**
- Hay inversión privada de primer nivel: Unseenlabs levantó 85 M€ para rastrear buques "oscuros" vía RF **[NUEVO]** (https://payloadspace.com/unseenlabs-raises-e85m-for-maritime-tracking/), y Kpler amplía su seguimiento de flota oscura con satélites de Airbus **[NUEVO]** (https://gcaptain.com/kpler-expands-dark-fleet-tracking-with-airbus-satellite-deal/).
- El reto DIANA 2027 de "sensores y procesado de datos para inteligencia" encaja (defensa.md §2).
- España tiene un litoral atlántico, el Estrecho y Canarias, con Salvamento Marítimo y la Armada como usuarios naturales.

**Camino a los primeros 10.000 €.** **[EST]** 
- Es la idea con el camino a ingresos **menos directo**.
- Mejor caso:
  1. Un piloto pagado del estilo de Vannevar (empezó con un piloto de ~25.000 $, 3 meses y 4 usuarios, convertido en un contrato de 1,3 M$; defensa.md §5) con una aseguradora marítima, un *trader* de cumplimiento de sanciones o una autoridad portuaria.
  2. O informes OSINT a medida sobre flota oscura (2-5 k€ cada uno) para despachos de sanciones o medios.
- Precedente de demanda: ACAMS da formación sobre "dark fleet" a investigadores de cumplimiento (https://www.acams.org/en/training/webinars/masterclass-dark-fleet-decoded-maritime-intelligence-investigators).

**Camino a 100.000 € de ARR.** **[EST]**
- 3-5 suscripciones de 20-30 k€/año de cumplimiento de sanciones o seguros, o un contrato público tras pasar por EUDIS o DIANA.

**Potencial.** Es la idea más "Palantir" en sentido literal: fusionar datos para crear conciencia del dominio. Si se gana un reto DIANA y un primer cliente soberano, el techo es de empresa de defensa de verdad (el camino de Vannevar va de 3,5 M$ en 2021 a 80 M$ en 2024).

**Ventaja del fundador.**
- El OSINT y el análisis de datos son vecinos del pentesting.
- La detección de *spoofing* de AIS es un problema de **integridad de señales**, un enfoque de seguridad que los analistas de datos puros no tienen.
- Precaución que el optimista acepta: tener en cuenta el control de exportación de ciberespionaje y el RGPD (defensa.md §3).

---

## 10. Preparación CMMC para proveedores europeos del DoD

**Corrección de un hecho del que parte la idea.** La fase 2 de CMMC **fue suspendida** el 13-07-2026 por el Departamento de Guerra, alegando que el coste expulsaba a pequeños proveedores. Las licitaciones que exigían certificación de un C3PAO se están modificando **[NUEVO]** (https://www.wolftheiss.com/insights/cmmc-phase-ii-suspended-what-changes-and-what-does-not-for-european-suppliers-to-the-us-defence-industrial-base/ ; https://www.crowell.com/en/insights/client-alerts/department-of-war-immediately-suspends-cmmc-phase-ii-requirements-launches-60-day-reform-review). A 30-10-2026 el informe del grupo de trabajo para la reforma seguía sin publicarse. Un resumen interno filtrado baraja reactivar la fase 2 en unos 90 días para un grupo más reducido, pero no hay nada decidido **[NUEVO]** (https://secureframe.com/hub/cmmc/news).

**Tesis del mejor caso (corregida).**
- La obligación de fondo sigue vigente: DFARS 252.204-7012, los 110 controles de NIST SP 800-171 Rev. 2, las autoevaluaciones de nivel 1 y 2 con puntuación en SPRS, la afirmación anual y el riesgo de **False Claims Act** si la autoevaluación es inexacta.
- Las primas seguirán trasladando requisitos a su cadena con cuestionarios y auditorías propias.
- CMMC no reconoce la ISO 27001 ni NIS2 (Wolf Theiss, arriba). Por eso el proveedor europeo necesita a alguien que le traduzca su ISO o su ENS a 800-171.
- La suspensión retira de este mercado a los grandes C3PAO estadounidenses, y el que siga aquí tiene menos competencia **[EST]**.

**Por qué ahora.** No hay un "ahora" duro, y el optimista lo reconoce. El mejor caso es una **opción barata**: posicionarse en 2026-2027 con autoevaluaciones (fase 1) y estar listo si se reactiva la fase 2 hacia principios de 2027.

**Camino a los primeros 10.000 €.** **[EST]** 2-3 evaluaciones de brechas frente a 800-171 a 3-5 k€ para pymes españolas que suministran a programas con componente estadounidense, presentadas como "evita el riesgo de la False Claims Act en tu afirmación SPRS".

**Camino a 100.000 € de ARR.** **[EST]** Solo es realista si se reactiva la fase 2. Hasta entonces funciona mejor como módulo del kit de la idea 5 que como negocio propio.

**Potencial.** Bajo como empresa independiente. Como "puente transatlántico de cumplimiento" (ENS/NIS2 ↔ 800-171), es un diferenciador para las ideas 5 y 6: los fabricantes europeos de drones que venden en EE. UU. también lo necesitan.

**Ventaja del fundador.** Domina marcos de control y sabe vender, pero acreditarse como CCP/CCA desde la UE es incierto (defensa.md §6.3). **Valoración del optimista: es la idea que más se ha debilitado con los datos nuevos.**

---

## 11. SaaS de SBOM y gestión de vulnerabilidades para dispositivos embebidos

**Tesis del mejor caso.**
- Toda obligación del CRA, de la FDA 524B y de RED necesita un SBOM vivo cruzado con CVE.
- Quien haya hecho a mano 10 PSIRT (idea 1) sabe exactamente qué automatizar. El SaaS nace con clientes de pago desde el primer día, que es el orden correcto.
- La categoría está validada:
  - Finite State vende "pruebas" de cumplimiento CRA (https://www.finitestate.io/cra).
  - ONEKEY (Düsseldorf) presenta los SBOM como "pasaportes de seguridad" para el CRA (https://www.itedgenews.africa/onekey-transforms-sboms-into-security-passports-to-streamline-eu-cyber-resilience-act-compliance/).
  - MedCrypt hizo lo mismo en medtech.

**Por qué ahora.**
- Las notificaciones CRA llevan vigentes desde el 11-09-2026.
- Las competidoras se centran en fabricantes medianos y grandes. Una herramienta en español, asequible y "con PSIRT incluido" para la pyme industrial española tiene hueco **[EST]**.

**Camino a los primeros 10.000 €.** **[EST]** No vender el SaaS solo al principio. Incluirlo en la cuota del PSIRT (idea 1) y cobrar *onboardings*. Los 10 k€ llegan por la vía de la idea 1.

**Camino a 100.000 € de ARR.** **[EST]**
- 40-60 productos monitorizados a 150-200 €/mes, o 15-20 clientes a 400-500 €/mes, combinando autoservicio y servicio gestionado.
- Financiable con **NEOTEC** (hasta 250 k€ al 70 %) cuando exista una SL con 20 k€ de capital, pagado con los ingresos de las ideas 1 y 2 (chips.md §3).

**Potencial.**
- Plataforma europea de cumplimiento continuo de producto (CRA + RED + MDR + PQC/CBOM).
- Es la idea con mejor estructura SaaS y la más fácil de financiar con VC.
- Salida natural hacia laboratorios o empresas de herramientas (el patrón de chips.md §5).

**Ventaja del fundador.** Es analista de firmware y de vulnerabilidades, que es el núcleo técnico del producto, y tiene las ideas 1 y 2 como canal propio sin coste de adquisición.

---

## 12. Laboratorio de ataques de canal lateral e inyección de fallos

**Tesis del mejor caso.**
- La seguridad hardware es el segmento de salidas más caras del documento: Cryptography Research (342,5 M$), Riscure (Keysight) y Secure-IC (Cadence).
- Se puede empezar con un banco ChipWhisperer de cientos o pocos miles de dólares (chips.md §2.3).
- La cuña es concreta y nueva: **auditar implementaciones de ML-KEM y ML-DSA en microcontroladores**, que toda la industria tiene que desplegar antes de 2030.
- Las empresas de chips españolas con mucho dinero son clientes en potencia: Openchip con 115,77 M€ de SETT, Semidynamics con SK hynix, Qilimanjaro con Indra (chips.md §1.3).

**Por qué ahora.**
- NIST IR 8547 (27-10-2026) fija los plazos.
- El CRA pide mecanismos "state of the art" en el anexo I, y RED/EN 18031 ya obliga.
- Faltan organismos notificados, así que los fabricantes necesitan evidencias técnicas sólidas para su autoevaluación (chips.md §6.3).

**Camino a los primeros 10.000 €.** **[EST]**
- Formación de pago (un taller de hardware hacking o fault injection, al estilo de Raelize en Ringzer0 o hardwear.io; chips.md §5) más una revisión de arranque seguro y firmware para un fabricante IoT.
- La revisión de firmware cuesta casi cero de arrancar.

**Camino a 100.000 € de ARR.** **[EST]** 4-6 contratos anuales con fabricantes de MCU, *secure elements* o medtech, de 15-25 k€, más formación. NewAE llegó a venderse a lowRISC con solo 6 empleados (chips.md §5), una prueba de que se puede ser rentable y atractivo siendo pequeño.

**Potencial.**
- Investigación, formación, consultoría, laboratorio y, a largo plazo, IP o patentes de contramedidas (el modelo Kocher).
- Con Tiny Tapeout (~70 € por *tile*, precio a confirmar) se puede sacar en silicio un demostrador abierto de contramedidas o un núcleo PQC endurecido como prueba de credibilidad (chips.md §2.4).

**Ventaja del fundador.**
- Es la extensión más técnica de su perfil investigador y la que más diferencia frente a consultoras genéricas.
- Se combina con las ideas 3 (medtech), 6 (drones) y 8 (PQC). Los mismos bancos de pruebas sirven para todas.

---

## 13. Software de detección de drones con SDR barato

**Tesis del mejor caso.**
- El antidrón ha pasado "de capacidad de nicho a requisito básico". BCG proyecta en Europa una demanda de **5.000-7.000 M$ en 2029**, con un crecimiento anual de más del 50 %, y entre **2.000 y 3.000 sistemas para proteger infraestructura civil** **[NUEVO]** (https://www.bcg.com/assets/2026/white-paper-countering-the-drone-threat-europes-cuas-opportunity.pdf, mayo de 2026).
- Los aeropuertos civiles **no pueden usar inhibidores ni medios cinéticos** y usan sobre todo herramientas de detección **[NUEVO]** (https://www.sowetan.co.za/news/world/2026-06-18-drone-threats-drive-surge-in-airport-defence-tech/). Eso es justo lo que propone la idea.
- Dedrone demostró que el software de detección vendido a través de revendedores grandes puede escalar: más de 200 instalaciones en 2016 y compra posterior por Axon (defensa.md §5).

**Por qué ahora.**
- Ha habido incidentes con drones en los aeropuertos de Múnich y Copenhague y en los países bálticos (fuente anterior).
- El Plan de Acción de la UE (11-02-2026) incluye una iniciativa voluntaria de despliegue antidrón para infraestructura crítica con **compra conjunta**, un esquema de certificación de sistemas antidrón, un centro de excelencia del JRC y guías antidrón para entidades críticas bajo la Directiva CER **[NUEVO]** (https://www.medialaws.eu/the-commission-action-plan-on-drone-and-counter-drone-security/).
- El Programa Coincidente 2026 tenía C-UAS como tema (defensa.md §2).
- Hay fragmentación: 35 plataformas antidrón en Europa frente a 13 en Norteamérica (BCG). Los integradores necesitan sensores y software de terceros.

**Camino a los primeros 10.000 €.** **[EST]** No vendiendo un producto terminado.
- Mejor caso: una **evaluación de exposición a drones** para una infraestructura crítica, un evento o un centro de datos (análisis del espectro RF con SDR + informe de riesgo según las guías CER), a 3-5 k€.
- O un piloto de detección pasiva (RemoteID + firmas RF de DJI y similares) con un operador.

**Camino a 100.000 € de ARR.** **[EST]**
- Licencias de software de detección pasiva para 10-20 emplazamientos a 5-10 k€/año, vendidas a través de un integrador de seguridad física o un revendedor (el modelo Dedrone).
- Con el producto en TRL 4, EUDIS (120 k€) y DIANA (hasta 400 k€) dan financiación no dilutiva.

**Potencial.** **Es la idea con más techo y la más "Anduril".** Si el software de fusión y clasificación RF llega a ser la capa de C2 que conecta sensores de terceros (BCG señala que las primas dependen de terceros para el software de IA y de sensores), el fundador posee el "sistema operativo" del antidrón civil en un mercado que crece a más del 50 % anual.

**Ventaja del fundador.**
- Análisis de RF y protocolos (BLE, MAVLink, enlaces DJI) desde el lado ofensivo. Sabe cómo se comunica un dron porque sabe atacarlo, y eso enlaza con la idea 6.
- Se queda en la **detección**, sin neutralización, y así evita el problema legal de la inhibición en entornos civiles.

---

## Top 3 del optimista

### 1. Ideas 2 → 1 → 11 como un único motor: "CRA Sprint + SECURE" que se convierte en PSIRT recurrente y después en SaaS
- **Por qué es la primera:** es la única combinación con **obligación ya vigente** (CRA, desde el 11-09-2026), **dinero que caduca y paga la mitad** (SECURE, hasta 30 k€, cierra el 11-12-2026), **oferta escasa** (ningún organismo notificado a septiembre de 2026) y **coste de arranque cero** sobre la consultora actual.
- **Escalera:** 10 k€ en noviembre y diciembre de 2026, 100 k€ de ARR en 12-18 meses con PSIRT, y después NEOTEC y SaaS. La ambición de largo plazo es una plataforma europea de cumplimiento continuo de producto (CRA + RED + MDR + PQC).
- Es la idea que **financia a todas las demás**.

### 2. Idea 3 (+ la 4 como motor de marketing): ciber-regulatorio para medtech y neurotech
- **Por qué es la segunda:** tickets altos (de 8 a 25 k€) con compradores que tienen caja recién levantada (BCI por encima de 1.000 M$ en 2026), una norma que bloquea la llegada al mercado (la 524B permite denegar solo por ciberseguridad), recurrencia impuesta por el mantenimiento postmercado y un precedente de escala claro (MedCrypt).
- Es donde **pasión y oficio coinciden**. La investigación pública sobre cascos EEG (idea 4) le da una marca que no se compra con dinero.

### 3. Idea 6 (como puente hacia la 13): pentesting de drones y sistemas autónomos
- **Por qué es la tercera:** los clientes son las empresas de defensa con más caja de Europa (Helsing, Quantum, Tekever, Stark), la UE adoptó un Plan de Acción sobre drones en febrero de 2026 y los ingresos llegan como servicio desde el primer contrato.
- Es el **único camino realista hacia la ambición "Anduril"**: atacar drones, después construir la seguridad del enlace C2 (TRL 4, EUDIS y DIANA 2027) y después software de detección (idea 13) en un mercado antidrón europeo de 5.000-7.000 M$ en 2029 según BCG.

**Menciones de honor:**
- La **8 (PQC)** y la **12 (canal lateral)** se suman como módulos a todo lo anterior: PQC se vende atada al CRA y el banco de canal lateral sirve para medtech, drones y chips.
- **La que el optimista rebaja:** la **10 (CMMC)**, porque la fase 2 está suspendida desde julio de 2026. Funciona como módulo del kit de la idea 5, no como empresa propia.
