# inspired by https://github.com/rakesh-i/MicroPython-Encoder-motor
from machine import Pin
from time import ticks_us


class Encoder:
    def __init__(self, c1, c2, ticks_per_rotation, dt):
        self.pos = 0
        self.last_time_us = ticks_us()
        self.freq = 0.0
        self.px = Pin(c1, Pin.IN)
        self.py = Pin(c2, Pin.IN)
        self.ticks_per_rotation = ticks_per_rotation
        self.dt = dt
        self.py.irq(trigger=Pin.IRQ_RISING, handler=self.handle_interrupt)
        self.filter_window_size = 10
        self.filter_window_size = 1
        self.counter_values = [0] * self.filter_window_size
        self.counter_index = 0
        self.counter_sum = 0
        self.counter_previous_pos = 0

    def get_speed_rpm(self):
        current_time_us = ticks_us()
        dt_us = current_time_us - self.last_time_us
        self.last_time_us = current_time_us
        self.freq = 1000000.0 / dt_us
        self.dt = dt_us / 1000000.0
        pos = self.pos
        delta_value = pos - self.counter_previous_pos

        # handle counter overflow
        if abs(delta_value) < 50000:
            self.counter_sum -= self.counter_values[self.counter_index]
            self.counter_sum += delta_value
            self.counter_values[self.counter_index] = delta_value
            self.counter_index = (self.counter_index + 1) % self.filter_window_size

        self.counter_previous_pos = pos
        rpm = self.counter_sum / self.filter_window_size / self.ticks_per_rotation / self.dt * 60
        return rpm

    # Interrupt handler
    def handle_interrupt(self, pin):
        a = self.px.value()
        if a > 0:
            self.pos = self.pos - 1
        else:
            self.pos = self.pos + 1

    def get_pos(self):
        return self.pos
