from imu import IMU
from gyro import Gyro
from parameters import RobotParameters
from time import ticks_ms
from machine import Pin
from math import pi

gyro = Gyro()
params = RobotParameters("192.168.1.20")


def imu_cb(wz):
    global gyro
    global params
    gyro.process(wz)
    if gyro.is_locked():
        # params.update_param('vz', [0.75 * gyro.get_angular_speed() + 0.25 * params.robot_params['vz']['value'][0]])
        # params.update_param('orientation', [0.75 * gyro.get_orientation() + 0.25 * params.robot_params['orientation']['value'][0]])
        # speed up above calls
        params.robot_params['gyro_vw']['value'][0] = 0.75 * gyro.get_angular_speed() + 0.25 * params.robot_params['gyro_vw']['value'][0]
        params.robot_params['gyro_w']['value'][0] = 0.75 * gyro.get_gyro_w() + 0.25 * params.robot_params['gyro_w']['value'][0]


imu = IMU()
test_pin = Pin(22, Pin.OUT)


def handle_interrupt(pin):
    global imu
    global test_pin
    test_pin.value(1)
    imu.read()
    test_pin.value(0)


imu.register_data_ready_callback(imu_cb)
int_pin = Pin(21, Pin.IN)
int_pin.irq(trigger=Pin.IRQ_RISING, handler=handle_interrupt)
last_called = ticks_ms()

while True:
    now = ticks_ms()
    if (now - last_called) > 100:
        last_called = now
        params.tele_plot.send_value("gyro_vw", params.robot_params['gyro_vw']['value'][0], unit='rad/sec')
        params.tele_plot.send_value("gyro_w", params.robot_params['gyro_w']['value'][0] / pi * 180, unit='deg')
