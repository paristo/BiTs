"""
this code simulate board game
By Tomas Paris and Ben Goldman
"""
from Tkinter import *

# this initializes the window
window = Tk()
window.geometry('500x300')
window.title("Go (game)")
window.config(bg="white")
window.iconbitmap("board.ico")
window.tk.call("tk", "scaling", 1)
window.state('zoomed')

rule1 = "1. Black moves first"
rule2 = "2. Empty spaces are called Breaths"
rule3 = "3. Stones without adjacent Breaths die"
rule4 = "4. Adjacent stones of the same color share Breaths"
korule = "ko rule: moves that revert the game to its state one turn ago cannot be made"
rule5 = "5. When stones of one color surround an empty space, that space becomes land"
rule6 = "6. The final score is the total land controlled by a color minus the number of dead stones of that color"
rule7 = "7. The game ends when both sides agree to end the game, when one side surrenders, or after two consecutive passes"

mainlist = []


def mainmenu():
    close()

    # this draws a backdrop for the main menu
    backdrop = Canvas(window, width=900, height=1000, bg="#DEB887", bd=5, relief=RAISED)
    backdrop.place(relx=0.5, rely=0.5, anchor=CENTER)

    # this is the welcome message
    welcome = Label(window, text="Welcome to Go!", font=("helvetica", 100), bg="#DEB887")
    welcome.place(relx=0.5, rely=0.2, anchor=CENTER)

    # this is the new game button, it activates the start function
    new = Button(window, text="NEW GAME", font=("helvetica", 50), bd=5, command=start, height=2, width=15, cursor="hand2")
    new.place(relx=0.5, rely=0.45, anchor=CENTER)

    # this is the rules button, it activates the explain function
    rules = Button(window, text="RULES", font=("helvetica", 50), bd=5, command=explain, height=2, width=15, cursor="hand2")
    rules.place(relx=0.5, rely=0.7, anchor=CENTER)

    attributes = [backdrop, welcome, new, rules]
    mainlist.extend(attributes)


def close():
    for item in mainlist:
        item.destroy()
    del mainlist[:]


# this function is junk, don't worry about it (it opens a window and displays the rules)
def explain():
    close()

    instructions = Message(window, text="Rules of Go:", font=("helvetica", 100), width=1000, bg="white")
    instructions.place(relx=0.5, rely=0.07, anchor=CENTER)
    rule_1 = Message(window, text=rule1, font=("helvetica", 50), width=800, justify=LEFT, bg="white")
    rule_1.place(relx=0.02, rely=0.12)
    rule_2 = Message(window, text=rule2, font=("helvetica", 50), width=800, justify=LEFT, bg="white")
    rule_2.place(relx=0.02, rely=0.22)
    rule_3 = Message(window, text=rule3, font=("helvetica", 50), width=800, justify=LEFT, bg="white")
    rule_3.place(relx=0.02, rely=0.32)
    rule_4 = Message(window, text=rule4, font=("helvetica", 50), width=800, justify=LEFT, bg="white")
    rule_4.place(relx=0.02, rely=0.452)
    rule_ko = Message(window, text=korule, font=("helvetica", 50), width=800, justify=LEFT, bg="white")
    rule_ko.place(relx=0.02, rely=0.6)
    rule_5 = Message(window, text=rule5, font=("helvetica", 50), width=800, justify=LEFT, bg="white")
    rule_5.place(relx=0.5, rely=0.12)
    rule_6 = Message(window, text=rule6, font=("helvetica", 50), width=800, justify=LEFT, bg="white")
    rule_6.place(relx=0.5, rely=0.32)
    rule_7 = Message(window, text=rule7, font=("helvetica", 50), width=800, justify=LEFT, bg="white")
    rule_7.place(relx=0.5, rely=0.52)

    mainreturn = Button(window, text="RETURN", font=("helvetica", 50), bd=5, command=mainmenu, height=2, width=15, cursor="hand2")
    mainreturn.place(relx=0.5, rely=0.85, anchor=CENTER)

    attributes = [instructions, rule_1, rule_2, rule_3, rule_4, rule_ko, rule_5, rule_6, rule_7, mainreturn]
    mainlist.extend(attributes)


def start():
    close()
    # this function just opens up the Game class, since buttons can't directly open a class
    gameplay = Game()


class Game:

    def __init__(self):
        # fills the left side of the window
        self.blackbumber = Canvas(window, width=350, height=900, bg="grey", bd=5, relief=RAISED)
        self.blackbumber.place(relx=0.11, rely=0.5, anchor=CENTER)

        self.blackbumber.create_text(160, 80, text="Black:", font=("helvetica", 80), width=300)
        self.blackbumber.create_text(180, 250, text="Pieces Captured:", font=("helvetica", 40), width=400)
        self.blackbumber.create_text(90, 600, text='Score:', font=("helvetica", 40), width=300)

        self.turn = "Black"
        self.blackstate = "(Moving)"
        self.currentblack = self.blackbumber.create_text(130, 140, text=self.blackstate, font=("helvetica", 40), width=300)

        self.blackscore = "TBD"
        self.blackscored = self.blackbumber.create_text(170, 760, text=self.blackscore, font=("helvetica", 120), width=300)

        # creates the table
        self.total = 0
        self.totalmove = StringVar()
        self.totalmove.set("Total Moves: " + str(self.total))
        self.counter = Message(window, textvariable=self.totalmove, font=("helvetica", 40), width=300, justify=RIGHT, bg="white")
        self.counter.place(relx=0.5, rely=0.03, anchor=CENTER)

        # this creates the board
        self.board = Canvas(window, width=1000, height=1000, bg="#DEB887", bd=5, relief=RAISED)
        self.board.place(relx=0.5, rely=0.5, anchor=CENTER)

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
                self.intersect[dot_x - 1][dot_y - 1] = self.board.create_oval(((100 * dot_x) - 40), ((100 * dot_y) - 40),
                                                                              ((100 * dot_x) + 40), ((100 * dot_y) + 40),
                                                                              fill="", outline="")

        self.last_pas = None

        # fils the right side of the window
        self.whitebumber = Canvas(window, width=350, height=900, bg="grey", bd=5, relief=RAISED)
        self.whitebumber.place(relx=0.89, rely=0.5, anchor=CENTER)

        self.whitebumber.create_text(160, 80, text="White:", font=("helvetica", 80), width=300)
        self.whitebumber.create_text(180, 250, text="Pieces Captured:", font=("helvetica", 40), width=400)
        self.whitebumber.create_text(90, 600, text='Score:', font=("helvetica", 40), width=300)

        self.whitestate = "(Waiting)"
        self.currentwhite = self.whitebumber.create_text(130, 140, text=self.whitestate, font=("helvetica", 40), width=300)

        self.whitescore = "TBD"
        self.whitescored = self.whitebumber.create_text(170, 760, text=self.whitescore, font=("helvetica", 120), width=300)

        self.unfreeze()

    # this function adds buttons
    def unfreeze(self):
        # this makes each stone a button
        for dot_x in range(1, 10):
            for dot_y in range(1, 10):
                self.board.tag_bind(self.intersect[dot_x-1][dot_y-1], "<Button-1>", self.move)

        self.board.config(cursor="tcross")  # this sets a new cursor for the board

        self.menubut = Button(window, text="OPTIONS", font=("helvetica", 40), bd=5, width=10, command=self.menu)
        self.menubut.place(relx=0.92, rely=0.05, anchor=CENTER)
        self.menubut.config(cursor="hand2")

        # this makes the pass button
        self.turn_pass = Button(window, text="PASS", font=("helvetica", 20), bd=5, width=15, command=self.pas)
        self.turn_pass.place(relx=0.38, rely=0.965, anchor=CENTER)
        self.turn_pass.config(cursor="hand2")

        # this makes the surrender button
        self.surrend_butn = Button(window, text="SURRENDER", font=("helvetica", 20), bd=5, width=15, command=self.surrender)
        self.surrend_butn.place(relx=0.5, rely=0.965, anchor=CENTER)
        self.surrend_butn.config(cursor="hand2")

        # this makes the end game button
        self.stop_game = Button(window, text="PROPOSE END", font=("helvetica", 20), bd=5, width=15, command=self.want_end)
        self.stop_game.place(relx=0.62, rely=0.965, anchor=CENTER)
        self.stop_game.config(cursor="hand2")

    def menu(self):
        # this chunk displays the request
        self.menuback = Canvas(window, width=400, height=600, bg="grey", bd=5, relief=RAISED)
        self.menuback.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.menuback.create_text(200, 100, text="MENU", font=("helvetica", 100), width=800, justify=CENTER)

        newgame = Button(self.menuback, text="New Game", font=("helvetica", 40), bd=5, width=9, command=start)
        newgame.place(relx=0.5, rely=0.4, anchor=CENTER)
        newgame.config(cursor="hand2")

        rulebut = Button(self.menuback, text="Rules", font=("helvetica", 40), bd=5, width=9, command=self.rulepopup)
        rulebut.place(relx=0.5, rely=0.6, anchor=CENTER)
        rulebut.config(cursor="hand2")

        exitbut = Button(self.menuback, text="Close", font=("helvetica", 50), bd=5, width=11, command=self.closemenu)
        exitbut.place(relx=0.5, rely=0.85, anchor=CENTER)
        exitbut.config(cursor="hand2")

        self.freeze()
        attributes = [self.blackbumber, self.counter, self.board, self.whitebumber, self.menuback]
        mainlist.extend(attributes)

    def closerule(self):
        self.ruleback.destroy()

    def closemenu(self):
        self.menuback.destroy()
        self.unfreeze()

    def rulepopup(self):
        self.ruleback = Canvas(window, width=600, height=800, bg="grey", bd=5, relief=RAISED)
        self.ruleback.place(relx=0.5, rely=0.5, anchor=CENTER)

        self.ruleback.create_text(300, 50, text="Rules of Go:", font=("helvetica", 50), width=1000)
        self.ruleback.create_text(150, 120, text=rule1, font=("helvetica", 25), width=250)
        self.ruleback.create_text(150, 180, text=rule2, font=("helvetica", 25), width=250)
        self.ruleback.create_text(150, 260, text=rule3, font=("helvetica", 25), width=250)
        self.ruleback.create_text(150, 350, text=rule4, font=("helvetica", 25), width=250)
        self.ruleback.create_text(150, 470, text=korule, font=("helvetica", 25), width=250)
        self.ruleback.create_text(450, 160, text=rule5, font=("helvetica", 25), width=250)
        self.ruleback.create_text(450, 320, text=rule6, font=("helvetica", 25), width=250)
        self.ruleback.create_text(450, 520, text=rule7, font=("helvetica", 25), width=250)

        norule = Button(self.ruleback, text="Close", font=("helvetica", 40), bd=5, width=16, height=1, command=self.closerule, cursor="hand2")
        norule.place(relx=0.5, rely=0.88, anchor=CENTER)

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
            self.blackstate = "(Waiting)"
            self.whitestate = "(Moving)"
            self.turn = "White"
        else:
            self.blackstate = "(Moving)"
            self.whitestate = "(Waiting)"
            self.turn = "Black"

        # this chunk increases the total moves, and deletes the pass message, if present
        self.total += 1
        if (self.total - 1) == self.last_pas:
            self.board.delete(self.pasmesg)

        # this chunk updates the displays on the board
        self.totalmove.set("Total Moves: " + str(self.total))
        self.blackbumber.itemconfig(self.currentblack, text=self.blackstate)
        self.whitebumber.itemconfig(self.currentwhite, text=self.whitestate)

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
        if self.turn == "Black":
            self.blackstate = "Winner!"
            self.blackscore = "Default"
            self.whitestate = "Loser"
            self.whitescore = "Forfeit"
        else:
            self.whitestate = "Winner!"
            self.whitescore = "Default"
            self.blackstate = "Loser"
            self.blackscore = "Forfeit"
        self.blackbumber.itemconfig(self.blackscored, font=("helvetica", 70))
        self.whitebumber.itemconfig(self.whitescored, font=("helvetica", 70))
        self.freeze()
        self.endgame()

    def freeze(self):
        # this chunk destroys unnecessary buttons
        self.turn_pass.destroy()
        self.surrend_butn.destroy()
        self.stop_game.destroy()
        self.menubut.destroy()

        self.board.config(cursor="arrow")

        # this chunk freezes the board and displays the score
        for dot_x in range(1, 10):
            for dot_y in range(1, 10):
                self.board.tag_unbind(self.intersect[dot_x - 1][dot_y - 1], "<Button-1>")

    # this function shows the final score
    def endgame(self):
        self.blackbumber.itemconfig(self.currentblack, text=self.blackstate)
        self.whitebumber.itemconfig(self.currentwhite, text=self.whitestate)
        self.blackbumber.itemconfig(self.blackscored, text=self.blackscore)
        self.whitebumber.itemconfig(self.whitescored, text=self.whitescore)

        newgame = Button(window, text="New Game", font=("helvetica", 20), bd=5, width=9, command=start)
        newgame.place(relx=0.5, rely=0.965, anchor=CENTER)
        newgame.config(cursor="hand2")

        attributes = [self.blackbumber, self.counter, self.board, self.whitebumber, newgame]
        mainlist.extend(attributes)

    # this function denies a request for endgame
    def deny(self):
        self.unfreeze()
        self.request.destroy()

    # this function accepts a request for endgame
    def accept(self):
        self.unfreeze()
        self.request.destroy()
        self.findscore()

    # this function proposes to end the game
    def want_end(self):
        # this chunk displays the request
        self.request = Canvas(window, width=600, height=400, bg="grey", bd=5, relief=RAISED)
        self.request.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.request.create_text(300, 100, text=self.turn + " requests end!", font=("helvetica", 50), width=800, justify=CENTER)

        ybut = Button(self.request, text="YES", font=("helvetica", 40), bd=5, width=9, command=self.accept)
        nbut = Button(self.request, text="NO", font=("helvetica", 40), bd=5, width=9, command=self.deny)
        ybut.place(relx=0.3, rely=0.6, anchor=CENTER)
        ybut.config(cursor="hand2")
        nbut.place(relx=0.7, rely=0.6, anchor=CENTER)
        nbut.config(cursor="hand2")
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


mainmenu()
mainloop()
