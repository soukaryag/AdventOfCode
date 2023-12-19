import sys
sys.path.append('../..')
from utils.constants import *


if __name__ == '__main__':
    global n, m
    lines = JUST_READ_FILE()

    MIN_VALUE = 1
    MAX_VALUE = 4000

    acceptedValues = {
        'x': [MIN_VALUE, MAX_VALUE],
        'm': [MIN_VALUE, MAX_VALUE],
        'a': [MIN_VALUE, MAX_VALUE],
        's': [MIN_VALUE, MAX_VALUE],
    }

    workflows = {}
    parts = []
    addingWorkflows = True
    for line in lines:
        if line.strip() == '':
            addingWorkflows = False
            continue

        if addingWorkflows:
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
        else:
            line = line.lstrip('{').rstrip('}')
            splitParts = line.split(',')
            addToParts = {}
            for part in splitParts:
                name, num = part.split('=')
                addToParts[name] = int(num)

            parts.append(addToParts)


    accepted = []
    for idx, part in enumerate(parts):
        workflowStepName = 'in'
        # print('\nNEW PART ------------------------------', idx, part)

        while workflowStepName:
            if workflowStepName == 'A':
                # print('accepted!')
                workflowStepName = None
                accepted.append(part)
                break
            elif workflowStepName == 'R':
                # print('rejceted!')
                workflowStepName = None
                break
            workflow = workflows.get(workflowStepName)
            # print('NEW WORKFLOW STEP ---------------------', workflowStepName)
            
            for step in workflow:
                # print('NEW STEP ---------------------', step)
                check, nxtStepName = step

                if not check:
                    # print('skip to', nxtStepName)
                    workflowStepName = nxtStepName
                    break

                partName, operator, value = check

                checkValue = value
                partValue = part.get(partName, 0)

                if operator == '<':
                    if partValue < checkValue:
                        # print('skip to', nxtStepName)
                        workflowStepName = nxtStepName 
                        break
                elif operator == '>':
                    if partValue > checkValue:
                        # print('skip to', nxtStepName)
                        workflowStepName = nxtStepName 
                        break

                # print('continuing check, did not match')


    answer = 0
    for prt in accepted:
        for v in prt.values():
            answer += v


    PRINT_ANSWER(answer)
    