#!/bin/bash

mkdir -p ~/pio-exampes
git clone https://github.com/platformio/platform-ststm32.git ~/pio-exampes/stm32
cd ~/pio-exampes/stm32/examples/arduino-blink
# change board
sed -i "s/nucleo_f401re/nucleo_f446re/" platformio.ini
~/.platformio/penv/bin/pio run -e nucleo_f446re
#~/.platformio/penv/bin/pio run -e nucleo_f446re --target upload
