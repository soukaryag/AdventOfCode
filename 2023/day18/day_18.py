import sys
sys.path.append('../..')
from utils.constants import *



# answer for puzzle = 62
if __name__ == '__main__':
    global n, m
    lines = JUST_READ_FILE()

    dir = {
        'U': [-1, 0],
        'R': [0, 1],
        'D': [1, 0],
        'L': [0, -1],
    }

    grid = [['.' for _ in range(15)] for __ in range(15)]
    instructions = []
    for line in lines:
        instructions.append(line.split(' '))


    
    c = [1, 1]
    grid[c[0]][c[1]] = '#'
    for direction, spaces, color in instructions:
        y, x = dir.get(direction, [0, 0])
        for i in range(int(spaces)):
            c = [c[0] + y, c[1] + x]
            grid[c[0]][c[1]] = '#'

    answer = 0
    for row in grid:
        inside = False
        tmp = 0
        n = len(row)
        for idx, cell in enumerate(row):
            if not inside and cell == '#':
                inside = True
                tmp += 1
                continue

            if inside and cell == '.':
                tmp += 1
            elif inside and cell == '#':
                tmp += 1
                if idx == n - 1:
                    inside = False
                elif row[idx + 1] != '#':
                    inside = False
        
        print(row, tmp)
        answer += tmp
            

    PRINT_MATRIX_NOARR(grid)

    PRINT_ANSWER(answer)
    