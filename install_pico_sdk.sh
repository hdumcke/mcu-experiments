#!/bin/bash

sudo apt update
sudo apt install -y cmake gcc-arm-none-eabi libnewlib-arm-none-eabi build-essential libusb-1.0-0-dev screen

cd ~
mkdir pico
cd pico
git clone --recursive -b master https://github.com/raspberrypi/pico-sdk.git
git clone -b master https://github.com/raspberrypi/pico-examples.git
git clone https://github.com/raspberrypi/picotool.git --branch master
cd picotool
mkdir build
cd build
export PICO_SDK_PATH=~/pico/pico-sdk
cmake ..
make -j4

echo "PATH=\$PATH:$(pwd)" >> ~/.bashrc

echo 'SUBSYSTEM=="usb", ATTRS{idVendor}=="2e8a", ATTRS{idProduct}=="0003", MODE="0666"' | sudo tee /etc/udev/rules.d/99-pico.rules
echo 'SUBSYSTEM=="tty", ATTRS{idVendor}=="2e8a", ATTRS{idProduct}=="0005", SYMLINK+="pico"' | sudo tee -a /etc/udev/rules.d/99-pico.rules
