from math import gcd
from functools import reduce


def lcm(arr):
    res = reduce(lambda x,y:(x*y) // gcd(x,y),arr)
    return res


def findSuperNode(startingNode):
    global BROADCASTER, FLIP_FLOP, CONJUNCTION, modules
    superNode = []
    binary = []
    q = [startingNode]
    
    CONJUNCTION_NODE = None
    nxtNodes, _ = modules.get(startingNode)

    for nodeName in nxtNodes:
        _, typ = modules.get(nodeName)
        if typ == CONJUNCTION:
            CONJUNCTION_NODE = nodeName
        elif typ == FLIP_FLOP:
            q.append(nodeName)

    while q:
        curr = q.pop(0)

        nxtNodes, _ = modules.get(curr)
        if curr not in superNode:
            superNode.append(curr)
            if CONJUNCTION_NODE in nxtNodes:
                binary.insert(0, '1')
            else:
                binary.insert(0, '0')
        
        for nodeName in nxtNodes:
            _, typ = modules.get(nodeName)
            if typ == FLIP_FLOP and nodeName not in superNode:
                q.append(nodeName)
            else:
                continue

    superNode.append(CONJUNCTION_NODE)
    return binary, superNode


def solveSuperNode(superNode):
    global BROADCASTER, FLIP_FLOP, CONJUNCTION, modules, state
    startNodeName = superNode[0]

    res = 0
    while True:
        res += 1
        q = [[startNodeName, modules.get(startNodeName), LOW_PULSE, None]]

        while q:
            currNode, nodeInfo, pulseType, prevNode = q.pop(0)

            if not nodeInfo:
                continue

            nxtNodes, instrType = nodeInfo

            if instrType == BROADCASTER:
                # just send a low pulse to all nxtNodes
                for node in nxtNodes:
                    q.append([node, modules.get(node), LOW_PULSE, currNode])
            elif instrType == FLIP_FLOP:
                if pulseType == HIGH_PULSE: continue
                elif pulseType == LOW_PULSE:
                    if states.get(currNode):
                        # flip-flip is on -> turn off and send low pulse
                        states[currNode] = False
                        for node in nxtNodes:
                            q.append([node, modules.get(node), LOW_PULSE, currNode])
                    else:
                        # flip-flip is off -> turn on and send high pulse
                        states[currNode] = True
                        for node in nxtNodes:
                            q.append([node, modules.get(node), HIGH_PULSE, currNode])
            elif instrType == CONJUNCTION:
                # check current state
                latestConjStates = states.get(currNode)
                latestConjStates[prevNode] = pulseType
                latestConjStatesValues = list(latestConjStates.values())

                if sum(latestConjStatesValues) == len(latestConjStatesValues) * HIGH_PULSE:
                    # if all remmebered pulses from input nodes are high -> send low)
                    # but in this case, we are done, just return
                    return res


if __name__ == '__main__':
    global BROADCASTER, FLIP_FLOP, CONJUNCTION, modules
    lines = open('day_20.txt', 'r')

    BROADCASTER = 'broadcaster'
    FLIP_FLOP = '%'
    CONJUNCTION = '&'
    SRC, DST, TYP = 'src', 'dst', 'type'

    LOW_PULSE = 1
    HIGH_PULSE = 2

    states = {}                 # on or off for flipflops, most recent input for conjunction
    modules = {}                # source : [[dest, ...], type]
    output_to_input_map = {}    # for conjunction modules
    for line in lines:
        source, dest = [i.strip() for i in line.strip().split('->')]
        dest = [i.strip() for i in dest.split(',')]
        for d in dest:
            if source != BROADCASTER:
                output_to_input_map[d] = output_to_input_map.get(d, []) + [source[1:]]

        instrType = BROADCASTER
        if source[0] == FLIP_FLOP:
            states[source[1:]] = False
            modules[source[1:]] = [dest, FLIP_FLOP]
            instrType = FLIP_FLOP
        elif source[0] == CONJUNCTION:
            modules[source[1:]] = [dest, CONJUNCTION]
            instrType = CONJUNCTION
        else:
            modules[source] = [dest, BROADCASTER]

    # fill in the states of the conjunctions
    for k, v in modules.items():
        if v[1] == CONJUNCTION:
            states[k] = {
                i: LOW_PULSE for i in output_to_input_map.get(k, [])
            }

    superNodes = []
    solutions = []
    binarySolutions = []
    for startNode in modules.get(BROADCASTER)[0]:
        # this is not needed but it took a while to write so I am keeping it >:(
        binary, sprNd = findSuperNode(startNode)
        binarySolutions.append(int(''.join(binary), 2))

        # find the first time the conjunction of each cluster outputs low pulse
        # 4 low pulses will get inverted to high pulse and get fed into a final inverter to make rx low pulse
        # so just find the lcm of the 4 clusters to see the first time they will overlap and all be low pulse
        sprNdLowPulseOutput = solveSuperNode([startNode])
        solutions.append(sprNdLowPulseOutput)
    
    PUSH_BUTTONS = lcm(solutions)
    BINARY_ANSWER = lcm(binarySolutions)
    print(f'ANSWER: {PUSH_BUTTONS}')
    print(f'BINARY ANSWER: {BINARY_ANSWER}')
