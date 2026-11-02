# El evaluador: puntuación de las 13 ideas

**Fecha:** 2026-11-02
**Rol:** neutral y cuantitativo. Puntúo; no decido.
**Fuentes:** ideas.md, optimista.md, pesimista.md, defensa.md, neuro_bio.md y chips.md, más 4 verificaciones propias (sección 3).

**Escala:** de 1 a 10. Un 10 es siempre lo mejor para el fundador: mucho encaje, poco capital, ingresos rápidos, mercado grande, foso alto, poco riesgo regulatorio y mucho techo.
**Pesos:** encaje 0,20 · capital 0,15 · rapidez 0,20 · mercado 0,15 · foso 0,10 · regulación 0,10 · ambición 0,10.

**Corrección asumida:** la fase 2 de CMMC se suspendió el 13-07-2026. Los dos debatientes coinciden y la idea 10 se puntúa sobre esa base.

---

## 1. Tabla de puntuaciones (ordenada por total)

| # | Idea | Encaje | Capital | Rapidez | Mercado | Foso | Regulación | Ambición | **Total** |
|---|---|---|---|---|---|---|---|---|---|
| 2 | Sprint "CRA Ready" (+ SECURE) | 9 | 10 | 8 | 7 | 3 | 8 | 3 | **7,35** |
| 3 | Paquete ciber-regulatorio medtech/neurotech | 7 | 9 | 5 | 7 | 6 | 6 | 6 | **6,60** |
| 1 | PSIRT-as-a-Service para el CRA | 8 | 9 | 6 | 6 | 3 | 5 | 4 | **6,25** |
| 8 | Migración postcuántica (PQC) | 7 | 9 | 4 | 6 | 3 | 8 | 5 | **6,05** |
| 12 | Laboratorio de canal lateral y fault injection | 8 | 6 | 4 | 4 | 7 | 8 | 6 | **6,00** |
| 6 | Pentesting de drones y sistemas autónomos | 8 | 6 | 4 | 6 | 6 | 4 | 7 | **5,90** |
| 5 | Kit "Proveedor de Defensa" (ENS/NIS2/HSEM) | 6 | 9 | 5 | 6 | 2 | 7 | 3 | **5,65** |
| 11 | SaaS de SBOM para embebidos | 7 | 4 | 3 | 7 | 3 | 7 | 6 | **5,25** |
| 4 | Auditorías de neurodatos | 8 | 8 | 3 | 2 | 5 | 4 | 4 | **5,00** |
| 7 | SaaS de licitaciones de defensa | 3 | 8 | 5 | 3 | 1 | 9 | 3 | **4,55** |
| 13 | Detección de drones con SDR | 5 | 2 | 1 | 9 | 3 | 2 | 9 | **4,25** |
| 9 | "Mini-Palantir" marítimo | 3 | 6 | 2 | 5 | 2 | 5 | 7 | **4,05** |
| 10 | Preparación CMMC | 5 | 8 | 2 | 2 | 3 | 5 | 1 | **3,80** |

**Cómo leer la tabla.**
- Las ideas que reutilizan el oficio actual (pentest de firmware y producto) y responden a una obligación ya vigente ocupan los cinco primeros puestos.
- Las tres ideas con más ambición (13, 9 y 6) bajan porque tienen la peor rapidez y el peor riesgo regulatorio con menos de 5.000 €.
- La distancia entre el 2.º y el 6.º puesto es de solo 0,70 puntos. Fuera del primer puesto, el orden es sensible a los pesos.

---

## 2. Justificación por idea (qué lado convenció más)

1. **Idea 2 (7,35).** En los hechos gana el **pesimista**: SECURE es competitiva, el trabajo no puede empezar antes de firmar y no hay fecha de resolución (verificado). Aun así, la idea sigue primera porque el núcleo (pentest de firmware con informe CRA/EN 18031) se vende sin la ayuda y su coste marginal es cero. Rapidez 8 y no 10 porque SECURE no adelanta caja en 2026.
2. **Idea 3 (6,60).** Empate con matices. El **optimista** acierta en el precio (Blue Goat cobra desde unos 15.000 $ solo por el pentest, verificado) y en que la norma obliga a comprar. El **pesimista** acierta en la credibilidad (no tiene casos FDA/MDR) y en los ciclos de 4 a 9 meses. Por eso la rapidez se queda en 5 y el encaje en 7.
3. **Idea 1 (6,25).** Gana el **pesimista**. Verifiqué en la FAQ de ENISA que solo se notifican vulnerabilidades explotadas activamente e incidentes graves, y que lo hace un representante del fabricante. Eso significa poco volumen, valor mensual difícil de justificar y servicio 24/7 imposible en solitario. Funciona como anexo de la idea 2, no como negocio propio.
4. **Idea 8 (6,05).** Gana el **pesimista**: el plazo de finales de 2026 es para los Estados miembros, no para las pymes, y el inventario se está automatizando con herramientas gratuitas (CBOMkit). El optimista acierta en que el mercado dura hasta 2035, y eso le da 6 en mercado. Como módulo PQC dentro del CRA es útil; vendida en abstracto, no.
5. **Idea 12 (6,00).** Gana el **pesimista** en el modelo de negocio: sin acreditación (Common Criteria, EUCC) no llega al cliente que paga mucho. Pero la idea tiene el mejor foso técnico de las 13 (7) y encaja con la investigación del fundador. Sirve como diferenciador de las ideas 2, 3 y 8, no como laboratorio independiente.
6. **Idea 6 (5,90).** Gana el **pesimista**. Las primas con más caja (Helsing, Quantum) contratan equipos internos, y el trabajo militar exige habilitación (con riesgo ITAR o de doble uso). El **optimista** tiene razón en que es el puente más corto hacia la ambición "Anduril", y por eso puntúa 7 en ambición. Es viable con drones civiles o duales como pentest IoT especializado.
7. **Idea 5 (5,65).** Gana el **pesimista**. La HSEM no se puede pedir sin una carta de expectativas, la consultoría ENS está muy comoditizada y la NIS2 española sigue sin transponerse. El optimista acierta con el volumen de gasto (IN+DEF), pero el dinero ya está adjudicado a las primas.
8. **Idea 11 (5,25).** Gana el **pesimista**. ONEKEY, Finite State, Cybellum y Dependency-Track (gratis) ya ocupan el espacio, y un SaaS de binarios no se construye con menos de 5.000 €. El optimista acierta en el orden correcto (servicio primero, producto después), y eso mantiene mercado 7 y ambición 6 como fase posterior a las ideas 1 y 2.
9. **Idea 4 (5,00).** Gana el **pesimista** en el negocio: el mercado de cascos EEG ronda los 146 M$ y las leyes exigentes son estadounidenses. El **optimista** gana en el valor de marca: la investigación pública cuesta unos cientos de euros y alimenta la idea 3. Como negocio independiente puntúa bajo; como marketing, mucho mejor.
10. **Idea 7 (4,55).** Gana claramente el **pesimista**. Los datos son públicos, ya existen Tendios y las consultoras de subvenciones, y la idea no usa la ventaja ciber del fundador. La comparación con GovDash (Serie B de 30 M$) es de otro mercado: el federal estadounidense, mucho mayor y con otra dinámica de compra.
11. **Idea 13 (4,25).** Gana el **pesimista** en todo lo que pesa a corto plazo. DroneShield tiene RfAI-3 y más de 200 M$ de ingresos comprometidos, los decodificadores DroneID son open source, la idea necesita hardware y pruebas de campo, y el cliente es el Estado. El **optimista** gana en mercado (9, con BCG estimando 5.000-7.000 M$ en Europa en 2029) y en ambición (9). Es la idea con la mayor distancia entre su techo y su viabilidad.
12. **Idea 9 (4,05).** Gana claramente el **pesimista**. Skylight es gratis, la EMSA ya ofrece ABM a las autoridades y Windward está respaldada por capital privado. La idea no explota la ventaja del fundador. El optimista solo sostiene la ambición (7).
13. **Idea 10 (3,80).** Los dos coinciden: la premisa ha caído con la suspensión de la fase 2. Gana el **pesimista** en la conclusión, porque no hay fecha que obligue a comprar y la acreditación CCP/CCA desde la UE es incierta. Queda como módulo NIST 800-171 de la idea 5.

---

## 3. Hechos verificados (con URL)

**Disputa 1: el calendario y el funcionamiento de SECURE (idea 2).** **Gana el pesimista.**
- Presupuesto de 11,5 M€ en la 2.ª convocatoria (16,5 M€ en total, con una 1.ª de 5 M€). Hasta 30.000 € por proyecto al 50 %. Abre el 1-10-2026 y cierra el 11-12-2026. Una sola propuesta por pyme.
  - https://www.cyberresilienceact.eu/news/secure-second-open-call-1-october-2026-cra-sme-funding.html
  - https://www.secure4sme.eu/cascade-funding/second-open-call
- La página indica que hay un hueco entre la solicitud y el acuerdo firmado "before any work, or spending, can begin", y que no se sabe cuándo se conocerán los proyectos financiados ni cuándo podrán empezar. Los resultados de la 1.ª convocatoria (cerrada el 29-03-2026) no se publicaron de inmediato.
  - https://www.cyberresilienceact.eu/news/secure-second-open-call-1-october-2026-cra-sme-funding.html
- La selección es **competitiva**, con tres criterios: excelencia y relevancia, impacto y claridad, e implementación. No es por orden de llegada.
  - https://www.salzburgresearch.at/en/2026/cyber-resilience-act-e5-million-in-funding-for-smes/
  - https://www.secure4sme.eu/cascade-funding/second-open-call
- Duración máxima del proyecto: 180 días naturales.
  - https://english.rvo.nl/funding-portal/secure-digital-europe-programme-cybersecurity
- **Consecuencia:** lo que se venda con SECURE en noviembre o diciembre de 2026 se ejecuta y se cobra en 2027, y solo si el cliente gana la ayuda.

**Disputa 2: el alcance real del PSIRT del CRA (idea 1).** **Gana el pesimista.**
- Por la SRP solo se notifican vulnerabilidades explotadas activamente (con "reliable evidence") e incidentes graves. Plazos: aviso temprano en 24 h, notificación en 72 h, informe final 14 días después del parche (en las vulnerabilidades) o un mes después (en los incidentes).
- Notifican los Assigned Representatives del fabricante, cada uno con su cuenta EU Login y MFA. La FAQ no aclara si un proveedor externo puede notificar en su nombre.
- https://www.enisa.europa.eu/topics/product-security/single-reporting-platform-srp/frequently-asked-questions

**Disputa 3: el precio de los servicios ciber medtech en la UE (idea 3).** **Gana el optimista en el precio**; la duda de credibilidad sigue abierta.
- Blue Goat (oferta UE) cobra el pentest de un dispositivo sencillo desde unos 15.000 $, con paquetes a precio cerrado tras una llamada de alcance. SBOM, SCA y modelo de amenazas se cobran aparte.
  - https://bluegoatcyber.com/eu/services/medical-device-penetration-testing
- El directorio de consultores de ciberseguridad medtech de OpenRegulatory no tiene **ningún** consultor listado. Es un indicio (débil) de poca oferta especializada visible en el canal de startups.
  - https://openregulatory.com/regulatory-consultants/cybersecurity
- **Conclusión:** el rango del optimista (8-25 k€ por paquete) es coherente con el mercado.

**Disputa 4: el precio de referencia del pentest en Europa (idea 2).** **Gana el optimista**, con matices.
- Una firma de Dublín publica estos rangos para 2026: unos 5.000 € para lo básico, 15.000-30.000 € para un pentest manual completo de una aplicación (1-2 semanas) y más de 50.000 € para entornos complejos.
  - https://7asecurity.com/blog/2026/04/the-2026-guide-to-penetration-testing-pricing-and-scoping/
- **Conclusión:** los sprints CRA de 5-15 k€ del optimista son realistas e incluso conservadores para un pentest de firmware y producto. No he encontrado datos de precios españoles accesibles (la página de hard2bit dio error).

**Hechos de los debatientes que no he vuelto a verificar** y doy por buenos porque los dos coinciden o porque citan una fuente primaria:
- La suspensión de la fase 2 de CMMC el 13-07-2026:
  - https://www.wilmerhale.com/en/insights/client-alerts/20260720-pentagon-suspends-cmmc-phase-2-requirements-and-launches-review-of-cybersecurity-certification-program
  - https://www.wolftheiss.com/insights/cmmc-phase-ii-suspended-what-changes-and-what-does-not-for-european-suppliers-to-the-us-defence-industrial-base/
- La ausencia de organismos notificados del CRA a septiembre de 2026.
- La densidad de competidores en SBOM (ONEKEY, Finite State), en drones (DroneShield) y en el sector marítimo (Skylight, EMSA, Windward), según las URL de pesimista.md.

---

## 4. Combinaciones que puntúan mejor juntas

**Método.** La idea de entrada fija el capital y la rapidez. Las ideas añadidas pueden subir el mercado, el foso y la ambición. El encaje se penaliza si la combinación dispersa a un fundador que trabaja solo.

| Combinación | Encaje | Capital | Rapidez | Mercado | Foso | Regulación | Ambición | **Total** |
|---|---|---|---|---|---|---|---|---|
| **A. 2 (entrada) + 3 (vertical medtech) + 4 (solo como marketing)** | 8 | 9 | 8 | 8 | 6 | 7 | 6 | **7,65** |
| **B. 2 → 1 (anexo) + 12 y 8 como diferenciadores** | 9 | 9 | 8 | 7 | 5 | 7 | 5 | **7,50** |
| C. 6 → 13 (escalera hacia el antidrón) | 7 | 5 | 4 | 8 | 6 | 3 | 9 | **5,95** |

- **A (7,65) es la única combinación que supera a la idea 2 sola (7,35).**
  - El mismo pentest de firmware y BLE sirve para fabricantes IoT (CRA) y para dispositivos médicos (MDR/524B).
  - El CRA cubre los wearables EEG de bienestar que el MDR deja fuera, así que los dos mercados se solapan.
  - La investigación de la idea 4 cuesta unos cientos de euros y da credibilidad en el punto débil de la idea 3.
- **B (7,50)** es la versión más prudente, que es la que proponen los dos debatientes: el PSIRT como anexo, y el canal lateral y la PQC como pruebas técnicas que diferencian frente a las consultoras GRC. Sube el foso de 3 a 5.
- **C (5,95)** apenas mejora a la idea 6 sola (5,90). La ambición sube, pero el capital y el riesgo regulatorio de la idea 13 se comen la mejora. Solo tiene sentido como opción a 18-24 meses, financiada con los ingresos de A o B y con EUDIS/DIANA.

**Nota de neutralidad.** El evaluador no decide. Los números indican que, con menos de 5.000 € y trabajando solo, las ideas mejor puntuadas son extensiones verticales de la consultora actual. Las ideas "deep tech" (13, 9 y 6 en su versión militar) puntúan alto en ambición y bajo en todo lo que pesa en los primeros 12 meses.
