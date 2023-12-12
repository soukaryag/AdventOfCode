from functools import lru_cache

def getAllGalaxies(mp):
    res = []

    for i in range(n):
        for j in range(m):
            if mp[i][j] == '#':
                res.append((i, j))

    return res


def getEmptyRows(mp):
    res = {}

    for i, row in enumerate(mp):
        if all(val == '.' for val in row):
            res[i] = True

    return res


def doubleEmptyRows(mp):
    mp = [list(m) for m in mp]
    addRows = {}
    rowLength = len(mp[0])

    for i, row in enumerate(mp):
        if all(val == '.' for val in row):
            addRows[i] = True

    added = 0
    for row in addRows:
        mp.insert(row + added, ['.' for _ in range(rowLength)])
        added += 1

    return mp


def inbounds(y, x):
    return 0 <= y < n and 0 <= x < m


# @lru_cache(maxsize=None)
def shortestPathBetween(strt, dst):
    # print(strt, dst, "shortestPathBetween")
    # if strt == dst:
    #     return 0

    # visited[f'{strt[0]},{strt[1]}'] = True

    # res = float('inf')
    # for delY, delX in directions:
    #     newY, newX = strt[0] + delY, strt[1] + delX
        
    #     if inbounds(newY, newX) and not visited.get(f'{newY},{newX}'):
    #         res = min(res, shortestPathBetween((newY, newX), dst) + 1)

    # return res

    res = abs(strt[0] - dst[0]) + abs(strt[1] - dst[1])

    return res


if __name__ == '__main__':
    global n, m, directions, emptyCols, emptyRows
    f = open("day_11.txt", "r")
    lines = f.read().splitlines()

    universe = []
    for line in lines:
        universe.append(list(line))

    universe = doubleEmptyRows(universe)
    universe = doubleEmptyRows(zip(*universe))
    universe = [list(u) for u in zip(*universe)]

    # for u in universe:
    #     print(''.join(u))

    n, m = len(universe), len(universe[0])
    directions = [(0, 1), (0, -1), (-1, 0), (1, 0)]

    galaxies = getAllGalaxies(universe)
    galaxies_n = len(galaxies)
    galaxyPairs = []

    for i in range(galaxies_n):
        for j in range(i + 1, galaxies_n):
            galaxyPairs.append((galaxies[i], galaxies[j]))

    visited = {}
    answer = 0
    for firstGalaxy, secondGalaxy in galaxyPairs:
        visited = {}
        path = shortestPathBetween(firstGalaxy, secondGalaxy)
        # print(path, firstGalaxy, secondGalaxy)
        answer += path

    print(f'ANSWER: {answer}')
