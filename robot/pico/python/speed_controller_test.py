from machine import Pin, Timer
from motor import Motor
from encoder_pio import Encoder
from robot_state import RobotState
from parameters import RobotParameters
from math import pi
from speed_controller import SpeedController

# wheel diameter [m]
wheel_diameter = 0.0336
wheel_perimeter = wheel_diameter * pi
wheel_dist = 0.077

frequency = 100

params = RobotParameters("192.168.1.20")
params.add_param('rpm', 'int', 2)
params.add_param('error', 'float', 2)
params.add_param('motor', 'int', 2)

pin_test1 = Pin(27, Pin.OUT)
pin_test2 = Pin(26, Pin.OUT)


def teleplot(t):
    global params
    global pin_test1
    pin_test1.on()
    params.tele_plot.send_value("enc_left_speed,w1", params.robot_params['encoder_speed']['value'][0], unit='rpm')
    params.tele_plot.send_value("enc_right_speed,w1", params.robot_params['encoder_speed']['value'][1], unit='rpm')
    params.tele_plot.send_value("left_speed_mps,w2", params.robot_params['encoder_speed']['value'][0] * wheel_perimeter / 60.0, unit='m/s')
    params.tele_plot.send_value("right_speed_mps,w2", params.robot_params['encoder_speed']['value'][1] * wheel_perimeter / 60.0, unit='m/s')
    params.tele_plot.send_value("left_error,w3", params.robot_params['error']['value'][0])
    params.tele_plot.send_value("right_error,w3", params.robot_params['error']['value'][1])
    params.tele_plot.send_value("left_motor,w4", params.robot_params['motor']['value'][0])
    params.tele_plot.send_value("right_motor,w4", params.robot_params['motor']['value'][1])
    pin_test1.off()


def cb(t):
    global robot_state
    global sc
    global motorL
    global motorR
    global pin_test2
    pin_test2.on()
    robot_state.process(t)
    s1, s2 = sc.process(params.robot_params['rpm']['value'][0], params.robot_params['rpm']['value'][1])
    params.robot_params['error']['value'][0] = params.robot_params['rpm']['value'][0] - params.robot_params['encoder_speed']['value'][0]
    params.robot_params['error']['value'][1] = params.robot_params['rpm']['value'][1] - params.robot_params['encoder_speed']['value'][1]
    params.robot_params['motor']['value'][0] = int(s1)
    params.robot_params['motor']['value'][1] = int(s2)
    motorL.motorControl(int(s1))
    motorR.motorControl(int(s2))
    pin_test2.off()


timer = Timer(freq=50, mode=Timer.PERIODIC, callback=teleplot)

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

dt = 1.0 / frequency

motorL = Motor(gpioPWA, gpioAN1, gpioAN2)
motorR = Motor(gpioPWB, gpioBN1, gpioBN2)

encL = Encoder(gpioEncAc1, gpioEncAc2, ENCODER_TICKS_PER_REVOLUTION, dt, sm_id=0)
encR = Encoder(gpioEncBc1, gpioEncBc2, ENCODER_TICKS_PER_REVOLUTION, dt, sm_id=1)
robot_state = RobotState(encL, encR, wheel_diameter, wheel_dist, dt, params)
sc = SpeedController(0.0, 0.0, 0.0,
                     450.0, 0.0, 10.0,
                     19.0, 3000.0, (2**16 - 3000) / 600, 0.0,
                     2**16 - 1, params, wheel_diameter)

loop_timer = Timer(freq=frequency, mode=Timer.PERIODIC, callback=cb)

pinSTANDBY = Pin(gpioStandby, mode=Pin.OUT)
pinSTANDBY.high()

params.robot_params['rpm']['value'][0] = 20
params.robot_params['rpm']['value'][1] = 20

sc.left_pid.tunings
sc.left_pid.tunings = (450.0, 0.0, 10.0)
sc.left_pid.components

pass
