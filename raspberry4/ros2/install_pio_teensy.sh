#!/bin/bash

# Start from scratch
rm -rf  ~/.platformio/

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
cat >> /tmp/TeensyTest/platformio.ini << EOF
lib_deps =
    https://github.com/micro-ROS/micro_ros_platformio
EOF
cd /tmp/TeensyTest
pio lib install
