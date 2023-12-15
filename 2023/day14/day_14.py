import sys
sys.path.append('../..')
from utils.constants import *
from copy import deepcopy

def rotate90Clockwise(A):
    res = []
    nn, mm = len(A), len(A[0])
    for i in range(mm):
        row = []
        for j in range(nn):
            row.append(A[j][i])
        row.reverse()
        res.append(row)

    return res
    

def calculateLoad(matrix):
    res = 0
    for i in range(n):
        for j in range(m):
            if matrix[i][j] == 'O':
                res += n - i

    return res


def tiltMatrix(m):
    newMatrix = TRANSPOSE_MATRIX(m)
    # PRINT_MATRIX(newMatrix)

    for idx, row in enumerate(newMatrix):
        newRowSubstrs = []
        rowStr = ''.join(row).split('#')

        # print(rowStr)

        for i, rowSubstr in enumerate(rowStr):
                
            rocks = rowSubstr.count('O')
            toAdd = 'O' * rocks + '.' * (len(rowSubstr) - rocks)
            if i != len(rowStr) - 1:
                toAdd += '#'
            newRowSubstrs.append(toAdd)

        # print('!!!!', ''.join(newRowSubstrs))
        newMatrix[idx] = list(''.join(newRowSubstrs))

    return TRANSPOSE_MATRIX(newMatrix)



if __name__ == '__main__':
    global n, m
    lines = JUST_READ_FILE()

    CYCLES = 1000000000
    matrix = []
    for line in lines:
        matrix.append(list(line))

    n, m = len(matrix), len(matrix[0])

    cache = {}
    cacheRotation = {}
    cacheLoad = {}
    answers = {}

    for _ in range(CYCLES):
        for __ in range(4):
            mStr = MATRIX_AS_STRING(matrix)
            if cache.get(mStr):
                matrix = cache.get(mStr)
            else: 
                print(_, __, 'tiltMatrix MISS')
                matrix = tiltMatrix(matrix)
                cache[mStr] = matrix

            if cacheRotation.get(mStr):
                matrix = cacheRotation.get(mStr)
            else: 
                print(_, __, 'rotate90Clockwise MISS')
                matrix = rotate90Clockwise(matrix)
                cacheRotation[mStr] = matrix

        # PRINT_MATRIX_NOARR(matrix)
        answer = -1
        if cacheLoad.get(mStr):
            answer = cacheLoad.get(mStr)
        else:
            print(_, 'calculateLoad MISS')
            answer = calculateLoad(matrix)
            cacheLoad[mStr] = answer

        answers[answer] = answers.get(answer, []) + [_]
        # print(f'{_},{answer}')

        # if _ % 100000 == 0:
        #     print(_)

    # print(answers)

    answer = calculateLoad(matrix)

    # PRINT_ANSWER(answer)