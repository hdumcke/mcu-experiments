from encoder import Encoder
from parameters import RobotParameters, ParamServer
from robot_state import RobotState
from time import ticks_ms
from time import sleep

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

while True:
    print("%s %s" % (encA.get_pos(), encB.get_pos()))
    now = ticks_ms()
    robot_state.process(1)
#    if (now - last_called) > 10:
#        last_called = now
#        params.tele_plot.send_value("encR_freq,w1", encA.freq, unit='Hz')
#        params.tele_plot.send_value("encL_freq,w1", encB.freq, unit='Hz')
#        params.tele_plot.send_value("encR_pos,w3", params.robot_params['pos']['value'][0])
#        params.tele_plot.send_value("encL_pos,w3", params.robot_params['pos']['value'][1])
#        params.tele_plot.send_value("encR_speed,w2", params.robot_params['encoder_speed']['value'][0], unit='rpm')
#        params.tele_plot.send_value("encL_speed,w2", params.robot_params['encoder_speed']['value'][1], unit='rpm')
#        params.tele_plot.send_value("robot_vel_lin", params.robot_params['robot_vel']['value'][0], unit='m/sec')
#        params.tele_plot.send_value("robot_vel_w", params.robot_params['robot_vel']['value'][2], unit='rad/sec')
#        params.tele_plot.send_values_xy("robot_location", params.robot_params['robot_pose']['value'][0:2])
#        params.tele_plot.send_value("robot_orientation", params.robot_params['robot_pose']['value'][2], unit='rad')
#        # params.tele_plot.send_value("robot_pose_x,w4", params.robot_params['robot_pose']['value'][0], unit='m')
#        # params.tele_plot.send_value("robot_pose_y,w4", params.robot_params['robot_pose']['value'][1], unit='m')
#        # params.tele_plot.send_value("vx", params.robot_params['cmd_vel']['value'][0], unit='m/sec', flags='np')
#        # params.tele_plot.send_value("vy", params.robot_params['cmd_vel']['value'][1], unit='m/sec', flags='np')
#        # params.tele_plot.send_value("vz", params.robot_params['cmd_vel']['value'][2], unit='m/sec', flags='np')
    sleep(0.01)
