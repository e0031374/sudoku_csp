import sys
import copy

# Running script: given code can be run with the command:
# python file.py, ./path/to/init_state.txt ./output/output.txt

class Sudoku(object):
    def __init__(self, puzzle):
        # you may add more attributes if you need
        self.puzzle = puzzle # self.puzzle is a list of lists
        self.ans = copy.deepcopy(puzzle) # self.ans is a list of lists

        # user added
        self.legalSet = copy.deepcopy(initCalcLegalSet(puzzle))

    def solve(self):
        # TODO: Write your code here

        #print(calcConstrainingValue(self.ans, 0, 1))
        #print(getNextVar(self.ans))
        ##print findLegalValues(self.ans, 0, 0)
        #legalSet = initCalcLegalSet(self.ans)
        #printGrid(legalSet)
        #print(hasLegalAss(legalSet))
        
        self.ans = self.backtrack(self.ans, self.legalSet)
        
        # self.ans is a list of lists
        return self.ans

    def backtrack(self, puzzle, legalSet):
        # def copy
        mypuzzle = copy.deepcopy(puzzle)
        mylegalSet = copy.deepcopy(legalSet)
        
        nextVarTuple = getNextVar(mypuzzle) 
        if (nextVarTuple[2] == -1):
            # success
            return mypuzzle
        row = nextVarTuple[0]
        col = nextVarTuple[1]
        print("r: " + str(row) + ", c: " + str(col))

        legalValues = mylegalSet[row][col]

        for v in legalValues:
            print("r: " + str(row) + ", c: " + str(col) + ", value: " + str(v))
            if True:
                iterpuzzle = copy.deepcopy(mypuzzle)
                iterlegalSet = copy.deepcopy(mylegalSet)
                iterpuzzle[row][col] = v
                iterlegalSet = recalcLegalSet(iterpuzzle, iterlegalSet)

                canContinue = hasLegalAss(iterlegalSet)
                if canContinue:
                    nextStage = self.backtrack(iterpuzzle, iterlegalSet)
                    if nextStage:
                        return nextStage
            #else:
        
        return False
        

    # you may add more classes/functions if you think is useful
    # However, ensure all the classes/functions are in this file ONLY
    # Note that our evaluation scripts only call the solve method.
    # Any other methods that you write should be used within the solve() method.


def getTestGrid():
    testGrid = [[-1 for i in range(9)] for j in range(9)]
    for r in range(9):
        for c in range(9):
            testGrid[r][c] = r
    return testGrid
        

def printGrid(grid):
    for r in range(9):
        print(grid[r])
    

def printLegalSet(grid):
    for r in range(9):
        print("Row: " + str(r))
        print(grid[r])
        #for c in range(9):
        #    print(grid[r][c])

# returns boolean given legalSet, False if any cell has no remaining legal moves
def hasLegalAss(legalSet): 
    for r in range(9):
        for c in range(9):
            cellLegalAssValues = legalSet[r][c]
            if len(cellLegalAssValues) <= 0:
                print("no legal at r: " + str(r) + ", c: " + str(c))
                return False
    return True

# for initial use only
def initCalcLegalSet(puzzle):
    legalSet = [[-1 for i in range(9)] for j in range(9)]
    for r in range(9):
        for c in range(9):
            legalSet[r][c] = findLegalValues(puzzle, r, c)
    return legalSet

# given existing legalSet, ensure any newer non legal values are removed
def recalcLegalSet(puzzle, inputLegalSet):
    outputLegalSet = copy.deepcopy(inputLegalSet)
    for r in range(9):
        for c in range(9):
            existingCellLegalValues = outputLegalSet[r][c]
            newCellLegalValues = findLegalValues(puzzle, r, c)
            reducedCellLegalValues = list(filter(lambda x: x in newCellLegalValues, existingCellLegalValues))
            outputLegalSet[r][c] = reducedCellLegalValues
    return outputLegalSet


# returns list of legal values for a specific given cell coords
def findLegalValues(puzzle, row, col):
    xs = [i+1 for i in range(9)] # start with list of 1..9
    currVal = puzzle[row][col]
    if currVal > 0:
        return [currVal]

    #for x in xs:
    #    print(x)

    for c in range(9):
        tmpVal = puzzle[row][c]
        if tmpVal > 0:
            xs = list(filter(lambda x: x != tmpVal, xs))

    for r in range(9):
        tmpVal = puzzle[r][col]
        if tmpVal > 0:
            xs = list(filter(lambda x: x != tmpVal, xs))

    subGridRow = row // 3
    subGridCol = col // 3
    for gr in range(3):
        for gc in range(3):
            #print("subGridRow: " + str(gr + subGridRow * 3) + ", subGridCol: " + str(gc + subGridCol * 3))
            tmpVal = puzzle[gr + subGridRow * 3][gc + subGridCol * 3]
            if tmpVal > 0:
                xs = list(filter(lambda x: x != tmpVal, xs))
                #print("tmpVal" + str(tmpVal) + " , xs: " + str(xs))
    return xs


# gets the most constraining variable to process next
# returns [2] = -1 for no next var
def getNextVar(puzzle):
    row = -1 
    col = -1 
    maxVal = -1

    for r in range(9):
        for c in range(9):
            cellVal = puzzle[r][c]
            if (cellVal > 0):
                continue # cell is not blank
            else:
                cellConstrainingVal = calcConstrainingValue(puzzle, r, c)
                if cellConstrainingVal > maxVal:
                    maxVal = cellConstrainingVal
                    row = r
                    col = c
                else:
                    continue
    return (row, col, maxVal)

def calcConstrainingValue(puzzle, row, col):
    #note, points can start from zero
    # also note i am triple counting the same zero here, but it cancels out promise
    val = puzzle[row][col]

    # cell is not blank no action required
    if (val > 0):
        return -1

    # count zeroes in column
    colCount = 0
    for c in range(9):
        tmpVal = puzzle[row][c]
        if tmpVal == 0:
            colCount = colCount + 1

    rowCount = 0
    for r in range(9):
        tmpVal = puzzle[r][col]
        if tmpVal == 0:
            rowCount = rowCount + 1

    gridCount = 0
    subGridRow = row // 3
    subGridCol = col // 3

    #print("SubGrid")
    for gr in range(3):
        for gc in range(3):
            #print("subGridRow: " + str(gr + subGridRow * 3) + ", subGridCol: " + str(gc + subGridCol * 3))
            tmpVal = puzzle[gr + subGridRow * 3][gc + subGridCol * 3]
            if tmpVal == 0:
                gridCount = gridCount + 1
    #print("subGridRow: " + str(subGridRow) + " subGridCol: " + str(subGridCol))
    return rowCount + colCount + gridCount




if __name__ == "__main__":
    # STRICTLY do NOT modify the code in the main function here
    if len(sys.argv) != 3:
        print ("\nUsage: python CS3243_P2_Sudoku_XX.py input.txt output.txt\n")
        raise ValueError("Wrong number of arguments!")

    try:
        f = open(sys.argv[1], 'r')
    except IOError:
        print ("\nUsage: python CS3243_P2_Sudoku_XX.py input.txt output.txt\n")
        raise IOError("Input file not found!")

    puzzle = [[0 for i in range(9)] for j in range(9)]
    lines = f.readlines()

    i, j = 0, 0
    for line in lines:
        for number in line:
            if '0' <= number <= '9':
                puzzle[i][j] = int(number)
                j += 1
                if j == 9:
                    i += 1
                    j = 0

    sudoku = Sudoku(puzzle)
    ans = sudoku.solve()

    with open(sys.argv[2], 'a') as f:
        for i in range(9):
            for j in range(9):
                f.write(str(ans[i][j]) + " ")
            f.write("\n")
