from machine import Pin, Timer
from motor import Motor
from time import sleep
from encoder_pio import Encoder
from robot_state import RobotState
from parameters import RobotParameters
from math import pi

# wheel diameter [m]
wheel_diameter = 0.0336
wheel_perimeter = wheel_diameter * pi
wheel_dist = 0.077

params = RobotParameters("192.168.1.20")


def teleplot(t):
    global params
    params.tele_plot.send_value("enc_left_speed,w1", params.robot_params['encoder_speed']['value'][0], unit='rpm')
    params.tele_plot.send_value("enc_right_speed,w1", params.robot_params['encoder_speed']['value'][1], unit='rpm')
    params.tele_plot.send_value("left_speed_mps,w2", params.robot_params['encoder_speed']['value'][0] * wheel_perimeter / 60.0, unit='m/s')
    params.tele_plot.send_value("right_speed_mps,w2", params.robot_params['encoder_speed']['value'][1] * wheel_perimeter / 60.0, unit='m/s')


timer = Timer(freq=10, mode=Timer.PERIODIC, callback=teleplot)

gpioPWA = 10
gpioPWB = 11

gpioAN1 = 13
gpioAN2 = 12

gpioBN1 = 15
gpioBN2 = 14

gpioStandby = 20

gpioEncAc1 = 2
gpioEncAc2 = 3

gpioEncBc1 = 0
gpioEncBc2 = 1

ENCODER_TICKS_PER_REVOLUTION = 1430

dt = 0.01

motorL = Motor(gpioPWA, gpioAN1, gpioAN2)
motorR = Motor(gpioPWB, gpioBN1, gpioBN2)

encL = Encoder(gpioEncAc1, gpioEncAc2, ENCODER_TICKS_PER_REVOLUTION, dt, sm_id=0)
encR = Encoder(gpioEncBc1, gpioEncBc2, ENCODER_TICKS_PER_REVOLUTION, dt, sm_id=1)
robot_state = RobotState(encL, encR, wheel_diameter, wheel_dist, dt, params)
state_timer = Timer(freq=100, mode=Timer.PERIODIC, callback=robot_state.process)

pinSTANDBY = Pin(gpioStandby, mode=Pin.OUT)
pinSTANDBY.high()

motorL.motorControl(3000)
motorR.motorControl(3000)

sleep(5)

motorL.motorControl(0)
motorR.motorControl(0)

motorL.motorControl(2**16 - 1)
motorR.motorControl(2**16 - 1)
