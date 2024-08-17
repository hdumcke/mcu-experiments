#!/bin/bash

### Get directory where this script is installed
BASEDIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

cd $BASEDIR
rm -rf $BASEDIR/pico-vl53l0x
git clone https://github.com/kevinmcaleer/vl53l0x.git $BASEDIR/pico-vl53l0x
cd $BASEDIR/pico-vl53l0x
echo cp vl53l0x.py /pyboard > /tmp/cmd
echo cp tof_test.py /pyboard >> /tmp/cmd
echo 'repl ~ machine.reset() ~' >> /tmp/cmd
rshell -f /tmp/cmd
