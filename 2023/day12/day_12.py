import sys
sys.path.append('../..')
from utils.constants import *


if __name__ == '__main__':
    arr = PARSE_INPUT_INTO_MATRIX()

    PRINT_MATRIX(arr)
    PRINT_MATRIX(TRANSPOSE_MATRIX(arr))

    PRINT_ANSWER(147)
