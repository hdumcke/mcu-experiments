#!/bin/bash

cd $HOME
curl -fsSL https://raw.githubusercontent.com/arduino/arduino-cli/master/install.sh | sh

echo 'PATH=$PATH:$HOME/bin' >> ~/.bashrc
