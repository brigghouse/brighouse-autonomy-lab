---
title: Roadmap
date: 2026-11-02
tags: [proyecto, roadmap]
---

# Roadmap

## Hecho

- [x] mavaudit v0.2 (pasivo + sonda de solo lectura, CRA, avisos, `--fail-on`)
- [x] Laboratorio SITL reproducible: ArduPilot 4.7.2, PX4 1.17.0 y PX4 1.18.0-rc1
- [x] Experimentos E1-E4 y [resultados](../../results/README.md)
- [x] Paper v0.2 con resultados

## Siguiente

- [ ] **E5:** interoperabilidad con estaciones de tierra (QGroundControl, Mission Planner, MAVProxy) y la experiencia de aprovisionar la clave. Necesita interfaz gráfica.
- [ ] **E6:** repetición de mensajes (*replay*) y persistencia del timestamp tras reiniciar
- [ ] Repetir con ArduPilot 4.6.3 y con PX4 v1.18.0 final cuando salga
- [ ] Confirmar con los mantenedores de PX4 la frase de las notas de v1.18 sobre "signing in v1.17"
- [ ] Revisar a mano los GitHub Security Advisories de QGC, Mission Planner, pymavlink y MAVSDK
- [ ] Contrastar el texto del CRA y de la 2019/945 (clase C3) con el PDF del Diario Oficial
- [ ] Pasar el paper a LaTeX (IEEEtran), publicarlo en Zenodo (DOI) y enviarlo a arXiv cs.CR
- [ ] mavaudit: aviso del *router* de MAVLink (mavlink-router / MAVProxy) cuando reenvía tramas sin firma

Related: [Diario 2026-11-02](../diario/2026-11-02.md)
