"""
This is the GUI file for BiTs
"""
from Tkinter import *
from tkColorChooser import askcolor
master = Tk()
RC = 200
BOX = 1000


class Pixel:
    def __init__(self, r, c):
        self.row = r
        self.col = c
        self.board = e.create_rectangle(c*width, r*height, (c+1)*width, (r+1)*height, fill="white")

    def filler(self):
        color = askcolor()
        e.itemconfigure(self.board, fill=color)


def startup():
    for i in range(RC):
        for j in range(RC):
            pxl[i][j] = Pixel(i, j)


def eyedrop(event):
    i = event.x//width
    j = event.y//height
    pxl[i][j].filler()

e = Canvas(master, width=BOX, height=BOX, bg="white")
e.bind("<Button-1>", eyedrop)
e.pack()
width = BOX / RC
height = BOX / RC
pxl = [[None for _ in range(RC)]for _ in range(RC)]
startup()
mainloop()
