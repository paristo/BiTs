"""
this code simulate board game
By Tomas Paris and Ben Goldman
"""
from Tkinter import *
master = Tk()
master.geometry('500x300')
master.title("menu")
master.config(bg="white")
master.iconbitmap("menu.ico")
master.tk.call("tk", "scaling", 1)


def menu():
    # this is the welcome message
    welcome = Label(master, text="Welcome to Go!", font=("helvetica", 50), bg="white")
    welcome.pack()

    entry = Frame(height=50, width=300, bg="white")
    entry.pack(expand=1)

    # this is the new game button, it activates the start function
    new = Button(entry, text="NEW GAME", font=("helvetica", 30), bd=5, command=start)
    new.pack(fill=BOTH, expand=1)
    new.config(cursor="hand2")

    # this is the rules button, it activates the explain function
    rules = Button(entry, text="RULES", font=("helvetica", 30), bd=5, command=explain)
    rules.pack(fill=BOTH, expand=1, pady=20)
    rules.config(cursor="hand2")


# this function is junk, don't worry about it (it opens a window and displays the rules)
def explain():
    instructions = Toplevel()
    instructions.title("Instructions")
    instructions.config(bg="white")
    instructions.iconbitmap("book.ico")
    instructions.grid()
    instructions.tk.call("tk", "scaling", 1)

    rule1 = "1. Black moves first"
    rule2 = "2. Empty spaces are called Breaths"
    rule3 = "3. Stones without adjacent Breaths die"
    rule4 = "4. Adjacent stones of the same color share Breaths"
    korule = "ko rule: moves that revert the game to its state one turn ago cannot be made"
    rule5 = "5. When stones of one color surround an empty space, that space becomes land"
    rule6 = "6. The final score is the total land controlled by a color minus the number of dead stones of that color"
    rule7 = "7. The game ends when both sides agree to end the game, when one side surrenders, or after two consecutive passes"

    rule_1 = Message(instructions, text=rule1, font=("helvetica", 15), width=200, justify=LEFT, bg="white")
    rule_1.grid(row=0, column=0)
    rule_2 = Message(instructions, text=rule2, font=("helvetica", 15), width=200, justify=LEFT, bg="white")
    rule_2.grid(row=1, column=0)
    rule_3 = Message(instructions, text=rule3, font=("helvetica", 15), width=200, justify=LEFT, bg="white")
    rule_3.grid(row=2, column=0)
    rule_4 = Message(instructions, text=rule4, font=("helvetica", 15), width=200, justify=LEFT, bg="white")
    rule_4.grid(row=3, column=0)
    rule_ko = Message(instructions, text=korule, font=("helvetica", 15), width=200, justify=LEFT, bg="white")
    rule_ko.grid(row=4, column=0)
    rule_5 = Message(instructions, text=rule5, font=("helvetica", 15), width=200, justify=LEFT, bg="white")
    rule_5.grid(row=0, rowspan=2, column=1)
    rule_6 = Message(instructions, text=rule6, font=("helvetica", 15), width=200, justify=LEFT, bg="white")
    rule_6.grid(row=2, rowspan=2, column=1)
    rule_7 = Message(instructions, text=rule7, font=("helvetica", 15), width=200, justify=LEFT, bg="white")
    rule_7.grid(row=4, rowspan=2, column=1)


def start():
    # this function just opens up the Game class, since buttons can't directly open a class
    gameplay = Game()


class Game:

    def __init__(self):
        self.table = Toplevel()                 # this creates a new window
        self.table.title("Tabletop")
        self.table.config(bg="white")
        self.table.iconbitmap("board.ico")
        self.table.tk.call("tk", "scaling", 1)
        self.table.state('zoomed')

        # this chunk displays the current player in the top left corner
        self.turn = "Black"
        self.playermove = StringVar()
        self.playermove.set(self.turn+"'s Turn:")
        self.player = Message(self.table, textvariable=self.playermove, font=("helvetica", 20), width=300, justify=LEFT, bg="white")
        self.player.grid(row=0, column=0)

        # this chunk is junk don't worry about it (it displays some text above the board)
        self.title = Message(self.table, text="Go", font=("helvetica", 30), width=300, justify=CENTER, bg="white")
        self.title.grid(row=0, column=1)

        # this chunk displays the total moves in the top right corner
        self.total = 0
        self.totalmove = StringVar()
        self.totalmove.set("Total Moves: " + str(self.total))
        self.counter = Message(self.table, textvariable=self.totalmove, font=("helvetica", 20), width=300, justify=RIGHT, bg="white")
        self.counter.grid(row=0, column=2)

        # this creates the board
        self.board = Canvas(self.table, width=1000, height=1000, bg="#DEB887", bd=5, relief=RAISED)
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
        self.unfreeze()

    # this function adds buttons
    def unfreeze(self):
        # this makes each stone a button
        for dot_x in range(1, 10):
            for dot_y in range(1, 10):
                self.board.tag_bind(self.intersect[dot_x-1][dot_y-1], "<Button-1>", self.move)

        self.board.config(cursor="tcross")  # this sets a new cursor for the board

        # this makes the pass button
        self.turn_pass = Button(self.table, text="PASS", font=("helvetica", 20), bd=5, command=self.pas)
        self.last_pas = None
        self.turn_pass.grid(row=2, column=0)
        self.turn_pass.config(cursor="hand2")

        # this makes the surrender button
        self.surrend_butn = Button(self.table, text="SURRENDER", font=("helvetica", 20), bd=5, command=self.surrender)
        self.surrend_butn.grid(row=2, column=1)
        self.surrend_butn.config(cursor="hand2")

        # this makes the end game button
        self.stop_game = Button(self.table, text="PROPOSE END", font=("helvetica", 20), bd=5, command=self.want_end)
        self.stop_game.grid(row=2, column=2)
        self.stop_game.config(cursor="hand2")

    # this function places a stone
    def move(self, event):
        x = (event.x - 50) // 100
        y = (event.y - 50) // 100
        if not self.places[x][y]:
            if self.turn == "Black":
                self.board.itemconfig(self.intersect[x][y], fill="black")
                self.places[x][y] = Stone(x, y, "B")                        # this calls the stone class
            else:
                self.board.itemconfig(self.intersect[x][y], fill="white")
                self.places[x][y] = Stone(x, y, "W")                        # this calls the stone class
            self.play()

    # this function changes whose turn it is
    def play(self):
        if self.turn == "Black":
            self.turn = "White"
        else:
            self.turn = "Black"

        # this chunk increases the total moves, and deletes the pass message, if present
        self.total += 1
        if (self.total - 1) == self.last_pas:
            self.board.delete(self.pasmesg)

        # this chunk updates the displays on the board
        self.totalmove.set("Total Moves: " + str(self.total))
        self.playermove.set(self.turn+"'s Turn:")

    # this function skips the players turn, or ends the game after two consecutive passes
    def pas(self):
        if self.total == self.last_pas:
            self.findscore()
        else:
            self.last_pas = self.total + 1
            self.pasmesg = self.board.create_text(500, 35, text=self.turn+" passed!", font=("helvetica", 25), width=300)
            self.play()

    # this function ends the game, whoever pushes it loses
    def surrender(self):
        # this chunk sets the scores
        self.play()
        self.winner = self.turn
        if self.turn == "Black":
            self.blackscore = "Default"
            self.whitescore = "Forfeit"
        else:
            self.whitescore = "Default"
            self.blackscore = "Forfeit"
        self.freeze()
        self.endgame()

    def freeze(self):
        # this chunk destroys unnecessary buttons
        self.turn_pass.destroy()
        self.surrend_butn.destroy()
        self.stop_game.destroy()

        self.board.config(cursor="arrow")

        # this chunk freezes the board and displays the score
        for dot_x in range(1, 10):
            for dot_y in range(1, 10):
                self.board.tag_unbind(self.intersect[dot_x - 1][dot_y - 1], "<Button-1>")

    def endgame(self):
        # this adds a button to bring up the score
        self.popbutn = Button(self.table, text="View Score", font=("helvetica", 20), bd=5, command=self.finalpopup)
        self.popbutn.grid(row=2, column=1)
        self.popbutn.config(cursor="hand2")
        self.finalpopup()

    # this function shows the final score
    def finalpopup(self):
        popup = Toplevel()
        popup.title("Score")
        popup.iconbitmap("score.ico")
        popup.grid()
        popup.tk.call("tk", "scaling", 1)

        # this chunk displays the popup text
        popwin = Message(popup, text=self.winner + " Wins!", font=("helvetica", 80), width=600, justify=CENTER)
        leftscore = Message(popup, text="Black Score:", font=("helvetica", 25), width=600, justify=CENTER)
        rightscore = Message(popup, text="White Score:", font=("helvetica", 25), width=600, justify=CENTER)
        finalblack = Message(popup, text=self.blackscore, font=("helvetica", 50), width=600, justify=CENTER)
        finalwhite = Message(popup, text=self.whitescore, font=("helvetica", 50), width=600, justify=CENTER)
        popwin.grid(row=0, columnspan=2)
        leftscore.grid(row=1, column=0)
        rightscore.grid(row=1, column=1)
        finalblack.grid(row=2, column=0)
        finalwhite.grid(row=2, column=1)

    # this function denies a request for endgame
    def deny(self):
        self.unfreeze()
        self.board.delete(self.request)
        self.board.delete(self.reqtitle)
        self.ybut.destroy()
        self.nbut.destroy()

    # this function accepts a request for endgame
    def accept(self):
        self.unfreeze()
        self.board.delete(self.request)
        self.board.delete(self.reqtitle)
        self.ybut.destroy()
        self.nbut.destroy()
        self.findscore()

    # this function proposes to end the game
    def want_end(self):
        # this chunk displays the request
        self.request = self.board.create_rectangle(200, 250, 800, 650, fill="grey", outline="white")
        self.reqtitle = self.board.create_text(500, 350, text=self.turn + " requests end!", font=("helvetica", 50), width=800)
        self.ybut = Button(self.board, text="YES", font=("helvetica", 40), bd=5, command=self.accept)
        self.nbut = Button(self.board, text="NO", font=("helvetica", 40), bd=5, command=self.deny)
        self.ybut.place(relx=0.325, rely=0.447, x=.5, y=.5)
        self.ybut.config(cursor="hand2")
        self.nbut.place(relx=0.535, rely=0.447, x=.5, y=.5)
        self.nbut.config(cursor="hand2")
        self.play()
        self.freeze()

    def findscore(self):
        print "e"
        self.freeze()
        self.endgame()


class Stone:

    def __init__(self, x, y, c):
        self.x_cord = x
        self.y_cord = y
        self.color = c

    # this function checks the life of a piece
    def life(self):
        print "e"

    # this function checks the effect of a piece on other nearby pieces
    def effect(self):
        print "e"

    # this  function reverts a stone to an empty space
    def destroy(self):
        print "e"

class Shape:

    def __init__(self):
        print "e"


menu()
mainloop()
