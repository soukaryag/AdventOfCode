from collections import defaultdict
import sys
sys.path.append('../..')
from utils.constants import *

dirShapesOpposite = {
    '>': (0, 1),
    '<': (0,-1),
    'v': (1, 0),
    '^': (-1, 0)
}

dirShapes = {
    (0, 1): '>',
    (0,-1): '<',
    (1, 0): 'v',
    (-1, 0): '^'
}


if __name__ == '__main__':
    global n, m
    lines = JUST_READ_FILE()

    matrix = []
    for line in lines:
        matrix.append(list(line))

    n, m = len(matrix), len(matrix[0])
    start = (0, matrix[0].index('.'))
    end = (n - 1, matrix[n-1].index('.'))

    visited = {}                                            # {pathId: (coords, ...), ...}
    hikeLength = -INFINITY

    cache = {}                                              # cache longest path to end from node
    intersections = defaultdict(set)                        # {pathId: set([intersectionCoords, ...])}
    q = [(start, f'{start[0]}{start[1]};', None, 0)]        # node, pathId, parentPathId, currHikeLength
    while q:
        curr, pathId, parentPathId, currLength = q.pop()
        y, x = curr

        # print(len(visited.keys()))

        if cache.get(curr, [-INFINITY])[0] > currLength:
            # check that they have visited the same intersections
            maxStepsToHere, maxPathId = cache.get(curr, [-INFINITY])
            if set(visited.get(maxPathId, [])) == set(intersections.get(pathId, [])):
                print("HIT CACHE AT", curr)
                # cachedLength = cache.get(curr)

                # pathLength = len(visited[pathId]) - 1
                # for i, c in enumerate(visited[pathId]):
                #     cache[c] = max(cache.get(c, -INFINITY), pathLength + cachedLength - i)

                # if currLength + cachedLength > hikeLength:
                #     print("SETTING TO", currLength)
                #     hikeLength = currLength
                continue

        if not visited.get(pathId):
            visited[pathId] = [i for i in visited.get(parentPathId, [])]
        visited[pathId].append(curr)

        if curr == end:
            # update cache
            for i, c in enumerate(visited[pathId]):
                if i + 1 > cache.get(c, [-INFINITY])[0]:
                    cache[c] = (i + 1, pathId)
                
            if currLength > hikeLength:
                hikeLength = currLength
            continue

        newBranch = False
        for dy, dx in FOUR_WAY_DIRECTIONS:
            newY, newX = y + dy, x + dx

            if IS_INBOUNDS(newY, newX, n, m) and (newY, newX) not in visited.get(pathId, {}) \
                and (matrix[newY][newX] == '.' or matrix[newY][newX] == dirShapes.get((dy, dx), '.')):
                newParent = None
                newPathId = pathId
                if newBranch:
                    # this is an INTERSECTION, cache it
                    newParent = pathId
                    newPathId = pathId + f'{newY}{newX};'
                    intersections[curr].add(pathId)
                    intersections[curr].add(newPathId)

                q.append(((newY, newX), newPathId, newParent, currLength + 1))
                newBranch = True
                
    
    PRINT_ANSWER_MAC(hikeLength)
    