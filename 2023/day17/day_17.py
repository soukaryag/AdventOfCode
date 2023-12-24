import sys
sys.path.append('../..')
from utils.constants import *
from heapq import heappop, heappush
from collections import defaultdict
from functools import lru_cache


def getNext():
    global priorityQueue
    while priorityQueue:
        _, __, el = heappop(priorityQueue)
        if el:
            del lookupTable[el]
            return el
        
    return None


def addToQueue(el, priority=0):
    global priorityQueue, lookupTable, uniqueValue
    if lookupTable.get(el):
        lookup = lookupTable.pop(el)
        lookup[-1] = None
    
    uniqueValue += 1
    lookupValue = [priority, uniqueValue, el]
    lookupTable[el] = lookupValue
    heappush(priorityQueue, lookupValue)
    

@lru_cache(maxsize=None)
def getOrthogonals(coords):
    if coords[1] == 0:
        return [((0, -1), 1), ((0, 1), 1)]
    else:
        return [((-1, 0), 1), ((1, 0), 1)]


if __name__ == '__main__':
    global n, m, grid, priorityQueue, lookupTable, uniqueValue
    lines = JUST_READ_FILE()

    MINIMUM_STRAIGHT = 0    #  4    for part 2
    MAXIMUM_STRAIGHT = 3    # 10    for part 2

    grid = []
    for line in lines:
        grid.append([int(i) for i in list(line)])

    n, m = len(grid), len(grid[0])
    endState = (n - 1, m - 1)
    priorityQueue = []
    lookupTable = {}
    uniqueValue = 0

    for i in range(n):
        for j in range(m):
            for dir in FOUR_WAY_DIRECTIONS:
                for straight in range(1, MAXIMUM_STRAIGHT + 1):
                    addToQueue((i, j, dir, straight), INFINITY)

    startingElVert = (0, 0, (1, 0), 0)
    startingElHor = (0, 0, (0, 1), 0)
    addToQueue(startingElVert)
    addToQueue(startingElHor)

    totalHeatAtNode = defaultdict(lambda: INFINITY)     # tracks the minimum heat at a node
    totalHeatAtNode[startingElVert] = 0
    totalHeatAtNode[startingElHor] = 0

    answer = 0
    while True:
        curr = getNext()
        y, x, dir, straight = curr
        if (y, x) == endState and straight >= MINIMUM_STRAIGHT:
            answer = totalHeatAtNode.get(curr)
            break

        nextNodes = []
        if straight >= MINIMUM_STRAIGHT:
            nextNodes += getOrthogonals(dir)
        if straight < MAXIMUM_STRAIGHT:
            nextNodes.append((dir, straight + 1))

        for deltas, strght in nextNodes:
            dy, dx = deltas
            newY, newX = y + dy, x + dx
            newEl = (newY, newX, deltas, strght)
            if IS_INBOUNDS(newY, newX, n, m):
                newTotalHeat = totalHeatAtNode.get(curr, INFINITY) +  grid[newY][newX]
                if newTotalHeat < totalHeatAtNode.get(newEl, INFINITY):
                    totalHeatAtNode[newEl] = newTotalHeat
                    addToQueue(newEl, newTotalHeat)


    PRINT_ANSWER_MAC(answer)
    
