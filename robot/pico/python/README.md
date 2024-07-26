# RPI Pico W

## Recovery

https://www.raspberrypi.com/documentation/microcontrollers/raspberry-pi-pico.html#resetting-flash-memory

Reinstall Micropython


in rshell:

```bash
cp MPU6050.py /pyboard/
cp MPU6050_calibrate.py /pyboard/
cp MPU6050_test.py /pyboard/
cp PID.py /pyboard/
cp boot.py /pyboard/
cp controller.py /pyboard/
cp dc_motor_pid.py /pyboard/
cp encoder.py /pyboard/
cp motor.py /pyboard/
cp wifi.py /pyboard/
cp wifi_credentials.py /pyboard/
```

## Teleplot on Mac OS

```bash
git clone https://github.com/nesnes/teleplot
cd server
npm i
node main.js
```
