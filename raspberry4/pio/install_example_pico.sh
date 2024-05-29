#!/bin/bash

cd /tmp
git clone https://github.com/platformio/platform-raspberrypi.git
cd platform-raspberrypi/examples/arduino-blink/
sed -i -e '/board = pico/,+3d' platformio.ini
cat >> platformio.ini << EOF
board = pico
upload_protocol = raspberrypi-swd
debug_speed = 5000
platform_packages =
  toolchain-gccarmnoneeabi@~1.90301.0
EOF
pio run -e pico
pio run -e pico --target upload
