import sys
sys.path.append('../..')
from utils.constants import *
import curses
import time


dirShapes = {
    (0, 1): '>',
    (0,-1): '<',
    (1, 0): 'v',
    (-1, 0): '^'
}


def findRayTracedPath(q):
    cache = {}
    visited = {}

    while q:
        coords, direction = q.pop(0)
        y, x = coords

        if not (0 <= y < n and 0 <= x < m):
            continue
        if cache.get((coords, direction)):
            continue

        cache[(coords, direction)] = coords
        visited[coords] = True

        shape = matrix[y][x]
        nextDirections = reflections.get((shape, direction), [])

        if nextDirections:
            for dir in nextDirections:
                delY, delX = dir
                q.append(((y + delY, x + delX), dir))
        else:
            q.append(((y + direction[0], x + direction[1]), direction))

        newMatrix = [['.' for _ in range(m)] for __ in range(n)]
        for c, d in cache.keys():
            newMatrix[c[0]][c[1]] = dirShapes.get(d, '#')

        myWindow.addstr(0, 0, MATRIX_TO_STR(newMatrix))
        myWindow.refresh()
        time.sleep(0.001)

    return(len(visited))


if __name__ == '__main__':
    global n, m, reflections, matrix
    lines = JUST_READ_FILE()
    myWindow = curses.initscr()

    matrix = []
    for line in lines:
        matrix.append(list(line))

    reflections = {
        ('|', (0, 1)): [(1, 0), (-1, 0)],
        ('|', (0, -1)): [(1, 0), (-1, 0)],

        ('-', (1, 0)): [(0, 1), (0, -1)],
        ('-', (-1, 0)): [(0, 1), (0, -1)],

        ('\\', (-1, 0)): [(0, -1)],
        ('\\', (1, 0)): [(0, 1)],
        ('\\', (0, -1)): [(-1, 0)],
        ('\\', (0, 1)): [(1, 0)],

        ('/', (-1, 0)): [(0, 1)],
        ('/', (1, 0)): [(0, -1)],
        ('/', (0, -1)): [(1, 0)],
        ('/', (0, 1)): [(-1, 0)],
    }

    n, m = len(matrix), len(matrix[0])
    ans = 0

    # part 1
    # tmp = findRayTracedPath([((0, 0), (0, 1))])

    # part 2
    for i in range(0, n):
        q = [((i, 0), (0, 1))]  # leftmost column going right
        tmp = findRayTracedPath(q)
        ans = max(ans, tmp)

        q = [((i, m - 1), (0, -1))]  # rightmost column going left
        tmp = findRayTracedPath(q)
        ans = max(ans, tmp)
    

    for j in range(0, m):
        q = [((0, j), (1, 0))]  # topmost row going down
        tmp = findRayTracedPath(q)
        ans = max(ans, tmp)

        q = [((n - 1, j), (-1, 0))]  # bottom row going up
        tmp = findRayTracedPath(q)
        ans = max(ans, tmp)


    PRINT_ANSWER(ans)
    curses.endwin()