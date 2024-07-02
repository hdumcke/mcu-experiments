#!/bin/bash

### Get directory where this script is installed
BASEDIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

cd $BASEDIR
rm -rf button_pico
cp -r ~/zephyrproject/zephyr/samples/basic/button button_pico
cd button_pico
source ~/zephyrproject/zephyr/zephyr-env.sh

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
cp ./build/zephyr/zephyr.uf2 /Volumes/RPI-RP2/
