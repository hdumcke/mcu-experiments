#!/bin/bash

set -e

### Get directory where this script is installed
BASEDIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

# Fix cloud-init script and remove this work around
echo "$USER ALL=(ALL) NOPASSWD:ALL" | sudo tee /etc/sudoers.d/$USER
sudo chmod 640 /etc/sudoers.d/$USER

sudo apt update
sudo apt install -y git openssh-server python-is-python3 python3-virtualenv curl

$BASEDIR/tools/install_screen_commander.sh
$BASEDIR/pio/install.sh
$BASEDIR/ros2/install.sh
$BASEDIR/ros2/build_example_linux.sh
