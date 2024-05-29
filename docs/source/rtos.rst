Real Time Operating System
==========================

https://micro.ros.org/docs/concepts/rtos/comparison/

FreeRTOS
--------

https://www.freertos.org

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

Zephyr
------

https://www.zephyrproject.org

https://docs.zephyrproject.org/latest/develop/getting_started/index.html

Install on MacOS
^^^^^^^^^^^^^^^^

.. code-block:: bash

   brew install cmake ninja gperf python3 ccache qemu dtc libmagic wget openocd
   mkvirtualenv zephyr
   $(which pip) install west
   west init ~/zephyrproject
   cd ~/zephyrproject
   west update
   west zephyr-export
   $(which pip) install -r ~/zephyrproject/zephyr/scripts/requirements.txt
   cd ~
   curl -L -O https://github.com/zephyrproject-rtos/sdk-ng/releases/download/v0.16.5-1/zephyr-sdk-0.16.5-1_macos-x86_64.tar.xz
   curl -L https://github.com/zephyrproject-rtos/sdk-ng/releases/download/v0.16.5-1/sha256.sum | shasum --check --ignore-missing
   tar xvf zephyr-sdk-0.16.5-1_macos-x86_64.tar.xz
   cd zephyr-sdk-0.16.5-1
   ./setup.sh
  
   cd ~/zephyrproject/zephyr
   west build -b qemu_x86 samples/hello_world
   west build -t run


NuttX
-----

https://nuttx.apache.org

Install on MacOS
^^^^^^^^^^^^^^^^

.. code-block:: bash

   brew tap discoteq/discoteq
   brew install flock
   brew install x86_64-elf-gcc  # Used by simulator
   brew install u-boot-tools  # Some platform integrate with u-boot
  
   cd /tmp
   git clone https://bitbucket.org/nuttx/tools.git
   cd tools/kconfig-frontends
   patch < ../kconfig-macos.diff -p 1
   ./configure --enable-mconf --disable-shared --enable-static --disable-gconf --disable-qconf --disable-nconf
   make
   sudo make install
   
   brew install --cask gcc-arm-embedded
   
   mkdir nuttxspace
   cd nuttxspace
   git clone https://github.com/apache/nuttx.git nuttx
   git clone https://github.com/apache/nuttx-apps apps
   
   # Prerequisites For macOS
   cd /tmp
   git clone https://github.com/chexum/genromfs.git
   cd genromfs
   make
   sudo cp genromfs /usr/local/bin/
  
   # To list all supported configurations 
   cd nuttx
   ./tools/configure.sh -L | less
  
  ./tools/configure.sh -m sim:nsh
  make menuconfig  # optional
  make
  
  ./nuttx  # login: admin password: Administrator
  nsh> poweroff
