#!/bin/bash

cd /tmp
git clone https://github.com/platformio/platform-atmelavr.git
cd platform-atmelavr/examples/arduino-blink
pio run -e uno
pio run -e uno --target upload
