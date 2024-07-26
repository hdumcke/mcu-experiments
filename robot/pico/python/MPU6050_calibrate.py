import machine
import time
import MPU6050

# Set up the I2C interface
i2c = machine.I2C(1, sda=machine.Pin(18), scl=machine.Pin(19))

# Set up the MPU6050 class
mpu = MPU6050.MPU6050(i2c)

gyro_cum = [0.0] * 3
accel_cum = [0.0] * 3

# wake up the MPU6050 from sleep
mpu.wake()

# let robot settle
time.sleep(5)

for i in range(100):
    gyro = list(mpu.read_gyro_data())
    accel = list(mpu.read_accel_data())
    for k in range(3):
        gyro_cum[k] += gyro[k]
        accel_cum[k] += accel[k]
    time.sleep(0.1)


with open("calibration.py", 'w') as fh:
    fh.write("gyro_cal = [%.4f, %.4f, %.4f]\n" % (gyro_cum[0] / 100.0, gyro_cum[1] / 100.0, gyro_cum[2] / 100.0))
    fh.write("accel_cal = [%.4f, %.4f, %.4f]" % (accel_cum[0] / 100.0, accel_cum[1] / 100.0, accel_cum[2] / 100.0))
