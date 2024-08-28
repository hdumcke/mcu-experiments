from imu import IMU
from gyro import Gyro
import asyncio
from machine import Timer, Pin
from encoder_pio import Encoder
from parameters import RobotParameters, ParamServer
from robot_state import RobotState
from time import ticks_ms
from math import pi

params = RobotParameters("192.168.1.20")
server = ParamServer(params)
last_called = ticks_ms()
frequency = 100  # Hz
dt = 1.0 / frequency
wheel_diameter = 0.0335
wheel_dist = 0.077
ENCODER_TICKS_PER_REVOLUTION = 1431.0

gpioEncAc1 = 0
gpioEncAc2 = 1

gpioEncBc1 = 2
gpioEncBc2 = 3

encA = Encoder(gpioEncAc1, gpioEncAc2, ENCODER_TICKS_PER_REVOLUTION, dt, sm_id=0)
encB = Encoder(gpioEncBc1, gpioEncBc2, ENCODER_TICKS_PER_REVOLUTION, dt, sm_id=1)

robot_state = RobotState(encA, encB, wheel_diameter, wheel_dist, dt, params)

timer = Timer(freq=frequency, mode=Timer.PERIODIC, callback=robot_state.process)

gyro = Gyro()


def imu_cb(wz):
    global gyro
    global params
    gyro.process(wz)
    if gyro.is_locked():
        # params.update_param('vz', [0.75 * gyro.get_angular_speed() + 0.25 * params.robot_params['vz']['value'][0]])
        # params.update_param('orientation', [0.75 * gyro.get_orientation() + 0.25 * params.robot_params['orientation']['value'][0]])
        # speed up above calls
        params.robot_params['gyro_vw']['value'][0] = 0.75 * gyro.get_angular_speed() + 0.25 * params.robot_params['gyro_vw']['value'][0]
        params.robot_params['gyro_w']['value'][0] = 0.75 * gyro.get_orientation() + 0.25 * params.robot_params['gyro_w']['value'][0]


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


async def show_cmd_vel(params):
    global last_called
    global encA
    global encB
    while True:
        now = ticks_ms()
        if (now - last_called) > 10:
            last_called = now
            # params.tele_plot.send_value("encR_freq,w1", encA.freq, unit='Hz')
            # params.tele_plot.send_value("encL_freq,w1", encB.freq, unit='Hz')
            # params.tele_plot.send_value("encR_pos,w3", params.robot_params['pos']['value'][0])
            # params.tele_plot.send_value("encL_pos,w3", params.robot_params['pos']['value'][1])
            params.tele_plot.send_value("encR_speed,w2", params.robot_params['encoder_speed']['value'][0], unit='rpm')
            params.tele_plot.send_value("encL_speed,w2", params.robot_params['encoder_speed']['value'][1], unit='rpm')
            params.tele_plot.send_value("robot_vel_lin", params.robot_params['robot_vel']['value'][0], unit='m/sec')
            params.tele_plot.send_value("robot_vel_w", params.robot_params['robot_vel']['value'][2], unit='rad/sec')
            params.tele_plot.send_values_xy("robot_location", params.robot_params['robot_pose']['value'][0:2])
            params.tele_plot.send_value("robot_orientation", params.robot_params['robot_pose']['value'][2] / pi * 180, unit='deg')
            params.tele_plot.send_value("gyro_vw", params.robot_params['gyro_vw']['value'][0], unit='rad/sec')
            params.tele_plot.send_value("gyro_w", params.robot_params['gyro_w']['value'][0] / pi * 180, unit='deg')
            # params.tele_plot.send_value("robot_pose_x,w4", params.robot_params['robot_pose']['value'][0], unit='m')
            # params.tele_plot.send_value("robot_pose_y,w4", params.robot_params['robot_pose']['value'][1], unit='m')
            # params.tele_plot.send_value("vx", params.robot_params['cmd_vel']['value'][0], unit='m/sec', flags='np')
            # params.tele_plot.send_value("vy", params.robot_params['cmd_vel']['value'][1], unit='m/sec', flags='np')
            # params.tele_plot.send_value("vz", params.robot_params['cmd_vel']['value'][2], unit='m/sec', flags='np')
        await asyncio.sleep_ms(100)


async def main(server, params):
    asyncio.create_task(server.serve())
    asyncio.create_task(show_cmd_vel(params))
    while True:
        await asyncio.sleep_ms(10_000)

loop = asyncio.get_event_loop()
loop.run_until_complete(main(server, params))
