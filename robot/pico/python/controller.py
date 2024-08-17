from machine import Pin, Timer
from motor import Motor
from encoder_pio import Encoder
from PID import PID
from robot_state import RobotState
from math import pi
from time import time


gpioPWA = 10
gpioPWB = 11

gpioAN1 = 13
gpioAN2 = 12

gpioBN1 = 15
gpioBN2 = 14

gpioStandby = 20

gpioEncAc1 = 0
gpioEncAc2 = 1

gpioEncBc1 = 2
gpioEncBc2 = 3

ENCODER_TICKS_PER_REVOLUTION = 1430
# wheel diameter [m]
wheel_diameter = 0.0336
wheel_perimeter = wheel_diameter * pi
wheel_dist = 0.077

# setpoint with acc/speed profil
acceleration_x = 1.0
acceleration_z = 1.0

pwm_max = 65535


def _clamp(value, limits):
    lower, upper = limits
    if value is None:
        return None
    elif (upper is not None) and (value > upper):
        return upper
    elif (lower is not None) and (value < lower):
        return lower
    return value


class Controller:
    def __init__(self,
                 x_Kp, x_Kd, x_Ki,
                 w_Kp, w_Kd, w_Ki,
                 params):
        self.dt = 0.01
        self.params = params
        self.params.add_param('setpoint', 'float', 2)
        self.params.add_param('motor_pwm', 'int', 2)
        self.params.add_param('pid_error', 'float', 2)
        self.params.add_param('pid_components_x', 'float', 3)
        self.params.add_param('pid_components_w', 'float', 3)
        self.motorA = Motor(gpioPWA, gpioAN1, gpioAN2)
        self.motorB = Motor(gpioPWB, gpioBN1, gpioBN2)
        self.pinSTANDBY = Pin(gpioStandby, mode=Pin.OUT)
        self.encL = Encoder(gpioEncAc1, gpioEncAc2, ENCODER_TICKS_PER_REVOLUTION, self.dt, sm_id=0)
        self.encR = Encoder(gpioEncBc1, gpioEncBc2, ENCODER_TICKS_PER_REVOLUTION, self.dt, sm_id=1)
        self.robot_state = RobotState(self.encL, self.encR, wheel_diameter, wheel_dist, self.dt, params)
        self.state_timer = Timer(freq=100, mode=Timer.PERIODIC, callback=self.robot_state.process)
        self.x_pid = PID(x_Kp, x_Kd, x_Ki, setpoint=0, output_limits=[-pwm_max, pwm_max], scale='us')
        self.w_pid = PID(w_Kp, w_Kd, w_Ki, setpoint=0, output_limits=[-pwm_max, pwm_max], scale='us')
        self.setpoint_vx = 0.0
        self.setpoint_vw = 0.0
        self.setpoint_timestamp = time()
        self.actual_vx_filtered = 0.0
        self.actual_vw_filtered = 0.0
        self.setpoint_vx_profil = 0.0
        self.setpoint_vw_profil = 0.0

    def start(self, cb):
        self.pinSTANDBY.high()
        self.pid_timer = Timer(freq=100, mode=Timer.PERIODIC, callback=cb)

    def stop(self):
        self.pid_timer.deinit()
        self.pinSTANDBY.low()
        self.x_pid.reset()
        self.w_pid.reset()
        self.params.update_param('pid_components_x', list(self.x_pid.components))
        self.params.update_param('pid_components_w', list(self.w_pid.components))

    def set_speed(self, vx, vw):
        self.setpoint_vx = vx
        self.setpoint_vw = vw
        self.setpoint_timestamp = time()

    def run(self):
        left_speed_mps = self.params.robot_params['encoder_speed']['value'][0] * wheel_perimeter / 60.0
        right_speed_mps = self.params.robot_params['encoder_speed']['value'][1] * wheel_perimeter / 60.0
        actual_vx = (left_speed_mps + right_speed_mps) / 2.0
        actual_vw = -(left_speed_mps - right_speed_mps) / wheel_dist * 2
        # filter speed feedback
        alpha = 0.5
        self.actual_vx_filtered = (1.0 - alpha) * self.actual_vx_filtered + alpha * actual_vx
        self.actual_vw_filtered = (1.0 - alpha) * self.actual_vw_filtered + alpha * actual_vw

        # no timeout during testing
        self.setpoint_timestamp = time()

        # 2 sec time out
        if time() > self.setpoint_timestamp + 2:
            self.setpoint_vx = 0.0
            self.setpoint_vw = 0.0

        # speed profil
        if self.setpoint_vx > self.setpoint_vx_profil:
            self.setpoint_vx_profil = min(self.setpoint_vx_profil + acceleration_x * self.dt, self.setpoint_vx)
        else:
            self.setpoint_vx_profil = max(self.setpoint_vx_profil - acceleration_x * self.dt, self.setpoint_vx)
        if self.setpoint_vw > self.setpoint_vw_profil:
            self.setpoint_vw_profil = min(self.setpoint_vw_profil + acceleration_z * self.dt, self.setpoint_vw)
        else:
            self.setpoint_vw_profil = max(self.setpoint_vw_profil - acceleration_z * self.dt, self.setpoint_vw)

        # control
        self.params.update_param('setpoint', [self.setpoint_vx, self.setpoint_vw])
        self.x_pid.setpoint = self.setpoint_vx_profil
        self.w_pid.setpoint = self.setpoint_vw_profil

        self.params.update_param('pid_error', [self.setpoint_vx - self.actual_vx_filtered, self.setpoint_vw - self.actual_vw_filtered])
        self.params.update_param('pid_components_x', list(self.x_pid.components))
        self.params.update_param('pid_components_w', list(self.w_pid.components))
        x_speed = self.x_pid.__call__(self.actual_vx_filtered)
        w_speed = self.w_pid.__call__(self.actual_vw_filtered)

        leftSpeed = int(x_speed + w_speed)
        rightSpeed = int(x_speed - w_speed)

        self.params.update_param('motor_pwm', [_clamp(leftSpeed, [-pwm_max, pwm_max]), _clamp(rightSpeed, [-pwm_max, pwm_max])])
        self.motorA.motorControl(self.params.robot_params['motor_pwm']['value'][0])
        self.motorB.motorControl(self.params.robot_params['motor_pwm']['value'][1])
