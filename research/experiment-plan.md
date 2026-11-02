# Plan de experimentos: Paper 1

Objetivo: obtener **datos propios y reproducibles** que respalden el paper, todo en simulación.

## Preguntas

1. **RQ1:** con su configuración por defecto, ¿qué autopilotos de código abierto (ArduPilot y PX4, últimas versiones estables) emiten y aceptan MAVLink sin firma?
2. **RQ2:** con la firma activada, ¿rechaza el vehículo los mensajes sin firma? ¿Qué excepciones permite (por ejemplo, RADIO_STATUS)?
3. **RQ3:** ¿cuánto cuesta en la práctica activar la firma: pasos, soporte en las estaciones de tierra (QGC, Mission Planner) y gestión de claves?
4. **RQ4:** ¿a qué requisitos del anexo I del CRA se asigna cada hallazgo y qué evidencias podría presentar un fabricante?

## Matriz de pruebas

| ID | Autopiloto | Versión | Configuración | Comando |
|---|---|---|---|---|
| E1 | ArduPilot Copter | estable actual | por defecto | `mavaudit scan --target udpin:127.0.0.1:14551 --duration 30 --active-probe --out reports/E1` |
| E2 | ArduPilot Copter | estable actual | firma activada | igual, con `--out reports/E2` |
| E3 | PX4 | estable actual | por defecto | `--target udpin:127.0.0.1:14540 --out reports/E3` |
| E4 | PX4 | estable actual | firma activada (si existe) | igual, con `--out reports/E4` |
| E5 | ArduPilot / PX4 | — | comprobar si QGC / Mission Planner aceptan la firma | manual, con capturas |

En cada prueba se registra: versión exacta (hash de git), sistema operativo, comando usado, informe JSON y una captura de Wireshark (`.pcapng`).

## Reproducibilidad

- Cada informe se guarda en `reports/` (excluido de git; se suben solo los resúmenes al paper).
- Los resultados se anotan en [el diario del vault](../vault/diario/2026-11-02.md).

## Ética

Solo software de código abierto, en simulación local. No se prueban sistemas de terceros. Si aparece algún comportamiento que parezca una vulnerabilidad nueva (no documentada), se informa en privado a los mantenedores por el canal que indique la política de seguridad publicada de cada proyecto (SECURITY.md o la sección de seguridad de su web) **antes** de publicarlo.
