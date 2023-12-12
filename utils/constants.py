import inspect


# constants
INFINITY = float('inf')
FOUR_WAY_DIRECTIONS = [(0, 1), (0, -1), (-1, 0), (1, 0)]
EIGHT_WAY_DIRECTIONS = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]


# helper functions used often
def JUST_READ_FILE():
    dayNumber = inspect.stack()[2].filename.split('\\')[-1].split('.')[0]
    f = open(f'{dayNumber}.txt', 'r')
    lines = f.read().splitlines()
    return lines


def PARSE_INPUT_INTO_MATRIX():
    res = []
    lines = JUST_READ_FILE()
    for line in lines:
        res.append(list(line.strip()))
    return res


def GET_MATRIX_DIMENSIONS(matrix):
    return len(matrix), len(matrix[0])


def IS_INBOUNDS(y, x, n, m):
    return 0 <= y < n and 0 <= x < m


"""
Take starting coords, dimensions of map, the map itself, visited nodes, and symbols used for the path
Returns the all nodes in the map connected to the starting node
"""
def FIND_ISLAND_SIZE(y, x, n, m, map, visited, pathSymbol=1):
    q = [[y, x]]
    res = []
    
    while q:
        currY, currX = q.pop(0)

        if not visited.get(f'{currY},{currX}'):
            res.append(f'{currY},{currX}')
            visited[f'{currY},{currX}'] = True
        else:
            continue

        for delY, delX in FOUR_WAY_DIRECTIONS:
            newY, newX = currY + delY, currX + delX

            if IS_INBOUNDS(newY, newX, n, m) and map[newY][newX] == pathSymbol and not visited.get(f'{newY},{newX}', False):
                q.append([newY, newX])

    return res

