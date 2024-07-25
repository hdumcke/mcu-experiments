# based on https://github.com/sflebrun/Pico-TTMotorTestBed

# Defines the class that represents one motor part of TB6612FNG Dual H-Bridge.
#
# Note: This class is actually independent of what type of DC Motor is attached to
#       the Dual H-Bridge Module.
#       hence the name.
#
# Three pins control each motor -- PMW, IN1, and IN2.
#
# Motors are labeled A and B on the H-Bridge module.  This class only deals with
# a single motor so the A and B labels are ignored.  See the MotorControl class
# for dealing with both motors and the Standby Pin.

from machine import Pin, PWM


# This class represents the part of the Dual H-Bridge module.
class Motor:
    """A Class that contains the state of a DC Motor"""

    # Default Constructor
    #
    # @param  gpioPWM   The GPIO Pin Number, not the physical pin number, of the
    #                   pin used to set the motor speed with a pulse width modulation
    # @param  gpioIN1   The GPIO Pin Number used to determine direction of motor in
    #                   conjunction with gpioIN2
    # @param  gpioIN2   The GPIO Pin Number used to determine direction of motor in
    #                    conjunction with gpioIN1
    #
    def __init__(self, gpioPWM: int, gpioIN1: int, gpioIN2: int):
        self.gpioPWM = gpioPWM
        self.gpioIN1 = gpioIN1
        self.gpioIN2 = gpioIN2

        if (gpioPWM < 0):
            # Invalid value
            raise ValueError("Motor Constructor: Invalid GPIO PWM Pin number: " + str(gpioPWM))
        else:
            # Initialize the PWM pin
            self.pinPWM = Pin(gpioPWM, mode=Pin.OUT)

            self.pwmPin = PWM(self.pinPWM)
            self.pwmPin.freq(10000)  # 10kHz
            self.pwmPin.duty_u16(0)  # off

            # Initialize the two signal input pins
            self.in1 = Pin(gpioIN1, mode=Pin.OUT)
            self.in2 = Pin(gpioIN2, mode=Pin.OUT)

            self.in1.low()
            self.in2.low()

    # Determine if Pin ID is one of the GPIO Pins associated with this motor
    def usesPin(self, pinID: int):
        if (pinID == self.gpioPWM or pinID == self.gpioIN1 or pinID == self.gpioIN2):
            return True
        else:
            return False

    # Return the configured GPIO Pin object
    def pwm(self):
        return self.gpioPWM

    # Returns the GPIO Pin object for IN1
    def signal1Pin(self):
        return self.in1

    # Returns the GPIO Pin object for IN2
    def signal2Pin(self):
        return self.in2

    # Returns what the IN1 Pin should be set to: True == HIGH, False == LOW
    def signal1(self):
        return self.IN1Value

    # Returns what the IN2 Pin should be set to: True == HIGH, False == LOW
    def signal2(self):
        return self.IN2Value

    # Set actual Motor Speed and Direction
    #
    # This function actually writes to the Dual H-Bridge module, hence causing the motors to
    # turn or to stop.
    def motorControl(self, speed):
        signal1 = False
        signal2 = False

        if speed > 0:
            signal2 = True
        elif speed < 0:
            signal1 = True
        else:
            speed = 0

        if (signal1):
            self.in1.on()
        else:
            self.in1.off()

        if (signal2):
            self.in2.on()
        else:
            self.in2.off()

        # Set Speed
        self.pwmPin.duty_u16(abs(speed))

        # End of MotorControl()
