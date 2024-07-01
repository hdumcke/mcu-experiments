#!/bin/bash

mkdir -p ~/pio-exampes
git clone https://github.com/platformio/platform-raspberrypi.git ~/pio-exampes/pico
cd ~/pio-exampes/pico/examples/arduino-blink/
sed -i -e '/board = pico/,+3d' platformio.ini
cat >> platformio.ini << EOF
board = pico
upload_protocol = raspberrypi-swd
debug_speed = 5000
platform_packages =
  toolchain-gccarmnoneeabi@~1.90301.0
EOF
~/.platformio/penv/bin/pio run -e pico
#~/.platformio/penv/bin/pio run -e pico --target upload
