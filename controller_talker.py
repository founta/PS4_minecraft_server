#from time import sleep
import asyncio
from asyncio import sleep
import RPi.GPIO as gpio


#teardown; clear and free gpio pins used
import signal, sys
def channel_cleanup_exit(signal, frame):
    gpio.cleanup((15, 16, 18, 22, 37))
    #print ("cleaning up!")
    sys.exit(0)
signal.signal(signal.SIGINT, channel_cleanup_exit)
signal.signal(signal.SIGTERM, channel_cleanup_exit)


class Control:
    def __init__(self, controller_delay):
        self.controller_delay = controller_delay
        self.all_sigs = (15, 16, 18, 22, 37) #BCM 22,23,24,25,26 respectively
        #logic_sigs = (15, 16, 18, 22) #BCM 22,23,24,25
        self.logic_sigs = (22, 18, 16, 15) #BCM 25,24,23,22
        self.en = 37  #BCM26
        
        #GPIO init
        gpio.setmode(gpio.BOARD)    #using board mode
        gpio.setup(self.all_sigs, gpio.OUT)  #all signals are outputs
        gpio.output(self.all_sigs, 0)        #clear all outputs
        #BCM22, BCM23, BCM24, BCM25, BCM26 = sigs; #individual BCMs, shouldn't need


    def enable(self):
        gpio.output(self.en, 1)

    def clear(self):
        gpio.output(self.all_sigs, 0)

    #bits should be a list with 4 elements
    def set_output(self,bits):
        gpio.output(self.logic_sigs, bits)

    #circle is out 6 on decoder
    async def circle(self):
        #print("circle")
        await sleep(self.controller_delay)
        self.set_output([0,1,1,0])  
        self.enable()
        await sleep(self.controller_delay)
        self.clear()

    #square is out 4 on decoder
    async def square(self):
        #print("square")
        await sleep(self.controller_delay)
        self.set_output([0,1,0,0])
        self.enable()
        await sleep(self.controller_delay)
        self.clear()

    #x is out 7 on decoder
    async def cross(self):
        #print("cross")
        await sleep(self.controller_delay)
        self.set_output([0,1,1,1])
        self.enable()
        await sleep(self.controller_delay)
        self.clear()

    #triangle is out 5 on decoder
    async def triangle(self):
        #print("triangle")
        await sleep(self.controller_delay)
        self.set_output([0,1,0,1])
        self.enable()
        await sleep(self.controller_delay)
        self.clear()

    #touchpad is decoder 2 out 0 (global out 8)
    async def touch(self):
        #print("touchpad")
        await sleep(self.controller_delay)
        self.set_output([1,0,0,0])
        self.enable()
        await sleep(self.controller_delay)
        self.clear()

    #playstation is global out 9
    async def ps(self):
        #print("ps button")
        await sleep(self.controller_delay)
        self.set_output([1,0,0,1])
        self.enable()
        await sleep(self.controller_delay)
        self.clear()

    #options button is global out 10
    async def options(self):
        #print("options")
        await sleep(self.controller_delay)
        self.set_output([1,0,1,0])
        self.enable()
        await sleep(self.controller_delay)
        self.clear()

    #left is out 2
    async def left(self):
        #print("left")
        await sleep(self.controller_delay)
        self.set_output([0,0,1,0])
        self.enable()
        await sleep(self.controller_delay)
        self.clear()

    #right is out 3
    async def right(self):
        #print("right")
        await sleep(self.controller_delay)
        self.set_output([0,0,1,1])
        self.enable()
        await sleep(self.controller_delay)
        self.clear()
        
    #up is out 0
    async def up(self):
        #print("up")
        await sleep(self.controller_delay)
        self.clear()
        self.enable()
        await sleep(self.controller_delay)
        self.clear()

    #down is out 1
    async def down(self):
        #print("down")
        await sleep(self.controller_delay)
        self.set_output([0,0,0,1])
        self.enable()
        await sleep(self.controller_delay)
        self.clear()

