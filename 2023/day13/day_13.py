import sys
sys.path.append('../..')
from utils.constants import *


def differencesInArray(arr1, arr2):
    res = 0
    for i in range(len(arr1)):
        if arr1[i] != arr2[i]: res += 1

    return res


def findReflectionByRow(matrix): 
    n = len(matrix)

    for i in range(1, n):
        smudges = 0
        for j in range(0, i):
            if 0 <= i-j-1 < n and 0 <= i+j < n:
                smudges += differencesInArray(matrix[i-j-1], matrix[i+j])

                if smudges > SMUDGES_CONSTANT:
                    break

        if smudges == SMUDGES_CONSTANT:
            return i
        
    return -1


if __name__ == '__main__':
    global SMUDGES_CONSTANT
    lines = JUST_READ_FILE()

    SMUDGES_CONSTANT = 1
    matrixes = []
    tmp = []
    for line in lines:
        line = line.strip()
        if line:
            tmp.append(list(line))
        else:
            matrixes.append(tmp)
            tmp = []

    matrixes.append(tmp)

    answer = 0
    for idx, matrix in enumerate(matrixes):
        tmpRes = findReflectionByRow(matrix)

        if tmpRes == -1:
            tmpRes = findReflectionByRow(TRANSPOSE_MATRIX(matrix))
            answer += tmpRes
        else:
            answer += 100 * tmpRes
        

    PRINT_ANSWER(answer)
