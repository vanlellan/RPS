#demostration of simple 2D animation with tkinter
#Randall Evan McClellan -- 2020-04-30

import tkinter as tk




class demoScreen():
    def __init__(self):
        self.root = tk.Tk()
        self.canvas = tk.Canvas(self.root, width=400, height=400)
        self.circle1 = self.canvas.create_oval(20,20,200,200,outline='black',fill='red')
        self.canvas.bind('<Escape>', self.bail)
        self.canvas.bind('<Key>', self.printEvent)
        self.canvas.bind('<Left>', self.moveLeft)
        self.canvas.pack()
        self.canvas.focus_set()
        self.canvas.update()
        print("Got Here end init")

    def printEvent(self, event):
        print("Got Here printEvent")
        position = "x={}, y={}".format(event.x, event.y)
        print(event.type, "event", position, event.keysym)

    def moveLeft(self, event):
        print("moveLeft")
        self.canvas.move(self.circle1, -1, 0)
        self.canvas.update()

    def bail(self, event):
        self.root.destroy()

if __name__ == "__main__":
    demo = demoScreen()
    demo.root.mainloop()
    


