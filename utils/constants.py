import os
import inspect
import tempfile
import subprocess
from functools import lru_cache


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# constants
INFINITY = float('inf')
FOUR_WAY_DIRECTIONS = [(0, 1), (0, -1), (-1, 0), (1, 0)]
EIGHT_WAY_DIRECTIONS = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]
TMP_FILE_PATH = f'{tempfile.gettempdir()}\previous_answers.txt'

# helper functions used often
def JUST_READ_FILE(index=1):
    dayNumber = inspect.stack()[index].filename.split('\\')[-1].split('.')[0]
    f = open(f'{dayNumber}.txt', 'r')
    lines = f.read().splitlines()
    return lines


def PARSE_INPUT_INTO_MATRIX():
    res = []
    lines = JUST_READ_FILE(2)
    for line in lines:
        res.append(list(line.strip()))
    return res


def GET_MATRIX_DIMENSIONS(matrix):
    return len(matrix), len(matrix[0])


@lru_cache(maxsize=None)
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


def PRINT_MATRIX(matrix):
    print('----------------------')
    for m in matrix:
        print(m)
    print('----------------------')

def PRINT_MATRIX_NOARR(matrix):
    print('----------------------')
    for m in matrix:
        print(''.join(m))
    print('----------------------')

def MATRIX_TO_STR(matrix):
    res = ''
    for m in matrix:
        res += ''.join(m) + '\n'

    return res


def MATRIX_AS_STRING(matrix):
    res = ''
    for m in matrix:
        res += ''.join(m)
    
    return res

def TRANSPOSE_MATRIX(matrix):
    return [list(_) for _ in zip(*matrix)]


def PRINT_ANSWER(answer, showHistory=True):
    COPY_TO_CLIPBOARD(answer)
    if not os.path.exists(TMP_FILE_PATH):
        f = open(TMP_FILE_PATH, 'x')
    else:
        f = open(TMP_FILE_PATH, 'r')
    
    lines = f.read().splitlines()
    prevAnswers = [ans.strip() for ans in lines]

    print('================================')
    PRINT_SUCCESS(f'CURRENT ANSWER: {BOLD_TEXT(answer)}\n')
    if showHistory:
        for i, ans in enumerate(prevAnswers):
            print(f'{i + 1} RUN{"" if i == 0 else "S"} AGO - ANSWER: {ans}')
    print('================================')
    f.close()

    prevAnswers.insert(0, answer)
    f = open(TMP_FILE_PATH, 'w')
    for i in range(min(len(prevAnswers), 10)):
        f.write(f'{prevAnswers[i]}\n')
    f.close()


def PRINT_SUCCESS(txt):
    print(f'{bcolors.OKGREEN}{txt}{bcolors.ENDC}')

def PRINT_WARNING(txt):
    print(f'{bcolors.WARNING}{txt}{bcolors.ENDC}')

def PRINT_ERROR(txt):
    print(f'{bcolors.FAIL}{txt}{bcolors.ENDC}')

def BOLD_TEXT(txt):
    return f'{bcolors.BOLD}{txt}{bcolors.ENDC}'


def COPY_TO_CLIPBOARD(txt):
    cmd=f'echo {str(txt).strip()}|clip'
    return subprocess.check_call(cmd, shell=True)
