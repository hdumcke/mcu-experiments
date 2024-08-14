#!/bin/bash

### Get directory where this script is installed
BASEDIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

cd $BASEDIR
rm -rf $BASEDIR/picow_ds4
git clone https://github.com/usedbytes/picow_ds4.git
cd $BASEDIR/picow_ds4
git submodule update --init --recursive
# update MAC address
sed -i "s/8C:41:F2:D0:32:43/8C:41:F2:6B:1B:9F/" src/bt_hid.c
# fix openocd scripts
sed -i "s/picoprobe.cfg/cmsis-dap.cfg/" *.sh
sed -i "s/rp2040.cfg/rp2040.cfg -c \"adapter speed 5000\"/" *.sh
mkdir -p $BASEDIR/picow_ds4/build
cd $BASEDIR/picow_ds4/build
cmake -DPICO_BOARD=pico_w ..
make
../flash.sh src/picow_ds4.elf
