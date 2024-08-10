from encoder import Encoder
from parameters import RobotParameters, ParamServer
from robot_state import RobotState
from time import ticks_ms, sleep

params = RobotParameters("192.168.1.32")
server = ParamServer(params)
last_called = ticks_ms()
frequency = 100  # Hz
dt = 1.0 / frequency
wheel_diameter = 0.0335
wheel_dist = 0.077
ENCODER_TICKS_PER_REVOLUTION = 358.0

gpioEncAc1 = 0
gpioEncAc2 = 1

gpioEncBc1 = 2
gpioEncBc2 = 3

encA = Encoder(gpioEncAc1, gpioEncAc2, ENCODER_TICKS_PER_REVOLUTION, dt)
encB = Encoder(gpioEncBc1, gpioEncBc2, ENCODER_TICKS_PER_REVOLUTION, dt)

robot_state = RobotState(encA, encB, wheel_diameter, wheel_dist, dt, params)

# timer = Timer(freq=frequency, mode=Timer.PERIODIC, callback=robot_state.process)

while True:
    print("%s %s" % (encA.get_pos(), encB.get_pos()))
    # robot_state.process(1)
    sleep(1)
