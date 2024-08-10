from time import ticks_us


ALPHA_MEAN = 0.002
ALPHA_VARIANCE = 0.04
ALPHA_BIAS = 0.005
ALPHA_VARIANCE_LOW_THRESHOLD = 0.0007  # rad


class Gyro:
    def __init__(self):
        self.last_time_us = ticks_us()
        self.locked = False
        self.dt = 0.000001  # 1Khx
        self.bias_update_counter = 0
        self.mean = 0.0
        self.variance = 0.0
        self.bias = 0.0
        self.speed_filtered = 0.0
        self.angle_filtered = 0.0

    def process(self, speed):
        #current_time_us = ticks_us()
        #dt_us = current_time_us - self.last_time_us
        #self.last_time_us = current_time_us
        #self.dt = dt_us / 1000000.0
        self.mean = ALPHA_MEAN * speed + (1.0 - ALPHA_MEAN) * self.mean
        self.variance = ALPHA_VARIANCE * (speed - self.mean)**2 + (1.0 - ALPHA_VARIANCE) * self.variance
        return
        if abs(self.variance) < ALPHA_VARIANCE_LOW_THRESHOLD:
            self.bias = ALPHA_BIAS * self.mean + (1.0 - ALPHA_BIAS) * self.bias
            self.bias_update_counter += 1
        if self.locked:
            self.speed_filtered = speed - self.bias
            self.angle_filtered += self.speed_filtered * self.dt
        else:
            self.speed_filtered = 0.0
            self.angle_filtered = 0.0
            self.locked = self.bias_update_counter > 1000

    def get_angular_speed(self):
        return self.speed_filtered

    def get_orientation(self):
        return self.angle_filtered

    def is_locked(self):
        return self.locked
