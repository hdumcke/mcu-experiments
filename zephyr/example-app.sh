#!/bin/bash

### Get directory where this script is installed
BASEDIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

cd $BASEDIR
west init -m https://github.com/zephyrproject-rtos/example-application --mr main my-workspace
cd my-workspace
west update
cd example-application
west build -b custom_plank app

cd doc
doxygen
#TODO error seams to be related to https://github.com/doxygen/doxygen/issues/10110, to investigate
pip install -r requirements.txt
make html
