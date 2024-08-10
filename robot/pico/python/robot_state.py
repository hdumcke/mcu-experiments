from math import pi, sin, cos
from time import ticks_us


class RobotState:
    def __init__(self, encRight, encLeft, wheel_diameter, wheel_dist, dt, params):
        self.last_time_us = ticks_us()
        self.freq = 0.0
        self.encRight = encRight
        self.encLeft = encLeft
        self.wheel_dist = wheel_dist
        self.wheel_diameter = wheel_diameter
        self.wheel_perimeter = pi * self.wheel_diameter
        self.dt = dt
        self.heading = 0.0
        self.params = params
        self.params.add_param('dt', 'float', 3)
        self.params.add_param('pos', 'float', 2)

    def process(self, t):
        current_time_us = ticks_us()
        dt_us = current_time_us - self.last_time_us
        self.last_time_us = current_time_us
        self.freq = 1000000.0 / dt_us
        # code inspired by https://github.com/merose/diff_drive/tree/master
        self.params.update_param('encoder_speed', [self.encRight.get_speed_rpm(), self.encLeft.get_speed_rpm()])
        self.params.update_param('dt', [1.0 / self.encRight.freq, 1.0 / self.encLeft.freq, 1.0 / self.freq])
        self.params.update_param('pos', [self.encRight.get_pos(), self.encLeft.get_pos()])
        self.dt = 1.0 / (self.encRight.freq + self.encLeft.freq + self.freq) * 3
        rightTravel = self.params.robot_params['encoder_speed']['value'][0] / 60 * self.dt * self.wheel_perimeter
        leftTravel = self.params.robot_params['encoder_speed']['value'][1] / 60 * self.dt * self.wheel_perimeter
        deltaTravel = (rightTravel + leftTravel) / 2
        deltaTheta = (rightTravel - leftTravel) / self.wheel_dist

        if rightTravel == leftTravel:
            deltaX = leftTravel * cos(self.params.robot_params['robot_pose']['value'][2])
            deltaY = leftTravel * sin(self.params.robot_params['robot_pose']['value'][2])
        else:
            radius = deltaTravel / deltaTheta

            # Find the instantaneous center of curvature (ICC).
            iccX = self.params.robot_params['robot_pose']['value'][0] - radius * sin(self.params.robot_params['robot_pose']['value'][2])
            iccY = self.params.robot_params['robot_pose']['value'][1] + radius * cos(self.params.robot_params['robot_pose']['value'][2])

            deltaX = cos(deltaTheta) * (self.params.robot_params['robot_pose']['value'][0] - iccX) \
                - sin(deltaTheta) * (self.params.robot_params['robot_pose']['value'][1] - iccY) \
                + iccX - self.params.robot_params['robot_pose']['value'][0]

            deltaY = sin(deltaTheta) * (self.params.robot_params['robot_pose']['value'][0] - iccX) \
                + cos(deltaTheta) * (self.params.robot_params['robot_pose']['value'][1] - iccY) \
                + iccY - self.params.robot_params['robot_pose']['value'][1]

        x = self.params.robot_params['robot_pose']['value'][0] + deltaX
        y = self.params.robot_params['robot_pose']['value'][1] + deltaY
        theta = (self.params.robot_params['robot_pose']['value'][2] + deltaTheta) % (2 * pi)
        self.params.update_param('robot_pose', [x, y, theta])
        v_x = deltaTravel / self.dt
        v_y = 0.0
        v_w = deltaTheta / self.dt
        self.params.update_param('robot_vel', [v_x, v_y, v_w])
        a_x = self.params.robot_params['robot_vel']['value'][0] / self.dt
        a_y = self.params.robot_params['robot_vel']['value'][1] / self.dt
        a_w = self.params.robot_params['robot_vel']['value'][2] / self.dt
        self.params.update_param('robot_acc', [a_x, a_y, a_w])
