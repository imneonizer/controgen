def check_for_updates(ssid, password, app_url):
    import network
    import machine
    import os
    from time import sleep

    # activate wifi module in station mode
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    # status indicator
    led = machine.Pin(2, machine.Pin.OUT)
    led.off() # turn led on
    
    try:
        # iterate through available networks
        for s in wlan.scan():
            if s[0].decode('utf-8') == ssid:
                print('Network found!')
                wlan.connect(ssid, password)
                while not wlan.isconnected():
                    machine.idle()

                print('WLAN connection succeeded!')
                # 2 times led blink to indicate, network connected
                for i in range(2):
                    led.on(); sleep(0.1); led.off(); sleep(0.1)
                led.on() # finally turn off the led

                try:
                    import urequests
                except:
                    import upip
                    upip.install("micropython-urequests")
                    import urequests

                # check for updates
                res = urequests.get(app_url).text
                
                current_version = '0.0'
                with open("app.py", "r") as f:
                    current_version = f.read().split("\n")[0].lstrip("#v")

                fetched_version = res.split("\n")[0].lstrip("#v")
                print("Fetched: v{}, Current: v{}".format(fetched_version, current_version))

                if fetched_version == current_version:
                    print("Not updating current app")
                else:
                    print("Updating current app to v{}".format(fetched_version))
                    
                    # 5 times long-short led blink to indicate, app update running
                    for i in range(5):
                        led.off(); sleep(0.5); led.on(); sleep(0.1)
                    led.on() # finally turn off the led
                    
                    with open("app.py", "w") as f:
                        f.write(res)
                    
                    # 2 times short led blink to indicate, app update finished
                    for i in range(2):
                        led.off(); sleep(0.1); led.on(); sleep(0.1)
                    led.on() # finally turn off the led

    except Exception as e:
        print(e)
        
        # if error is about scan failed, don't use led indicator
        if str(e) != "scan failed":
            # 7 times long-short led blink to indicate, error occured
            for i in range(7):
                s = 0.5 if i%2 == 0 else 0.1
                led.off(); sleep(s); led.on(); sleep(0.5)
            led.on() # finally turn off the led

    wlan.active(False)
    led.on() # finally turn off the led
    # sleep(0.5)

def run_app():
    from app import App
    App().run()
 
# use direct link to app.py in app_url parameter
check_for_updates(ssid="ota", password="123456789", app_url="https://raw.githubusercontent.com/imneonizer/controgen/master/app.py")

# entrypoint for the application
run_app()