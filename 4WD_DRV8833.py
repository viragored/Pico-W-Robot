import network
import socket
from time import sleep
import machine, neopixel
from machine import Pin, PWM
from secret import ssid,password,hostname
led = Pin(28, Pin.OUT)
kip = 0.025

frq = 20 # lower number gets more torque at the wheels
dutymax = 65535 # highest duty cycle value
dutymin = dutymax * 0.2 # lowest
dutyrange = dutymax-dutymin
steps = 10 # No of speed controller steps 
currentstep = 1 # initialise at slow speed
duty = int(dutymin+(dutyrange/10)*currentstep)
lastaction = "" # the module to run after speed change

in1 = machine.PWM(Pin(18)) # fwd
in1.freq(frq)
in2 = machine.PWM(Pin(19)) # bwd
in2.freq(frq)
in3 = machine.PWM(Pin(20)) # fwd
in3.freq(frq)
in4 = machine.PWM(Pin(21)) # bwd
in4.freq(frq)

def LEDon(): 
    led.on()
def LEDoff():
    led.off()
def blink (n):
    for times in range (n):
        led.on()    
        sleep(kip)
        led.off()
        sleep(kip)
    led.on()    
def fwd():
    global lastaction
    lastaction = "f"
    blink (5)
    in1.duty_u16(duty)
    in3.duty_u16(duty)
    in2.duty_u16(0)
    in4.duty_u16(0)
def bwd():
    global lastaction
    lastaction = "b"
    blink (5)
    in1.duty_u16(0)
    in3.duty_u16(0)
    in2.duty_u16(duty)
    in4.duty_u16(duty)
def stop():
    global lastaction
    lastaction = "s"
    LEDoff()
    in1.duty_u16(0)
    in3.duty_u16(0)
    in2.duty_u16(0)
    in4.duty_u16(0)
def right():
    global lastaction
    lastaction = "r"
    blink (5)
    in1.duty_u16(int(dutymax*0.65))
    in3.duty_u16(0)
    in2.duty_u16(0)
    in4.duty_u16(int(dutymax*0.65))
def left():
    global lastaction
    lastaction = "l"
    blink (5)
    in1.duty_u16(0)
    in3.duty_u16(int(dutymax*0.65))
    in2.duty_u16(int(dutymax*0.65))
    in4.duty_u16(0)
def slow():
    global currentstep, duty
    if (currentstep > 0):
        currentstep -= 1
        duty = int(dutymin+(dutyrange/10)*currentstep)
    blink (5)
    print ("Slower, currentstep now:",currentstep,"duty now",duty)
    if lastaction == "f":
        fwd()
    elif lastaction == "b":
        bwd()
    elif lastaction == "r":
        right()
    elif lastaction == "l":
        left()
    elif lastaction == "s":
        stop()
def fast():
    global currentstep, duty
    if (currentstep < steps):
        currentstep += 1
        duty = int(dutymin+(dutyrange/10)*currentstep)
    blink (5)
    print ("Faster, currentstep now:",currentstep,"duty now",duty)
    if lastaction == "f":
        fwd()
    elif lastaction == "b":
        bwd()
    elif lastaction == "r":
        right()
    elif lastaction == "l":
        left()
    elif lastaction == "s":
        stop()
def connect():
    #Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    network.hostname(hostname)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        sleep(1)
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    blink (10)
    return ip
def open_socket(ip): # Open a socket
    address = (ip, 80)
    connection = socket.socket()
    connection.bind(address)
    connection.listen(1)
    return connection

def webpage():
    #Template HTML
    html = f"""
            <!DOCTYPE html>
            <html>
            <head>
            <title>4WD Robot Control</title>
            </head>
            <body>
            <center><b>
            <table>
            <tr>
            <td>
            <form action="./fast">
            <input type="submit" value="Faster" style="background-color: #eb9234; border-radius: 50px; height:175px; width:120px; font-weight: bold; border: none; color: blue; padding: 16px 24px; margin: 4px 2px"  />
            </form>
            </td>
            <td>
            <form action="./forward">
            <input type="submit" value="Forward" style="background-color: #04AA6D; border-radius: 15px; height:120px; width:175px; border: none; color: white; padding: 16px 24px; margin: 4px 2px"  />
            </form>
            </td>
            <td>
            <form action="./null">
            <input type="submit" value="null" style="background-color: #FFFFFF; border-radius: 15px; height:120px; width:120px; border: none; color: white; padding: 16px 24px; margin: 4px 2px" />
            </form>
            </td>
            </tr>
            </table>
            <table>
            <tr>
            <td><form action="./left">
            <input type="submit" value="Left" style="background-color: #04AA6D; border-radius: 15px; height:120px; width:175px; border: none; color: white; padding: 16px 24px; margin: 4px 2px" />
            </form>
            </td>
            <td>
            <form action="./stop">
            <input type="submit" value="Stop" style="background-color: #FF0000; border-radius: 50px; height:150px; width:150px; font-weight: bold; border: none; color: white; padding: 16px 24px; margin: 4px 2px" />
            </form>
            </td>
            <td>
            <form action="./right">
            <input type="submit" value="Right" style="background-color: #04AA6D; border-radius: 15px; height:120px; width:175px; border: none; color: white; padding: 16px 24px; margin: 4px 2px" />
            </form>
            </td>
            </tr>
            </table>
            <table>
            <tr>
            <td>
            <form action="./slow">
            <input type="submit" value="Slower" style="background-color: #eb9234; border-radius: 50px; height:175px; width:120px; font-weight: bold; border: none; color: blue; padding: 16px 24px; margin: 4px 2px"  />
            </form>
            </td>
            <td>
            <form action="./back">
            <input type="submit" value="Back" style="background-color: #04AA6D; border-radius: 15px; height:120px; width:175px; border: none; color: white; padding: 16px 24px; margin: 4px 2px" />
            </form>
            </td>
            <td>
            <form action="./null">
            <input type="submit" value="null" style="background-color: #FFFFFF; border-radius: 15px; height:120px; width:120px; border: none; color: white; padding: 16px 24px; margin: 4px 2px" />
            </form>
            </td>
            </tr>
            </table>
            </body>
            </html>
            """
    return str(html)

def serve(connection):
    #Start web server
    while True:
        client = connection.accept()[0]
        request = client.recv(1024)
        request = str(request)
        try:
            request = request.split()[1]
        except IndexError:
            pass
        if request == '/forward?':
            fwd()
        elif request =='/left?':
            left()
        elif request =='/stop?':
            stop()
        elif request =='/right?':
            right()
        elif request =='/back?':
            bwd()
        elif request =='/slow?':
            slow()
        elif request =='/fast?':
            fast()
        html = webpage()
        client.send(html)
        client.close()
#Stop the robot as soon as possible
stop()
    
try:
    ip = connect()
    connection = open_socket(ip)
    serve(connection)
    sleep(0.25)
except KeyboardInterrupt:
    stop()
    LEDoff()
    machine.reset()

    