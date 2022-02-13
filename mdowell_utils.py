"""
Meghan Dowell
CS7375 OL
Assignment 1 (8 Puzzle)
02/13/2022
"""
import copy
import heapq


### Class for creating the puzzles as objects to be used in the state tree
class PuzzleBoard(object):
    # initialize the board
    def __init__(self, startState, goalState):
        self.state = startState  # give start state of the board
        self.goal = goalState  # give destination state of the board
        self.blankLocation = []  # location of the 0 in this board
        self.determineBlankLocation()

    # returns true if the board's state is the same as the destination state
    def isEnd(self):
        return self.state == self.goal

    # finds the location of the 0 in the current state, updates its stored blank location, and returns the location
    def determineBlankLocation(self):
        for i, row in enumerate(self.state):  # loop through row
            for j, column in enumerate(row):  # loop through columns in the row
                if column == 0:  # if the column is 0, blank space is found
                    self.blankLocation = [i, j]  # record location of 0 for this state
                    return [i, j]  # return the location of the blank space


### Model (tree) - nodes are PuzzleBoards
class TreeNode:
    def __init__(self, value, parent=None, lastMove=None, curCost=1):
        self.value = value  # this node's board
        self.children = []  # list of child nodes
        self.parent = parent  # parent node
        self.curCost = curCost  # cost of getting to this node from previous node
        self.blankLoc = value.blankLocation  # get the blank location of this node's board
        self.lastMove = lastMove  # the last action that was taken to get to this node

    # Creates the children of this node and adds them to the children list
    def createChildren(self):
        # if the blank space is not on the bottom edge and current state wasn't reached from moving up, add the down movement
        if (self.blankLoc[0] < 2) and (self.lastMove != "up"):
            self.children.append(TreeNode(moveBlank(self.value, "down"), self, "down"))
        # if the blank space is not on the top edge and current state wasn't reached from moving down, add the up movement
        if (self.blankLoc[0] > 0) and (self.lastMove != "down"):
            self.children.append(TreeNode(moveBlank(self.value, "up"), self, "up"))
        # if the blank space is not on the right edge and current state wasn't reached from moving left, add the right movement
        if (self.blankLoc[1] < 2) and (self.lastMove != "left"):
            self.children.append(TreeNode(moveBlank(self.value, "right"), self, "right"))
        # if the blank space is not on the left edge and current state wasn't reached from moving right, add the left movement
        if (self.blankLoc[1] > 0) and (self.lastMove != "right"):
            self.children.append(TreeNode(moveBlank(self.value, "left"), self, "left"))

    def __lt__(self, other):  # provide a comparison function for the priority queue
        return self.curCost < other.curCost  # return if this cost is less than the one being compared to


# Class containing static methods to find a solution using BFS, DFS, and UCS
class BinaryTreeUtils:

    # Breadth First Search
    @staticmethod
    def bfs(root: TreeNode):
        if not root:  # if a root was not supplied, return none
            return None

        steps = 0  # number of explored states
        unexplored = [root]  # initialize the unexplored list with the root
        explored = []  # store visited states

        while unexplored:  # while there are nodes in the unexplored list
            curr = unexplored.pop(0)  # remove first node from unexplored list - this is the current node

            if curr.value.isEnd():  # if the current node is also the destination node
                return [curr, steps]  # return the current node and how many states were explored to reach it

            # skip to the next loop if we've already seen this node - children have also already been seen or added to unexplored
            if explored.__contains__(curr.value.state):
                continue
            explored.append(curr.value.state)
            steps += 1  # increase number of explored nodes
            curr.createChildren()  # create the children nodes of the current node
            unexplored.extend(curr.children)  # add the child nodes of the current node to the unexplored list

        # if a solution is not found, return none - this should never be reached if a puzzle is solvable
        return [None, steps]

    # Depth First Search
    @staticmethod
    def dfs(root: TreeNode, maxDepth=7):
        steps = 0  # number of explored states

        # preorder explores root first, then recursively explores children in order added
        def preOrder(rootNode, curDepth=0):
            nonlocal steps  # needed to use the steps in the outer def
            if rootNode and curDepth < maxDepth:  # if the given node is not none, and we haven't reached the max depth
                if rootNode.value.isEnd():  # if the current node is also the destination node, return it
                    return rootNode

                steps += 1  # increase number of explored nodes
                rootNode.createChildren()  # create the children nodes of the current node
                for child in rootNode.children:  # iterate through all children of this node
                    node = preOrder(child, curDepth + 1)  # recursively search through the child node
                    if node:  # if the recursive call returned a node (found the destination node)
                        return node  # return it to the caller

        return [preOrder(root), steps]

    # Uniform Cost Search
    @staticmethod
    def ucs(root: TreeNode):
        frontier = PriorityQueue()  # frontier is states that have been seen
        frontier.enqueue(root, 0)  # start by adding the given node to the frontier - cost is 0 since it's the root
        steps = 0  # counter to keep track of how many board configurations have been seen

        while True:  # run until we return a state
            curState, pastCost = frontier.dequeue()  # get the state + cost with the highest priority (lowest cost)
            if curState.value.isEnd():  # if the state is the goal state
                return curState, steps, pastCost  # return the state, how many configurations were visited, and its cost

            curState.createChildren()  # expand the state by getting its child nodes
            steps += 1  # add this to number of seen states
            for newState in curState.children:  # loop through the expanded states
                frontier.enqueue(newState, pastCost + newState.curCost)  # add them to the frontier using their cost + the current cost


#  Priority Queue data structure for UCS
class PriorityQueue:
    def __init__(self):
        self.heap = []  # need a heap for holding states by priority
        self.priorities = {}  # dictionary that holds a state as the key and the priority as the value

    def enqueue(self, state, priority) -> bool:  # attempts to add a state to the heap and returns if it was added
        oldPriority = self.priorities.get(state)  # get the recorded priority of the state
        if oldPriority is None or priority < oldPriority:  # if there isn't a previous priority or the new one is better
            self.priorities[state] = priority  # update the state's stored priority
            heapq.heappush(self.heap, (priority, state))  # add the priority and state to the heap
            return True  # return if it was added
        return False  # return if it wasn't added

    def dequeue(self):  # removes a state from the heap and returns it
        while len(self.heap) > 0:
            priority, state = heapq.heappop(self.heap)  # get the priority + state with the highest priority (lowest cost)
            if self.priorities[state] == -1:  # if we have already explored this state, do not update it
                continue
            self.priorities[state] = -1  # mark this state as explored in the priorities
            return state, priority  # return the state and priority
        return None, None  # return none if heap is empty


# Moves the blank space in a board and returns the new board object
def moveBlank(state, action) -> PuzzleBoard:
    index = state.blankLocation  # get the current blank location
    newBoard = copy.deepcopy(state)  # copy the given board to alter
    currentBoard = newBoard.state  # get current state

    if action == "up":  # move up - index (i, j) should switch with (i - 1, j)
        tempInt = currentBoard[index[0] - 1][index[1]]  # record the number currently above the blank spot
        currentBoard[index[0]][index[1]] = tempInt  # replace the blank spot with the number above the blank spot
        currentBoard[index[0] - 1][index[1]] = 0  # replace the number that was above the blank spot with 0
    elif action == "down":  # move down - index (i, j) should switch with (i + 1, j)
        tempInt = currentBoard[index[0] + 1][index[1]]
        currentBoard[index[0]][index[1]] = tempInt
        currentBoard[index[0] + 1][index[1]] = 0
    elif action == "left":  # move left - index (i, j) should switch with (i, j-1)
        tempInt = currentBoard[index[0]][index[1] - 1]
        currentBoard[index[0]][index[1]] = tempInt
        currentBoard[index[0]][index[1] - 1] = 0
    elif action == "right":  # move right - index (i, j) should switch with (i, j+1)
        tempInt = currentBoard[index[0]][index[1] + 1]
        currentBoard[index[0]][index[1]] = tempInt
        currentBoard[index[0]][index[1] + 1] = 0

    newBoard.determineBlankLocation()  # get the new blank location for the board
    return newBoard  # return the new board


# traces from the given node back to the parent node and returns them in a list
def backTrace(child: TreeNode):
    nodeLineage = []  # empty list to store lineage of given child

    while child.parent:  # loop until the root node is reached
        nodeLineage.append(child)  # add the current node to the lineage list
        child = child.parent  # set the current node to be this node's parent

    nodeLineage.append(child)  # add the last node to the list - should be the root
    return nodeLineage  # return the lineage list of the given node


# gets how many inversions for the given state
# inversions are how many tiles are in the incorrect order
# if item 2 is greater than item 3, that is an inversion
# returns True if the inversions are even, False if they are odd
def evenInversions(state) -> bool:
    # converting the 2D array into a 1D array to use in checking inversions
    stateFlattened = []  # 1D array version of the given 2D array
    for row in state:  # loop through each row
        for column in row:  # loop through each column
            stateFlattened.append(column)  # add the item to the 1D array

    inversions = 0  # number of inversions
    length = len(stateFlattened)
    for i in range(0, length):
        if stateFlattened[i] == 0:  # don't loop through j if i is the blank space
            continue
        for j in range(i+1, length):  # loop through the items after i
            # if this is not the blank space and is less than the item at i, this is an inversion
            if stateFlattened[j] != 0 and stateFlattened[i] > stateFlattened[j]:
                inversions += 1  # increase inversions

    return inversions % 2 == 0  # returns if the inversion count is divisible by 2


# function to determine if the given starting 8 puzzle is solvable
# 8 puzzle is solvable IF the parity of the start state matches that of the goal state
# returns true if the puzzle can be solved
def isSolvable(goal, startState) -> bool:
    goalParity = evenInversions(goal)  # get if goal has even inversions
    startParity = evenInversions(startState)  # get if start state has even inversions

    return goalParity == startParity  # return if their parity is the same
