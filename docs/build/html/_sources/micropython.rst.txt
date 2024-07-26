Micro Python
============

https://micropython.org

.. code-block:: bash

   cd /tmp
   wget https://micropython.org/download/rp2-pico/rp2-pico-latest.uf2
   $PICODIR/picotool/build/picotool load /tmp/rp2-pico-latest.uf2 
   cu.usbmodem1414301 # python shell
   >>> import sys
   >>> sys.implementation
   >>> print("Hello, Pico!")
   Hello, Pico!
   >>> from machine import Pin
   >>> led = Pin("LED", Pin.OUT)
   >>> led.value(1)
   >>> led.value(0)
   
rshell
^^^^^^

Installation:

.. code-block:: bash

   sudo pip3 install rshell

Sample session:

.. code-block:: bash

   cd $PICODIR/pico-micropython-examples/blink/
   rshell
   cp blink.py /pyboard/main.py
   ls -l /pyboard
   repl ~ machine.reset() ~
   
webrepl
^^^^^^^

You can access REPL over Wifi. The installation procedure requires the presence of a boot.py file on the board. 

Board installation:

.. code-block:: bash

   import webrepl_setup  # answer the questions

Local installation:

.. code-block:: bash

   git clone https://github.com/micropython/webrepl

Usage:

.. code-block:: bash

   open webrepl/webrepl.html
   
   # connect to 192.168.1.67:8266 where you replace 192.168.1.67 with the IP address of your board
