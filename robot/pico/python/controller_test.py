from controller import Controller
from time import sleep
from machine import UART, Pin

uart = UART(0, baudrate=115200, tx=Pin(16), rx=Pin(17))

controller = Controller(70000.0, 0.0, 0.0,
                        70000.0, 0.0, 0.0,
                        uart)

controller.x_pid.Kp = 350000.0
controller.x_pid.Ki = 0.0
controller.x_pid.Kd = 0.0

Ku = 350000.0
controller.x_pid.Kp = Ku * 0.5
controller.x_pid.Ki = Ku * 0.45
controller.x_pid.Kd = Ku * 0.8


def call_back(t):
    global controller
    controller.run()


controller.set_speed(0.12, 0.12)
# expect motor input of 5000
controller.start(call_back)
sleep(5)
controller.stop()


controller.set_speed(0.0, 0.0)
controller.start(call_back)
sleep(5)
controller.set_speed(0.5, 0.0)
sleep(5)
controller.set_speed(1.0, 0.0)
sleep(5)
controller.set_speed(1.5, 0.0)
sleep(5)
controller.stop()
