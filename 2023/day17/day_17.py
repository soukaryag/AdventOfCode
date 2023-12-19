import sys
sys.path.append('../..')
from utils.constants import *
from functools import lru_cache
import curses
import time

sys.setrecursionlimit(3500)

dirShapes = {
    (0, 1): '>',
    (0,-1): '<',
    (1, 0): 'v',
    (-1, 0): '^'
}

opposite = {
    (0, 1): (0, -1),
    (0, -1): (0, 1),
    (1, 0): (-1, 0),
    (-1, 0): (1, 0)
}


@lru_cache(maxsize=None)
def calcHeatLoss(history):
    if not history: return INFINITY
    # y, x = history[0]
    # return matrix[y][x] + calcHeatLoss(history[1:])

    res = 0
    for h in history:
        curr = h[0]
        if not IS_INBOUNDS(curr[0], curr[1], n, m): return INFINITY
        res += matrix[curr[0]][curr[1]]

    return res


@lru_cache(maxsize=None)
def minimizeHeatLossPath(coords, direction, straightSteps, past):
    y, x = coords
    # if y == 1 and x == 2 and direction == (1, 0):
    #     print(y, x, direction, straightSteps)

    if len(past) > 167:
        print('!!!', coords, past)
        exit()

    if y == n - 1 and x == m - 1:
        print(y, x, dirShapes.get(direction), straightSteps, matrix[y][x], "END!!")
        cache[(coords, direction, straightSteps)] = (((y, x), direction),)
        print(cache)
        return (((y, x), direction),)
    
    if cache.get((coords, direction, straightSteps)):
        print('1. CACHE HIT!!')
        return cache.get((coords, direction, straightSteps))
    
    
    res = INFINITY
    bestHist = ()
    for delY, delX in FOUR_WAY_DIRECTIONS:
        # can't reverse
        if (delY, delX) == opposite.get(direction):
            continue

        newCoords = (y + delY, x + delX)
        newDir = (delY, delX)

        # if same way, can only take 3 steps
        if newDir == direction:
            if straightSteps < 2 and IS_INBOUNDS(y + delY, x + delX, n, m) and newCoords not in past:
                if cache.get((newCoords, newDir, straightSteps + 1)):
                    print('2. CACHE HIT!!')
                    bestHist = cache.get(newCoords, newDir, straightSteps + 1)
                    tmpRes = calcHeatLoss(bestHist)
                else:
                    hist = minimizeHeatLossPath(newCoords, newDir, straightSteps + 1, past + ((y, x),))
                    if hist:
                        tmpRes = calcHeatLoss(hist)
                        if tmpRes != 0 and tmpRes < res:
                            res = tmpRes
                            bestHist = hist
            else:
                continue
        # otherwise go crazy go stupid
        else:
            if IS_INBOUNDS(y + delY, x + delX, n, m) and newCoords not in past:
                if cache.get((newCoords, newDir, 1)):
                    print('3. CACHE HIT!!')
                    bestHist = cache.get(newCoords, newDir, 1)
                    tmpRes = calcHeatLoss(bestHist)
                else:
                    hist = minimizeHeatLossPath(newCoords, newDir, 1, past + ((y, x),))
                    if hist:
                        tmpRes = calcHeatLoss(hist)
                        if tmpRes != 0 and tmpRes < res:
                            res = tmpRes
                            bestHist = hist
                
    if res == INFINITY:
        return False
    else:
        cache[(coords, direction, straightSteps)] = (((y, x), direction),) + bestHist
        return (((y, x), direction),) + bestHist



if __name__ == '__main__':
    global n, m, matrix, cache
    lines = JUST_READ_FILE()
    # myWindow = curses.initscr()

    matrix = []
    for line in lines:
        matrix.append([int(i) for i in list(line)])

    n, m = len(matrix), len(matrix[0])
    cache = {}
    
    start = (0, 0)
    answer = INFINITY
    for dir in [(0, 1), (1, 0)]:
        cache = {}
        if IS_INBOUNDS(start[0] + dir[0], start[1] + dir[1], n, m):
            hist = minimizeHeatLossPath((start[0] + dir[0], start[1] + dir[1]), dir, 1, ((0,0),))
            if hist:
                printMap = [[str(matrix[i][j]) for j in range(m)] for i in range(n)]
                # print('---')
                currDir = dir
                for h in hist:
                    curr = h[0]
                    currDir = h[1]
                    # print(h)
                    printMap[curr[0]][curr[1]] = dirShapes.get(currDir, '#')
                    # myWindow.addstr(0, 0, MATRIX_TO_STR(printMap))
                    # myWindow.refresh()
                    # time.sleep(0.2)
                    
                # print('---')
                # PRINT_MATRIX_NOARR(printMap)
                curses.endwin()

            tmpRes = calcHeatLoss(hist)
            if tmpRes != 0:
                answer = min(answer, tmpRes)
        exit()

    PRINT_ANSWER(answer)
    # curses.endwin()
