from machine import UART, Pin
uart = UART(0, baudrate=115200, tx=Pin(16), rx=Pin(17))
print('testing', file=uart)

uart.write('testing')
uart.read(5)
