#!/bin/bash

### Get directory where this script is installed
BASEDIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

cd $BASEDIR
rm -rf button_esp32
cp -r ~/zephyrproject/zephyr/samples/basic/button button_esp32
cd button_esp32
source ~/zephyrproject/zephyr/zephyr-env.sh

west update
west blobs fetch hal_espressif
west build -b esp_wrover_kit
#west flash
#west espressif monitor
