#!/bin/bash

cd /tmp
git clone https://github.com/platformio/platform-teensy.git
cd platform-teensy/examples/arduino-blink
pio run -e teensy41
pio run -e teensy41 --target upload
