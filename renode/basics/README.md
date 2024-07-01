# Run Example

To run the exmaple:

.. code-block:: bash

   mono /Applications/Renode.app/Contents/MacOS/bin/Renode.exe nrf52_adafruit_feather.resc

To run the exmaple using telnet:

.. code-block:: bash

   workon renode
   renode-run -- --disable-xwt -P 5555
   
To access the monitor run   

.. code-block:: bash

   telnet 127.0.0.1 5555
   
TODO: run example   
   
To run the example from Python:

.. code-block:: bash

   $(which python) pytest.py
   
TODO: fix example
