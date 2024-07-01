#!/bin/bash

mkdir -p ~/pio-exampes
git clone https://github.com/platformio/platform-atmelavr.git ~/pio-exampes/uno
cd ~/pio-exampes/uno/examples/arduino-blink
~/.platformio/penv/bin/pio run -e uno
#~/.platformio/penv/bin/pio run -e uno --target upload
