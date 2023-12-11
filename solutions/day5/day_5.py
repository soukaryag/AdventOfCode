from bisect import bisect
from functools import lru_cache
from collections import deque
from operator import itemgetter

# @lru_cache(maxsize=None)
# def cachedResult(i, nextVal):
#     idx = None
#     prevVal = None
#     if i == 0:
#         idx = bisect(seedToSoilArr, nextVal)
#         prevVal = seedToSoilArr[idx - 1]
#     elif i == 1:
#         idx = bisect(soilToFertilizerArr, nextVal)
#         prevVal = soilToFertilizerArr[idx - 1]
#     elif i == 2:
#         idx = bisect(fertilizerToWaterArr, nextVal)
#         prevVal = fertilizerToWaterArr[idx - 1]
#     elif i == 3:
#         idx = bisect(waterToLightArr, nextVal)
#         prevVal = waterToLightArr[idx - 1]
#     elif i == 4:
#         idx = bisect(lightToTempArr, nextVal)
#         prevVal = lightToTempArr[idx - 1]
#     elif i == 5:
#         idx = bisect(tempToHumidityArr, nextVal)
#         prevVal = tempToHumidityArr[idx - 1]
#     elif i == 6:
#         idx = bisect(humidityToLocationArr, nextVal)
#         prevVal = humidityToLocationArr[idx - 1]

    # # print(_, idx, prevVal, nextVal)
    # if not idx: nextVal
    
    # if idx % 2 == 1 or (idx % 2 == 0 and nextVal == prevVal and idx > 1):
    #     if idx % 2 == 0 and nextVal == prevVal and idx > 1:
    #         # nextValue is equal to the end value of a range
    #         if i == 0:
    #             prevVal = seedToSoilArr[idx - 2]
    #         elif i == 1:
    #             prevVal = soilToFertilizerArr[idx - 2]
    #         elif i == 2:
    #             prevVal = fertilizerToWaterArr[idx - 2]
    #         elif i == 3:
    #             prevVal = waterToLightArr[idx - 2]
    #         elif i == 4:
    #             prevVal = lightToTempArr[idx - 2]
    #         elif i == 5:
    #             prevVal = tempToHumidityArr[idx - 2]
    #         elif i == 6:
    #             prevVal = humidityToLocationArr[idx - 2]
            
    #         # print("Redoing prevVal to", prevVal)


    #     if i == 0:
    #         nextVal = seedToSoilDest[prevVal] + (nextVal - prevVal)
    #     elif i == 1:
    #         nextVal = soilToFertilizerDest[prevVal] + (nextVal - prevVal)
    #     elif i == 2:
    #         nextVal = fertilizerToWaterDest[prevVal] + (nextVal - prevVal)
    #     elif i == 3:
    #         nextVal = waterToLightDest[prevVal] + (nextVal - prevVal)
    #     elif i == 4:
    #         nextVal = lightToTempDest[prevVal] + (nextVal - prevVal)
    #     elif i == 5:
    #         nextVal = tempToHumidityDest[prevVal] + (nextVal - prevVal)
    #     elif i == 6:
    #         nextVal = humidityToLocationDest[prevVal] + (nextVal - prevVal)

    # return nextVal




if __name__ == '__main__':
    f = open('day_5.txt', 'r')

    order = {
        0: 'seed-to-soil',
        1: 'soil-to-fertilizer',
        2: 'fertilizer-to-water',
        3: 'water-to-light',
        4: 'light-to-temperature',
        5: 'temperature-to-humidity',
        6: 'humidity-to-location',
    }

    data = f.read().split('\n\n')
    seeds = [int(i) for i in data[0].split(':')[-1].strip().split()]
    steps = []

    for nums in data[1:]:
        lines = nums.split('\n')[1:]
        tmp = []
        for l in lines:
            tmp.append([int(n) for n in l.strip().split()])
        steps.append(tmp)

    res = float('inf')

    # print(steps)

    @lru_cache(maxsize=None)
    def overlap(currStart, currEnd, rangeStart, rangeEnd):
        # if left side is left of second bound AND right size is right of first bound -> then ranges overlap
        return currStart <= rangeEnd and currEnd >= rangeStart

    q = [(a, a + b - 1) for a, b in [seeds[i:i+2] for i in range(0, len(seeds), 2)]]


    for index, step in enumerate(steps):
        replaceQ = []

        oldQ = [i for i in q]
        while q:
            currStart, currEnd = q.pop(0)
            print('step', step, oldQ)
            for dest, source, iter in step:
                print(dest, source, iter, 'replaceQ:', replaceQ)
                rangeStart, rangeEnd = source, source + iter - 1
                delta = dest - source

                if not overlap(currStart, currEnd, rangeStart, rangeEnd):
                    # need to add back in?
                    continue

                if rangeStart <= currStart <= rangeEnd and rangeStart <= currEnd <= rangeEnd:
                    replaceQ.append((currStart + delta, currEnd + delta))
                    break
                if rangeStart <= currEnd <= rangeEnd:
                    replaceQ.append((rangeStart + delta, currEnd + delta))
                    # check if this has a smaller path down to the end
                    q.append((currStart, rangeStart - 1))
                    break
                if rangeStart <= currStart <= rangeEnd:
                    replaceQ.append((currStart + delta, rangeEnd + delta))
                    # check if this has a smaller path down to the end
                    q.append((rangeEnd + 1, currEnd))
                    break
                if currStart < rangeStart and currEnd > rangeEnd:
                    replaceQ.append((rangeStart + delta, rangeEnd + delta))
                    # check if these has a smaller path down to the end
                    q.append((rangeEnd + 1, currEnd))
                    q.append((currStart, rangeStart - 1))
                    break
            else:
                print("!!!!!!!!!!!!!")
                replaceQ.append((currStart, currEnd))



        print(f'==============={order[index]}===============')
        print(oldQ, 'maps to', replaceQ, '\n')
        q = replaceQ

    # sort by start of range and get the smallest value
    res = sorted(q, key=lambda el: el[0])[0][0]
    print("Answer:", res)
