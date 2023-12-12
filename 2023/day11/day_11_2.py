

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


def shortestPathBetween(strt, dst):
    res = abs(strt[0] - dst[0]) + abs(strt[1] - dst[1])

    a, b = min(strt[0], dst[0]), max(strt[0], dst[0])
    for row in emptyRows:
        if a < row < b:
            res += SPACE_EXPANSION_CONSTANT

    a, b = min(strt[1], dst[1]), max(strt[1], dst[1])
    for col in emptyCols:
        if a < col < b:
            res += SPACE_EXPANSION_CONSTANT

    return res


if __name__ == '__main__':
    global n, m, directions, emptyCols, emptyRows, SPACE_EXPANSION_CONSTANT
    f = open("day_11.txt", "r")
    lines = f.read().splitlines()

    universe = []
    for line in lines:
        universe.append(list(line))

    SPACE_EXPANSION_CONSTANT = 1000000 - 1
    n, m = len(universe), len(universe[0])
    directions = [(0, 1), (0, -1), (-1, 0), (1, 0)]

    galaxies = getAllGalaxies(universe)
    galaxies_n = len(galaxies)
    galaxyPairs = []

    for i in range(galaxies_n):
        for j in range(i + 1, galaxies_n):
            galaxyPairs.append((galaxies[i], galaxies[j]))

    emptyRows = getEmptyRows(universe)
    emptyCols = getEmptyRows(zip(*universe))

    visited = {}
    answer = 0
    for firstGalaxy, secondGalaxy in galaxyPairs:
        visited = {}
        path = shortestPathBetween(firstGalaxy, secondGalaxy)
        # print(path, firstGalaxy, secondGalaxy)
        answer += path

    print(f'ANSWER: {answer}')
