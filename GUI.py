"""
This is the GUI file for BiTs
"""
from tkinter import *
master = Tk()
f = Frame(master, height=5, width=5)
f.pack_propagate(0) # don't shrink
f.pack()


class pixel:
    def __init__(self, r, c):
        self.row = r
        self.column = c
        p = Button(f, relief="flat", bg="white")
        p.grid(row = self.row, column = self.column)
   # def  filler(self, ):

def startup(c):
    for i in range(2):
        c.append(i)
        for j in range(2):
            c[i] = pixel(i,j)
        
        
        

while True:
    canvas = []
    startup(canvas)
