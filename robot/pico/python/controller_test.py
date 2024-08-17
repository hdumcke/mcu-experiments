from controller import Controller
from parameters import RobotParameters
from math import pi
from machine import Timer
from time import sleep

wheel_diameter = 0.0336
wheel_perimeter = wheel_diameter * pi
wheel_dist = 0.077

params = RobotParameters("192.168.1.32")
controller = Controller(6000.0, 5000.0, 100.0,
                        0.0, 0.0, 0.0,
                        params)


def call_back(t):
    global controller
    controller.run()


def teleplot(t):
    global params
    params.tele_plot.send_value("enc_left_speed,w1", params.robot_params['encoder_speed']['value'][0], unit='rpm')
    params.tele_plot.send_value("enc_right_speed,w1", params.robot_params['encoder_speed']['value'][1], unit='rpm')
    params.tele_plot.send_value("left_speed_mps,w2", params.robot_params['encoder_speed']['value'][0] * wheel_perimeter / 60.0, unit='m/s')
    params.tele_plot.send_value("right_speed_mps,w2", params.robot_params['encoder_speed']['value'][1] * wheel_perimeter / 60.0, unit='m/s')
    params.tele_plot.send_value("setpoint_vx,w2", params.robot_params['setpoint']['value'][0], unit='m/s')
    # params.tele_plot.send_value("setpoint_vw", params.robot_params['setpoint']['value'][1], unit='rad/s')
    params.tele_plot.send_value("x_p,w3", params.robot_params['pid_components_x']['value'][0])
    params.tele_plot.send_value("x_i,w3", params.robot_params['pid_components_x']['value'][1])
    params.tele_plot.send_value("x_d,w3", params.robot_params['pid_components_x']['value'][2])
    params.tele_plot.send_value("w_p,w5", params.robot_params['pid_components_w']['value'][0])
    params.tele_plot.send_value("w_i,w5", params.robot_params['pid_components_w']['value'][1])
    params.tele_plot.send_value("w_d,w5", params.robot_params['pid_components_w']['value'][2])
    params.tele_plot.send_value("left_motor_pwm,w4", params.robot_params['motor_pwm']['value'][0])
    params.tele_plot.send_value("right_motor_pwm,w4", params.robot_params['motor_pwm']['value'][1])
    params.tele_plot.send_value("pid_error_vx", params.robot_params['pid_error']['value'][0], unit='m/s')
    params.tele_plot.send_value("pid_error_vw", params.robot_params['pid_error']['value'][1], unit='rad/s')
    # params.tele_plot.send_value("pid_error_vw", params.robot_params['pid_error']['value'][1], unit='rad/s')


timer = Timer(freq=10, mode=Timer.PERIODIC, callback=teleplot)

controller.set_speed(0.2, 0.0)

# Ziegler–Nichols method
Ku = 25000.0
controller.x_pid.Kp = Ku * 0.5
controller.x_pid.Ki = Ku * 0.45
controller.x_pid.Kd = Ku * 0.8

Ku = 25000.0
controller.x_pid.Kp = Ku * 0.5
controller.x_pid.Ki = Ku * 0.45
controller.x_pid.Kd = Ku * 0.03

controller.w_pid.Kp = 30000.0
controller.w_pid.Ki = 0.0
controller.w_pid.Kd = 0.0

controller.start(call_back)
sleep(4)
controller.stop()

pass
