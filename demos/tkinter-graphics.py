#demostration of simple 2D animation with tkinter
#Randall Evan McClellan -- 2020-04-30

import tkinter as tk
import os
import platform
import math

#ToDo:
#   [ ] Use pressed dict to handle key press/release, rather than OS


class circ():
    def __init__(self, aScreen):
        self.aScreen = aScreen
        self.keyMap = {'Left':(-1,0), 'Right':(1,0), 'Up':(0,-1), 'Down':(0,1)}
        self.circle1 = self.aScreen.canvas.create_oval(20,20,30,30,outline='black',fill='red')
        self.vel = [0.0, 0.0]
        self.speed = 0.1
        self.brake = 0.2
        self.draw()

    def draw(self):
        #add to velocities based on currently pressed arrow keys
        self.vel[0] += self.speed*self.keyMap['Right'][0]*self.aScreen.pressedDict['Right']     #right
        self.vel[1] += self.speed*self.keyMap['Up'][1]*self.aScreen.pressedDict['Up']           #up
        self.vel[0] += self.speed*self.keyMap['Left'][0]*self.aScreen.pressedDict['Left']       #left
        self.vel[1] += self.speed*self.keyMap['Down'][1]*self.aScreen.pressedDict['Down']       #down
        #reduce velocity if brake key is pressed (space)
        brakev0 = -math.copysign(1,self.vel[0])*self.brake*self.aScreen.pressedDict['space']
        brakev1 = -math.copysign(1,self.vel[1])*self.brake*self.aScreen.pressedDict['space']
        self.vel[0] += brakev0
        self.vel[1] += brakev1
        if 2.0*abs(brakev0) > abs(self.vel[0]):
            self.vel[0] = 0.0
        if 2.0*abs(brakev1) > abs(self.vel[1]):
            self.vel[1] = 0.0
        #move circle based on current values of velocities
        self.aScreen.canvas.move(self.circle1, self.vel[0], self.vel[1])
        #update canvas and set up for next loop
        self.aScreen.canvas.update()
        self.aScreen.canvas.after(10, self.draw)


class demoScreen():
    def __init__(self):
        self.root = tk.Tk()
        self.pressedDict = {'Left':False, 'Right':False, 'Up':False, 'Down':False, 'space':False}
        self.canvas = tk.Canvas(self.root, width=400, height=400)
        self.circ1 = circ(self)
        self.canvas.bind('<Escape>', self.bail)
        self.canvas.bind('<KeyPress>', self.printEvent)
        self.canvas.bind('<KeyRelease>', self.printEvent)
        self.canvas.pack()
        self.canvas.focus_set()
        self.canvas.update()

    def printEvent(self, event):
        position = "x={}, y={}".format(event.x, event.y)
        if str(event.type) == 'KeyPress':
            self.pressedDict[event.keysym] = True
        if str(event.type) == 'KeyRelease':
            self.pressedDict[event.keysym] = False

    def bail(self, event):
        self.root.destroy()

if __name__ == "__main__":
    if 'Linux' == platform.system():
        print('Detected Linux, disabling keypress autorepeat...')
        os.system('xset r off')

    demo = demoScreen()
    try:
        demo.root.mainloop()
    except Exception as excpt:
        print(excpt)

    print('re-enabling keypress autorepeat...')
    os.system('xset r on')
    


