import sys
sys.path.append('../..')
from utils.constants import *

from functools import lru_cache
import re


def substrDoesntWork(row, rowIdx, doesntWork):
    for i in range(rowIdx):
        if doesntWork.get(row[0:i]):
            return True
    
    return False

"""
ENDED UP NOT USING THIS!
"""
# @lru_cache(maxsize=None)
def getRowArrangements(row, emotionalDamage):
    res = 0
    n = len(row)
    q = [[row, 0]]  # modified row string, row_index

    doesntWork = {}

    while q:
        row, rowIdx = q.pop()
        # print(rowIdx, row)
        skip = False

        if rowIdx != 0:
            groupingsArrFromRow = getGroupingsFromRow(row)
            # print("groupingsArrFromRow", groupingsArrFromRow)
            # print("emotionalDamage", emotionalDamage)
            for i, g in enumerate(groupingsArrFromRow):
                if i == len(groupingsArrFromRow) - 1: continue

                if g != emotionalDamage[i]:
                    # print('!!!!!!!!!!!!!!')
                    for j in range(rowIdx, n + 1):
                        # print('adding', row[0: j + 1])
                        doesntWork[row[0: j + 1]] = True

                    skip = True
                    break

        if skip: continue
        # print(doesntWsork)

        if rowIdx == n:
            if isEqualGrouping(groupingsArrFromRow, emotionalDamage):
                res += 1
            else:
                for i in range(rowIdx, n + 1):
                    doesntWork[row[0: i - 1]] = True
            continue

        if not substrDoesntWork(row, rowIdx, doesntWork):
            if row[rowIdx] == '?':
                q.append([row[:rowIdx] + '.' + row[rowIdx + 1:], rowIdx + 1])
                q.append([row[:rowIdx] + '#' + row[rowIdx + 1:], rowIdx + 1])
            else:
                q.append([row, rowIdx + 1])

        # print('====================')

    return res


"""
Takes subset of full row and subset of broken group and the running broken group length
Returns the total number of possible arrangements of broken groups in row
"""
@lru_cache(maxsize=None)
def recurse(row, brokenGroups, currGroupLen=0):
    if not brokenGroups and '#' not in row: 
        return 1
    elif not row and len(brokenGroups) == 1 and currGroupLen == brokenGroups[0]:
        return 1
    elif not row and not brokenGroups:
        return 1
    elif not row or not brokenGroups: 
        return 0
    
    if currGroupLen > brokenGroups[0] or (currGroupLen > 0 and not brokenGroups):
        return 0

    res = 0    
    if row[0] == '.':
        if currGroupLen == 0:
            # print("Counting as FIRST .\n")
            res += recurse(row[1:], brokenGroups, 0)
        else:
            # print("Counting as .")
            if brokenGroups[0] == currGroupLen:
                # print("Completed a broken set!!!")
                res += recurse(row[1:], brokenGroups[1:], 0)
    elif row[0] == '#':
        # print("Counting as #\n")
        res += recurse(row[1:], brokenGroups, currGroupLen + 1)
    elif row[0] == '?':
        # print("Found a ?")
        if currGroupLen == brokenGroups[0] or not brokenGroups:
            # print("Counting as .\n")
            # this means it should be '.'
            # print("Completed a broken set!!!")
            res += recurse(row[1:], brokenGroups[1:], 0)
        elif currGroupLen < brokenGroups[0]:
            # this means it should be '#'
            if currGroupLen == 0:
                # print("Counting as . or #\n")
                res += recurse(row[1:], brokenGroups, 0) + recurse(row[1:], brokenGroups, 1)
            elif currGroupLen > 0:
                # print("Counting as #\n")
                res += recurse(row[1:], brokenGroups, currGroupLen + 1)

        else:
            print("AHHH SOMETHING IS SUPER WRONG")

    # print(''.join(row), "RESULT:", res)
    return res



def getGroupingsFromRow(row):
    # print("getGroupingsFromRow", _RE_COMBINE_PERIODS.sub('.', row.replace('?', '.')).strip('.').split('.'))
    return [len(i) for i in _RE_COMBINE_PERIODS.sub('.', row.replace('?', '.')).strip('.').split('.')]


def isEqualGrouping(groupingsArrFromRow, groups):
    return groups == groupingsArrFromRow


if __name__ == '__main__':
    global _RE_COMBINE_PERIODS

    _RE_COMBINE_PERIODS = re.compile(r"[\.]+")
    lines = JUST_READ_FILE()
    records = []
    brokenGroups = []
    for line in lines:
        record, bG = line.split(' ')

        # part 2
        records.append('?'.join([record.strip()] * 5))
        brokenGroups.append([int(i) for i in bG.split(',') * 5])

        # part 1
        # records.append(record.strip())
        # brokenGroups.append(bG.strip())

    answer = 0
    for idx, row in enumerate(records):
        res = recurse(tuple(list(row)), tuple(brokenGroups[idx]))
        # print(idx, res)
       
        answer += res

    PRINT_ANSWER(answer)
