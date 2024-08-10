parameters import TelePlot
from time import ticks_us
from machine import Timer

tele_plot = TelePlot("192.168.1.32")
last_time = ticks_us()
cb_cnt = 0


def call_back(t):
    global tele_plot
    global last_time
    global cb_cnt
    cb_cnt += 1
    now = ticks_us()
    if (cb_cnt % 50) == 0:
        tele_plot.send_value("cb_time", [now - last_time])
    last_time = now


timer = Timer(freq=500, mode=Timer.PERIODIC, callback=call_back)

loop_cnt = 0
previous_ticks = 0
delta_avg = 0.0
while True:
    now = ticks_us()
    loop_cnt += 1
    delta = now - previous_ticks
    delta_avg = 0.8 * delta_avg + 0.2 * delta
    previous_ticks = now
    if (loop_cnt % 10000) == 0:
        tele_plot.send_value("ticks", [delta_avg])
