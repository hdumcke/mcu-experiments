from feedforward import FeedForward
from PID import PID, _clamp
from math import pi

global params


class SpeedController:
    def __init__(self,
                 speed_pid_kp,
                 speed_pid_ki,
                 speed_pid_kd,
                 speed_pid_output_limit,
                 speed_pid_alpha_derivative,
                 speed_pid_alpha_output,
                 speed_ff_threshold,
                 speed_ff_bias,
                 speed_ff_kp,
                 speed_ff_kd,
                 limit,
                 params,
                 wheel_diameter):
        self.left_pid = PID(Kp=speed_pid_kp, Ki=speed_pid_ki, Kd=speed_pid_kd)
        self.right_pid = PID(Kp=speed_pid_kp, Ki=speed_pid_ki, Kd=speed_pid_kd)
        self.left_ff = FeedForward(speed_ff_threshold, speed_ff_bias, speed_ff_kp, speed_ff_kd)
        self.right_ff = FeedForward(speed_ff_threshold, speed_ff_bias, speed_ff_kp, speed_ff_kd)
        self.speed_pid_output_limit = speed_pid_output_limit
        self.speed_pid_alpha_derivative = speed_pid_alpha_derivative
        self.speed_pid_alpha_output = speed_pid_alpha_output
        self.limit = limit
        self.params = params
        self.wheel_perimeter = wheel_diameter * pi

    def reset(self):
        self.left_pid.reset()
        self.left_ff.reset()
        self.right_pid.reset()
        self.right_ff.reset()

    def process(self, left_setpoint, right_setpoint):
        self.right_pid.setpoint = right_setpoint
        self.left_pid.setpoint = left_setpoint
        right_pid_out = self.right_pid(self.params.robot_params['encoder_speed']['value'][1])
        left_pid_out = self.left_pid(self.params.robot_params['encoder_speed']['value'][0])
        right_ff_out = self.right_ff.process(right_setpoint)
        left_ff_out = self.left_ff.process(left_setpoint)
        return _clamp(left_pid_out + left_ff_out, [-self.limit, self.limit]), _clamp(right_pid_out + right_ff_out, [-self.limit, self.limit])
