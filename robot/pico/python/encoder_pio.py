# code from https://github.com/orgs/micropython/discussions/13528

# Quadrature encoder for RPi 2040 PIO
#
# Resolution: 4 in-/decrements per cycle.
#
# Original version (c) 2021 pmarques-dev @ github
#   (https://github.com/raspberrypi/pico-examples/blob/master/pio/quadrature_encoder/quadrature_encoder.pio).
# Adapted and modified for micropython 2022 by rkompass.
#
# Quadrature encoding uses a state table in form of a jump table
#   which is fast and has no interrupts.
# This program was reduced to take 'only' 25 of 32 available PIO instructions.
# The jump table has to reside at the beginning of PIO program memory, therefore
#   the instructions are filled up with 7 nop()'s.
# 
# The counter x is permanently pushed nonblockingly to the FIFO.
# Reading the actual value requires emptying the FIFO then waiting for and getting the next pushed value.

# The worst case sampling loop takes 14 cycles, so this program is able to read step
#   rates up to sysclk / 14  (e.g., sysclk 125MHz, max step rate = 8.9 Msteps/sec).
#
# SPDX-License-Identifier: BSD-3-Clause
#
#
# --------------------------------------------------------


from rp2 import PIO, StateMachine, asm_pio
from machine import Pin
from time import ticks_us

# -----  Quadrature encoder class, using RPI2040 PIO. Resolution: 4 in-/decrements per cycle  --------

class QEnc_Pio_4:
    def __init__(self, pins, sm_id=0, freq=10_000_000):
        if not isinstance(pins, (tuple, list)) or len(pins) != 2:
            raise ValueError('2 successive pins required')
        pinA = int(str(pins[0]).split(')')[0].split('(')[1].split(',')[0].replace('GPIO', ''))
        pinB = int(str(pins[1]).split(')')[0].split('(')[1].split(',')[0].replace('GPIO', ''))
        if abs(pinA-pinB) != 1:
            raise ValueError('2 successive pins required')
        in_base = pins[0] if pinA < pinB else pins[1]
        self.qenc = StateMachine(sm_id, self.sm_qenc, freq=freq, in_base=in_base)
        self.qenc.exec("set(x, 0)")  # instead of sm_qenc.restart()
        self.qenc.exec("in_(pins, 2)")
        self.qenc.active(1)
    
    @asm_pio(in_shiftdir=PIO.SHIFT_LEFT, out_shiftdir=PIO.SHIFT_RIGHT)
    def sm_qenc():         #             AB    AB     !!! *** this logic is wrong, it's BA, the lower pin always is on the right side
        jmp("read")        # 0000 : from 00 to 00 = no change
        jmp("decr")        # 0001 : from 00 to 01 = backward
        jmp("incr")        # 0010 : from 00 to 10 = forward
        jmp("read")        # 0011 : from 00 to 11 = error
        jmp("incr")        # 0100 : from 01 to 00 = forward
        jmp("read")        # 0101 : from 01 to 01 = no change
        jmp("read")        # 0110 : from 01 to 10 = error
        jmp("decr")        # 0111 : from 01 to 11 = backward
        jmp("decr")        # 1000 : from 10 to 00 = backward
        jmp("read")        # 1001 : from 10 to 01 = error
        jmp("read")        # 1010 : from 10 to 10 = no change
        jmp("incr")        # 1011 : from 10 to 11 = forward
        jmp("read")        # 1100 : from 11 to 00 = error
        jmp("incr")        # 1101 : from 11 to 01 = forward
        label("decr")
        jmp(x_dec, "read") # 1110 : from 11 to 10 = backward    !!! we cannot change all incr <-> decr because
        label("read")      # 1111 : from 11 to 11 = no change   !!! this next read has to be here after a decrement
        mov(osr, isr)      # save last pin input in OSR
        mov(isr, x)
        push(noblock)
        out(isr, 2)        # 2 right bits of OSR into ISR, all other 0
        in_(pins, 2)       # combined with current reading of input pins
        mov(pc, isr)       # jump into jump-table at addr 0
        label("incr")      # increment x by inverting, decrementing and inverting
        mov(x, invert(x))
        jmp(x_dec, "here")
        label("here")
        mov(x, invert(x))
        jmp("read")        
        nop()
        nop()
        nop()
        nop()
        nop()
        nop()
        nop()

    def read(self):
        for _ in range(self.qenc.rx_fifo()):
            self.qenc.get()
        n = self.qenc.get()
        return -n if n < (1<<31) else (1<<32)-n  #  !!! *** therefore we change the polarity of counting here


class Encoder:
    def __init__(self, c1, c2, ticks_per_rotation, dt, sm_id):
        self.last_time_us = ticks_us()
        self.freq = 0.0
        self.px = Pin(c1, Pin.IN, Pin.PULL_UP)
        self.py = Pin(c2, Pin.IN, Pin.PULL_UP)
        self.ticks_per_rotation = ticks_per_rotation
        self.dt = dt
        self.qenc = QEnc_Pio_4((self.px, self.py), sm_id, freq=125_000_000)
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
        pos = self.qenc.read()
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

    def get_pos(self):
        return self.qenc.read()
