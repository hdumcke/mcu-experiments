#!/bin/bash

cd /tmp
git clone https://github.com/platformio/platform-ststm32.git
cd /tmp/platform-ststm32/examples/arduino-blink
# change board
sed -i "s/nucleo_f401re/nucleo_f446re/" platformio.ini
pio run -e nucleo_f446re
pio run -e nucleo_f446re --target upload
