#v0.01

from machine import Pin
import time

# NodeMCU Pinout Mapping
D0 = 16 # Gen start relay
D1 = 5 # Gen stop relay
D2 = 4 # Gen switch relay
D5 = 14 # Mains switch relay

D6 = 12 # Gen on / off signal
D7 = 13 # Mains on / off signal

class Console:
    i = 0

    @property
    def idx(self):
        self.i = 0 if self.i == 9 else self.i+1
        return self.i

    def log(self):
        msg = ""
        msg += "| I = {} | ".format(self.idx)
        msg += "| M = {} | ".format("ON" if mains.isactive else "OFF")
        msg += "G = {} | ".format("ON" if gen.isactive else "OFF")
        msg += "G_START = {} | ".format("ON" if self.ison(gen.start_pin) else "OFF")
        msg += "G_STOP = {} | ".format("ON" if self.ison(gen.stop_pin) else "OFF")
        msg += "G_SWITCH = {} | ".format("ON" if self.ison(gen.activate_pin) else "OFF")
        msg += "M_SWITCH = {} | ".format("ON" if self.ison(mains.activate_pin) else "OFF")
        print(msg, end="\r")

    def sleep(self, t=0, delay=0.09):
        # utility function to update console, while sleeping
        st = time.time()
        while (time.time() - st ) < t:
            self.log()
            time.sleep(delay if t > delay else t)
    
    def toggle(self, a, b):
        a.deactivate()
        self.sleep(0.3)
        b.activate()

    def off(self, pin):
        # it's a bug, board returns opposite values
        pin.on()

    def on(self, pin):
        # it's a bug, board returns opposite values
        pin.off()
    
    def ison(self, pin):
        # it's a bug, board returns opposite values
        return (not bool(pin.value()))
    
    def observe(self, source, t=1):
        self.sleep(t)
        if source.isactive:
            return True
        return False

class Generator(Console):
    def __init__(self, input_pin=D6, activate_pin=D2, start_pin=D0, stop_pin=D1):
        self.input_pin = Pin(input_pin, Pin.IN, Pin.PULL_UP)
        self.activate_pin = Pin(activate_pin, Pin.OUT)
        self.start_pin = Pin(start_pin, Pin.OUT)
        self.stop_pin = Pin(stop_pin, Pin.OUT)

        # set configuration to off by default
        self.off(self.activate_pin)
        self.off(self.start_pin)
        self.off(self.stop_pin)

        self.retry = 3
        self.start_failed = 0
        self.stop_failed = 0
        self.sleep_time = 3 #sec

    @property
    def isactive(self):
        return self.ison(self.input_pin)

    def activate(self):
        self.on(self.activate_pin)

    def deactivate(self):
        self.off(self.activate_pin)
    
    def reset_failed(self):
        self.start_failed = 0
        self.stop_failed = 0

    def start(self):
        for i in range(self.retry):
            if self.start_failed == self.retry:
                break

            self.on(self.start_pin)
            self.sleep(self.sleep_time)
            self.off(self.start_pin)
            self.sleep(self.sleep_time)

            if self.isactive:
                self.off(self.start_pin)
                break

            self.start_failed += 1

    def stop(self):
        for i in range(self.retry):
            if self.stop_failed == self.retry:
                break

            self.on(self.stop_pin)
            self.sleep(self.sleep_time)
            self.off(self.stop_pin)
            self.sleep(self.sleep_time)

            if not self.isactive:
                self.off(self.stop_pin)
                break

            self.stop_failed += 1

class Mains(Console):
    def __init__(self, input_pin=D7, activate_pin=D5):
        self.input_pin = Pin(input_pin, Pin.IN, Pin.PULL_UP)
        self.activate_pin = Pin(activate_pin, Pin.OUT)

        # set configuration to off by default
        self.off(self.activate_pin)
    
    @property
    def isactive(self):
        return self.ison(self.input_pin)
    
    def activate(self):
        self.on(self.activate_pin)

    def deactivate(self):
        self.off(self.activate_pin)

mains = Mains()
gen = Generator()
console = Console()

class App:
    def run(self):
        print("Program: controgen, started...")

        while True:
            # logic to switch relays
            if mains.isactive:
                gen.reset_failed()
                console.toggle(gen, mains)

            elif gen.isactive:
                gen.reset_failed()
                console.toggle(mains, gen)

            else:
                console.toggle(gen, mains)
            
            # logic to handle generator
            if (not mains.isactive) and (not gen.isactive):
                # if both mains and generator is off
                if console.observe(mains, t=5):
                    # if mains is activated within 5 sec
                    # ignore generator start
                    continue

                gen.start()
            
            elif mains.isactive and gen.isactive:
                # if both mains and generator is on
                if not console.observe(mains, t=5):
                    # if mains is gone within 5 sec
                    # ignore generator stop
                    continue

                gen.stop()

            console.sleep(0.3)