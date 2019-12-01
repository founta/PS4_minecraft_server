#import time
import asyncio
from asyncio import sleep
import controller_talker as controller

virtual_kb_layout = (('1', '2', '3', '4', '5', '6', '7', '8', '9', '0'), 
                     ('q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p'), 
                     ('a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', '\''),
                     ('z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '?'))

control = controller.Control(0.06)

'''control.up()
control.down()
control.left()
control.right()
'''
'''control.square()
control.triangle()
control.circle()
control.cross()
control.touch()
control.ps()
control.options()'''
async def init_controller():
    await control.ps()
    await sleep(2)
    await control.cross()
#real simple. presses touchpad, square and waits a couple seconds
async def open_invite_screen():
    await control.touch()
    await control.square()
    await sleep(2)


async def search():
    await control.up()
    await control.right()
    await control.cross()
    await sleep(1)
    
async def select_player():
    await sleep(4)
    await control.down()    
    await control.cross()
    await control.right()
    await control.cross()
    
async def send_invite():
    await sleep(0.5)
    await control.cross()
    await sleep(2)

async def close_invite_screen():
    await control.circle()
    await sleep(1)

async def write_kb_str(string, upper=False, x=4, y=2):
    cap = upper
    i = x
    j = y
    
    to_cap = cap
    for char in string:
        y_dst = 0;
        x_dst = 0;
        if char == '_':
            to_cap = (cap == False)
            x_dst  = 8
            y_dst  = 3
        elif char == '-':
            to_cap = (cap == False)
            x_dst = 7
            y_dst = 3
        else:
            if ((char >= 'A') & (char <= 'Z')):
                to_cap = (cap == False) #we need to be in capitalize mode
                char = char.lower() #convert uppercase to lower
            elif ((char < '0') | (char > '9')) :
                to_cap = (cap == True) #we need to be in lowercase mode if its not a number
            for line in virtual_kb_layout:
                try:
                    x_dst = line.index(char)
                    break
                except:
                    y_dst += 1
        if to_cap: #press cap button to toggle caps
            while i != 0:
                if i > 0:
                    await control.left()
                    i -= 1
            while j != 4:
                if j > 4:
                    await control.up()
                    j -= 1
                if j < 4:
                    await control.down()
                    j += 1
            await control.cross()
            cap = not cap
        while j != y_dst: #move up or down
            if j > y_dst: #move up
                await control.up()
                j-=1
            if j < y_dst: #move down
                await control.down()
                j+=1
        while i != x_dst: #move left or right
            if i > x_dst: #then we need to go left
                await control.left()
                i-=1
            if i < x_dst: #then we need to go right
                await control.right()
                i+=1
        await control.cross() #press the button
        cap = False
        #print(virtual_kb_layout[y_dst][x_dst])
     
    #escape virtual keyboard
    await control.circle()                
            
    
    
    
    