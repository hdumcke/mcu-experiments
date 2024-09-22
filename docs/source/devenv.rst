Development Environments
========================

Status
------
+-------------+--------+-------------------------+---------+
|             | Mac OS | Raspberry Pi            | Windows |
+=============+========+=========================+=========+
| CubeIDE     | OK     | n/a                     | ?       |
+-------------+--------+-------------------------+---------+
| esp-idf     | OK     | OK                      | ?       |
+-------------+--------+-------------------------+---------+
| Arduino-cli | OK     | OK                      | ?       |
+-------------+--------+-------------------------+---------+
| Teensy      | OK     | not working on bookworm | ?       |
+-------------+--------+-------------------------+---------+
| RP2040      | OK     | OK                      | ?       |
+-------------+--------+-------------------------+---------+
| VS Code     | OK     | OK                      | ?       |
+-------------+--------+-------------------------+---------+
| PlatformIO  | OK     | OK                      | ?       |
+-------------+--------+-------------------------+---------+
| gdb         |        |                         | ?       |
+-------------+--------+-------------------------+---------+
| OpenOCD     |        |                         | ?       |
+-------------+--------+-------------------------+---------+
| pyOCD       |        |                         | ?       |
+-------------+--------+-------------------------+---------+
| Debug Probe |        |                         | ?       |
+-------------+--------+-------------------------+---------+

STM32
-----

Installation of CubeIDE
^^^^^^^^^^^^^^^^^^^^^^^

https://www.st.com/en/development-tools/stm32cubeide.html

Requires registration with ST

Example Program
^^^^^^^^^^^^^^^

https://wiki.st.com/stm32mcu/wiki/STM32StepByStep:Step2_Blink_LED

On Raspberry Pi
^^^^^^^^^^^^^^^

TODO: Try binutils-arm-none-eabi tool chain

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
   arduino-cli compile -b teensy:avr:teensy41 --output-dir build .
   teensy_loader_cli -w -s --mcu=TEENSY41 build/Blink.ino.hex # push reset button (Mac OS)
   
TODO: reset not supported on Mac OS, is there an other solution?

Reset the Teensy to it's shipping program, by holding in the program button for something like 20 seconds, until the small led near the USB blinks and then release. 

TODO: Teensy support for RPi (Bookworm) Apparently it is working for Ubuntu

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
   
Note: Integration into Arduino https://www.tomshardware.com/how-to/program-raspberry-pi-pico-with-arduino-ide
   
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
   sudo make install
   
Flash example:

.. code-block:: bash

   cd $PICODIR/pico-examples/build
   $PICODIR/picotool/build/picotool info -a
   $PICODIR/picotool/build/picotool load ./hello_world/usb/hello_usb.uf2
   $PICODIR/picotool/build/picotool reboot
   screen /dev/cu.usbmodem1424301
   
Raspberry Pi Debug Probe
^^^^^^^^^^^^^^^^^^^^^^^^

https://www.raspberrypi.com/documentation/microcontrollers/debug-probe.html#serial-wire-debug-swd

Flash example:

.. code-block:: bash

   cd $PICODIR/pico-examples/build
   openocd -f interface/cmsis-dap.cfg -f target/rp2040.cfg -c "adapter speed 5000" -c "program blink/blink.elf verify reset exit"
   
Debug example:

.. code-block:: bash

   openocd -f interface/cmsis-dap.cfg -f target/rp2040.cfg -c "adapter speed 5000"

2nd terminal

.. code-block:: bash

   cd $PICODIR/pico-examples/build/blink
   gdb blink.elf
   target remote localhost:3333
   monitor reset init
   continue

TODO: compile with debugging symbols
      Run debugger with vi

Pico Programming using Raspberry Pi
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   sudo apt install -y cmake gcc-arm-none-eabi libnewlib-arm-none-eabi libstdc++-arm-none-eabi-newlib
   git clone --recursive -b master https://github.com/~/pico-sdk.git
   git clone -b master https://github.com/~co-examples.git
   git clone https://github.com/~/picotool.git --branch master
   mkdir picotool/build
   cd picotool/build
   export PICO_SDK_PATH=../../pico-sdk
   cmake ..
   make
   sudo make install
   cd ../..
   mkdir pico-examples/build
   cd pico-examples/build
   export PICO_SDK_PATH=../../pico-sdk
   cmake ..
   make
   openocd -f interface/cmsis-dap.cfg -f target/rp2040.cfg -c "adapter speed 5000" -c "program blink/blink.elf verify reset exit"
   
Arduino IDE
-----------

https://www.youtube.com/watch?v=nL34zDTPkcs

https://www.arduino.cc/reference/en/

VS Code
-------

https://code.visualstudio.com

Install on Mac OS
^^^^^^^^^^^^^^^^^

Download and install MacOS installer

Install on Raspberry Pi
^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   sudo apt update
   sudo apt install code


PlatformIO
----------

https://platformio.org/install/ide?install=vscode

Install on Mac OS
^^^^^^^^^^^^^^^^^

.. code-block:: bash

   brew install platformio
   cd /tmp
   git clone https://github.com/platformio/platform-teensy.git
   cd platform-teensy/examples/arduino-blink
   pio run -e teensy41
   pio run -e teensy41 --target upload
   pio run --target clean
   
   # new project
   mkdir -p /tmp/TeensyTest
   pio project init -d /tmp/TeensyTest --board teensy41 --project-option "framework=arduino"

VI Ingetreation
^^^^^^^^^^^^^^^

https://github.com/normen/vim-pio

Install on Raspberry PI
^^^^^^^^^^^^^^^^^^^^^^^

See directory raspberry4/pio/

Status
^^^^^^

Compiling and uploading blink executing the following commands

.. code-block:: bash

   cd ~/pio-exampes/uno/examples/arduino-blink
   pio run -e uno --target upload
   
   cd ~/pio-exampes/uno/examples/arduino-blink
   echo "[env:nanoatmega328]" >> platformio.ini
   echo "platform = atmelavr" >> platformio.ini
   echo "board = nanoatmega328" >> platformio.ini
   echo "framework = arduino" >> platformio.ini
   pio run -e nanoatmega328 --target upload

   cd ~/pio-exampes/esp32/examples/espidf-arduino-blink
   pio run -e esp32dev --target upload

   cd ~/pio-exampes/stm32/examples/arduino-blink/
   sed -i "s/f401/f446/" platformio.ini
   pio run -e nucleo_f446re --target upload

   cd ~/pio-exampes/pico/examples/arduino-blink
   sed -i "/board = pico/a \ \ toolchain-gccarmnoneeabi@~1.90301.0" platformio.ini
   sed -i "/board = pico/a platform_packages =" platformio.ini
   sed -i "/board = pico/a debug_speed = 5000" platformio.ini
   sed -i "/board = pico/a upload_protocol = picotool" platformio.ini
   pio run -e pico --target upload

+-------+--------+--------------+---------+
|       | Mac OS | Raspberry Pi | Windows |
+=======+========+==============+=========+
| uno   | OK     | OK           | ?       |
+-------+--------+--------------+---------+
| nano  | NOT OK | NOT OK       | ?       |
+-------+--------+--------------+---------+
| esp32 | OK     | OK           | ?       |
+-------+--------+--------------+---------+
| stm32 | NOT OK | OK           | ?       |
+-------+--------+--------------+---------+
| pico  | OK     | OK           | ?       |
+-------+--------+--------------+---------+
  
ToDo
^^^^

Investigate error message for stm32 on MacOS: "** OpenOCD init failed **"

Investigate error message for nano: "avrdude: stk500_recv(): programmer is not responding"

Debugger
--------

gdb
^^^

https://en.wikipedia.org/wiki/GNU_Debugger

https://sourceware.org/gdb/current/onlinedocs/gdb.html/

https://sourceware.org/gdb/wiki/Internals

OpenOCD
-------

OpenOCD stands for Open On-Chip Debugger. It aims to provide debugging, in-system program- ming and boundary-scan testing for embedded target devices.

Detail can be found in the user guide https://openocd.org/doc/pdf/openocd.pdf

.. code-block:: bash

   brew install openocd
   
pyOCD
-----

https://pyocd.io

Create a Python virtual environment and install with

.. code-block:: bash

   pip install pyocd

