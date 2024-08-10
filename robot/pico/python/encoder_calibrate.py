from encoder_pio import Encoder
from time import sleep

gpioEncAc1 = 0
gpioEncAc2 = 1
gpioEncBc1 = 2
gpioEncBc2 = 3
ENCODER_TICKS_PER_REVOLUTION = 0
dt = 0.01

encA = Encoder(gpioEncAc1, gpioEncAc2, ENCODER_TICKS_PER_REVOLUTION, dt, sm_id=0)
encB = Encoder(gpioEncBc1, gpioEncBc2, ENCODER_TICKS_PER_REVOLUTION, dt, sm_id=1)

while True:
    print("%s %s" % (encA.get_pos(), encB.get_pos()))
    sleep(1)
