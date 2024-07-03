#!/bin/bash

### Get directory where this script is installed
BASEDIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

cd $BASEDIR
rm -rf blinky_nucleo
cp -r ~/zephyrproject/zephyr/samples/basic/blinky blinky_nucleo
cd blinky_nucleo
source ~/zephyrproject/zephyr/zephyr-env.sh

west build -b nucleo_f411re

cp build/zephyr/zephyr.bin /Volumes/NOD_F446RE
