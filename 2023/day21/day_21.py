

from collections import defaultdict


def inbounds(y, x):
    return 0 <= y < n and 0 <= x < m


def expand(grid, by):
    return [[grid[i % n][j % m] for j in range(by * m)] for i in range(by * n)]

if __name__ == '__main__':
    global n, m
    lines = open('day_21.txt', 'r')

    STEPS_WANTED = 327
    DIRS = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    grid = []
    for line in lines:
        grid.append(list(line.strip()))

    n, m = len(grid), len(grid[0])
    
    start = None
    for i in range(n):
        for j in range(m):
            if grid[i][j] == 'S':
                grid[i][j] = '.'
                start = (i, j)
                break

        if start: break

    grid = expand(grid)
    n, m = len(grid), len(grid[0])
    start = (n // 2, m // 2)

    levels = defaultdict(list)
    q = [(start, (0, 0), 0)]   # [real grid coords, multiverse coords, level]   original universe is (0, 0)
    recorded = []

    # print('x, y')
    while q:
        currCoords, currUniverse, level = q.pop(0)
        currY, currX = currCoords
        currUniY, currUniX = currUniverse

        # if level == 66 and level - 1 not in recorded:
        #     recorded.append(level - 1)
        #     print(f'65: {len(levels.get(level - 1, []))}')
        # if level == 197:
        #     recorded.append(level - 1)
        #     print(f'196: {len(levels.get(level - 1, []))}')
        if level == STEPS_WANTED + 1:
            recorded.append(level - 1)
            print(f'{STEPS_WANTED}: {len(levels.get(level - 1, []))}')
            break

        if level - 1 not in recorded:
            recorded.append(level - 1)
            fx = len(levels.get(level - 1, []))
            print(f'{level - 1}, {fx}, {(level ** 2) - fx}')

        if currCoords not in levels.get(level, []):
            levels[level].append(currCoords)
        else: continue

        # print(levels)

        for delY, delX in DIRS:
            newY, newX = currY + delY, currX + delX
            wrappedY, wrappedX = newY % n, newX % m
            universeY, universeX = newY // n, newX // m

            if grid[wrappedY][wrappedX] != '#':
                q.append(((newY, newX), (universeY, universeX), level + 1))
            continue
            
        

    # print(levels)