"""
this code simulate board game
By Tomas Paris and Ben Goldman
    Tomas wrote the graphic interface (the gameplay class, excluding the code which calculates final score), and the mainmenu, explain, close, and start functions
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
rules = [["1. Black is the first player to move", 4, 6.6], ["2. Empty spaces are called Breaths", 4, 4.4], ["3. Stones without adjacent Breaths die", 4, 3.1],
         ["4. Stones next to one other and of the same color share Breaths", 4, 2.3], ["ko rule: moves that revert the game to its state one turn ago can not be made", 4, 1.7],
         ["5. When stones of one color wrap around an empty space, that space becomes land", 1.3, 5],
         ["6. The final score is the total land controlled by a color minus the number of dead stones of that color", 1.3, 2.5],
         ["7. The game ends when both sides agree to end the game, when one side surrenders, or after two consecutive passes", 1.3, 1.5]]
    # list to hold objects for deletion
mainlist = []


# displays the main menu; written by Tomas
def mainmenu():
        # draws a backdrop for the main menu
    backdrop = Canvas(window, width=W/2.0, height=H/1.2, bg="#DEB887", bd=5, relief=RIDGE)
    backdrop.place(relx=0.5, rely=0.5, anchor=CENTER)
        # the welcome message
    welcome = Label(backdrop, text="Welcome to Go!", font=("helvetica", int(W//18.2)), bg="#DEB887")
    welcome.place(relx=0.5, rely=0.2, anchor=CENTER)
        # the new game button, it activates the start function
    new = Clicker(backdrop, "NEW GAME", 36.4, start, 121, 0.5, 0.45, 405)
        # the rules button, it activates the explain function
    rules = Clicker(backdrop, "RULES", 36.4, explain, 121, 0.5, 0.7, 405)
        # places all the displayed objects into mainlist, to be destroyed later
    attributes = [backdrop]
    mainlist.append(attributes)

#clears the display; by Tommas
def close():
    front = len(mainlist)-1
        #destroys every item in mainlist, clearing the display for new objects
    for item in mainlist[front]:
        item.destroy()
    del mainlist[front]


# opens a window and displays the rules; by Tomas
def explain():
    blank = Canvas(window, width=W, height=H, bg="white")
    blank.place(relx=0.5, rely=0.5, anchor=CENTER)
    fill_rules(blank, W, H,)


def fill_rules(backdrop, rule_W, rule_H):
        # displays all the text of the rules
    backdrop.create_text(int(rule_W//2), int(rule_H//16), text="Rules of Go:", font=("helvetica", int(rule_W//18.2)), width=W)
    for rule in rules:
        backdrop.create_text(int(rule_W//rule[1]), int(rule_H//rule[2]), text=rule[0], font=("helvetica", int(rule_W//36.4)), width=int(rule_W//2.3), justify=LEFT)
        # makes the close button
    norule = Button(backdrop, text="CLOSE", font=("helvetica", int(rule_W//36.4)), bd=5, width=int(rule_W//121), height=int(H//405), command=close, cursor="hand2")
    norule.place(relx=0.5, rely=0.88, anchor=CENTER)
        # adds all the displayed object to the mainlist to be destroyed later
    attributes = [backdrop]
    mainlist.append(attributes)


# new game button is directed here to open up the Game class, since buttons can't directly open a class; by Tomas
def start():
    close()     # clears the display
    global white, black, go, game, shapelist, landlist, screenshot
    shapelist = [None]
    landlist = [None]
    white = Bumper("White:", 0.89)
    black = Bumper("Black:", 0.11)
    go = Board()
    game = Gameplay()
    screenshot = Gamestate()
    
    


# a datatype for the game display interface and movement; by Tomas
class Gameplay:

    def __init__(self):
            # displays the total moves played, using necessary tkinter variable types
        self.total = 0
        self.totalmove = StringVar()    # tkinter Message() objects need StringVar() in order to update display while still running
        self.totalmove.set("Total Moves: " + str(self.total))
        self.counter = Message(window, textvariable=self.totalmove, font=("helvetica", int(W//45.6)), width=int(W//6), justify=RIGHT, bg="white")
        self.counter.place(relx=0.5, rely=0.04, anchor=CENTER)

        self.turn = "Black"     # black moves first
        self.places = [[None for x in range(9)] for x in range(9)]      # this array will represent moves using the Stone class
        self.last_pas = None    # allows comparison operations with this variable before it is really assigned an important value
        self.unfreeze()         # calls another function to finish displaying the game interface

# adds buttons
    def unfreeze(self):
            # makes buttons
        self.menu = Clicker(window, "OPTIONS", 45.6, self.menu, 182.4, 0.92, 0.05)
        self.X_menu = Clicker(window, "UNDO", 45.6, self.undo, 182.4, 0.08, 0.05)
        self.T_pass = Clicker(window, "PASS", 91.2, self.pas, 121.6, 0.38, 0.965)
        self.surrend = Clicker(window, "SURRENDER", 91.2, self.surrender, 121.6, 0.5, 0.965)
        self.stop = Clicker(window, "PROPOSE END", 91.2, self.want_end, 121.6, 0.62, 0.965)
        go.unfreeze()   # unfreezes the board

# deletes all the buttons
    def freeze(self, ):
        remove(self.menu, self.X_menu, self.T_pass, self.surrend, self.stop)    # destroys unnecessary buttons
        go.freeze()     # freezes the board

# changes whose turn it is
    def play(self):
            # if else statement changes whose turn it is
        if self.turn == "Black":
            self.turn = "White"
        else:
            self.turn = "Black"
            # increases the total moves, and deletes the pass message, if present
        self.total += 1
        if (self.total - 1) == self.last_pas:
            go.board.delete(self.pasmesg)
            # updates the displays on the board using tkinter methods
        self.totalmove.set("Total Moves: " + str(self.total))
        black.change_state()
        white.change_state()
        
    def undo(self):
        print screenshot.preimage, "pre"
        print screenshot.image
        for y in range(9):
            for x in range(9):
                if screenshot.preimage[0] == "T" and game.places[x][y]:
                    game.places[x][y].destroy()
                    screenshot.preimage = screenshot.preimage[1:]
                
                elif screenshot.preimage[0] == "T" and not game.places[x][y]:
                    screenshot.preimage = screenshot.preimage[1:]
                    continue
                elif screenshot.preimage[0] =="W":
                    self.places[x][y].color = "W"
                    screenshot.preimage = screenshot.preimage[1:]
                else:
                    self.places[x][y].color = "B"
                    screenshot.preimage = screenshot.preimage[1:]

                    

# displays the menu popup
    def menu(self):
        global menu
        menu = Popup(4.5, 2, 6, "MENU", 18.2)   # displays the popup window
            # makes buttons
        newgame = Clicker(menu.back, "New Game", 45.6, start, 182.4, 0.5, 0.4)
        rule = Clicker(menu.back, "Rules", 45.6, self.rulepopup, 182.4, 0.5, 0.6)
        exit = Clicker(menu.back, "Close", 30, self.closemenu, 165, 0.5, 0.85)

        self.freeze()   # shuts down all the gameplay buttons so the menu popup cannot be overriden or ignored
        attributes = [black.bumper, self.counter, go.board, white.bumper, menu.back]
        mainlist.append(attributes)     # adds all the currently displayed objects to mainlist, so that they are destroyed if the newgame button is pushed

# destroys the menu popup
    def closemenu(self):
        menu.back.destroy()
        del mainlist[0]     # clears the currently active objects from mainlist so that they do not build up each time the menu is opened
        self.unfreeze()     # reactivates the buttons on the board to continue gameplay

# displays the rules popup
    def rulepopup(self):
        global rule
        rule = Popup(2, 2)
        fill_rules(rule.back, rule.PW, rule.PH)

# skips the players turn, or ends the game after two consecutive passes
    def pas(self):
        if self.total == self.last_pas:
            self.findscore()    # ends the game if pass button was pressed by both players consecutively
        else:
            self.last_pas = self.total + 1      # last_pas helps check if two players passed consecutively
                # displays a message notifying that a move was passed
            self.pasmesg = go.board.create_text(int(go.BS//2), int(go.BS//25), text=self.turn+" passed!", font=("helvetica", int(W//72.9)), width=int(W//6))
            self.play()

# ends the game, whoever pushes it loses
    def surrender(self):
            # sets the scores
        self.play()
        if self.turn == "Black":
            black.state = "Winner!"
            black.score = "Default"
            white.state = "Loser"
            white.score = "Forfeit"
        else:
            white.state = "Winner!"
            white.score = "Default"
            black.state = "Loser"
            black.score = "Forfeit"
            # updates the display
        black.bumper.itemconfig(black.scored, font=("helvetica", int(W//26)))
        white.bumper.itemconfig(white.scored, font=("helvetica", int(W//26)))
        self.freeze()
        self.endgame()

# proposes to end the game
    def want_end(self):
            # displays the request
        global want
        want = Popup(3, 3, 4, (self.turn + " requests end!"), 36.4)
            # creates yes and no buttons
        yes = Clicker(want.back, "YES", 45.6, self.accept, 182.4, 0.3, 0.6)
        no = Clicker(want.back, "NO", 45.6, self.deny, 182.4, 0.7, 0.6)
        self.play()
        self.freeze()

# denies a request for endgame
    def deny(self):
            # destroys the request popup
        want.back.destroy()
        self.unfreeze()

# accepts a request for endgame
    def accept(self):
            # destroys the request popup and ends the game
        self.unfreeze()
        want.back.destroy()
        self.findscore()

# shows the final score
    def endgame(self):
            # updates the display
        black.update()
        white.update()
        newgame = Clicker(window, "New Game", 91.2, start, 182.4, 0.5, 0.965)   # creates new game button
        attributes = [black.bumper, self.counter, go.board, white.bumper, newgame.click]
        mainlist.append(attributes)     # adds all the currently displayed objects to mainlist, so that they are destroyed if the newgame button is pushed

# analyzes the board and finds the final score
    def findscore(self):
        edgecount = 0
        black.score = 0
        white.score = 0
        
        for y in range(9):
            for x in range(9):
                if not self.places[x][y]:
                    self.places[x][y] = Stone(x, y, "Y")
        for y in range(9):
            for x in range(9):
                if self.places[x][y].island == 0 and self.places[x][y].color == "Y":
                        adjacent_places = []
                        if (x + 1) < 9:
                            adjacent_places.append((x + 1, y))
                        if (y - 1) >= 0:
                            adjacent_places.append((x, y - 1))
                        if (x - 1) >= 0:
                            adjacent_places.append((x - 1, y))
                        if (y + 1) < 9:
                            adjacent_places.append((x, y + 1))
                        landlist.append(Shape())
                        self.places[x][y].island = len(landlist) - 1
                        landlist[self.places[x][y].island].add_stone(self.places[x][y])
                        for place in adjacent_places:
                            piece = self.places[place[0]][place[1]]
                            if piece.color == "Y" and not landlist[piece.island]:
                                if (piece.x + 1) < 9:
                                    adjacent_places.append((piece.x + 1, piece.y))
                                if (piece.y - 1) >= 0:
                                    adjacent_places.append((piece.x, piece.y - 1))
                                if (piece.x - 1) >= 0:
                                    adjacent_places.append((piece.x - 1, piece.y))
                                if (piece.y + 1) < 9:
                                    adjacent_places.append((piece.x, piece.y + 1))
                                piece.island = self.places[x][y].island
                                landlist[piece.island].add_stone(piece)                       
                           
        for land in landlist[1:]:
            print "check\n"
            for space in land.stones:
                if space.x == 0 or space.x == 8 or space.y == 0 or space.y == 8:
                    edgecount = edgecount + 1
                    if edgecount > 1:
                        break
                if edgecount < 2:
                    adjacencies = []
                    if (space.x + 1) < 9:
                        adjacencies.append((space.x + 1, space.y))
                    if (space.y - 1) >= 0:
                        adjacencies.append((space.x, space.y - 1))
                    if (space.x - 1) >= 0:
                        adjacencies.append((space.x - 1, space.y))
                    if (space.y + 1) < 9:
                        adjacencies.append((space.x, space.y + 1))
                    for spot in adjacencies:
                        piece = self.places[place[0]][place[1]]
                        if piece != "Y":
                            if color:
                                if piece.color != color:
                                    check = True
                                    break
                            else:
                                color = piece.color
                    if not check:
                        if color == "B":
                            black.score = black.score + 1
                        else:
                            white.score = white.score + 1
                            
            else:
                continue
        self.freeze()
        self.endgame()


class Board:

    def __init__(self):
    # creates the board
        self.BS = int(H // 1.2)  # BS stands for board side
        BS = self.BS
        self.board = Canvas(window, width=BS, height=BS, bg="#DEB887", bd=5, relief=RIDGE)
        self.board.place(relx=0.5, rely=0.5, anchor=CENTER)
        # creates the grid of lines on the board
        G = BS / 10.0  # G stands for grid
        for line in range(1, 10):
            self.board.create_line(G, (G * line), 9 * G, (G * line), width=2)
            self.board.create_line((G * line), G, (G * line), 9 * G, width=2)
            # creates the diamonds on the grid
        UD = 3 * G  # UD stands for upper diamond
        LD = 7 * G  # LD stands for lower diamond
        DS = int(BS // 50)  # DS stands for diamond size
        self.board.create_polygon(UD, UD - DS, UD + DS, UD, UD, UD + DS, UD - DS, UD, fill="black")
        self.board.create_polygon(LD, UD - DS, LD + DS, UD, LD, UD + DS, LD - DS, UD, fill="black")
        self.board.create_polygon(UD, LD - DS, UD + DS, LD, UD, LD + DS, UD - DS, LD, fill="black")
        self.board.create_polygon(LD, LD - DS, LD + DS, LD, LD, LD + DS, LD - DS, LD, fill="black")
        M = int(BS // 2)  # M stands for middle
        self.board.create_polygon(M, M - DS, M + DS, M, M, M + DS, M - DS, M, fill="black")
        # creates the pieces on the board (they start out invisible)
        C = int(BS // 25)  # C stands for circle size
        self.intersect = [[None for x in range(9)] for x in range(9)]
        for dot_x in range(1, 10):
            for dot_y in range(1, 10):
                self.intersect[dot_x - 1][dot_y - 1] = self.board.create_oval(((G * dot_x) - C), ((G * dot_y) - C), ((G * dot_x) + C), ((G * dot_y) + C), fill="", outline="")

    def freeze(self):
        # disables the special cursor above the board
        self.board.config(cursor="arrow")
        # unbinds the buttons attached to each stone
        for dot_x in range(1, 10):
            for dot_y in range(1, 10):
                self.board.tag_unbind(self.intersect[dot_x - 1][dot_y - 1], "<Button-1>")

    def unfreeze(self):
        # makes each stone a button
        for dot_x in range(1, 10):
            for dot_y in range(1, 10):
                self.board.tag_bind(self.intersect[dot_x - 1][dot_y - 1], "<Button-1>", self.move)
                # sets a new cursor for the board
        self.board.config(cursor="tcross")

# places a stone
    def move(self, event):
            # grabs the location of the mouse when it was clicked, and through fancy division finds the stone location that was clicked
        BS = self.BS
        x = (event.x - int(BS//20)) // int(BS//10)
        y = (event.y - int(BS//20)) // int(BS//10)
            # fills the stone that was clicked depending on whose turn it was
        if not game.places[x][y]:
            if game.turn == "Black":
                self.board.itemconfig(self.intersect[x][y], fill="black")
                game.places[x][y] = Stone(x, y, "B")                        # calls the stone class
            else:
                self.board.itemconfig(self.intersect[x][y], fill="white")
                game.places[x][y] = Stone(x, y, "W")                        # calls the stone class
            game.play()     # changes whose turn it is
            game.places[x][y].effect()


class Bumper:

    def __init__(self, color, place):
        BW = int(W // 5.2)  # BW stands for bumper width
        BH = int(H // 1.3)  # BH stands for bumper height

        self.bumper = Canvas(window, width=BW, height=BH, bg="grey", bd=5, relief=GROOVE)
        self.bumper.place(relx=place, rely=0.5, anchor=CENTER)
        # displays text labels on bumper
        self.bumper.create_text(int(BW // 2.1), int(BH // 11.2), text=color, font=("helvetica", int(W // 22.8)), width=int(W // 6))
        self.bumper.create_text(int(BW // 1.9), int(BH // 3.6), text="Pieces Captured:", font=("helvetica", int(W // 45.6)), width=int(W // 4.5))
        self.bumper.create_text(int(BW // 3.8), int(BH // 1.5), text='Score:', font=("helvetica", int(W // 45.6)), width=int(W // 6))
        # displays the state of side
        if color == "White:":
            self.state = "(Waiting)"
        else:
            self.state = "(Moving)"
        self.current = self.bumper.create_text(int(BW // 2.6), int(BH // 6.4), text=self.state, font=("helvetica", int(W // 45.6)), width=int(W // 6))
        # displays the captured pieces
        self.capture = 0
        self.captured = self.bumper.create_text(int(BW // 2), int(BH // 2.2), text=str(self.capture), font=("helvetica", int(W // 15.2)), width=int(W // 6))
        # displays the score of side
        self.score = "TBD"
        self.scored = self.bumper.create_text(int(BW // 2), int(BH // 1.2), text=self.score, font=("helvetica", int(W // 15.2)), width=int(W // 6))

    def change_state(self):
        if self.state == "(Moving)":
            self.state = "(Waiting)"
        else:
            self.state = "(Moving)"
            # updates the displays on the board using tkinter methods
        self.update()

    def update(self):
        self.bumper.itemconfig(self.current, text=self.state)
        self.bumper.itemconfig(self.scored, text=self.score)


# creates button
class Clicker:

    def __init__(self, anchor, mesg, size, go_to, wide, place_x, place_y, high=H):
        self.click = Button(anchor, text=mesg, font=("helvetica", int(W//size)), bd=5, width=int(W//wide), height=int(H//high), command=go_to, cursor="hand2")
        self.click.place(relx=place_x, rely=place_y, anchor=CENTER)


def remove(*buttons):
    for button in buttons:
        button.click.destroy()


class Popup:

    def __init__(self, div_wid, div_high, title_high=1, title="", title_font=1):
        # displays the popup background
        self.PW = int(W // div_wid)  # stands for popup width
        self.PH = int(H // div_high)  # stands for popup height
        self.back = Canvas(window, width=self.PW, height=self.PH, bg="grey", bd=5, relief=RAISED)
        self.back.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.back.create_text(int(self.PW//2), int(self.PH//title_high), text=title, font=("helvetica", int(W//title_font)), width=W, justify=CENTER)


# establishes the game logic and determines when stones die; by Ben
class Stone:

    def __init__(self, x, y, c):
        self.x = x
        self.y = y
        self.color = c
        self.island = 0
        self.life = 0
        self.checked_shapes = []
        self.adjacent_places = []
        if (self.x + 1) < 9:
            self.adjacent_places.append((self.x + 1, self.y))
        if (self.y - 1) >= 0:
            self.adjacent_places.append((self.x, self.y-1))
        if (self.x - 1) >= 0:
            self.adjacent_places.append((self.x - 1, self.y))
        if (self.y + 1) < 9:
            self.adjacent_places.append((self.x, self.y + 1))
            
            

    def give_life(self):
        for piece in self.adjacent_places:
            if not game.places[piece[0]][piece[1]] and (piece not in shapelist[self.island].empty_pieces):
                shapelist[self.island].empty_pieces.append(piece)
                shapelist[self.island].shape_life = shapelist[self.island].shape_life + 1
        

    # this function checks the life of a piece
    def check_life(self):
        if self.life == 0:
            self.destroy()
        

    # this function checks the effect of a piece on other nearby pieces
    def effect(self):
        for place in self.adjacent_places:
            piece = game.places[place[0]][place[1]]
            if not piece:
                self.life = self.life + 1
            elif self.color == piece.color:
                piece.life = piece.life - 1
                if shapelist[piece.island]:
                    if shapelist[self.island] and self.island == piece.island:
                        continue
                        
                    elif shapelist[self.island] and self.island != piece.island:
                        holder = self.island
                        for stone in shapelist[self.island].stones:
                            stone.island = piece.island
                            shapelist[piece.island].add_stone(stone)
                        shapelist[holder] = None
                        
                    else:
                        self.island = piece.island
                        shapelist[piece.island].shape_life = shapelist[piece.island].shape_life - 1
                        shapelist[piece.island].add_stone(self)
                        
                else:
                    if shapelist[self.island]:
                        piece.island = self.island
                        shapelist[self.island].add_stone(piece)
                    else:
                        shapelist.append(Shape()) 
                        self.island = len(shapelist)-1
                        piece.island = self.island
                        shapelist[self.island].indexed = self.island
                        shapelist[self.island].add_stone(piece)
                        shapelist[self.island].add_stone(self)
                    
                     


                    
            else:
                # if the piece is in an island byt the placed stone has not subtracted a life from the shape
                if shapelist[piece.island] and (piece.island not in self.checked_shapes):
                    self.checked_shapes.append(piece.island)
                    shapelist[piece.island].shape_life = shapelist[piece.island].shape_life - 1
                    shapelist[piece.island].check_life()

                # if the piece is in an island but the placed stone has already subtracted a life from the shape
                elif shapelist[piece.island] and (piece.island in self.checked_shapes):
                    piece.life = piece.life - 1
                    
                else:
                    # only if the piece is the opposite color
                    piece.life = piece.life - 1
                    piece.check_life()
                
                
        if shapelist[self.island]:
            shapelist[self.island].check_life()
        else:
            self.check_life()
        screenshot.update()
        screenshot.create_image()
        
        
        
        #check spaces around it if its empty then add breath
        #if opposite collor
        # then check its breathes if its the same color group into shape
        # if it encouters a stone adjancent it auto loses a life        

    # this  function reverts a stone to an empty space
    def destroy(self):
        del self.checked_shapes[:]
        for place in self.adjacent_places:
            piece = game.places[place[0]][place[1]]
            if piece:
                piece.life = piece.life + 1
                if shapelist[piece.island] and (piece.island not in self.checked_shapes):
                    shapelist[piece.island].shape_life = shapelist[piece.island].shape_life + 1
                    self.checked_shapes.append(piece.island)
        if self.color == "W":
            black.capture = black.capture + 1
            black.bumper.itemconfig(black.captured, text=black.capture)
        else:
            white.capture = white.capture + 1
            white.bumper.itemconfig(white.captured, text=white.capture)
        go.board.itemconfig(go.intersect[self.x][self.y], fill="")
        game.places[self.x][self.y] = None
        # add a life to the shape around it 


# a datatype for groups of adjacent stones that are the same color, therefore sharing breaths; by Ben
class Shape(Stone): 

    def __init__(self):
        self.stones = []
        self.shape_life = 0
        self.empty_pieces = []
        # creates list
        
        
            
    def add_stone(self, stone):
        self.stones.append(stone)
        if stone.color != "Y":
            stone.give_life()
        # adds to list

    def check_life(self):
        print self.shape_life
        if self.shape_life == 0:
            self.destroy_shape()
            
        # goes through list and runs life on each stone

    def destroy_shape(self):
        for parts in self.stones:
            parts.destroy()

        

# a datatype for enforcing the ko rule
class Gamestate:
    def __init__(self):
        self.preimage = []
        self.image = []
        for j in range (81):
            self.preimage.append("T")
    def create_image(self):
        self.image = []
        for y in range(9):
            for x in range(9):
                if game.places[x][y]:
                    self.image.append(game.places[x][y].color)
                else:
                    self.image.append("T")
    def update(self):
        self.preimage = self.image

    


mainmenu()
mainloop()
