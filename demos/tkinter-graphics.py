#demostration of simple 2D animation with tkinter
#Randall Evan McClellan -- 2020-04-30

import tkinter as tk

#ToDo:
#   [ ] Use pressed dict to handle key press/release, rather than OS


class demoScreen():
    def __init__(self):
        self.root = tk.Tk()
        self.pressedDict = {'Left':False, 'Right':False, 'Up':False, 'Down':False}
        self.canvas = tk.Canvas(self.root, width=400, height=400)
        self.circle1 = self.canvas.create_oval(20,20,200,200,outline='black',fill='red')
        self.canvas.bind('<Escape>', self.bail)
        self.canvas.bind('<KeyPress>', self.printEvent)
        self.canvas.bind('<KeyRelease>', self.printEvent)
        self.canvas.pack()
        self.canvas.focus_set()
        self.canvas.update()
        print("Got Here end init")

    def printEvent(self, event):
        print("Got Here printEvent")
        position = "x={}, y={}".format(event.x, event.y)
        print(event.type, "event", position, event.keysym)
        if event.keysym in ['Left', 'Right', 'Up', 'Down']:
            self.move(self, event.keysym)

    def move(self, event, aKey):
        print("move")
        keyMap = {'Left':(-1,0), 'Right':(1,0), 'Up':(0,-1), 'Down':(0,1)}
        self.canvas.move(self.circle1, keyMap[aKey][0], keyMap[aKey][1])
        self.canvas.update()

    def bail(self, event):
        self.root.destroy()

if __name__ == "__main__":
    demo = demoScreen()
    demo.root.mainloop()
    


