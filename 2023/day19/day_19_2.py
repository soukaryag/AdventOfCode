import sys
sys.path.append('../..')
from utils.constants import *


def copyArray(a):
    return [[a[x][y] for y in range(len(a[0]))] for x in range(len(a))]


def getMultiplication(combs):
    res = 1
    for comb in combs:
        lower, upper = comb
        res *= upper - lower + 1

    return res


def recurse(stepName, tracking):
    # make it copy to not alter pass by reference array
    tracking = copyArray(tracking)

    # base case
    if stepName == 'A':
        return getMultiplication(tracking)
    elif stepName == 'R':
        return 0
    
    stepInstructions = workflows.get(stepName, [])

    answer = 0
    for step in stepInstructions:
        check, nxtStepName = step

        if not check:
            answer += recurse(nxtStepName, tracking)
            continue

        partName, operator, value = check
        partIdx = PART_TO_IDX.get(partName, 0)

        if operator == '<':
            prevValue = tracking[partIdx][UPPER]
            tracking[partIdx][UPPER] = value - 1

            answer += recurse(nxtStepName, tracking)

            tracking[partIdx][UPPER] = prevValue
            tracking[partIdx][LOWER] = value
        elif operator == '>':
            prevValue = tracking[partIdx][LOWER]
            tracking[partIdx][LOWER] = value + 1

            answer += recurse(nxtStepName, tracking)

            tracking[partIdx][UPPER] = value
            tracking[partIdx][LOWER] = prevValue

    return answer
    
    


if __name__ == '__main__':
    global n, m, workflows, PART_TO_IDX, MIN_VALUE, MAX_VALUE, UPPER, LOWER
    lines = JUST_READ_FILE()

    UPPER, LOWER = 1, 0
    MIN_VALUE = 1
    MAX_VALUE = 4000
    PART_TO_IDX = {
        'x': 0,
        'm': 1,
        'a': 2,
        's': 3,
    }


    workflows = {}
    for line in lines:
        if line.strip() == '':
            break

        workflowName = line.split('{')[0]
        workflowDefinition = line.split('{')[1].rstrip('}')

        workflowDefSplit = workflowDefinition.split(',')
        addToWorkflow = []
        for subWorkflow in workflowDefSplit:
            if ':' in subWorkflow:
                check, nxt = subWorkflow.split(':')
                check = [check[0], check[1], int(check[2:])]
                addToWorkflow.append([check, nxt])
            else:
                addToWorkflow.append([None, subWorkflow])

        workflows[workflowName] = addToWorkflow

    answer = recurse('in', [[MIN_VALUE, MAX_VALUE], [MIN_VALUE, MAX_VALUE], [MIN_VALUE, MAX_VALUE], [MIN_VALUE, MAX_VALUE]])


    PRINT_ANSWER(answer)
    