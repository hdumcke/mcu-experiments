Real Time Operating System
==========================

FreeRTOS
--------

Installation
^^^^^^^^^^^^

.. code-block:: bash

   git clone https://github.com/FreeRTOS/FreeRTOS.git --recurse-submodules
   cd FreeRTOS/FreeRTOS/Demo
   mkdir other
   cd other
   git clone https://github.com/FreeRTOS/FreeRTOS-Community-Supported-Demos.git
   
Qemu Demo
^^^^^^^^^

.. code-block:: bash

   cd FreeRTOS/FreeRTOS/Demo/CORTEX_MPS2_QEMU_IAR_GCC/build/gcc
   make
   qemu-system-arm -machine mps2-an385 -cpu cortex-m3 -kernel ./output/RTOSDemo.out -monitor none -nographic -serial stdio
   
Pico Demo
^^^^^^^^^

.. code-block:: bash

   cd FreeRTOS/Demo/other/FreeRTOS-Community-Supported-Demos/CORTEX_M0+_RP2040/
   mkdir build
   cd build
   PICO_SDK_PATH=../../../../../../../Pico/pico-sdk/
   cmake ..
   make -j4
   picotool load ./Standard/main_blinky.uf2
