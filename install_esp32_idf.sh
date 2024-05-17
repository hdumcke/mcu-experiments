#!/bin/bash
sudo apt-get install -y git wget flex bison gperf python3 python3-pip python3-venv cmake ninja-build ccache libffi-dev libssl-dev dfu-util libusb-1.0-0

mkdir -p ~/esp
cd ~/esp
git clone -b v5.2.1 --recursive https://github.com/espressif/esp-idf.git

cd ~/esp/esp-idf
./install.sh all

echo "alias get_idf='. \$HOME/esp/esp-idf/export.sh'" >> ~/.bashrc
