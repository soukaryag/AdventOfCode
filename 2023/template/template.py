import sys
sys.path.append('../..')
from utils.constants import *


if __name__ == '__main__':
    global n, m
    lines = JUST_READ_FILE()

    matrix = []
    for line in lines:
        matrix.append(list(line))

    print(matrix)

    answer = 0


    PRINT_ANSWER(answer)
    