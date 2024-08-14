from machine import Pin
from motor import Motor
from time import sleep

gpioPWA = 10
gpioPWB = 11

gpioAN1 = 13
gpioAN2 = 12

gpioBN1 = 15
gpioBN2 = 14

gpioStandby = 20

gpioLED = 25

motorA = Motor(gpioPWA, gpioAN1, gpioAN2)
motorB = Motor(gpioPWB, gpioBN1, gpioBN2)

pinSTANDBY = Pin(gpioStandby, mode=Pin.OUT)
pinSTANDBY.high()

motorA.motorControl(5000)
motorB.motorControl(5000)

sleep(5)

motorA.motorControl(0)
motorB.motorControl(0)

motorA.motorControl(2**16)
motorB.motorControl(2**16)
