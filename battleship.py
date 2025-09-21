"""
15-110 - Battleship Project
Name: Freya Zhai
AndrewID: siyuanzh
"""

import battleship_tests as test

project = "Battleship" # don't edit this

### SIMULATION FUNCTIONS ###

from tkinter import *
import random

EMPTY_UNCLICKED = 1
SHIP_UNCLICKED = 2
EMPTY_CLICKED = 3
SHIP_CLICKED = 4


'''
makeModel(data)
Parameters: dict mapping strs to values
Returns: None
'''
def makeModel(data):
    data["row"] = 10
    data["col"] = 10
    data["board"] = 500
    data["cell"] = 50
    data["shipNumUser"] = 0
    data["shipNumComp"] = 5
    data["userBoard"] = emptyGrid(data["row"], data["col"])
    data["compBoard"] = emptyGrid(data["row"], data["col"])
    data["compBoard"] = addShips(data["compBoard"], data["shipNumComp"])
    data["tmpShip"] = []
    data["maxShip"] = 5
    data["winner"] = None
    data["maxTurn"] = 50
    data["currentTurn"] = 0
    return


'''
makeView(data, userCanvas, compCanvas)
Parameters: dict mapping strs to values ; Tkinter canvas ; Tkinter canvas
Returns: None
'''
def makeView(data, userCanvas, compCanvas):
    drawGrid(data, userCanvas, data["userBoard"], True)
    drawGrid(data, compCanvas, data["compBoard"], False)
    drawShip(data, userCanvas, data["tmpShip"])
    drawGameOver(data, userCanvas)
    return


'''
keyPressed(data, events)
Parameters: dict mapping strs to values ; key event object
Returns: None
'''
def keyPressed(data, event):
    if event.keysym == "Return":
        makeModel(data)
    pass


'''
mousePressed(data, event, board)
Parameters: dict mapping strs to values ; mouse event object ; 2D list of ints
Returns: None
'''
def mousePressed(data, event, board):
    if data["winner"] != None:
        return
    coord = getClickedCell(data, event)
    row = coord[0]
    col = coord[1]
    if board == "user":
        clickUserBoard(data, row, col)
    else:
        if data["shipNumUser"] == data["maxShip"]:
            runGameTurn(data, row, col)
    

#### WEEK 1 ####

'''
emptyGrid(rows, cols)
#1 [Check6-1]
Parameters: int ; int
Returns: 2D list of ints
'''
def emptyGrid(rows, cols):
    grid = []
    for i in range(rows):
        grid.append([EMPTY_UNCLICKED]*cols)
    return grid


'''
createShip()
#2 [Check6-1]
Parameters: no parameters
Returns: 2D list of ints
'''
def createShip():
    ship = []
    col = random.randint(1,8)
    row = random.randint(1,8)
    direction = random.randint(0,1)
    if direction == 1:
        location1 = [row-1, col]
        location2 = [row, col]
        location3 = [row+1, col]
    else:
        location1 = [row, col-1]
        location2 = [row, col]
        location3 = [row, col+1]
    ship = [location1, location2, location3]
    return ship


'''
checkShip(grid, ship)
#3 [Check6-1]
Parameters: 2D list of ints ; 2D list of ints
Returns: bool
'''
def checkShip(grid, ship):
    for i in range(len(ship)):
        row = ship[i][0]
        col = ship[i][1]
        if grid[row][col] != EMPTY_UNCLICKED:
            return False
    return True


'''
addShips(grid, numShips)
#4 [Check6-1]
Parameters: 2D list of ints ; int
Returns: 2D list of ints
'''
def addShips(grid, numShips):
    count = 0
    while count < 3*numShips:
        ship = createShip()
        if checkShip(grid, ship) == True:
            for i in range(len(ship)):
                n = ship[i][0]
                m = ship[i][1]               
                grid[n][m] = SHIP_UNCLICKED
                count = count + 1
    return grid


'''
drawGrid(data, canvas, grid, showShips)
Parameters: dict mapping strs to values ; Tkinter canvas ; 2D list of ints ; bool
Returns: None
'''
def drawGrid(data, canvas, grid, showShips):
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == SHIP_UNCLICKED:
                if showShips == False:
                    color = "blue"
                else:
                    color = "yellow"
            elif grid[i][j] == EMPTY_UNCLICKED:
                color = "blue"
            elif grid[i][j] == SHIP_CLICKED:
                color = "red"
            elif grid[i][j] == EMPTY_CLICKED:
                color = "white"
            canvas.create_rectangle(data["cell"]*j, data["cell"]*i, data["cell"]*(j+1), data["cell"]*(i+1), fill = color)
    return


### WEEK 2 ###

'''
isVertical(ship)
#1 [Check6-2]
Parameters: 2D list of ints
Returns: bool
'''
def isVertical(ship):
    ship.sort()
    if ship[0][1] == ship[1][1] and ship[1][1] ==ship[2][1]:
        if abs(ship[0][0] - ship[1][0]) == 1 and abs(ship[1][0] - ship[2][0]) == 1:
            return True
        else:
            return False
    else:
        return False

  

'''
isHorizontal(ship)
#1 [Check6-2]
Parameters: 2D list of ints
Returns: bool
'''
def isHorizontal(ship):
    ship.sort()
    if ship[0][0] == ship[1][0] and ship[1][0] ==ship[2][0]:
        if abs(ship[0][1] - ship[1][1]) == 1 and abs(ship[1][1] - ship[2][1]) == 1:
            return True
        else:
            return False
    else:
        return False


'''
getClickedCell(data, event)
#2 [Check6-2]
Parameters: dict mapping strs to values ; mouse event object
Returns: list of ints
'''
def getClickedCell(data, event):
    col = event.x
    row = event.y
    click = []
    if row <=499 and col <=499:
        click.append(row // data["cell"])
        click.append(col // data["cell"])
        return click       



'''
drawShip(data, canvas, ship)
#3 [Check6-2]
Parameters: dict mapping strs to values ; Tkinter canvas; 2D list of ints
Returns: None
'''
def drawShip(data, canvas, ship):
    cellsize = data["cell"]
    for coordinate in ship:
        top = coordinate[0]*cellsize
        left = coordinate[1]*cellsize
        canvas.create_rectangle(left, top, left + cellsize, top + cellsize, fill = "white")
    return



'''
shipIsValid(grid, ship)
#4 [Check6-2]
Parameters: 2D list of ints ; 2D list of ints
Returns: bool
'''
def shipIsValid(grid, ship):
    return (isVertical(ship) or isHorizontal(ship)) and checkShip(grid, ship)


'''
placeShip(data)
#4 [Check6-2]
Parameters: dict mapping strs to values
Returns: None
'''
def placeShip(data):
    grid = data["userBoard"]
    ship = data["tmpShip"]
    if shipIsValid(grid,ship) == True:
        for coordinate in data["tmpShip"]:
            data["userBoard"][coordinate[0]][coordinate[1]] = SHIP_UNCLICKED
        data["shipNumUser"] = data["shipNumUser"] + 1
    else:
        print("Sorry, the ship is not valid.")
    data["tmpShip"] = []
    return


'''
clickUserBoard(data, row, col)
#4 [Check6-2]
Parameters: dict mapping strs to values ; int ; int
Returns: None
'''
def clickUserBoard(data, row, col):
    if data["shipNumUser"] == data["maxShip"]:
        print("You have add max number of ships.")
        return
    else:        
        for coord in data["tmpShip"]:
            if row == coord[0] and col == coord[1]:
                return
        data["tmpShip"].append([row,col])
        if len(data["tmpShip"]) == 3:
            placeShip(data)
        if data["shipNumUser"] == data["maxShip"]:
            print("You have add max number of ships. Please start the game!")
            return


### WEEK 3 ###

'''
updateBoard(data, board, row, col, player)
Parameters: dict mapping strs to values ; 2D list of ints ; int ; int ; str
Returns: None
'''
def updateBoard(data, board, row, col, player):
    if board[row][col] == SHIP_UNCLICKED:
        board[row][col] = SHIP_CLICKED
    elif board[row][col] == EMPTY_UNCLICKED:
        board[row][col] = EMPTY_CLICKED
    if isGameOver(board) == True:
        data["winner"] = player
    return


'''
runGameTurn(data, row, col)
Parameters: dict mapping strs to values ; int ; int
Returns: None
'''
def runGameTurn(data, row, col):
    if data["compBoard"][row][col] == SHIP_CLICKED or data["compBoard"][row][col] == EMPTY_CLICKED:
        return
    else:
        board = data["compBoard"]
        updateBoard(data, board, row, col, "user")
    coord = getComputerGuess(board)
    row = coord[0]
    col = coord[1]
    board = data["userBoard"]
    updateBoard(data, board, row, col, "comp")
    data["currentTurn"] += 1
    if data["currentTurn"] == data["maxTurn"]:
        data["winner"] = "draw" 
    return
    


'''
getComputerGuess(board)
Parameters: 2D list of ints
Returns: list of ints
'''
def getComputerGuess(board):
    row = random.randint(0,9)
    col = random.randint(0,9)
    while board[row][col] == EMPTY_CLICKED:
        row = random.randint(0,9)
        col = random.randint(0,9)
    return [row,col]


'''
isGameOver(board)
Parameters: 2D list of ints
Returns: bool
'''
def isGameOver(board):
    for i in range(len(board)):
        if SHIP_UNCLICKED in board[i]:
            return False
    return True
    


'''
drawGameOver(data, canvas)
Parameters: dict mapping strs to values ; Tkinter canvas
Returns: None
'''
def drawGameOver(data, canvas):
    if data["winner"] == "user":
        canvas.create_text(250, 125, fill = "orange", font=('Helvetica 50 bold'), text = "YOU WIN!")    
        canvas.create_text(250, 200, fill = "orange", font=('Helvetica 27 bold'), text = "Press Enter to play again.")
    elif data["winner"] == "comp":
        canvas.create_text(250, 125, fill = "orange", font=('Helvetica 50 bold'), text = "YOU LOST! ")        
        canvas.create_text(250, 200, fill = "orange", font=('Helvetica 27 bold'), text = "Press Enter to play again.")
    elif data["winner"] == "draw":
        canvas.create_text(250, 125, fill = "orange", font=('Helvetica 13 bold'), text = "You have run out of moves and have reached a draw.")
        canvas.create_text(250, 200, fill = "orange", font=('Helvetica 27 bold'), text = "Press Enter to play again.")
    return


### SIMULATION FRAMEWORK ###

from tkinter import *

def updateView(data, userCanvas, compCanvas):
    userCanvas.delete(ALL)
    compCanvas.delete(ALL)
    makeView(data, userCanvas, compCanvas)
    userCanvas.update()
    compCanvas.update()

def keyEventHandler(data, userCanvas, compCanvas, event):
    keyPressed(data, event)
    updateView(data, userCanvas, compCanvas)

def mouseEventHandler(data, userCanvas, compCanvas, event, board):
    mousePressed(data, event, board)
    updateView(data, userCanvas, compCanvas)

def runSimulation(w, h):
    data = { }
    makeModel(data)

    root = Tk()
    root.resizable(width=False, height=False) # prevents resizing window

    # We need two canvases - one for the user, one for the computer
    Label(root, text = "USER BOARD - click cells to place ships on your board.").pack()
    userCanvas = Canvas(root, width=w, height=h)
    userCanvas.configure(bd=0, highlightthickness=0)
    userCanvas.pack()

    compWindow = Toplevel(root)
    compWindow.resizable(width=False, height=False) # prevents resizing window
    Label(compWindow, text = "COMPUTER BOARD - click to make guesses. The computer will guess on your board.").pack()
    compCanvas = Canvas(compWindow, width=w, height=h)
    compCanvas.configure(bd=0, highlightthickness=0)
    compCanvas.pack()

    makeView(data, userCanvas, compCanvas)

    root.bind("<Key>", lambda event : keyEventHandler(data, userCanvas, compCanvas, event))
    compWindow.bind("<Key>", lambda event : keyEventHandler(data, userCanvas, compCanvas, event))
    userCanvas.bind("<Button-1>", lambda event : mouseEventHandler(data, userCanvas, compCanvas, event, "user"))
    compCanvas.bind("<Button-1>", lambda event : mouseEventHandler(data, userCanvas, compCanvas, event, "comp"))

    updateView(data, userCanvas, compCanvas)

    root.mainloop()


### RUN CODE ###

# This code runs the test cases to check your work
if __name__ == "__main__":
    print("\n" + "#"*15 + " WEEK 1 TESTS " +  "#" * 16 + "\n")
    test.week1Tests()

    ## Uncomment these for Week 2 ##
    
    print("\n" + "#"*15 + " WEEK 2 TESTS " +  "#" * 16 + "\n")
    test.week2Tests()
    

    ## Uncomment these for Week 3 ##
    
    print("\n" + "#"*15 + " WEEK 3 TESTS " +  "#" * 16 + "\n")
    test.week3Tests()
    

    ## Finally, run the simulation to test it manually ##
    runSimulation(500, 500)
