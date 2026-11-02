#!/usr/bin/env bash
# Build ArduPilot Copter SITL and PX4 SITL (SIH, no Gazebo) on a headless Ubuntu 24.04 box.
# This is the exact sequence used to produce results/ (2 vCPU, 7 GB RAM, ~25 min total).
#
#   bash scripts/setup_sitl.sh [install_dir]     (default: ~/sitl)
#
# Versions are pinned for reproducibility; override with AP_REF / PX4_REF.
set -euo pipefail

DIR="${1:-$HOME/sitl}"
AP_REF="${AP_REF:-Copter-4.7.2}"
PX4_REF="${PX4_REF:-v1.18.0-rc1}"
SUDO=""; [ "$(id -u)" -ne 0 ] && SUDO="sudo"
mkdir -p "$DIR"; cd "$DIR"

echo "== system packages"
$SUDO apt-get update -qq
$SUDO apt-get install -y -qq build-essential g++ python3-dev python3-pip python3-venv git libtool \
    cmake ninja-build ccache libxml2-utils zip

echo "== python packages (virtualenv at $DIR/venv; both builds use it)"
python3 -m venv "$DIR/venv"
# shellcheck disable=SC1091
source "$DIR/venv/bin/activate"
pip install -q "empy==3.3.4" pexpect future lxml pymavlink MAVProxy \
    jinja2 pyyaml kconfiglib jsonschema pyros-genmsg packaging toml numpy psutil pyserial

echo "== ArduPilot $AP_REF"
if [ ! -d ardupilot ]; then
  git clone -q --depth 1 --branch "$AP_REF" --recurse-submodules --shallow-submodules \
      https://github.com/ArduPilot/ardupilot.git
fi
(cd ardupilot && ./waf configure --board sitl && ./waf copter)

echo "== PX4 $PX4_REF"
if [ ! -d px4 ]; then
  git clone -q --depth 1 --branch "$PX4_REF" https://github.com/PX4/PX4-Autopilot.git px4
fi
cd px4
# ModalAI VOXL2 submodules live on gitlab.com and are not needed for SITL: skip them.
git config submodule.libmodal-json.update none
git config submodule.libmodal-pipe.update none
git config submodule.boards/modalai/voxl2/libfc-sensor-api.update none
git submodule update --init --recursive --depth 1 -j 4
# Shallow submodule checkouts can leave empty work trees; restore them.
git submodule foreach --recursive -q 'git reset -q --hard HEAD'
make px4_sitl_default

echo "== done"
echo "ArduPilot: $DIR/ardupilot/build/sitl/bin/arducopter"
echo "PX4:       $DIR/px4/build/px4_sitl_default/bin/px4"
echo "Activate the environment first:  source $DIR/venv/bin/activate && pip install -e ."
echo "Run the experiments:"
echo "  python3 scripts/run_ardupilot.py --ardupilot $DIR/ardupilot --out results/ardupilot-${AP_REF#Copter-}"
echo "  python3 scripts/run_px4.py --px4 $DIR/px4 --out results/px4-${PX4_REF#v}"
