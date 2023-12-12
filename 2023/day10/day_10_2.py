directions = [(0, 1), (0, -1), (-1, 0), (1, 0)]
transitions = {
    '.': [(0, 0)],
    '|': [(1, 0), (-1, 0)],
    '-': [(0, 1), (0, -1)],
    'L': [(-1, 0), (0, 1)],
    'J': [(-1, 0), (0, -1)],
    '7': [(1, 0), (0, -1)],
    'F': [(1, 0), (0, 1)],
    'S': [(0, 1), (0, -1), (-1, 0), (1, 0)],
}


def connected(dir, shape):
    return (-dir[0], -dir[1]) in transitions.get(shape, [])


def inbounds(y, x, n, m):
    return 0 <= y < n and 0 <= x < m 


def bfs(y, x, n, m, islands, visitedIslands):
    # print('----------------', n, m)
    q = [[y, x]]
    res = []
    outsideCase = False
    
    while q:
        currY, currX = q.pop(0)

        if currY in [0, n - 1] or currX in [0, m - 1]: # and not shape+dire works: 
            outsideCase = True
        
        if not visitedIslands.get(f'{currY},{currX}'):
            res.append(f'{currY},{currX}')
            visitedIslands[f'{currY},{currX}'] = True

            # if not outsideCase:
            #     print(f'{currY},{currX}')
        else:
            continue

        

        for delY, delX in directions:
            newY, newX = currY + delY, currX + delX

            if inbounds(newY, newX, n, m) and islands[newY][newX] == 0 and not visitedIslands.get(f'{newY},{newX}', False):
                q.append([newY, newX])

    # print(y, x, outsideCase)
    if outsideCase: return []
    return res


def checkKrutisLogic(grouping, islands, grid, n, m):
    # print('========================')
    # print(grouping)
    for i in range(n):
        insidePipe = False
        for j in range(m):
            # 1 means pipe
            if islands[i][j] != 0:
                if grid[i][j] in ['L', 'J', '|']:
                    insidePipe = not insidePipe
                continue

            if f'{i},{j}' in grouping and not insidePipe:
                return False

    return True


if __name__ == '__main__':
    f = open("day_10.txt", "r")
    lines = f.read().splitlines()

    grid = []
    start = (-1, -1)
    for idx, line in enumerate(lines):
        grid.append(list(line))
        if 'S' in line:
            start = (idx, line.index('S'))

    visited = {}
    inside, outside = set([]), set([])
    q = [[start, 0, []]]       # [currLocation, steps, path]
    n, m = len(grid), len(grid[0])
    res = 0

    actualPath = []

    while q:
        curr, steps, path = q.pop(0)
        y, x = curr
        visited[f'{y},{x}'] = True

        newPath = path + [f'{y},{x}']

        if steps > res:
            res = steps
            actualPath = newPath
            
        dirs = transitions.get(grid[y][x], [])
        for delY, delX in dirs:
            newY, newX = y + delY, x + delX

            if inbounds(newY, newX, n, m) and connected((delY, delX), grid[newY][newX]) and not visited.get(f'{newY},{newX}', False):
                q.append([(newY, newX), steps + 1, newPath])
                break

    islands = []
    for i in range(n):
        tmp = []
        for j in range(m):
            if visited.get(f'{i},{j}'):
                tmp.append(actualPath.index(f'{i},{j}') + 1)
            else: tmp.append(0)

        islands.append(tmp)


    visitedIslands = {}
    answer = 0
    for i in range(n):
        for j in range(m):
            
            currVal = islands[i][j]
            if currVal == 0 and not visitedIslands.get(f'{i},{j}'):
                cells = bfs(i, j, n, m, islands, visitedIslands)
                # print(i, j, len(cells))

                if cells and checkKrutisLogic(cells, islands, grid, n, m):
                    # print(cells)
                    answer += len(cells)


    print(f'ANSWER: {answer}')


    # for row in islands:
    #     print(' '.join([str(i) for i in row]))



    