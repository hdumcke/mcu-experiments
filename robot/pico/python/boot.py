from wifi import connect
from machine import Pin
from time import sleep
import rp2

# Run IMU calibration
import MPU6050_calibrate  # noqa

led = Pin("LED", Pin.OUT)
status = connect()

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

    # run MPU6050_test
    import MPU6050_test  # noqa
