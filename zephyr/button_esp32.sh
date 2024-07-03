#!/bin/bash

### Get directory where this script is installed
BASEDIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

cd $BASEDIR
rm -rf button_esp32
cp -r ~/zephyrproject/zephyr/samples/basic/button button_esp32
cd button_esp32
source ~/zephyrproject/zephyr/zephyr-env.sh

cat > app.overlay << EOF
/ {

    gpio_keys {
        compatible = "gpio-keys";
        user_button: button {
            label = "User";
            gpios = <&gpio0 0 GPIO_ACTIVE_LOW>;
        };
    };

    aliases {
        sw0 = &user_button;
        led3 = &ext_led;
    };
    leds {
        compatible = "gpio-leds";
        ext_led: led_3 {
            gpios = < &gpio0 0x11 0x0 >;
            label = "Ext - LED";
        };
    };
};
EOF

sed -i "s/led0/led3/" src/main.c

west update
west blobs fetch hal_espressif
west build -b esp_wrover_kit
west flash
west espressif monitor
