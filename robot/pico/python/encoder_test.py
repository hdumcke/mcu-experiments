from encoder import Encoder
from machine import Timer
from parameters import RobotParameters
from time import ticks_ms

params = RobotParameters("192.168.1.32")
dt = 0.01  # 100 Hz
wheel_diameter = 0.0336
ENCODER_TICKS_PER_REVOLUTION = 356

gpioEncAc1 = 0
gpioEncAc2 = 1

gpioEncBc1 = 2
gpioEncBc2 = 3

encA = Encoder(gpioEncAc1, gpioEncAc2, ENCODER_TICKS_PER_REVOLUTION, dt)
encB = Encoder(gpioEncBc1, gpioEncBc2, ENCODER_TICKS_PER_REVOLUTION, dt)


def call_back(t):
    global params
    global encA
    global encB
    params.update_param('encoder_speed', [encA.get_speed_rpm(), encB.get_speed_rpm()])


timer = Timer(freq=100, mode=Timer.PERIODIC, callback=call_back)

last_called = ticks_ms()

while True:
    now = ticks_ms()
    if (now - last_called) > 100:
        last_called = now
        params.tele_plot.send_value("encA_speed,w1", params.robot_params['encoder_speed']['value'][0], unit='rpm')
        params.tele_plot.send_value("encB_speed,w1", params.robot_params['encoder_speed']['value'][1], unit='rpm')
