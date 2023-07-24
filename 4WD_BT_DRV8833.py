from time import sleep
import machine
from machine import Pin, PWM, UART
led = Pin(28, Pin.OUT)
kip = 0.025

frq = 50 # 50 - 100 work best
dutymax = 65535 # highest duty cycle value
dutymin = dutymax * 0.4 # lowest
dutyrange = dutymax-dutymin
step = 50 # middle of range
duty = int((dutyrange/100)*step) # 0 = fastest
lastaction = "" # the module to run after speed change
terminate = False # flag to control endless loop
uart= UART(0,9600)
in1 = PWM(Pin(18))
in1.freq(frq)
din1 = Pin(18, Pin.OUT)
in2 = PWM(Pin(19))
in2.freq(frq)
din2 = Pin(19, Pin.OUT)
in3 = PWM(Pin(20))
in3.freq(frq)
din3 = Pin(20, Pin.OUT)
in4 = PWM(Pin(21))
in4.freq(frq)
din4 = Pin(21, Pin.OUT)

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
    blink (3)
    din1 = Pin(18, Pin.OUT)
    din1.on()
    in2 = PWM(Pin(19))
    in2.duty_u16(duty)
    din3 = Pin(20, Pin.OUT)
    din3.on()
    in4 = PWM(Pin(21))
    in4.duty_u16(duty)
def bwd():
    global lastaction
    lastaction = "b"
    blink (3)
    din2 = Pin(19, Pin.OUT)
    din2.on()
    in1 = PWM(Pin(18))
    in1.duty_u16(duty)
    din4 = Pin(21, Pin.OUT)
    din4.on()
    in3 = PWM(Pin(20))
    in3.duty_u16(duty)
def right ():
    global lastaction
    lastaction = "r"
    blink (3)
    din1 = Pin(18, Pin.OUT)
    din1.on()
    in2 = PWM(Pin(19))
    in2.duty_u16(duty)
    in3 = PWM(Pin(20))
    in3.duty_u16(duty)
    din4 = Pin(21, Pin.OUT)
    din4.on()
def left ():
    global lastaction
    lastaction = "l"
    blink (3)
    din2 = Pin(19, Pin.OUT)
    din2.on()
    in1 = PWM(Pin(18))
    in1.duty_u16(duty)
    din3 = Pin(20, Pin.OUT)
    din3.on()
    in4 = PWM(Pin(21))
    in4.duty_u16(duty)   
def stop():
    global lastaction
    lastaction = "s"
    LEDoff()
    din1 = Pin(18, Pin.OUT)
    din1.on()
    din2 = Pin(19, Pin.OUT)
    din2.on()
    din3 = Pin(20, Pin.OUT)
    din3.on()
    din4 = Pin(21, Pin.OUT)
    din4.on()

#Stop the robot as soon as possible
stop()
    
try:
    while terminate != True:
        if uart.any(): #Checking if data available
            data=uart.read() #Getting data
            data=str(data) #Converting bytes to str type
            print(data)
            if ('stop' in data):
                pass
            elif ('exit' in data):
                terminate = True
            elif('forward' in data):
                fwd() #Forward
            elif('backward' in data):
                bwd() #Backward
            elif('right' in data):
                right() #Turn Right
            elif('left' in data):
                left() #Turn Left
            elif('halt' in data):
                stop() #Stop
            elif('E' in data):
                blink (3)
                speed=data.split("|")
                step = float(speed[1])
                if (step >= 95):
                    step = 100
                elif (step < 5):
                    step = 5
                duty = int(dutyrange-(step/100) * dutyrange) # 0 = fastest
                print ("step:",step,"duty =",duty)
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
        else:
            pass
except KeyboardInterrupt:
    stop()
    LEDoff()
stop()
LEDoff()
#     machine.reset()

    