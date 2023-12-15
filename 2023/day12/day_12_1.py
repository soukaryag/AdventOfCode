import sys
sys.path.append('../..')
from utils.constants import *

from functools import lru_cache
import re


def substrDoesntWork(row, doesntWork):
    n = len(row)
    for i in range(n // 2, n):
        if doesntWork.get(row[0:i]):
            return True
    
    return False


# @lru_cache(maxsize=None)
def getRowArrangements(row, emotionalDamage):
    res = 0
    n = len(row)
    q = [[row, 0]]  # modified row string, row_index

    # doesntWork = {}

    while q:
        row, rowIdx = q.pop()
        # print(rowIdx, row)

        if rowIdx == n:
            if isEqualGrouping(row, emotionalDamage):
                res += 1
            # else:
            #     for i in range(n // 2, n):
            #         doesntWork[row[0:i]] = True
            continue

        if row[rowIdx] == '?':
            q.append([row[:rowIdx] + '.' + row[rowIdx + 1:], rowIdx + 1])
            q.append([row[:rowIdx] + '#' + row[rowIdx + 1:], rowIdx + 1])
        else:
            q.append([row, rowIdx + 1])

    return res


def isEqualGrouping(row, groups):
    tmp = [str(len(i)) for i in _RE_COMBINE_PERIODS.sub('.', row).strip('.').replace('#', '?').split('.')]
    # print("isEqualGrouping", ','.join(tmp), groups)
    
    return groups == ','.join(tmp)


if __name__ == '__main__':
    global _RE_COMBINE_PERIODS

    _RE_COMBINE_PERIODS = re.compile(r"[\.]+")
    lines = JUST_READ_FILE()
    records = []
    brokenGroups = []
    for line in lines:
        record, brokenGroup = line.split(' ')

        # records.append('?'.join([record.strip()] * 5))
        # brokenGroups.append(','.join([brokenGroup.strip()] * 5))

        records.append(record.strip())
        brokenGroups.append(brokenGroup.strip())

    # print(records, brokenGroups)

    answer = 0
    for idx, row in enumerate(records):
        tmp = getRowArrangements(row, brokenGroups[idx])
        print(idx, tmp)
        
        answer += tmp

    PRINT_ANSWER(answer)
