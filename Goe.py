"""
this code simulate board game

By Tomas Paris and Ben Goldman
"""
import sys
from Tkinter import *
master = Tk()


def menu():
    # this is the welcome message
    welcome = Label(master, text="Welcome to Goe!", font=("helvetica", 50))
    welcome.pack()

    # this is the new game button, it activates the start function
    new = Button(master, text="NEW GAME", font=("helvetica", 30), command=start)
    new.pack(fill=BOTH, expand=1)

    # this is the rules button, it activates the explain function
    rules = Button(master, text="RULES", font=("helvetica", 30), command=explain)
    rules.pack(fill=BOTH, expand=1)


# this function is junk, don't worry about it
def explain():
    instructions = Toplevel()
    instructions.title("Instructions")
    instructions.grid()

    rule1 = "1. Black moves first"
    rule2 = "2. Empty spaces are called Breaths"
    rule3 = "3. Stones without adjacent Breaths die"
    rule4 = "4. Adjacent stones of the same color share Breaths"
    korule = "ko rule: moves that revert the game to its state one turn ago cannot be made"
    rule5 = "5. When stones of one color surround an empty space, that space becomes land"
    rule6 = "6. The final score is the total land controlled by a color minus the number of dead stones of that color"
    rule7 = "7. The game ends when both sides agree to end the game, when one side surrenders, or after 2 consecutive passes"

    rule_1 = Message(instructions, text=rule1, font=("helvetica", 15), width=200)
    rule_1.grid(row=0, column=0)
    rule_2 = Message(instructions, text=rule2, font=("helvetica", 15), width=200)
    rule_2.grid(row=1, column=0)
    rule_3 = Message(instructions, text=rule3, font=("helvetica", 15), width=200)
    rule_3.grid(row=2, column=0)
    rule_4 = Message(instructions, text=rule4, font=("helvetica", 15), width=200)
    rule_4.grid(row=3, column=0)
    rule_ko = Message(instructions, text=korule, font=("helvetica", 15), width=200)
    rule_ko.grid(row=4, column=0)
    rule_5 = Message(instructions, text=rule5, font=("helvetica", 15), width=200)
    rule_5.grid(row=0, rowspan=2, column=1)
    rule_6 = Message(instructions, text=rule6, font=("helvetica", 15), width=200)
    rule_6.grid(row=2, rowspan=2, column=1)
    rule_7 = Message(instructions, text=rule7, font=("helvetica", 15), width=200)
    rule_7.grid(row=4, rowspan=2, column=1)


def start():
    # this function just opens up the Game class, since buttons can't directly open a class
    gameplay = Game()


class Game:

    def __init__(self):
        self.table = Toplevel()                 # this creates a new window
        self.table.title("Tabletop")
        self.table.grid()
        self.hand = "left_ptr"
        self.table.config(cursor=self.hand)     # this sets a new cursor for the window

        # this chunk displays the current player in the top left corner
        self.turn = "Black's Turn:"
        self.playermove = StringVar()
        self.playermove.set(self.turn)
        self.player = Message(self.table, textvariable=self.playermove, font=("helvetica", 20), width=300, justify=LEFT)
        self.player.grid(row=0, column=0)

        # this chunk is junk don't worry about it
        self.title = Message(self.table, text="Goe", font=("helvetica", 30), width=300, justify=CENTER)
        self.title.grid(row=0, column=1)

        # this chunk displays the total moves in the top right corner
        self.total = 0
        self.totalmove = StringVar()
        self.totalmove.set("Total Moves: " + str(self.total))
        self.counter = Message(self.table, textvariable=self.totalmove, font=("helvetica", 20), width=300, justify=RIGHT)
        self.counter.grid(row=0, column=2)

        # this creates the board
        self.board = Canvas(self.table, width=1000, height=1000, bg="#DEB887")
        self.board.grid(row=1, columnspan=3)

        # this creates the grid of lines on the board
        for line in range(1, 10):
            self.board.create_line(100, (100 * line), 900, (100 * line))
            self.board.create_line((100 * line), 100, (100 * line), 900)

        # this array represents the places for stones
        self.places = [[None for x in range(9)] for x in range(9)]

        # this creates the pieces on the board (they start out invisible)
        self.intersect = [[None for x in range(9)] for x in range(9)]
        for dot_x in range(1, 10):
            for dot_y in range(1, 10):
                self.intersect[dot_x-1][dot_y-1] = self.board.create_oval(((100*dot_x)-40), ((100*dot_y)-40),
                                                                          ((100*dot_x)+40), ((100*dot_y)+40), fill="",
                                                                          outline="")
                self.board.tag_bind(self.intersect[dot_x-1][dot_y-1], "<Button-1>", self.move)

        # this makes the pass button
        self.turn_pass = Button(self.table, text="PASS", font=("helvetica", 20), command=self.play)
        self.turn_pass.grid(row=2, column=0)

        # this makes the surrender button
        self.surrend_butn = Button(self.table, text="SURRENDER", font=("helvetica", 20), command=self.surrender)
        self.surrend_butn.grid(row=2, column=1)

        # this makes the end game button
        self.stop_game = Button(self.table, text="PROPOSE END", font=("helvetica", 20), command=self.endgame)
        self.stop_game.grid(row=2, column=2)

    # this function places a stone
    def move(self, event):
        x = (event.x - 50) // 100
        y = (event.y - 50) // 100
        if not self.places[x][y]:
            if self.turn == "Black's Turn:":
                self.board.itemconfig(self.intersect[x][y], fill="black")
                self.places[x][y] = Stone(x, y, "B")                        # this calls the stone class
            else:
                self.board.itemconfig(self.intersect[x][y], fill="white")
                self.places[x][y] = Stone(x, y, "W")                        # this calls the stone class
            self.play()

    # this function changes whose turn it is
    def play(self):
        if self.turn == "Black's Turn:":
            self.turn = "White's Turn:"
            self.hand = "right_ptr"
        else:
            self.turn = "Black's Turn:"
            self.hand = "left_ptr"
        self.total += 1
        self.totalmove.set("Total Moves: " + str(self.total))
        self.playermove.set(self.turn)
        self.table.config(cursor=self.hand)

    # this function ends the game, whoever pushes it loses
    def surrender(self):
        print "e"

    # this function proposes to end the game
    def endgame(self):
        print "e"


class Stone:

    def __init__(self, x, y, c):
        self.x_cord = x
        self.y_cord = y
        self.color = c

    # this function checks the life of a piece
    def life(self):
        print "e"

    # this function checks the effect of a piece
    def effect(self):
        print "e"
        
    # this  function reverts a stone to an empty space
    def destroy(self):
        print "e"


menu()
mainloop()
