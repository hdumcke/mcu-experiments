#!/bin/bash

set -e

### Get directory where this script is installed
BASEDIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

sudo apt update
sudo apt install -y git openssh-server python-is-python3 python3-venv curl python3-pip

$BASEDIR/tools/install_screen_commander.sh
$BASEDIR/pio/install.sh
$BASEDIR/ros2/install.sh
$BASEDIR/services/install.sh

# enable uart3 and 4
echo "dtoverlay=uart3" | sudo tee -a /boot/firmware/config.txt

# UART GPIO
# 0    14/15
# 1    14/15
# 2    0/1
# 3    4/5
# 4    8/9
# 5    12/13
