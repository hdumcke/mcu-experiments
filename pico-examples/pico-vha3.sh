#!/bin/bash

### Get directory where this script is installed
BASEDIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

cd $BASEDIR
rm -rf $BASEDIR/pico-vha3
git clone https://github.com/vha3/Hunter-Adams-RP2040-Demos.git pico-vha3
# I am using PNP based circuit to switch transmitter on/off
sed -i "s/gpio_put(TRANSCIEVER_EN, 0)/gpio_put(TRANSCIEVER_EN, X)/" pico-vha3/Networking/CAN/can_driver.h
sed -i "s/gpio_put(TRANSCIEVER_EN, 1)/gpio_put(TRANSCIEVER_EN, 0)/" pico-vha3/Networking/CAN/can_driver.h
sed -i "s/gpio_put(TRANSCIEVER_EN, X)/gpio_put(TRANSCIEVER_EN, 1)/" pico-vha3/Networking/CAN/can_driver.h
sed -i "8i pico_enable_stdio_usb(can_transciever 1)" pico-vha3/Networking/CAN/CMakeLists.txt
sed -i "8i pico_enable_stdio_uart(can_transciever 0)" pico-vha3/Networking/CAN/CMakeLists.txt
sed -i "8i # enable usb output, disable uart output" pico-vha3/Networking/CAN/CMakeLists.txt
sed -i "/number_to_send+1/a \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ printf(\"MY_ARBITRATION_VALUE: %04x arbitration: %04x\\\n\", MY_ARBITRATION_VALUE, arbitration) ;" pico-vha3/Networking/CAN/can_demo.c
mkdir -p $BASEDIR/pico-vha3/build
cd $BASEDIR/pico-vha3/build
echo '#!/bin/bash' > node1.sh
echo 'sed -i "s/#define MY_ARBITRATION_VALUE.*/#define MY_ARBITRATION_VALUE     0x1234/" ../Networking/CAN/can_parameters.h' >> node1.sh
echo 'sed -i "s/unsigned short arbitration.*/unsigned short arbitration = 0x2234 ;/" ../Networking/CAN/can_parameters.h' >> node1.sh
echo '#!/bin/bash' > node2.sh
echo 'sed -i "s/#define MY_ARBITRATION_VALUE.*/#define MY_ARBITRATION_VALUE     0x2234/" ../Networking/CAN/can_parameters.h' >> node2.sh
echo 'sed -i "s/unsigned short arbitration.*/unsigned short arbitration = 0x3234 ;/" ../Networking/CAN/can_parameters.h' >> node2.sh
echo '#!/bin/bash' > node3.sh
echo 'sed -i "s/#define MY_ARBITRATION_VALUE.*/#define MY_ARBITRATION_VALUE     0x3234/" ../Networking/CAN/can_parameters.h' >> node3.sh
echo 'sed -i "s/unsigned short arbitration.*/unsigned short arbitration = 0x4234 ;/" ../Networking/CAN/can_parameters.h' >> node3.sh
echo '#!/bin/bash' > node4.sh
echo 'sed -i "s/#define MY_ARBITRATION_VALUE.*/#define MY_ARBITRATION_VALUE     0x4234/" ../Networking/CAN/can_parameters.h' >> node4.sh
echo 'sed -i "s/unsigned short arbitration.*/unsigned short arbitration = 0x1234 ;/" ../Networking/CAN/can_parameters.h' >> node4.sh
chmod +x node*.sh
cmake ..
make
