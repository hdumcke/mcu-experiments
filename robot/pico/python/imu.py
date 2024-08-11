from machine import I2C, Pin
import MPU6050
from math import pi


class IMU:
    def __init__(self, sda_pin=18, scl_pin=19):
        self.i2c = I2C(1, sda=Pin(sda_pin), scl=Pin(scl_pin))
        self.mpu = MPU6050.MPU6050(self.i2c)
        self.mpu.i2c.writeto_mem(self.mpu.address, 0x6B, bytes([0x80]))
        self.mpu.i2c.writeto_mem(self.mpu.address, 0x6B, bytes([0x03]))
        self.mpu.i2c.writeto_mem(self.mpu.address, 0x6C, bytes([0x00]))
        self.mpu.i2c.writeto_mem(self.mpu.address, 0x1A, bytes([0x04]))
        self.mpu.i2c.writeto_mem(self.mpu.address, 0x1B, bytes([0x18]))
        self.mpu.i2c.writeto_mem(self.mpu.address, 0x1C, bytes([0x10]))
        self.mpu.i2c.writeto_mem(self.mpu.address, 0x1D, bytes([0x02]))
        self.mpu.i2c.writeto_mem(self.mpu.address, 0x6A, bytes([0x20]))
        self.mpu.i2c.writeto_mem(self.mpu.address, 0x37, bytes([0x00]))
        self.mpu.i2c.writeto_mem(self.mpu.address, 0x38, bytes([0x01]))
        self.mpu.wake()
        self.cb = None

    def register_data_ready_callback(self, cb):
        self.cb = cb

    def read(self):
        # We can not use mpu.read_gyro_data() as it does two reads via i2c
        data = self.mpu.i2c.readfrom_mem(self.mpu.address, 0x43, 6)  # read 6 bytes (gyro data)
        # 1 / 16.384 * pi / 180.0 = 0.001065264
        z = (self.mpu._translate_pair(data[4], data[5])) * 0.001065264
        if self.cb:
            self.cb(z)
