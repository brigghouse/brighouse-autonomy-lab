# Brighouse Autonomy Security Lab

Investigación defensiva de seguridad en drones, robots y sistemas autónomos, con foco en el **EU Cyber Resilience Act (CRA)**. Repositorio privado de [Brighouse Security Labs](https://brighousesec.com).

## Qué hay aquí

| Carpeta | Contenido |
|---|---|
| [`mavaudit/`](mavaudit/) | **mavaudit**: auditor defensivo de configuración MAVLink. Detecta MAVLink 1, tráfico sin firma y si el vehículo responde a peticiones sin firma, y asigna cada hallazgo a un requisito del anexo I del CRA |
| [`tests/`](tests/) | Tests con un vehículo MAVLink simulado en Python (no requieren autopiloto) |
| [`docs/setup.md`](docs/setup.md) | Cómo montar el laboratorio virtual: ArduPilot y PX4 SITL, Gazebo, QGC, Wireshark |
| [`docs/example-report-unsigned.md`](docs/example-report-unsigned.md) | Informe de ejemplo |
| [`docker/`](docker/) | Dockerfile de ArduPilot SITL (sin probar en CI) |
| [`research/`](research/) | Revisión bibliográfica, plan de experimentos y research de mercado |
| [`paper/`](paper/) | Borrador del Paper 1 |
| [`vault/`](vault/INDEX.md) | Segundo cerebro (vault de Obsidian): plan, decisiones, diario y aprendizajes |

## Uso rápido

```bash
python3 -m pip install -e ".[dev]"
python3 -m pytest -q
python3 -m mavaudit.sim.fake_vehicle --mode unsigned --port 14550 &
python3 -m mavaudit scan --target udpin:127.0.0.1:14550 --duration 10 --active-probe
```

## Principios

- **Pasivo por defecto.** La única prueba activa (`--active-probe`) envía una sola petición de parámetro de solo lectura.
- **Ámbito restringido.** Solo direcciones de loopback o privadas, salvo `--authorized --scope-ref <id>` con autorización escrita.
- **Solo simulación o banco.** Nada de emisión RF ni interferencias.
- **Divulgación coordinada** de cualquier vulnerabilidad nueva.
- El mapeo al CRA es una interpretación técnica, no asesoramiento jurídico.

## Estado

v0.1 (2026-11-02). Siguientes pasos en [`vault/proyecto/pendientes.md`](vault/proyecto/pendientes.md).
