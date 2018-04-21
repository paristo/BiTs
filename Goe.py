"""
this code simulate board game
By Tomas Paris and Ben Goldman
"""
from Tkinter import *

# this initializes the window
master = Tk()
master.geometry('500x300')
master.title("Go (game)")
master.config(bg="white")
master.iconbitmap("board.ico")
master.call("tk", "scaling", 1)
# master.attributes('-fullscreen', True)
master.state('zoomed')
H = master.winfo_screenheight() - (master.winfo_screenheight() * 0.1)
W = master.winfo_screenwidth() - (master.winfo_screenwidth() * 0.02)
window = Frame(height=H, width=W, bg="white")
window.place(relx=0.5, rely=0.5, anchor=CENTER)

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
    backdrop = Canvas(window, width=W/2.0, height=H/1.2, bg="#DEB887", bd=5, relief=RIDGE)
    backdrop.place(relx=0.5, rely=0.5, anchor=CENTER)

    # this is the welcome message
    welcome = Label(window, text="Welcome to Go!", font=("helvetica", int(W//18.2)), bg="#DEB887")
    welcome.place(relx=0.5, rely=0.2, anchor=CENTER)

    # this is the new game button, it activates the start function
    new = Button(window, text="NEW GAME", font=("helvetica", int(W//36.4)), bd=5, command=start, height=int(H//405), width=int(W//121), cursor="hand2")
    new.place(relx=0.5, rely=0.45, anchor=CENTER)

    # this is the rules button, it activates the explain function
    rules = Button(window, text="RULES", font=("helvetica", int(W//36.4)), bd=5, command=explain, height=int(H//405), width=int(W//121), cursor="hand2")
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

    instructions = Message(window, text="Rules of Go:", font=("helvetica", int(W//18.2)), width=int(W//1.8), bg="white")
    instructions.place(relx=0.5, rely=0.07, anchor=CENTER)
    rule_1 = Message(window, text=rule1, font=("helvetica", int(W//36.4)), width=int(W//2.3), justify=LEFT, bg="white")
    rule_1.place(relx=0.02, rely=0.12)
    rule_2 = Message(window, text=rule2, font=("helvetica", int(W//36.4)), width=int(W//2.3), justify=LEFT, bg="white")
    rule_2.place(relx=0.02, rely=0.22)
    rule_3 = Message(window, text=rule3, font=("helvetica", int(W//36.4)), width=int(W//2.3), justify=LEFT, bg="white")
    rule_3.place(relx=0.02, rely=0.32)
    rule_4 = Message(window, text=rule4, font=("helvetica", int(W//36.4)), width=int(W//2.3), justify=LEFT, bg="white")
    rule_4.place(relx=0.02, rely=0.452)
    rule_ko = Message(window, text=korule, font=("helvetica", int(W//36.4)), width=int(W//2.3), justify=LEFT, bg="white")
    rule_ko.place(relx=0.02, rely=0.6)
    rule_5 = Message(window, text=rule5, font=("helvetica", int(W//36.4)), width=int(W//2.3), justify=LEFT, bg="white")
    rule_5.place(relx=0.5, rely=0.12)
    rule_6 = Message(window, text=rule6, font=("helvetica", int(W//36.4)), width=int(W//2.3), justify=LEFT, bg="white")
    rule_6.place(relx=0.5, rely=0.32)
    rule_7 = Message(window, text=rule7, font=("helvetica", int(W//36.4)), width=int(W//2.3), justify=LEFT, bg="white")
    rule_7.place(relx=0.5, rely=0.52)

    mainreturn = Button(window, text="RETURN", font=("helvetica", int(W//36.4)), bd=5, command=mainmenu, height=int(H//405), width=int(W//121), cursor="hand2")
    mainreturn.place(relx=0.5, rely=0.85, anchor=CENTER)

    attributes = [instructions, rule_1, rule_2, rule_3, rule_4, rule_ko, rule_5, rule_6, rule_7, mainreturn]
    mainlist.extend(attributes)


def start():
    close()
    # this function just opens up the Game class, since buttons can't directly open a class
    gameplay = Game()


class Game:

    def __init__(self):
        BW = int(W//5.2)    # BW stands for bumper width
        BH = int(H//1.3)    # BH stands for bumper height
        # fills the left side of the window
        self.blackbumber = Canvas(window, width=BW, height=BH, bg="grey", bd=5, relief=GROOVE)
        self.blackbumber.place(relx=0.11, rely=0.5, anchor=CENTER)

        self.blackbumber.create_text(int(BW//2.1), int(BH//11.2), text="Black:", font=("helvetica", int(W//22.8)), width=int(W//6))
        self.blackbumber.create_text(int(BW//1.9), int(BH//3.6), text="Pieces Captured:", font=("helvetica", int(W//45.6)), width=int(W//4.5))
        self.blackbumber.create_text(int(BW//3.8), int(BH//1.5), text='Score:', font=("helvetica", int(W//45.6)), width=int(W//6))

        self.turn = "Black"
        self.blackstate = "(Moving)"
        self.currentblack = self.blackbumber.create_text(int(BW//2.6), int(BH//6.4), text=self.blackstate, font=("helvetica", int(W//45.6)), width=int(W//6))

        self.blackscore = "TBD"
        self.blackscored = self.blackbumber.create_text(int(BW//2), int(BH//1.2), text=self.blackscore, font=("helvetica", int(W//15.2)), width=int(W//6))

        # fils the right side of the window
        self.whitebumber = Canvas(window, width=BW, height=BH, bg="grey", bd=5, relief=GROOVE)
        self.whitebumber.place(relx=0.89, rely=0.5, anchor=CENTER)

        self.whitebumber.create_text(int(BW//2.1), int(BH//11.2), text="White:", font=("helvetica", int(W//22.8)), width=int(W//6))
        self.whitebumber.create_text(int(BW//1.9), int(BH//3.6), text="Pieces Captured:", font=("helvetica", int(W//45.6)), width=int(W//4.5))
        self.whitebumber.create_text(int(BW//3.8), int(BH//1.5), text='Score:', font=("helvetica", int(W//45.6)), width=int(W//6))

        self.whitestate = "(Waiting)"
        self.currentwhite = self.whitebumber.create_text(int(BW//2.6), int(BH//6.4), text=self.whitestate, font=("helvetica", int(W//45.6)), width=int(W//6))

        self.whitescore = "TBD"
        self.whitescored = self.whitebumber.create_text(int(BW//2), int(BH//1.2), text=self.whitescore, font=("helvetica", int(W//15.2)), width=int(W//6))

        # creates the table
        self.total = 0
        self.totalmove = StringVar()
        self.totalmove.set("Total Moves: " + str(self.total))
        self.counter = Message(window, textvariable=self.totalmove, font=("helvetica", int(W//45.6)), width=int(W//6), justify=RIGHT, bg="white")
        self.counter.place(relx=0.5, rely=0.04, anchor=CENTER)

        # this creates the board
        self.BS = int(H//1.2)    # BS stands for board side
        BS = self.BS
        self.board = Canvas(window, width=BS, height=BS, bg="#DEB887", bd=5, relief=RIDGE)
        self.board.place(relx=0.5, rely=0.5, anchor=CENTER)

        # this creates the grid of lines on the board
        G = int(BS//10)     # G stands for grid
        for line in range(1, 10):
            self.board.create_line(G, (G * line), BS-G, (G * line), width=2)
            self.board.create_line((G * line), G, (G * line), BS-G, width=2)
        UD = 3*G    # UD stands for upper diamond
        LD = 7*G    # LD stands for lower diamond
        DS = int(BS//50)    # DS stands for diamond size
        self.board.create_polygon(UD, UD-DS, UD+DS, UD, UD, UD+DS, UD-DS, UD, fill="black")
        self.board.create_polygon(LD, UD-DS, LD+DS, UD, LD, UD+DS, LD-DS, UD, fill="black")
        self.board.create_polygon(UD, LD-DS, UD+DS, LD, UD, LD+DS, UD-DS, LD, fill="black")
        self.board.create_polygon(LD, LD-DS, LD+DS, LD, LD, LD+DS, LD-DS, LD, fill="black")
        M = int(BS//2)  # M stands for middle
        self.board.create_polygon(M, M-DS, M+DS, M, M, M+DS, M-DS, M, fill="black")

        # this array represents the places for stones
        self.places = [[None for x in range(9)] for x in range(9)]

        # this creates the pieces on the board (they start out invisible)
        C = int(BS//25)     # C stands for circle size
        self.intersect = [[None for x in range(9)] for x in range(9)]
        for dot_x in range(1, 10):
            for dot_y in range(1, 10):
                self.intersect[dot_x - 1][dot_y - 1] = self.board.create_oval(((G * dot_x) - C), ((G * dot_y) - C),
                                                                              ((G * dot_x) + C), ((G * dot_y) + C),
                                                                              fill="", outline="")

        self.last_pas = None

        self.unfreeze()

    # this function adds buttons
    def unfreeze(self):
        # this makes each stone a button
        for dot_x in range(1, 10):
            for dot_y in range(1, 10):
                self.board.tag_bind(self.intersect[dot_x-1][dot_y-1], "<Button-1>", self.move)

        self.board.config(cursor="tcross")  # this sets a new cursor for the board

        # this makes the menu button
        self.menubut = Button(window, text="OPTIONS", font=("helvetica", int(W//45.6)), bd=5, width=int(W//182.4), command=self.menu)
        self.menubut.place(relx=0.92, rely=0.05, anchor=CENTER)
        self.menubut.config(cursor="hand2")

        # this makes the pass button
        self.turn_pass = Button(window, text="PASS", font=("helvetica", int(W//91.2)), bd=5, width=int(W//121.6), command=self.pas)
        self.turn_pass.place(relx=0.38, rely=0.965, anchor=CENTER)
        self.turn_pass.config(cursor="hand2")

        # this makes the surrender button
        self.surrend_butn = Button(window, text="SURRENDER", font=("helvetica", int(W//91.2)), bd=5, width=int(W//121.6), command=self.surrender)
        self.surrend_butn.place(relx=0.5, rely=0.965, anchor=CENTER)
        self.surrend_butn.config(cursor="hand2")

        # this makes the end game button
        self.stop_game = Button(window, text="PROPOSE END", font=("helvetica", int(W//91.2)), bd=5, width=int(W//121.6), command=self.want_end)
        self.stop_game.place(relx=0.62, rely=0.965, anchor=CENTER)
        self.stop_game.config(cursor="hand2")

    def menu(self):
        # this chunk displays the request
        MW = int(W//4.5)    # stands for menu width
        MH = int(H//2)      # stands for menu height
        self.menuback = Canvas(window, width=MW, height=MH, bg="grey", bd=5, relief=RAISED)
        self.menuback.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.menuback.create_text(int(MW//2), int(MH//6), text="MENU", font=("helvetica", int(W//18.2)), width=int(W//2.2), justify=CENTER)

        newgame = Button(self.menuback, text="New Game", font=("helvetica", int(W//45.6)), bd=5, width=int(W//182.4), command=start)
        newgame.place(relx=0.5, rely=0.4, anchor=CENTER)
        newgame.config(cursor="hand2")

        rulebut = Button(self.menuback, text="Rules", font=("helvetica", int(W//45.6)), bd=5, width=int(W//182.4), command=self.rulepopup)
        rulebut.place(relx=0.5, rely=0.6, anchor=CENTER)
        rulebut.config(cursor="hand2")

        exitbut = Button(self.menuback, text="Close", font=("helvetica", int(W//36.4)), bd=5, width=int(W//165.8), command=self.closemenu)
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
        RW = int(W//3)      # stands for rule width
        RH = int(H//1.5)    # stands for rule height
        self.ruleback = Canvas(window, width=RW, height=RH, bg="grey", bd=5, relief=RAISED)
        self.ruleback.place(relx=0.5, rely=0.5, anchor=CENTER)

        self.ruleback.create_text(int(RW//2), int(RH//16), text="Rules of Go:", font=("helvetica", int(W//36.4)), width=W)
        self.ruleback.create_text(int(RW//4), int(RH//6.6), text=rule1, font=("helvetica", int(W//72.9)), width=int(W//7.3))
        self.ruleback.create_text(int(RW//4), int(RH//4.4), text=rule2, font=("helvetica", int(W//72.9)), width=int(W//7.3))
        self.ruleback.create_text(int(RW//4), int(RH//3.1), text=rule3, font=("helvetica", int(W//72.9)), width=int(W//7.3))
        self.ruleback.create_text(int(RW//4), int(RH//2.3), text=rule4, font=("helvetica", int(W//72.9)), width=int(W//7.3))
        self.ruleback.create_text(int(RW//4), int(RH//1.7), text=korule, font=("helvetica", int(W//72.9)), width=int(W//7.3))
        self.ruleback.create_text(int(RW//1.3), int(RH//5), text=rule5, font=("helvetica", int(W//72.9)), width=int(W//7.3))
        self.ruleback.create_text(int(RW//1.3), int(RH//2.5), text=rule6, font=("helvetica", int(W//72.9)), width=int(W//7.3))
        self.ruleback.create_text(int(RW//1.3), int(RH//1.5), text=rule7, font=("helvetica", int(W//72.9)), width=int(W//7.3))

        norule = Button(self.ruleback, text="Close", font=("helvetica", int(W//45.6)), bd=5, width=int(W//114), height=1, command=self.closerule, cursor="hand2")
        norule.place(relx=0.5, rely=0.88, anchor=CENTER)

    # this function places a stone
    def move(self, event):
        BS = self.BS
        x = (event.x - int(BS//20)) // int(BS//10)
        y = (event.y - int(BS//20)) // int(BS//10)
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
            BS = self.BS
            self.pasmesg = self.board.create_text(int(BS//2), int(BS//20), text=self.turn+" passed!", font=("helvetica", int(W//72.9)), width=int(W//6))
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
        self.blackbumber.itemconfig(self.blackscored, font=("helvetica", int(W//26)))
        self.whitebumber.itemconfig(self.whitescored, font=("helvetica", int(W//26)))
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

        newgame = Button(window, text="New Game", font=("helvetica", int(W//91.2)), bd=5, width=int(W//182.4), command=start)
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
        QW = int(W//3)      # stands for request width
        QH = int(H//3)      # stands for request height
        self.request = Canvas(window, width=QW, height=QH, bg="grey", bd=5, relief=RAISED)
        self.request.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.request.create_text(int(QW//2), int(QH/4), text=self.turn + " requests end!", font=("helvetica", int(W//36.4)), width=int(W//2.2), justify=CENTER)

        ybut = Button(self.request, text="YES", font=("helvetica", int(W//45.6)), bd=5, width=int(W//182.4), command=self.accept)
        nbut = Button(self.request, text="NO", font=("helvetica", int(W//45.6)), bd=5, width=int(W//182.4), command=self.deny)
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
