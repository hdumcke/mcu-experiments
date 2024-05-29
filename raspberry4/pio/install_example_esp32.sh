#!/bin/bash

cd /tmp
git clone https://github.com/platformio/platform-espressif32.git
cd /tmp/platform-espressif32/examples/espidf-arduino-blink
pio run -e esp32dev
pio run -e esp32dev --target upload
