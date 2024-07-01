#!/bin/bash

mkdir -p ~/pio-exampes
git clone https://github.com/platformio/platform-teensy.git ~/pio-exampes/teensy
cd ~/pio-exampes/teensy/examples/arduino-blink
~/.platformio/penv/bin/pio run -e teensy41
#~/.platformio/penv/bin/pio run -e teensy41 --target upload
