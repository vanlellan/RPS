#demostration of simple 2D animation with tkinter
#Randall Evan McClellan -- 2020-04-30

import tkinter as tk
import os
import platform

#ToDo:
#   [ ] Use pressed dict to handle key press/release, rather than OS


class demoScreen():
    def __init__(self):
        self.root = tk.Tk()
        self.pressedDict = {'Left':False, 'Right':False, 'Up':False, 'Down':False}
        self.keyMap = {'Left':(-1,0), 'Right':(1,0), 'Up':(0,-1), 'Down':(0,1)}
        self.canvas = tk.Canvas(self.root, width=400, height=400)
        self.circle1 = self.canvas.create_oval(20,20,30,30,outline='black',fill='red')
        self.canvas.bind('<Escape>', self.bail)
        self.canvas.bind('<KeyPress>', self.printEvent)
        self.canvas.bind('<KeyRelease>', self.printEvent)
        self.canvas.pack()
        self.canvas.focus_set()
        self.canvas.update()
        self.draw()

    def printEvent(self, event):
        position = "x={}, y={}".format(event.x, event.y)
        if str(event.type) == 'KeyPress':
            self.pressedDict[event.keysym] = True
        if str(event.type) == 'KeyRelease':
            self.pressedDict[event.keysym] = False

    def draw(self):
        self.canvas.move(self.circle1, self.keyMap['Right'][0]*self.pressedDict['Right'], 0)     #right
        self.canvas.move(self.circle1, 0, self.keyMap['Up'][1]*self.pressedDict['Up'])           #up
        self.canvas.move(self.circle1, self.keyMap['Left'][0]*self.pressedDict['Left'], 0)       #left
        self.canvas.move(self.circle1, 0, self.keyMap['Down'][1]*self.pressedDict['Down'])      #down
        self.canvas.update()
        self.canvas.after(10, self.draw)

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
    


