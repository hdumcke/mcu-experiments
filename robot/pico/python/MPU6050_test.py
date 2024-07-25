import machine
import time
import MPU6050

gyro_cal = [ -4.9342, 1.8476, 0.9966]
accel_cal = [ -0.0629, -0.0112, 0.9863]

# Set up the I2C interface
i2c = machine.I2C(1, sda=machine.Pin(18), scl=machine.Pin(19))

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
    time.sleep(0.1)
