"""
This is the GUI file for BiTs
"""
from Tkinter import *
import time
from tkColorChooser import askcolor
master = Tk()
RC = 200
BOX = 1000
LOCK = False


class Pixel:
    def __init__(self, r, c):
        self.row = r
        self.col = c
        self.board = e.create_rectangle(c*width, r*height, (c+1)*width, (r+1)*height, fill="white", outline="")

    def filler(self):
        global LOCK
        color = askcolor()
        e.itemconfigure(self.board, fill=color[1])
        LOCK = True


def startup():
    for i in range(RC):
        for j in range(RC):
            pxl[i][j] = Pixel(i, j)


def eyedrop(event):
    global LOCK
    if LOCK:
        time.sleep(5)
        LOCK = False
    j = event.x//width
    i = event.y//height
    pxl[i][j].filler()


e = Canvas(master, width=BOX, height=BOX, bg="white")
e.bind("<Button-1>", eyedrop)
e.pack()

width = BOX / RC
height = BOX / RC
pxl = [[None for _ in range(RC)]for _ in range(RC)]

startup()
mainloop()
