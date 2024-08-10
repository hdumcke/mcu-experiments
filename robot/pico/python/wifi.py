import network
from time import sleep
from wifi_credentials import ssid, password


class Wifi:
    def __init__(self):
        self.wlan = network.WLAN(network.STA_IF)

    def connect(self):
        # Connect to WLAN
        self.wlan.active(True)
        self.wlan.connect(ssid, password)

        counter = 0
        while not self.wlan.isconnected():
            print('Waiting for connection...')
            sleep(1)
            counter += 1
            if counter > 20:
                return False

        return True

    def get_ip(self):
        if self.wlan.isconnected():
            return self.wlan.ifconfig()[0]
        else:
            return None
