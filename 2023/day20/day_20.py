if __name__ == '__main__':
    global n, m, BROADCASTER, FLIP_FLOP, CONJUNCTION
    lines = open('day_20.txt', 'r')

    BROADCASTER = 'broadcaster'
    FLIP_FLOP = '%'
    CONJUNCTION = '&'
    SRC, DST, TYP = 'src', 'dst', 'type'

    LOW_PULSE = 1
    HIGH_PULSE = 2


    states = {}  # on or off for flipflops, most recent input for conjunction
    modules = {}  # source : [[dest, ...], type]
    output_to_input_map = {}   # for conjunction modules
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

    # print(modules)
    # print()
    # print(states)
    # print()
    # print(output_to_input_map)
    # exit()

    PUSH_BUTTONS = 0
    # high_count = 0
    # low_count = 0

    while True:
        PUSH_BUTTONS += 1
        if PUSH_BUTTONS % 1000000 == 0: print(PUSH_BUTTONS)
        start = modules.get(BROADCASTER)
        q = [[BROADCASTER, start, LOW_PULSE, None]]    # [[currentNode, [[nextNodes,...], nodeType], pulseType, previousNode], ...]
        while q:
            currNode, nodeInfo, pulseType, prevNode = q.pop(0)

            if currNode == 'rx' and pulseType == LOW_PULSE:
                print(f'PART 2: {PUSH_BUTTONS}')
                exit()

            # if pulseType == HIGH_PULSE: high_count += 1
            # if pulseType == LOW_PULSE: low_count += 1

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
                    # if all remmebered pulses from input nodes are high -> send low
                    for node in nxtNodes:
                        q.append([node, modules.get(node), LOW_PULSE, currNode])
                else:
                    # otherwise, if at least one low pulse exists -> send high
                    for node in nxtNodes:
                        q.append([node, modules.get(node), HIGH_PULSE, currNode])

    # print(high_count, low_count)

    # print(f'ANSWER: {high_count * low_count}')
