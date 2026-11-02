# ArduPilot SITL (software-in-the-loop) for the Brighouse Autonomy Security Lab.
# Build:  docker build -t bas-ardupilot-sitl docker/ardupilot
# Run:    docker run --rm -it -p 5760:5760 bas-ardupilot-sitl
# Then:   python -m mavaudit scan --target tcp:127.0.0.1:5760 --duration 15
#
# NOTE: not yet built in CI. If the ref below no longer exists, pick a current
# stable tag from https://github.com/ArduPilot/ardupilot/tags (e.g. Copter-4.x.y).
FROM ubuntu:22.04

ARG ARDUPILOT_REF=Copter-4.7.2
ENV DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC

RUN apt-get update && apt-get install -y --no-install-recommends \
        git sudo lsb-release tzdata ca-certificates python3 python3-pip \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m ap && echo "ap ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers
USER ap
WORKDIR /home/ap

RUN git clone --depth 1 --branch ${ARDUPILOT_REF} --recurse-submodules --shallow-submodules \
        https://github.com/ArduPilot/ardupilot.git

WORKDIR /home/ap/ardupilot
RUN USER=ap SKIP_AP_GRAPHIC_ENV=1 SKIP_AP_COV_ENV=1 SKIP_AP_GIT_CHECK=1 \
        Tools/environment_install/install-prereqs-ubuntu.sh -y
RUN bash -lc "./waf configure --board sitl && ./waf copter"

EXPOSE 5760
# Default params, no MAVProxy: the vehicle listens on TCP 5760 (SERIAL0).
CMD ["bash", "-lc", "build/sitl/bin/arducopter --model + --speedup 1 -I0 --defaults Tools/autotest/default_params/copter.parm"]
