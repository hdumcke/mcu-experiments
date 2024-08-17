#!/bin/bash

### Get directory where this script is installed
BASEDIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

cd $BASEDIR
rm -rf $BASEDIR/vha3
git clone https://github.com/vha3/Hunter-Adams-RP2040-Demos.git vha3
mkdir -p $BASEDIR/vha3/build
cd $BASEDIR/vha3/build
cmake ..
make
