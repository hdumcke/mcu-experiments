#!/bin/bash

### Get directory where this script is installed
BASEDIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

$BASEDIR/install_example_esp32.sh
$BASEDIR/install_example_pico.sh
$BASEDIR/install_example_stm32.sh
$BASEDIR/install_example_teensy41.sh
$BASEDIR/install_example_uno.sh
