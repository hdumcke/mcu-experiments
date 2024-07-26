from machine import I2C, Pin
from time import sleep, ticks_ms
import MPU6050
from calibration import gyro_cal, accel_cal
import socket

UDP_IP = "192.168.1.32"
UDP_PORT = 47269

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)

# Set up the I2C interface
i2c = I2C(1, sda=Pin(18), scl=Pin(19))

# Set up the MPU6050 class
mpu = MPU6050.MPU6050(i2c)

# wake up the MPU6050 from sleep
mpu.wake()

# continuously print the data
while True:
    gyro = list(mpu.read_gyro_data())
    accel = list(mpu.read_accel_data())
    print("Gyro: %.2f %.2f %.2f Accel: %.2f %.2f %.2f" % (gyro[0] - gyro_cal[0],
                                                          gyro[1] - gyro_cal[1],
                                                          gyro[2] - gyro_cal[2],
                                                          accel[0] - accel_cal[0],
                                                          accel[1] - accel_cal[1],
                                                          accel[2] - accel_cal[2]))
    now = ticks_ms()
    a = "gx:%s:%s" % (now, gyro[0] - gyro_cal[0])
    s.sendto(a.encode('utf-8'), (UDP_IP, UDP_PORT))
    a = "gy:%s:%s" % (now, gyro[1] - gyro_cal[1])
    s.sendto(a.encode('utf-8'), (UDP_IP, UDP_PORT))
    a = "gz:%s:%s" % (now, gyro[2] - gyro_cal[2])
    s.sendto(a.encode('utf-8'), (UDP_IP, UDP_PORT))
    a = "ax:%s:%s" % (now, accel[0] - accel_cal[0])
    s.sendto(a.encode('utf-8'), (UDP_IP, UDP_PORT))
    a = "ay:%s:%s" % (now, accel[1] - accel_cal[1])
    s.sendto(a.encode('utf-8'), (UDP_IP, UDP_PORT))
    a = "az:%s:%s" % (now, accel[2] - accel_cal[2])
    s.sendto(a.encode('utf-8'), (UDP_IP, UDP_PORT))
    sleep(0.1)
