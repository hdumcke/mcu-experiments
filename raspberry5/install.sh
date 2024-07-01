#!/bin/bash

set -e

### Get directory where this script is installed
BASEDIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

sudo apt update
sudo apt install -y git python-is-python3 python3-venv python3-pip curl

$BASEDIR/pio/install.sh
$BASEDIR/pio/install_all_examples.sh
