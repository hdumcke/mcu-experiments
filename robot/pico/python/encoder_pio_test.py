from machine import Pin
from encoder_pio import QEnc_Pio_4
from time import sleep


pinRA = Pin(0, Pin.IN, Pin.PULL_UP)
pinRB = Pin(1, Pin.IN, Pin.PULL_UP)
pinLA = Pin(2, Pin.IN, Pin.PULL_UP)
pinLB = Pin(3, Pin.IN, Pin.PULL_UP)

qencR = QEnc_Pio_4((pinRA, pinRB), sm_id=0, freq=125_000_000)
qencL = QEnc_Pio_4((pinLA, pinLB), sm_id=1, freq=125_000_000)
while True:
    print('R: %s L: %s' % (qencR.read(), qencL.read()))
    sleep(0.1)
