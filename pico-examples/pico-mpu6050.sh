#!/bin/bash

### Get directory where this script is installed
BASEDIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

cd $BASEDIR
rm -rf $BASEDIR/pico-mpu6050
git clone https://github.com/HumansAreWeak/rpi-pico-mpu6050.git pico-mpu6050
mkdir -p $BASEDIR/pico-mpu6050/build
cd $BASEDIR/pico-mpu6050/build
cmake ..
make
