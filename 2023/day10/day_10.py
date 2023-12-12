
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
    q = [[start, 0]]
    n, m = len(grid), len(grid[0])
    res = 0

    while q:
        curr, steps = q.pop(0)
        y, x = curr
        visited[f'{y},{x}'] = True

        res = max(res, steps)
        dirs = transitions.get(grid[y][x], [])
        for delY, delX in dirs:
            newY, newX = y + delY, x + delX

            if 0 <= newY < n and 0 <= newX < m and connected((delY, delX), grid[newY][newX]) and not visited.get(f'{newY},{newX}', False):
                q.append([(newY, newX), steps + 1])


        print(q)

    print(f'ANSWER: {res}')
    