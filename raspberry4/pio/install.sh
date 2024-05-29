#!/bin/bash

cd /tmp
curl -fsSL -o get-platformio.py https://raw.githubusercontent.com/platformio/platformio-core-installer/master/get-platformio.py
python3 get-platformio.py
export PATH=$PATH:~/.platformio/penv/bin
echo "PATH=$PATH:~/.platformio/penv/bin" >> ~/.bashrc

curl -fsSL https://raw.githubusercontent.com/platformio/platformio-core/develop/platformio/assets/system/99-platformio-udev.rules | sudo tee /etc/udev/rules.d/99-platformio-udev.rules
sudo service udev restart

# Install Teensy 4.1
mkdir -p /tmp/TeensyTest
pio project init -d /tmp/TeensyTest --board teensy41 --project-option "framework=arduino"

# Install Raspberry Pico
mkdir -p /tmp/PicoTest
pio project init -d /tmp/PicoTest --board pico
# Fix platformio issue
cat >> /tmp/PicoTest/platformio.ini << EOF
platform_packages =
  toolchain-gccarmnoneeabi@~1.90301.0
EOF
cd /tmp/PicoTest
pio run -e pico

# support for pico probe
echo 'SUBSYSTEMS=="usb", ATTRS{idVendor}=="2e8a", ATTRS{idProduct}=="0004", MODE="0666"' | sudo tee -a /etc/udev/rules.d/98-PicoProbe.rules
sudo udevadm control --reload
sudo udevadm trigger -w -s usb
sudo usermod -a -G dialout $USER

# Install Arduino Uno
mkdir -p /tmp/UnoTest
pio project init -d /tmp/UnoTest --board uno

# Install ESP32
mkdir -p /tmp/ESP32Test
pio project init -d /tmp/ESP32Test --board esp32dev

# Install STM32
mkdir -p /tmp/STM32Test
pio project init -d /tmp/STM32Test --board nucleo_f446re
