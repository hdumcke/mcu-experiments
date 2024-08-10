#!/bin/bash

### Get directory where this script is installed
BASEDIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

cd $BASEDIR
rm -rf $BASEDIR/pico-micropython-examples
git clone https://github.com/raspberrypi/pico-micropython-examples.git
