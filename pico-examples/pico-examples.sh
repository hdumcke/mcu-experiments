#!/bin/bash

### Get directory where this script is installed
BASEDIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

cd $BASEDIR
rm -rf $BASEDIR/pico-examples
git clone https://github.com/raspberrypi/pico-examples
mkdir -p $BASEDIR/pico-examples/build
cd $BASEDIR/pico-examples/build
cmake ..
make
