#!/bin/bash

### Get directory where this script is installed
BASEDIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

cd $BASEDIR
cp -r ~/zephyrproject/zephyr/samples/basic/button .
cd button
source ~/zephyrproject/zephyr/zephyr-env.sh

west build -b nucleo_f411re

cat > app.overlay << EOF
/ {

    gpio_keys {
        compatible = "gpio-keys";
        user_button: button {
            label = "User";
            gpios = <&gpio0 28 GPIO_ACTIVE_LOW>;
        };
    };

    aliases {
        sw0 = &user_button;
    };
};
EOF

sed -i "4i set(BOARD rpi_pico)"  CMakeLists.txt

west build

