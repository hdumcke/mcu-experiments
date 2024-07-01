#!/bin/bash

mkdir -p ~/pio-exampes
git clone https://github.com/platformio/platform-espressif32.git ~/pio-exampes/esp32
cd ~/pio-exampes/esp32/examples/espidf-arduino-blink
~/.platformio/penv/bin/pio run -e esp32dev
#~/.platformio/penv/bin/pio run -e esp32dev --target upload
