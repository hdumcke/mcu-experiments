from encoder import Encoder
from time import sleep_ms

dt = 0.02  # 50 Hz
wheel_diameter = 0.0336
ENCODER_TICKS_PER_REVOLUTION = 205

gpioEncAc1 = 0
gpioEncAc2 = 1

gpioEncBc1 = 2
gpioEncBc2 = 3

encA = Encoder(gpioEncAc1, gpioEncAc2, wheel_diameter, ENCODER_TICKS_PER_REVOLUTION, dt)
encB = Encoder(gpioEncBc1, gpioEncBc2, wheel_diameter, ENCODER_TICKS_PER_REVOLUTION, dt)

while True:
    print("%s %s %s %s" % (encA.pos - encA.counter_previous_pos, encB.pos - encB.counter_previous_pos, encA.get_speed(), encB.get_speed()))
    sleep_ms(20)
