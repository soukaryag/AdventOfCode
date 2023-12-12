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


# @lru_cache(maxsize=None)
def getRowArrangements(row, emotionalDamage):
    res = 0
    n = len(row)
    q = [[row, 0]]  # modified row string, row_index

    doesntWork = {}

    while q:
        row, rowIdx = q.pop()
        print(rowIdx, row)
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

        print('====================')

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
        record, brokenGroup = line.split(' ')

        records.append('?'.join([record.strip()] * 5))
        brokenGroups.append([int(i) for i in brokenGroup.split(',') * 5])

        # records.append(record.strip())
        # brokenGroups.append(brokenGroup.strip())

    # print(records, brokenGroups)

    answer = 0
    for idx, row in enumerate(records):
        tmp = getRowArrangements(row, brokenGroups[idx])
        print(idx, tmp)
        
        answer += tmp

    PRINT_ANSWER(answer)
