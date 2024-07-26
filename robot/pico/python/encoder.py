# inspired by https://github.com/rakesh-i/MicroPython-Encoder-motor
from machine import Pin
import math


class Encoder:
    # Instance variable for keeping the record of the encoder position
    pos = 0

    # Interrupt handler
    def handle_interrupt(self, pin):
        a = self.px.value()
        if a > 0:
            self.pos = self.pos - 1
        else:
            self.pos = self.pos + 1

    def __init__(self, c1, c2, wheel_diameter, ticks_per_rotation, dt):
        self.px = Pin(c1, Pin.IN)
        self.py = Pin(c2, Pin.IN)
        self.wheel_diameter = wheel_diameter
        self.wheel_perimeter = math.pi * self.wheel_diameter
        self.ticks_per_rotation = ticks_per_rotation
        self.dt = dt
        self.py.irq(trigger=Pin.IRQ_RISING, handler=self.handle_interrupt)
        self.filter_window_size = 10
        self.counter_values = [0] * self.filter_window_size
        self.counter_index = 0
        self.counter_sum = 0
        self.counter_previous_pos = 0

    def get_speed(self):
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
        speed = self.wheel_perimeter * rpm / 60
        return speed
