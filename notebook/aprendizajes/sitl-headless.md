---
title: Montar SITL sin Docker ni Gazebo
date: 2026-11-02
tags: [aprendizaje, sitl, px4, ardupilot]
---

# Montar SITL sin Docker ni Gazebo (VM en la nube, 2 vCPU, 7 GB)

El script completo es [scripts/setup_sitl.sh](../../scripts/setup_sitl.sh). Lo que costó averiguar:

1. **ArduPilot:** basta con `./waf configure --board sitl && ./waf copter`; no hace falta `install-prereqs`, solo `g++`, `python3-dev`, `empy==3.3.4`, `pexpect`, `future` y `lxml`. Tarda unos 9 minutos. **SERIAL0 espera a que alguien se conecte por TCP 5760 antes de arrancar**: hay que conectarse primero a ese puerto. SERIAL1 se abre con `--serial1 tcp:2`, que es el puerto 5762.
2. **PX4:** algunos submódulos de ModalAI VOXL2 están en gitlab.com, que no es accesible desde la nube. No hacen falta para SITL, así que se marcan con `git config submodule.<nombre>.update none` (atención: el nombre del submódulo no siempre coincide con su ruta; mira `.gitmodules`).
3. **PX4:** después de un `git submodule update --depth 1`, algunos submódulos quedaron con el `.git` pero **sin archivos** (heatshrink, gps/devices) y CMake fallaba con "No SOURCES given". Se arregla con `git submodule foreach --recursive 'git reset --hard HEAD'`.
4. **PX4 sin Gazebo:** `PX4_SIM_MODEL=sihsim_quadx bin/px4 -d etc -w <rootfs>` usa la física SIH integrada. El enlace GCS envía a udp 14550 y el enlace Onboard a udp 14540, y solo escuchan en localhost.
5. **PX4 v1.18:** la clave de firma se guarda en `<rootfs>/mavlink/mavlink-signing-key.bin` (40 bytes).
6. **pymavlink no decodifica algunos ID de mensaje de PX4 1.18** (290, 291, 380, 411, 514, 8), ni siquiera con el dialecto `all`. mavaudit lee el sysid/compid de la cabecera cruda para no atribuirlos al sistema 0, y la comprobación con clave los excluye.
7. **`git describe` en un clon superficial de ArduPilot** devuelve una etiqueta equivocada (APMrover2-beta), porque hay muchas etiquetas en el mismo commit. Mejor `git tag --points-at HEAD`, filtrando las que llevan número de versión.
8. **`pkill -f arducopter` se mata a sí mismo** si la línea de comandos contiene "arducopter". Usa `pkill -x`.

Related: [Diario 2026-11-02](../diario/2026-11-02.md) · [pymavlink y MAVLink 2](pymavlink-mavlink2.md)
