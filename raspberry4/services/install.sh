#!/bin/bash

### Get directory where this script is installed
BASEDIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

# Install services
mkdir -p ~/services
cp $BASEDIR/micro-ros.service ~/services/
cp $BASEDIR/micro-ros.sh ~/services/
sed -i "s/USER/$USER/" ~/services/*
cd ~/services
sudo ln -s $(realpath .)/micro-ros.service /etc/systemd/system/
