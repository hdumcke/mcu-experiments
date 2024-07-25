Virtualisation
==============

Quemu
-----

https://www.qemu.org

Renode
------

https://github.com/renode/renode

https://renode.io

https://interrupt.memfault.com/blog/intro-to-renode

https://github.com/tarciszera/renode_guide

Installation for MacOS
^^^^^^^^^^^^^^^^^^^^^^

https://download.mono-project.com/archive/2.10.6/macos-10-x86/1/MonoFramework-MRE-2.10.6_1.macos10.xamarin.x86.dmg

.. code-block:: bash

   cd /tmp
   wget https://download.mono-project.com/archive/6.12.0/macos-10-universal/MonoFramework-MDK-6.12.0.206.macos10.xamarin.universal.pkg
   open MonoFramework-MDK-6.12.0.206.macos10.xamarin.universal.pkg
   # install package
   echo "export PATH=/Library/Frameworks/Mono.framework/Versions/Current/bin:\$PATH" >> ~/.bash_profile
   wget https://github.com/renode/renode/releases/download/v1.15.0/renode_1.15.0.dmg
   open renode_1.15.0.dmg
   # drag to application folder
   echo "" >> ~/.bash_profile
   echo "#required for renode" >> ~/.bash_profile
   echo PATH=/Library/Frameworks/Mono.framework/Versions/Current/bin:\$PATH >> ~/.bash_profile
   mkvirtualenv renode
   ./renode/setup-virtenv.sh

PlatformIO Integration
^^^^^^^^^^^^^^^^^^^^^^

https://github.com/carlosedp/PlatformIO-Renode-Demos

Wokwi
-----

https://wokwi.com

TinkerCAD
---------

https://www.tinkercad.com/circuits
