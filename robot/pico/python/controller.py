from machine import Pin, Timer
from motor import Motor
from encoder import Encoder
from PID import PID
from time import time, ticks_ms

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

ENCODER_TICKS_PER_REVOLUTION = 356
# wheel diameter [m]
wheel_diameter = 0.0336

# setpoint with acc/speed profil
acceleration_x = 1.0
acceleration_z = 1.0

# wheel width [m]
base_width = 0.116

pwm_max = 65535


class Controller:
    def __init__(self,
                 x_Kp, x_Kd, x_Ki,
                 w_Kp, w_Kd, w_Ki,
                 uart=None):
        self.dt = 0.01
        self.uart = uart
        self.motorA = Motor(gpioPWA, gpioAN1, gpioAN2)
        self.motorB = Motor(gpioPWB, gpioBN1, gpioBN2)
        self.pinSTANDBY = Pin(gpioStandby, mode=Pin.OUT)
        self.encA = Encoder(gpioEncAc1, gpioEncAc2, wheel_diameter, ENCODER_TICKS_PER_REVOLUTION, self.dt)
        self.encB = Encoder(gpioEncBc1, gpioEncBc2, wheel_diameter, ENCODER_TICKS_PER_REVOLUTION, self.dt)
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

    def set_speed(self, vx, vw):
        self.setpoint_vx = vx
        self.setpoint_vw = vw
        self.setpoint_timestamp = time()

    def run(self):
        # correct motor direction
        left_speed_mps = -self.encA.get_speed()
        right_speed_mps = self.encB.get_speed()
        actual_vx = (left_speed_mps + right_speed_mps) / 2.0
        #TODO remove after testing
        actual_vx = left_speed_mps
        actual_vw = -(left_speed_mps - right_speed_mps) / base_width
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
        self.x_pid.setpoint = self.setpoint_vx_profil
        self.w_pid.setpoint = self.setpoint_vw_profil

        x_speed = self.x_pid.__call__(self.actual_vx_filtered, self.dt)
        w_speed = self.w_pid.__call__(self.actual_vw_filtered, self.dt)

        #TODO remove after testing
        w_speed = 0.0

        leftSpeed = int(x_speed + w_speed)
        rightSpeed = int(x_speed - w_speed)

        if (self.uart is not None):
            now = ticks_ms()
            print(">error_x:%s:%s" % (now, self.x_pid.setpoint - self.actual_vx_filtered), file=self.uart)
            print(">setpoint_vx_profil:%s:%s" % (now, self.setpoint_vx_profil), file=self.uart)
            print(">left_speed_mps:%s:%s" % (now, left_speed_mps), file=self.uart)
            print(">actual_vx_filtered:%s:%s" % (now, self.actual_vx_filtered), file=self.uart)
            print(">pwmA:%s:%s" % (now, leftSpeed), file=self.uart)

        self.motorA.motorControl(leftSpeed)
        self.motorB.motorControl(rightSpeed)
