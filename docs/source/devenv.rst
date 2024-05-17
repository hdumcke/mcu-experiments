Development Environments
========================

STM32
-----

https://www.st.com/en/development-tools/stm32cubeide.html

Requires registration with ST

esp32
-----

https://docs.espressif.com/projects/esp-idf/en/stable/esp32/index.html

.. code-block:: bash

   brew install cmake ninja dfu-util
   mkdir -p ~/esp
   cd ~/esp
   git clone -b v5.2.1 --recursive https://github.com/espressif/esp-idf.git
   cd ~/esp/esp-idf
   ./install.sh esp32

Building the examples:

.. code-block:: bash

   . $HOME/esp/esp-idf/export.sh
   cd ~/esp/esp-idf/examples/get-started/hello_world
   idf.py set-target esp32
   idf.py menuconfig  # not required for this simple application
   idf.py -p /dev/cu.usbserial-0001 flash monitor  # use Ctrl + ] to exit monitor


Arduino
-------

https://support.arduino.cc/hc/en-us/articles/360019833020-Download-and-install-Arduino-IDE # only required if you want a GUI

https://github.com/arduino/arduino-cli

.. code-block:: bash

   git clone https://github.com/arduino/arduino-examples
   cd arduino-examples/examples/01.Basics/Blink/
   arduino-cli board list  # provides board name and port
   arduino-cli compile -b arduino:avr:uno --output-dir build .
   arduino-cli upload -b arduino:avr:uno .
   
Teensy
------

https://www.pjrc.com/teensy/loader.html
https://github.com/PaulStoffregen/teensy_loader_cli

.. code-block:: bash

   git clone https://github.com/arduino/arduino-examples
   cd arduino-examples/examples/01.Basics/Blink/
   arduino-cli board list  # provides board name and port
   arduino-cli compile -b teensy:avr:teensy41 .
   teensy_loader_cli -w -s --mcu=TEENSY41 build/Blink.ino.hex
   
TODO: needs more work   

Reset the Teensy to it's shipping program, by holding in the program button for something like 20 seconds, until the small led near the USB blinks and then release. 

TODO: Teensy support for RPi

RP2040
------

https://datasheets.raspberrypi.com/pico/getting-started-with-pico.pdf

.. code-block:: bash

   brew install cmake
   brew tap ArmMbed/homebrew-formulae
   brew install gcc-arm-embedded
   mkdir Pico
   cd ./Pico/
   PICODIR=$(pwd)
   git clone --recursive -b master https://github.com/raspberrypi/pico-sdk.git
   git clone -b master https://github.com/raspberrypi/pico-examples.git

Building the examples:

.. code-block:: bash

   mkdir $PICODIR/pico-examples/build
   cd $PICODIR/pico-examples/build
   export PICO_SDK_PATH=../../pico-sdk
   cmake ..
   make
   
picotool
^^^^^^^^

.. code-block:: bash

   brew install libusb pkg-config
   git clone https://github.com/raspberrypi/picotool.git --branch master
   cd picotool
   mkdir build
   cd build
   export PICO_SDK_PATH=../../pico-sdk
   cmake ..
   make

.. code-block:: bash

   cd $PICODIR/pico-examples/build
   $PICODIR/picotool/build/picotool info -a
   $PICODIR/picotool/build/picotool load ./hello_world/usb/hello_usb.uf2
   $PICODIR/picotool/build/picotool reboot
   screen /dev/cu.usbmodem1424301
   
Arduino IDE
-----------

https://www.youtube.com/watch?v=nL34zDTPkcs

https://www.arduino.cc/reference/en/

VS Code
-------

https://code.visualstudio.com

PlatformIO
----------

https://platformio.org/install/ide?install=vscode
   
Debugger
--------

OpenOCD
-------

OpenOCD stands for Open On-Chip Debugger. It aims to provide debugging, in-system program- ming and boundary-scan testing for embedded target devices.

Detail can be found in the user guide https://openocd.org/doc/pdf/openocd.pdf

.. code-block:: bash

   brew install openocd
   
pyOCD
-----

https://pyocd.io

