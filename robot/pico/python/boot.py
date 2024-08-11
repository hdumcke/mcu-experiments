from wifi import Wifi
from machine import Pin
from time import sleep
import rp2

led = Pin("LED", Pin.OUT)

wifi = Wifi()
status = wifi.connect()

# escape when bootsel button is pressed
if not rp2.bootsel_button():

    if status:
        # now that we are connected turn LED on
        led.on()
    else:
        while True:
            led.on()
            sleep(1)
            led.off()
            sleep(1)

    # start robot
    import robot  # noqa
