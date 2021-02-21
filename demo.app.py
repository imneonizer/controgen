#v0.01

import machine
import time

class App:
    def __init__(self, pin=2):
        self.pin = machine.Pin(pin, machine.Pin.OUT)

    def run(self, t=0.02):
        print("Begin Led blinking")

        while True:
            # there is a bug in nodemcu
            # due to which pin.on() actually works opposite
            # print("led value => off")
            self.pin.on()
            time.sleep(t)

            # print("led value => on")
            self.pin.off()
            time.sleep(t)