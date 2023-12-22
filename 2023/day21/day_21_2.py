

from collections import defaultdict


def inbounds(y, x):
    return 0 <= y < n and 0 <= x < m


def getCell(delY, delX):
    global n, m, grid, start

    newY = (start[0] + delY) % n
    newX = (start[1] + delX) % m

    return grid[newY][newX]

def setRock(delY, delX, i):
    global start, rocks

    newY = start[0] + delY
    newX = start[1] + delX

    # print("SETTING ROCK", newY, newX)
    if rocks.get(i):
        rocks[i][(newY, newX)] = '#'
    else:
        rocks[i] = {(newY, newX): '#'}

def isRock(delY, delX, i):
    global rocks, start

    newY = start[0] + delY
    newX = start[1] + delX

    checkMap = {**rocks.get(-1, {}), **rocks.get(i, {})}

    return checkMap.get((newY, newX), False)

def increaseCount(i):
    global evenWave, oddWave
    if i % 2 == 0: evenWave += 1
    else: oddWave += 1

def printGrid(r2={}):
    global n, m, grid, rocks
    r1 = rocks.get(-1, {})

    gr = [['.' for _ in range(m)] for __ in range(n)]
    for i, j in r1:
        gr[i][j] = '#'
    for i, j in r2:
        if inbounds(i,j):
            gr[i][j] = '%'

    print('-'*10)
    for g in gr:
        print(''.join(g))
    print('-'*10, '\n')


if __name__ == '__main__':
    global n, m, grid, start, evenWave, oddWave, rocks
    lines = open('day_21.txt', 'r')

    STEPS_WANTED = 26501365
    DIRS = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    grid = []
    for line in lines:
        grid.append(list(line.strip()))

    rocks = {-1: {}}
    start = None
    n, m = len(grid), len(grid[0])
    for i in range(n):
        for j in range(m):
            if grid[i][j] == 'S':
                start = (i, j)
            elif grid[i][j] == '#':
                rocks[-1][(i, j)] = '#'

    evenWave = 0
    oddWave = 0
    y, x = start
    for i in range(1000):
        rocksCounted = 0
        for j in range(i + 1):
            # print('a', (-i+j, j), end=' ')
            # NORTHEAST
            y, x = -i+j, j
            if isRock(y, x, i-1) != '#':
                if (x == 0 and y != 0 and isRock(y + 1, x, i-1) == '#') or \
                    (y == 0 and x != 0 and isRock(y, x - 1, i-1) == '#') or \
                    (y != 0 and x != 0 and isRock(y + 1, x, i-1) == '#' and isRock(y, x - 1, i-1) == '#'):
                    # can't fill this because of blocking rocks
                    setRock(y, x, i)
                else:
                    # all good to go, passed all checks
                    increaseCount(i)

            if i-j != 0:
                # print('b', (i-j, j), end=' ')
                # SOUTHEAST
                y, x = i-j, j
                if isRock(y, x, i-1) != '#':
                    if (x == 0 and y != 0 and isRock(y - 1, x, i-1) == '#') or \
                        (y == 0 and x != 0 and isRock(y, x - 1, i-1) == '#') or \
                        (y != 0 and x != 0 and isRock(y - 1, x, i-1) == '#' and isRock(y, x - 1, i-1) == '#'):
                        # can't fill this because of blocking rocks
                        setRock(y, x, i)
                    else:
                        # all good to go, passed all checks
                        increaseCount(i)

            if j != 0:
                # print('c', (-i+j, -j), end=' ')
                # NORTHWEST
                y, x = -i+j, -j
                if isRock(y, x, i-1) != '#':
                    if (y == 0 and x != 0 and isRock(y, x + 1, i-1) == '#') or \
                        (y != 0 and x != 0 and isRock(y + 1, x, i-1) == '#' and isRock(y, x + 1, i-1) == '#'):
                        # can't fill this because of blocking rocks
                        setRock(y, x, i)
                    else:
                        # all good to go, passed all checks
                        increaseCount(i)

                if i-j != 0:
                    # print('c', (i-j, -j), end=' ')
                    # SOUTHWEST
                    y, x = i-j, -j
                    if isRock(y, x, i-1) != '#':
                        if (y == 0 and x != 0 and isRock(y - 1, x, i-1) == '#' and isRock(y, x + 1, i-1) == '#'):
                            # this is a SW cell and cells ABOVE and to the RIGHT are rocks
                            setRock(y, x, i)
                        else:
                            # all good to go, passed all checks
                            increaseCount(i)


        # printGrid(rocks.get(i, {}))
        if i % 2 == 0:
            print(f'{i}, {evenWave}')
            # if evenWave >= STEPS_WANTED:
            #     print(i, evenWave, STEPS_WANTED, 'DONE')
            #     exit()
        else:
            print(f'{i}, {oddWave}')
            # if oddWave >= STEPS_WANTED:
            #     print(i, oddWave, STEPS_WANTED, 'DONE')
            #     exit()

    # print(evenRocks)
