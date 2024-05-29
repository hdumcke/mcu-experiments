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

