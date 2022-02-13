"""
Meghan Dowell
CS7375 OL
Assignment 1 (8 Puzzle)
02/13/2022
"""
import random

import mdowell_utils


# function to generate and return a random board
def generatePuzzle() -> [[]]:
    usedVals = []  # keep track of which numbers have already been used
    randState = [[0] * 3 for row in range(3)]  # create a new 2D array with 3 columns and 3 rows

    for i, row in enumerate(randState):  # loop through each row in the array
        for j, column in enumerate(row):  # loop through each column
            # generate a random number 0 <= n <= 8 that has not already been used
            num = random.choice([n for n in range(0, 9) if n not in usedVals])
            usedVals.append(num)  # record that this number has been used
            randState[i][j] = num  # set the generated number to this location

    return randState  # return the generated puzzle


# function to print puzzle board
def printPuzzle(puzzleBoard):
    for row in puzzleBoard:  # loop through row
        for column in row:  # loop through columns in the row
            print(column, end=" ")  # print the column and a space
        print()  # new line between rows


# function to print the solution and information
def printSolution(puzzleSolution):
    # inform user and quit if the puzzle is unsolvable - CHANGE THIS
    if puzzleSolution[0] is None:
        print("Solution could not be found, looked through " + str(puzzleSolution[1]) + " configurations")
        quit()

    finalNode = puzzleSolution[0]  # get the final node from the solution
    lineage = mdowell_utils.backTrace(finalNode)  # use the final node to trace the solution from end to beginning

    # go through the lineage and display each state, cost, and move
    movements = ""
    while lineage:
        p = lineage.pop()  # get state in list
        if p.lastMove is not None:  # if the board has a previous move (not the starting node), display what the move is
            print("move " + p.lastMove + ": ")
            movements += p.lastMove + ", "
        printPuzzle(p.value.state)  # print the node's puzzle
        print()

    print("Went through " + str(
        puzzleSolution[
            1]) + " different configurations.")  # display how many configurations were seen before reaching the goal
    print(movements)
    if len(puzzleSolution) > 2:  # if UCS was used, solution will have a third item for the cost
        print("total cost: " + str(puzzleSolution[2]))  # print the total cost to get to this node


# region Problem Setup

treeUtils = mdowell_utils.BinaryTreeUtils()  # create the tree utils

goal = [[1, 2, 3], [8, 0, 4], [7, 6, 5]]  # 2d array for the puzzle solution
#puzzle = [[1, 3, 4], [8, 0, 5], [7, 2, 6]]  # 2d array for the mixed up puzzle - can be solved with previous goal
#puzzle = [[1, 3, 4], [8, 6, 2], [0, 7, 5]]  # can be solved with previous goal
# puzzle = [[1, 8, 2], [0, 4, 3], [7, 6, 5]]  # cannot be solved with previous goal
#puzzle = [[7, 3, 0], [5, 4, 2], [1, 8, 6]]  # requires a lot of moves/long running time to solve
puzzle = generatePuzzle()  # random puzzle generation

print("Start puzzle:")
printPuzzle(puzzle)
print(" ---------------------------------- \n")


# check if the puzzle can be solved before continuing
if mdowell_utils.isSolvable(goal, puzzle) is False:
    print("Puzzle is unsolvable.")
    quit()  # quit if it cannot be solved

board = mdowell_utils.PuzzleBoard(puzzle, goal)  # creates the starting board using the puzzle and goal
startNode = mdowell_utils.TreeNode(board)  # create a root tree node with the starting board
# endregion


# region Solving Puzzle

# solve the puzzle - returns the final node (goal) and the number of puzzle configurations seen before reaching the goal
# uncomment which one to use
solution = treeUtils.bfs(startNode)  # BFS
#solution = treeUtils.dfs(startNode, 20)  # DFS
#solution = treeUtils.ucs(startNode)  # UCS - also returns final cost

printSolution(solution)

# endregion
