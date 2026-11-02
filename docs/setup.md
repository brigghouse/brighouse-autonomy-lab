# Montar el laboratorio virtual (coste cero)

Todo corre en tu ordenador: no hace falta ningún dron real ni emitir radio.
Probado en Ubuntu 22.04/24.04 (en Windows, usa WSL2 con Ubuntu).

## 0. Requisitos

- Ubuntu 22.04 o 24.04 (o WSL2), 16 GB de RAM recomendados, unos 15 GB libres
- Python 3.10 o superior, git
- Opcional: Docker

## 1. Este repo y mavaudit

```bash
git clone <url-del-repo-privado> brighouse-autonomy-lab
cd brighouse-autonomy-lab
python3 -m pip install -e ".[dev]"
python3 -m pytest -q          # 5 tests con un vehículo simulado en Python
```

Prueba rápida sin instalar ningún autopiloto:

```bash
# Terminal 1: vehículo falso sin firma (configuración típica por defecto)
python3 -m mavaudit.sim.fake_vehicle --mode unsigned --port 14550
# Terminal 2: auditoría (pasiva + 1 petición de solo lectura)
python3 -m mavaudit scan --target udpin:127.0.0.1:14550 --duration 10 --active-probe
```

Repite con `--mode signed` y `--mode v1` para ver cómo cambian los hallazgos.

## 2. ArduPilot SITL (el firmware real, simulado)

Opción A, nativa (la recomendada por ArduPilot):

```bash
git clone --recurse-submodules https://github.com/ArduPilot/ardupilot.git
cd ardupilot
Tools/environment_install/install-prereqs-ubuntu.sh -y
. ~/.profile
sim_vehicle.py -v ArduCopter --console --map     # arranca SITL + MAVProxy
```

Por defecto MAVProxy reenvía la telemetría a `udp:127.0.0.1:14550` (donde escucha QGroundControl) y a `14551`. Audita con:

```bash
python3 -m mavaudit scan --target udpin:127.0.0.1:14551 --duration 15 --active-probe
```

Opción B, Docker: ver [`docker/ardupilot/Dockerfile`](../docker/ardupilot/Dockerfile) (todavía sin probar en CI).

**Activar la firma de MAVLink en ArduPilot (para el experimento "con firma"):** en la consola de MAVProxy, `module load signing` y `signing setup <frase-secreta>`. Después, en la estación de tierra hay que configurar la misma clave. Comprueba la sintaxis exacta en la documentación de MAVProxy y anota la versión que uses en el diario.

## 3. PX4 SITL

```bash
git clone https://github.com/PX4/PX4-Autopilot.git --recursive
cd PX4-Autopilot
bash ./Tools/setup/ubuntu.sh
make px4_sitl gz_x500        # Gazebo + cuadricóptero x500
```

PX4 publica telemetría hacia `udp:127.0.0.1:14550` (estación de tierra) y tiene un enlace "onboard/offboard" en `14540`. Audita con:

```bash
python3 -m mavaudit scan --target udpin:127.0.0.1:14540 --duration 15 --active-probe
```

Si QGroundControl está abierto en 14550, usa el puerto offboard o cierra QGC. El estado del soporte de firma en PX4 está documentado en [`research/literature-review.md`](../research/literature-review.md).

## 4. Estaciones de tierra (GCS)

- **QGroundControl**: AppImage desde qgroundcontrol.com
- **Mission Planner**: Windows, o Mono en Linux

## 5. Análisis

- **Wireshark** con el disector de MAVLink (genera el plugin Lua con `mavgen --lang=WLua`)
- **pymavlink / MAVProxy**: `pip install pymavlink MAVProxy`
- **Ghidra / binwalk**: análisis de firmware compilado (solo builds propias o de código abierto)

## Reglas del laboratorio

1. Solo simulación, banco cableado o jaula de Faraday. **Nunca** emitir RF ni interferir GNSS sin licencia.
2. Solo sistemas propios o con autorización escrita. mavaudit bloquea por defecto las IP públicas.
3. Cualquier vulnerabilidad nueva se comunica primero a los mantenedores (divulgación coordinada) y se publica después.
