"""
this code simulate board game
By Tomas Paris and Ben Goldman
    Tomas wrote the graphic interface (the Game class), including the code which calculates final score, and the mainmenu, explain, close, and start functions
    Ben wrote the game logic (the Stone and Shape class)

## DOC TESTS ##
    because this program cannot accept normal doctest inputs, this section will simply be a list of commands for the user to test on their own
NOTE: try performing each doctest onn both colors

>> encircle a stone of opposite color
the encircled stone should dissapear, and a captured piece should be added
    example:
_ X _       _ X _
X O X  -->  X _ X
_ X _       _ X _

>> aftre playing a few moves, open the menu and start a new game
the board, captured pieces, score, and total moves should reset

>> press the surrender button
the game should end, and the other player should win by default, regardless of potential score

>> pass a move two times in a row
the game should end, and a final score should be calculated and displayed

>> request an end to the game
press no, and the game should continue; press yes, and the game should end and the score should be displayed

>> surround land with one color, then surround one node of that circle with another color
that one node should dissapear, even though the last stone placed technically has no breaths at first
    example:
_ _ X _       _ O X _       _ O X _       _ O X _
_ X _ X  -->  O X _ X  -->  O X O X  -->  O _ O X
_ _ X _       _ O X _       _ O X _       _ O X _
                                ^
                                ^ this moment is the moment when the O piece is first placed; its location has no breaths, but because it
                                  takes away the breaths of one of the enemy X pieces, the X is removed first, giving the new O a breath

# I ask for a square here to make sure the code will not fall into an infinite loop if a line of stones is continuous
>> create a hollow 3x3 square of one color on the board, with all adjacent pieces, and then take away all of that square's breaths
the entire square should dissapear
    example:
_ _ _ _ _       _ O O O _       _ O O O _
_ X X X _       O X X X O       O _ _ _ O
_ X _ X _  -->  O X O X O  -->  O _ O _ O
_ X X X _       O X X X O       O _ _ _ O
_ _ _ _ _       _ O O O _       _ O O O _

## DOC TEST END ##

"""
from Tkinter import *

# the following chunk of code was written by Tomas
#
#
    # initializes the window, and customizes its features
master = Tk()
master.title("Go (game)")
master.config(bg="white")
master.iconbitmap("board.ico")      # board.ico should be a file in the same directory as this code
master.call("tk", "scaling", 1)
master.state('zoomed')      # opens the window in fullscreen, only works on windows, not mac
    # creates height and width values based off of the screen being used
H = master.winfo_screenheight() - (master.winfo_screenheight() * 0.1)
W = master.winfo_screenwidth() - (master.winfo_screenwidth() * 0.02)
master.geometry('%dx%d+0+%d' % (W, H, H*.05))       # opens the window almost fullscreen, on mac
    # initalizes a frame with a fixed size and position for all the other objects to be displayed on
window = Frame(height=H, width=W, bg="white")
window.place(relx=0.5, rely=0.5, anchor=CENTER)
    # text of all the rules for Go
rule1 = "1. Black moves first"
rule2 = "2. Empty spaces are called Breaths"
rule3 = "3. Stones without adjacent Breaths die"
rule4 = "4. Adjacent stones of the same color share Breaths"
korule = "ko rule: moves that revert the game to its state one turn ago cannot be made"
rule5 = "5. When stones of one color surround an empty space, that space becomes land"
rule6 = "6. The final score is the total land controlled by a color minus the number of dead stones of that color"
rule7 = "7. The game ends when both sides agree to end the game, when one side surrenders, or after two consecutive passes"
    # list to hold objects for deletion
mainlist = []


# displays the main menu; written by Tomas
def mainmenu():
    close()     # clears the display
        # draws a backdrop for the main menu
    backdrop = Canvas(window, width=W/2.0, height=H/1.2, bg="#DEB887", bd=5, relief=RIDGE)
    backdrop.place(relx=0.5, rely=0.5, anchor=CENTER)
        # the welcome message
    welcome = Label(window, text="Welcome to Go!", font=("helvetica", int(W//18.2)), bg="#DEB887")
    welcome.place(relx=0.5, rely=0.2, anchor=CENTER)
        # the new game button, it activates the start function
    new = Button(window, text="NEW GAME", font=("helvetica", int(W//36.4)), bd=5, command=start, height=int(H//405), width=int(W//121), cursor="hand2")
    new.place(relx=0.5, rely=0.45, anchor=CENTER)
        # the rules button, it activates the explain function
    rules = Button(window, text="RULES", font=("helvetica", int(W//36.4)), bd=5, command=explain, height=int(H//405), width=int(W//121), cursor="hand2")
    rules.place(relx=0.5, rely=0.7, anchor=CENTER)
        # places all the displayed objects into mainlist, to be destroyed later
    attributes = [backdrop, welcome, new, rules]
    mainlist.extend(attributes)

#clears the display; by Tommas
def close():
        #destroys every item in mainlist, clearing the display for new objects
    for item in mainlist:
        item.destroy()
    del mainlist[:]


# opens a window and displays the rules; by Tomas
def explain():
    close()     # clears the display
        # displays all the text of the rules
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
        # creates the menu button
    mainreturn = Button(window, text="RETURN", font=("helvetica", int(W//36.4)), bd=5, command=mainmenu, height=int(H//405), width=int(W//121), cursor="hand2")
    mainreturn.place(relx=0.5, rely=0.85, anchor=CENTER)
        # adds all the displayed object to the mainlist to be destroyed later
    attributes = [instructions, rule_1, rule_2, rule_3, rule_4, rule_ko, rule_5, rule_6, rule_7, mainreturn]
    mainlist.extend(attributes)


# new game button is directed here to open up the Game class, since buttons can't directly open a class; by Tomas
def start():
    close()     # clears the display
    gameplay = Game()


# a datatype for the game display interface and movement; by Tomas
class Game:

    def __init__(self):
        # next 20 lines fill the left side of the window
            # creates grey bumper
        BW = int(W//5.2)    # BW stands for bumper width
        BH = int(H//1.3)    # BH stands for bumper height
        self.blackbumber = Canvas(window, width=BW, height=BH, bg="grey", bd=5, relief=GROOVE)
        self.blackbumber.place(relx=0.11, rely=0.5, anchor=CENTER)
            # displays text labels on bumper
        self.blackbumber.create_text(int(BW//2.1), int(BH//11.2), text="Black:", font=("helvetica", int(W//22.8)), width=int(W//6))
        self.blackbumber.create_text(int(BW//1.9), int(BH//3.6), text="Pieces Captured:", font=("helvetica", int(W//45.6)), width=int(W//4.5))
        self.blackbumber.create_text(int(BW//3.8), int(BH//1.5), text='Score:', font=("helvetica", int(W//45.6)), width=int(W//6))
            # displays the state of black side
        self.turn = "Black"     # used as an easy way to check whose turn it is
        self.blackstate = "(Moving)"
        self.currentblack = self.blackbumber.create_text(int(BW//2.6), int(BH//6.4), text=self.blackstate, font=("helvetica", int(W//45.6)), width=int(W//6))
            # displays the score of black side
        self.blackscore = "TBD"
        self.blackscored = self.blackbumber.create_text(int(BW//2), int(BH//1.2), text=self.blackscore, font=("helvetica", int(W//15.2)), width=int(W//6))
    #
    #
        # next 15 lines fill the right side of the window
            # creates the grey bumper
        self.whitebumber = Canvas(window, width=BW, height=BH, bg="grey", bd=5, relief=GROOVE)
        self.whitebumber.place(relx=0.89, rely=0.5, anchor=CENTER)
            # displays text labels on bumper
        self.whitebumber.create_text(int(BW//2.1), int(BH//11.2), text="White:", font=("helvetica", int(W//22.8)), width=int(W//6))
        self.whitebumber.create_text(int(BW//1.9), int(BH//3.6), text="Pieces Captured:", font=("helvetica", int(W//45.6)), width=int(W//4.5))
        self.whitebumber.create_text(int(BW//3.8), int(BH//1.5), text='Score:', font=("helvetica", int(W//45.6)), width=int(W//6))
            # displays the state of white side
        self.whitestate = "(Waiting)"
        self.currentwhite = self.whitebumber.create_text(int(BW//2.6), int(BH//6.4), text=self.whitestate, font=("helvetica", int(W//45.6)), width=int(W//6))
            # displays the score of white side
        self.whitescore = "TBD"
        self.whitescored = self.whitebumber.create_text(int(BW//2), int(BH//1.2), text=self.whitescore, font=("helvetica", int(W//15.2)), width=int(W//6))
    #
    #
        # fills the center of the window
            # displays the total moves played, using necessary tkinter variable types
        self.total = 0
        self.totalmove = StringVar()    # tkinter Message() objects need StringVar() in order to update display while still running
        self.totalmove.set("Total Moves: " + str(self.total))
        self.counter = Message(window, textvariable=self.totalmove, font=("helvetica", int(W//45.6)), width=int(W//6), justify=RIGHT, bg="white")
        self.counter.place(relx=0.5, rely=0.04, anchor=CENTER)
            # creates the board
        self.BS = int(H//1.2)    # BS stands for board side
        BS = self.BS
        self.board = Canvas(window, width=BS, height=BS, bg="#DEB887", bd=5, relief=RIDGE)
        self.board.place(relx=0.5, rely=0.5, anchor=CENTER)
            # creates the grid of lines on the board
        G = BS/10.0     # G stands for grid
        for line in range(1, 10):
            self.board.create_line(G, (G * line), 9*G, (G * line), width=2)
            self.board.create_line((G * line), G, (G * line), 9*G, width=2)
            # creates the diamonds on the grid
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
            # creates the pieces on the board (they start out invisible)
        C = int(BS//25)     # C stands for circle size
        self.intersect = [[None for x in range(9)] for x in range(9)]
        for dot_x in range(1, 10):
            for dot_y in range(1, 10):
                self.intersect[dot_x - 1][dot_y - 1] = self.board.create_oval(((G * dot_x) - C), ((G * dot_y) - C),
                                                                              ((G * dot_x) + C), ((G * dot_y) + C),
                                                                              fill="", outline="")
        self.last_pas = None    # allows comparison operations with this variable before it is really assigned an important value
        self.unfreeze()         # calls another function to finish displaying the game interface

# places a stone
    def move(self, event):
            # grabs the location of the mouse when it was clicked, and through fancy division finds the stone location that was clicked
        BS = self.BS
        x = (event.x - int(BS//20)) // int(BS//10)
        y = (event.y - int(BS//20)) // int(BS//10)
            # fills the stone that was clicked depending on whose turn it was
        if not self.places[x][y]:
            if self.turn == "Black":
                self.board.itemconfig(self.intersect[x][y], fill="black")
                self.places[x][y] = Stone(x, y, "B")                        # calls the stone class
            else:
                self.board.itemconfig(self.intersect[x][y], fill="white")
                self.places[x][y] = Stone(x, y, "W")                        # calls the stone class
            self.play()     # changes whose turn it is

# changes whose turn it is
    def play(self):
            # if else statement changes whose turn it is
        if self.turn == "Black":
            self.blackstate = "(Waiting)"
            self.whitestate = "(Moving)"
            self.turn = "White"
        else:
            self.blackstate = "(Moving)"
            self.whitestate = "(Waiting)"
            self.turn = "Black"
            # increases the total moves, and deletes the pass message, if present
        self.total += 1
        if (self.total - 1) == self.last_pas:
            self.board.delete(self.pasmesg)
            # updates the displays on the board using tkinter methods
        self.totalmove.set("Total Moves: " + str(self.total))
        self.blackbumber.itemconfig(self.currentblack, text=self.blackstate)
        self.whitebumber.itemconfig(self.currentwhite, text=self.whitestate)

# adds buttons
    def unfreeze(self):
            # makes each stone a button
        for dot_x in range(1, 10):
            for dot_y in range(1, 10):
                self.board.tag_bind(self.intersect[dot_x-1][dot_y-1], "<Button-1>", self.move)
            # sets a new cursor for the board
        self.board.config(cursor="tcross")
            # makes the menu button
        self.menubut = Button(window, text="OPTIONS", font=("helvetica", int(W//45.6)), bd=5, width=int(W//182.4), command=self.menu, cursor="hand2")
        self.menubut.place(relx=0.92, rely=0.05, anchor=CENTER)
            # makes the pass button
        self.turn_pass = Button(window, text="PASS", font=("helvetica", int(W//91.2)), bd=5, width=int(W//121.6), command=self.pas, cursor="hand2")
        self.turn_pass.place(relx=0.38, rely=0.965, anchor=CENTER)
            # makes the surrender button
        self.surrend_butn = Button(window, text="SURRENDER", font=("helvetica", int(W//91.2)), bd=5, width=int(W//121.6), command=self.surrender, cursor="hand2")
        self.surrend_butn.place(relx=0.5, rely=0.965, anchor=CENTER)
            # makes the end game button
        self.stop_game = Button(window, text="PROPOSE END", font=("helvetica", int(W//91.2)), bd=5, width=int(W//121.6), command=self.want_end, cursor="hand2")
        self.stop_game.place(relx=0.62, rely=0.965, anchor=CENTER)

# deletes all the buttons
    def freeze(self):
            # destroys unnecessary buttons
        self.turn_pass.destroy()
        self.surrend_butn.destroy()
        self.stop_game.destroy()
        self.menubut.destroy()
            # disables the special cursor above the board
        self.board.config(cursor="arrow")
            # unbinds the buttons attached to each stone
        for dot_x in range(1, 10):
            for dot_y in range(1, 10):
                self.board.tag_unbind(self.intersect[dot_x - 1][dot_y - 1], "<Button-1>")

# displays the menu popup
    def menu(self):
            # displays the popup window
        MW = int(W//4.5)    # stands for menu width
        MH = int(H//2)      # stands for menu height
        self.menuback = Canvas(window, width=MW, height=MH, bg="grey", bd=5, relief=RAISED)
        self.menuback.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.menuback.create_text(int(MW//2), int(MH//6), text="MENU", font=("helvetica", int(W//18.2)), width=int(W//2.2), justify=CENTER)
            # makes the new game button
        newgame = Button(self.menuback, text="New Game", font=("helvetica", int(W//45.6)), bd=5, width=int(W//182.4), command=start, cursor="hand2")
        newgame.place(relx=0.5, rely=0.4, anchor=CENTER)
            # makes the rules button
        rulebut = Button(self.menuback, text="Rules", font=("helvetica", int(W//45.6)), bd=5, width=int(W//182.4), command=self.rulepopup, cursor="hand2")
        rulebut.place(relx=0.5, rely=0.6, anchor=CENTER)
            # makes the close button
        exitbut = Button(self.menuback, text="Close", font=("helvetica", int(W//36.4)), bd=5, width=int(W//165.8), command=self.closemenu, cursor="hand2")
        exitbut.place(relx=0.5, rely=0.85, anchor=CENTER)
    #
    #
        self.freeze()   # shuts down all the gameplay buttons so the menu popup cannot be overriden or ignored
        attributes = [self.blackbumber, self.counter, self.board, self.whitebumber, self.menuback]
        mainlist.extend(attributes)     # adds all the currently displayed objects to mainlist, so that they are destroyed if the newgame button is pushed

# destroys the menu popup
    def closemenu(self):
        self.menuback.destroy()
        del mainlist[:]     # clears the currently active objects from mainlist so that they do not build up each time the menu is opened
        self.unfreeze()     # reactivates the buttons on the board to continue gameplay

# displays the rules popup
    def rulepopup(self):
            # displays the popup background
        RW = int(W//3)      # stands for rule width
        RH = int(H//1.5)    # stands for rule height
        self.ruleback = Canvas(window, width=RW, height=RH, bg="grey", bd=5, relief=RAISED)
        self.ruleback.place(relx=0.5, rely=0.5, anchor=CENTER)
            # displays the text of all the rules
        self.ruleback.create_text(int(RW//2), int(RH//16), text="Rules of Go:", font=("helvetica", int(W//36.4)), width=W)
        self.ruleback.create_text(int(RW//4), int(RH//6.6), text=rule1, font=("helvetica", int(W//72.9)), width=int(W//7.3))
        self.ruleback.create_text(int(RW//4), int(RH//4.4), text=rule2, font=("helvetica", int(W//72.9)), width=int(W//7.3))
        self.ruleback.create_text(int(RW//4), int(RH//3.1), text=rule3, font=("helvetica", int(W//72.9)), width=int(W//7.3))
        self.ruleback.create_text(int(RW//4), int(RH//2.3), text=rule4, font=("helvetica", int(W//72.9)), width=int(W//7.3))
        self.ruleback.create_text(int(RW//4), int(RH//1.7), text=korule, font=("helvetica", int(W//72.9)), width=int(W//7.3))
        self.ruleback.create_text(int(RW//1.3), int(RH//5), text=rule5, font=("helvetica", int(W//72.9)), width=int(W//7.3))
        self.ruleback.create_text(int(RW//1.3), int(RH//2.5), text=rule6, font=("helvetica", int(W//72.9)), width=int(W//7.3))
        self.ruleback.create_text(int(RW//1.3), int(RH//1.5), text=rule7, font=("helvetica", int(W//72.9)), width=int(W//7.3))
            # makes the close button
        norule = Button(self.ruleback, text="Close", font=("helvetica", int(W//45.6)), bd=5, width=int(W//114), height=1, command=self.closerule, cursor="hand2")
        norule.place(relx=0.5, rely=0.88, anchor=CENTER)

# destroys the rules popup
    def closerule(self):
        self.ruleback.destroy()

# skips the players turn, or ends the game after two consecutive passes
    def pas(self):
        if self.total == self.last_pas:
            self.findscore()    # ends the game if pass button was pressed by both players consecutively
        else:
            self.last_pas = self.total + 1      # last_pas helps check if two players passed consecutively
                # displays a message notifying that a move was passed
            BS = self.BS
            self.pasmesg = self.board.create_text(int(BS//2), int(BS//25), text=self.turn+" passed!", font=("helvetica", int(W//72.9)), width=int(W//6))
            self.play()

# ends the game, whoever pushes it loses
    def surrender(self):
            # sets the scores
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
            # updates the display
        self.blackbumber.itemconfig(self.blackscored, font=("helvetica", int(W//26)))
        self.whitebumber.itemconfig(self.whitescored, font=("helvetica", int(W//26)))
        self.freeze()
        self.endgame()

# proposes to end the game
    def want_end(self):
            # displays the request
        QW = int(W//3)      # stands for request width
        QH = int(H//3)      # stands for request height
        self.request = Canvas(window, width=QW, height=QH, bg="grey", bd=5, relief=RAISED)
        self.request.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.request.create_text(int(QW//2), int(QH/4), text=self.turn + " requests end!", font=("helvetica", int(W//36.4)), width=int(W//2.2), justify=CENTER)
            # creates yes and no buttons
        ybut = Button(self.request, text="YES", font=("helvetica", int(W//45.6)), bd=5, width=int(W//182.4), command=self.accept)
        nbut = Button(self.request, text="NO", font=("helvetica", int(W//45.6)), bd=5, width=int(W//182.4), command=self.deny)
        ybut.place(relx=0.3, rely=0.6, anchor=CENTER)
        ybut.config(cursor="hand2")
        nbut.place(relx=0.7, rely=0.6, anchor=CENTER)
        nbut.config(cursor="hand2")
        self.play()
        self.freeze()

# denies a request for endgame
    def deny(self):
            # destroys the request popup
        self.unfreeze()
        self.request.destroy()

# accepts a request for endgame
    def accept(self):
            # destroys the request popup and ends the game
        self.unfreeze()
        self.request.destroy()
        self.findscore()

# shows the final score
    def endgame(self):
            # updates the display
        self.blackbumber.itemconfig(self.currentblack, text=self.blackstate)
        self.whitebumber.itemconfig(self.currentwhite, text=self.whitestate)
        self.blackbumber.itemconfig(self.blackscored, text=self.blackscore)
        self.whitebumber.itemconfig(self.whitescored, text=self.whitescore)
            # creates new game button
        newgame = Button(window, text="New Game", font=("helvetica", int(W // 91.2)), bd=5, width=int(W // 182.4), command=start)
        newgame.place(relx=0.5, rely=0.965, anchor=CENTER)
        newgame.config(cursor="hand2")
            # adds all the currently displayed objects to mainlist, so that they are destroyed if the newgame button is pushed
        attributes = [self.blackbumber, self.counter, self.board, self.whitebumber, newgame]
        mainlist.extend(attributes)

# analyzes the board and finds the final score
    def findscore(self):
        print "e"
        self.freeze()
        self.endgame()


# establishes the game logic and determines when stones die; by Ben
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


# a datatype for groups of adjacent stones that are the same color, therefore sharing breaths; by Ben
class Shape:

    def __init__(self):
        print "e"


# a datatype for enforcing the ko rule
class Gamestate:

    def __init__(self):
        print "e"


mainmenu()
mainloop()
