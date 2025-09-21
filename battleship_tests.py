from battleship import *

### SUPPLEMENTAL TEST FUNCTIONS ###

def testGrid(): 
    grid = [ [1] * 10 for row in range(10) ]
    grid[0][2] = 2
    grid[0][3] = 2
    grid[0][4] = 2
    grid[2][7] = 2
    grid[3][7] = 2
    grid[4][7] = 2
    return grid
    print("... done!")

def testShip():
    return [ [5, 4], [5, 5], [5, 6] ]




def testEmptyGrid():
    print("Testing emptyGrid()...", end="")
    assert(emptyGrid(5, 5) == [ [1,1,1,1,1],
                                [1,1,1,1,1],
                                [1,1,1,1,1],
                                [1,1,1,1,1],
                                [1,1,1,1,1] ])
    assert(emptyGrid(4, 6) == [ [1,1,1,1,1,1],
                                [1,1,1,1,1,1],
                                [1,1,1,1,1,1],
                                [1,1,1,1,1,1] ])
    assert(emptyGrid(0, 0) == [ ])

    # Make sure that the grid doesn't have any aliasing problems
    g = emptyGrid(3, 3)
    g[0][1] = "foo"
    assert(g[1][1] != "foo")
    g = emptyGrid(8, 8)
    g[4][7] = "bar"
    assert(g[6][7] != "bar")
    print("... done!")

def testCreateShip():
    print("Testing createShip()...", end="")
    ship = createShip()
    assert(type(ship) == list)
    assert(len(ship) == 3)
    ship.sort()
    # All in same row/col
    assert((ship[0][0] == ship[1][0] == ship[2][0]) or \
        (ship[0][1] == ship[1][1] == ship[2][1]))
    # All connected
    assert((ship[0][0] + 1 == ship[1][0] == ship[2][0] - 1) or \
        (ship[0][1] + 1 == ship[1][1] == ship[2][1] - 1))

    # When 100 ships are generated, each center row (for vertical ships)
    # and center col (for horizontal ships) in the range [1, 8] should
    # occur at least once
    centerRows = [0] * 9
    centerCols = [0] * 9
    for i in range(100):
        ship = createShip()
        ship.sort()
        # Horizontal
        if (ship[0][0] == ship[1][0] == ship[2][0]):
            assert(1 <= ship[1][1] <= 8) # center col is legal
            centerCols[ship[1][1]] += 1
        # Vertical
        elif (ship[0][1] == ship[1][1] == ship[2][1]):
            assert(1 <= ship[1][0] <= 8) # center row is legal
            centerRows[ship[1][0]] += 1
        else:
            print("Found bad ship:", ship)
            assert(False) # found a ship that is neither horizontal nor vertical
    for index in range(1, 9): # [1, 8]
        assert(centerCols[index] > 0) # all center cols in [1, 8] possible
        assert(centerRows[index] > 0) # all center rows in [1, 8] possible

    print("... done!")

def testCheckShip():
    print("Testing checkShip()...", end="")
    grid = [ [1, 1, 2, 1], [1, 1, 2, 1], [1, 1, 2, 1], [2, 2, 2, 1] ]
    assert(checkShip(grid, [[0, 0], [1, 0], [2, 0]]) == True)
    assert(checkShip(grid, [[0, 2], [1, 2], [2, 2]]) == False)
    assert(checkShip(grid, [[1, 1], [2, 1], [3, 1]]) == False)

    grid2 = [ [1] * 10 for row in range(10) ]
    grid2[5][4] = grid2[5][5] = grid2[5][6] = 2
    grid2[7][8] = grid2[8][8] = grid2[9][8] = 2
    assert(checkShip(grid2, [[5, 4], [5, 5], [5, 6]]) == False)
    assert(checkShip(grid2, [[9, 5], [9, 7], [9, 8]]) == False)
    assert(checkShip(grid2, [[4, 5], [5, 5], [6, 5]]) == False)
    assert(checkShip(grid2, [[5, 8], [6, 8], [7, 8]]) == False)
    assert(checkShip(grid2, [[5, 7], [6, 7], [7, 7]]) == True)

    print("... done!")

def testAddShips():
    print("Testing addShips()...", end="")
    grid = [ [1] * 10 for row in range(10) ]
    grid2 = addShips(grid, 2)
    count = 0
    for row in grid2:
        for cell in row:
            if cell == 2:
                count += 1
    assert(count == 6) # Two ships should take up 6 cells total

    grid = [ [1] * 10 for row in range(10) ]
    grid5 = addShips(grid, 5)
    count = 0
    for row in grid5:
        for cell in row:
            if cell == 2:
                count += 1
    assert(count == 15) # Five ships should take up 15 cells total

    grid = [ [2] * 10 for row in range(10) ]
    grid[8][1] = grid[8][2] = grid[8][3] = 1 # only one open location
    gridAll = addShips(grid, 1)
    count = 0
    for row in gridAll:
        for cell in row:
            if cell == 2:
                count += 1
    assert(count == 100)
    print("... done!")

def testMakeModel():
    print("Testing makeModel()...", end="")
    data = { }
    makeModel(data)
    values = data.values()
    assert(10 in values) # have you stored the number of rows and cols?
    assert(500 in values) # have you stored the board size?
    assert(5 in values) # have you stored the number of ships?
    listCount = 0
    for value in values:
        if type(value) == list:
            listCount += 1
    assert(listCount >= 2) # have you set up grids for both the user and the enemy?
    print("... done!")

def testDrawGrid():
    print("Testing drawGrid()...")
    print("TEMPORARILY SET YOUR USER GRID TO test.testGrid()")
    print("THEN CHECK WHETHER THE CANVAS SHOWS THE PICTURE IN THE WRITEUP")
    print("... done!")

def week1Tests():
    testEmptyGrid()
    testCreateShip()
    testCheckShip()
    testAddShips()
    testMakeModel()
    testDrawGrid()



def testIsVertical():
    print("Testing isVertical()...", end="")
    assert(isVertical([ [0, 1], [1, 1], [2, 1] ]) == True)
    assert(isVertical([ [2, 1], [0, 1], [1, 1] ]) == True) # order doesn't matter
    assert(isVertical([ [1, 0], [1, 1], [1, 2] ]) == False)
    assert(isVertical([ [0, 7], [1, 7], [3, 7] ]) == False) # must be sequential
    assert(isVertical([ [1, 0], [3, 0], [5, 0] ]) == False)
    assert(isVertical([ [1, 0], [3, 2], [0, 1] ]) == False)
    assert(isVertical([ [4, 5], [5, 5], [6, 5] ]) == True)
    assert(isVertical([ [3, 6], [4, 5], [5, 4] ]) == False) # diagonals don't work!
    assert(isVertical([ [3, 0], [1, 0], [5, 0] ]) == False) # checks for ships in a X_X_X configuration to not pass
    assert(isVertical([ [1, 0], [3, 0], [5, 0] ]) == False) # checks for ships in a X_X_X configuration to not pass
    print("... done!")

def testIsHorizontal():
    print("Testing isHorizontal()...", end="")
    assert(isHorizontal([ [1, 0], [1, 1], [1, 2] ]) == True)
    assert(isHorizontal([ [1, 2], [1, 0], [1, 1] ]) == True) # order doesn't matter
    assert(isHorizontal([ [0, 1], [1, 1], [2, 1] ]) == False)
    assert(isHorizontal([ [0, 0], [0, 1], [0, 3] ]) == False) # must be sequential
    assert(isHorizontal([ [7, 1], [7, 3], [7, 5] ]) == False)
    assert(isHorizontal([ [0, 1], [2, 3], [1, 0] ]) == False)
    assert(isHorizontal([ [5, 4], [5, 5], [5, 6] ]) == True)
    assert(isHorizontal([ [3, 6], [4, 5], [5, 4] ]) == False) # diagonals don't work!
    assert(isHorizontal([ [7, 3], [7, 1], [7, 5] ]) == False) # checks for ships in a X_X_X configuration to not pass
    assert(isHorizontal([ [7, 1], [7, 3], [7, 5] ]) == False) # checks for ships in a X_X_X configuration to not pass
    print("... done!")

def testGetClickedCell():
    print("Testing getClickedCell()...", end="")
    data = { }
    makeModel(data)
    class Struct():
        pass
    event = Struct()
    event.x = 140
    event.y = 321
    # Note that y corresponds to row, and x corresponds to col
    assert(getClickedCell(data, event) == [6, 2])
    event.x = 499
    event.y = 1
    assert(getClickedCell(data, event) == [0, 9])
    # Make sure to get edges right! 200 could go either way
    event.x = 201
    event.y = 199
    assert(getClickedCell(data, event) == [3, 4])
    print("... done!")

def testDrawShip():
    print("Testing drawShip()...")
    print("TEMPORARILY SET YOUR USER GRID TO test.testShip()")
    print("THEN CHECK WHETHER THE CANVAS SHOWS THE PICTURE IN THE WRITEUP")
    print("... done!")

def testShipIsValid():
    print("Testing shipIsValid()...", end="")
    grid = [ [1] * 10 for row in range(10) ]
    grid[0][1] = 2

    # can't place a ship that overlaps the board
    ship = [ [0, 1], [1, 1], [2, 1] ]
    assert(shipIsValid(grid, ship) == False)
    grid[0][1] = 1
    grid[1][1] = 2
    assert(shipIsValid(grid, ship) == False)
    grid[1][1] = 1
    grid[2][1] = 2
    assert(shipIsValid(grid, ship) == False)
    grid[2][1] = 1
    grid[9][9] = 2
    assert(shipIsValid(grid, ship) == True) # no overlap!

    # can't place a ship that isn't horizontal or vertical
    ship = [ [0, 1], [2, 3], [5, 6] ]
    assert(shipIsValid(grid, ship) == False)
    print("... done!")

def week2Tests():
    testIsVertical()
    testIsHorizontal()
    testGetClickedCell()
    testDrawShip()
    testShipIsValid()


def testUpdateBoard():
    print("Testing updateBoard()...", end="")
    data = { }
    makeModel(data)
    class Struct():
        pass

    board = [ [1] * 10 for row in range(10) ]
    board[4][3] = 2
    board[8][5] = 2
    updateBoard(data, board, 2, 1, "user")
    assert(board[2][1] == 3)
    updateBoard(data, board, 7, 4, "comp")
    assert(board[7][4] == 3)
    updateBoard(data, board, 4, 3, "user")
    assert(board[4][3] == 4)
    updateBoard(data, board, 8, 5, "comp")
    assert(board[8][5] == 4)
    print("... done!")

def testGetComputerGuess():
    print("Testing getComputerGuess()...", end="")
    # You can guess anywhere on an empty board
    board = [ [1] * 10 for row in range(10) ]
    guess = getComputerGuess(board)
    assert(len(guess) == 2 and 0 <= guess[0] < 10 and 0 <= guess[1] < 10)

    # If the board is full except for one spot, you need to guess that one
    board = [ [3] * 10 for row in range(10) ]
    board[3][6] = 1
    assert(getComputerGuess(board) == [3, 6])
    print("... done!")

def testIsGameOver():
    print("Testing isGameOver()...", end="")
    board = [ [3] * 10 for row in range(10) ]
    board[4][3] = 4
    board[5][3] = 4
    board[6][3] = 4
    assert(isGameOver(board) == True)
    board[3][5] = 1
    assert(isGameOver(board) == True) # cells can be unclicked if they aren't ships
    board[7][9] = 2
    assert(isGameOver(board) == False) # even one ship left means the game isn't over!
    print("... done!")

def testDrawGameOver():
    print("Testing drawGameOver()...")
    print("TEMPORARILY SET YOUR WINNER VARIABLE TO 'user'")
    print("THEN CHECK WHETHER THE CANVAS DISPLAYS THE APPROPRIATE MESSAGE")
    print("REPEAT BY SETTING THE WINNER VARIABLE TO 'comp'")
    print("... done!")

def week3Tests():
    testUpdateBoard()
    testGetComputerGuess()
    testIsGameOver()
    testDrawGameOver()
