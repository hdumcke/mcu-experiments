import network
from time import sleep
from wifi_credentials import ssid, password


def connect():
    # Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)

    counter = 0
    while not wlan.isconnected():
        print('Waiting for connection...')
        sleep(1)
        counter += 1
        if counter > 20:
            return False

    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    return True
