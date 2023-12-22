

from collections import defaultdict


def inbounds(y, x):
    return 0 <= y < n and 0 <= x < m


def expand(grid, by, n, m):
    return [[grid[i % n][j % m] for j in range(by * m)] for i in range(by * n)]

def search(walkTo):
    global n, m, grid, start

    q = [(start,  0)]   # [real grid coords, steps]
    visited = {}

    while q:
        currCoords, steps = q.pop(0)
        if steps > walkTo:
            continue

        currY, currX = currCoords

        for delY, delX in DIRS:
            newY, newX = currY + delY, currX + delX

            if grid[newY][newX] != '#' and not visited.get((newY, newX)):
                q.append(((newY, newX), steps + 1))
                visited[(newY, newX)] = True
            
    return len([(r, c) for r, c in list(visited.keys()) if (r + c) % 2 == walkTo % 2])



if __name__ == '__main__':
    global originalN, originalM, n, m, grid, start
    lines = open('day_21.txt', 'r')

    DIRS = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    grid = []
    for line in lines:
        grid.append(list(line.strip()))

    originalN, originalM = len(grid), len(grid[0])
    
    start = None
    for i in range(originalN):
        for j in range(originalM):
            if grid[i][j] == 'S':
                grid[i][j] = '.'
                start = (i, j)
                break

        if start: break

    grid = expand(grid, 7, originalN, originalM)
    n, m = len(grid), len(grid[0])
    start = (n // 2, m // 2)

    for x in range(originalN // 2, int(5/2 * originalN) + 1, originalN):
        y = search(x)
        print(f'{x}, {y}')

    target = (26501365 - (originalN // 2)) // originalN
    print(f'TARGET: {target}')

    # 12419982014000
    a, b, c = 14871, 15005, 3776
    print(f'ANSWER: {(a * (target ** 2)) + (b * target) + c}')

