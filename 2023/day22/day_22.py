from collections import defaultdict
from functools import lru_cache
from math import sqrt
import json


def getBrickName(i):
    return chr(i + 97)

@lru_cache(maxsize=None)
def getBrickSize(brick):
    brick = json.loads(brick)
    a, b = brick
    x1, y1, z1 = a
    x2, y2, z2 = b

    # return int(sqrt(abs(x1 - x2)**2 + abs(y1 - y2)**2 + abs(z1 - z2)**2)) + 1

    if x1 != x2:
        return abs(x1-x2) + 1
    elif y1 != y2:
        return abs(y1-y2) + 1
    elif z1 != z2:
        return abs(z1-z2) + 1
    else:
        return 1


@lru_cache(maxsize=None)
def getBrickOrientation(brick):
    brick = json.loads(brick)
    a, b = brick
    x1, y1, z1 = a
    x2, y2, z2 = b

    if z1 != z2: return VERTICAL
    else: return HORIZONTAL


def addBrickToState(brick, brickName):
    global visited
    a, b = brick
    x1, y1, z1 = a
    x2, y2, z2 = b

    if x1 != x2:
        for j in range(min(x1, x2), max(x1, x2) + 1):
            visited[(j, y1, z1)] = brickName
    elif y1 != y2:
        for i in range(min(y1, y2), max(y1, y2) + 1):
            visited[(x1, i, z1)] = brickName
    elif z1 != z2:
        for k in range(min(z1, z2), max(z1, z2) + 1):
            visited[(x1, y1, k)] = brickName
    else:
        visited[(x1, y1, z1)] = brickName


def checkBrickCollision(brick, brickName):
    global visited
    a, b = brick
    x1, y1, z1 = a
    x2, y2, z2 = b

    allCollisions = []
    # print(visited)
    # print(brickName, brick)

    if x1 != x2:
        for j in range(min(x1, x2), max(x1, x2) + 1):
            if visited.get((j, y1, z1)):
                allCollisions.append(visited.get((j, y1, z1)))
    elif y1 != y2:
        for i in range(min(y1, y2), max(y1, y2) + 1):
            if visited.get((x1, i, z1)):
                allCollisions.append(visited.get((x1, i, z1)))
    elif z1 != z2:
        for k in range(min(z1, z2), max(z1, z2) + 1):
            if visited.get((x1, y1, k)):
                allCollisions.append(visited.get((x1, y1, k)))
    else:
        if visited.get((x1, y1, z1)):
            allCollisions.append(visited.get((x1, y1, z1)))

    return list(set(allCollisions))


def dropBrick(brick, brickName):
    global visited, supportedBy, supporting
    a, b = brick
    x1, y1, z1 = a
    x2, y2, z2 = b

    # first coord will ALWAYS be lower 
    # because of sorting during input parsing
    if z1 == 1:
        # ground, end it here
        addBrickToState(brick, brickName)
        supportedBy[brickName] = [GROUND]
        return brick
    
    z1 -= 1
    z2 -= 1
    newBrickLocation = [[x1, y1, z1], [x2, y2, z2]]
    allCollisions = checkBrickCollision(newBrickLocation, brickName)
    if allCollisions:
        addBrickToState(brick, brickName)
        supportedBy[brickName] = allCollisions
        for cl in allCollisions:
            supporting[cl].append(brickName)
        return brick

    return dropBrick(newBrickLocation, brickName)


if __name__ == '__main__':
    global n, VERTICAL, HORIZONTAL, visited, supportedBy, supporting
    lines = open('day_22.txt', 'r')

    VERTICAL = 'v'
    HORIZONTAL = 'h'

    GROUND = 1

    visited = {}                        # {(x,y,z): brickIdx, ...}          Maps coords to what brick owns it
    supportedBy = defaultdict(list)     # {brickIdx: [brickIdx, ...], ...}  Maps what each brick is supported by in the level directly below
    supporting = defaultdict(list)      # {brickIdx: [brickIdx, ...], ...}  Maps what each brick is supporting directly a level above
    bricks = []
    for line in lines:
        positions = line.strip().split('~')
        brick = [[int(i) for i in p.split(',')] for p in positions]
        brick = sorted(brick, key=lambda y: y[2])
        bricks.append(brick)

    n = len(bricks)  

    bricks = sorted(bricks, key=lambda y: y[0][2])
    newBricks = []
    for idx, brick in enumerate(bricks):
        newBrick = dropBrick(brick, getBrickName(idx))
        newBricks.append(newBrick)

    processed = {}
    disintegrate = []
    for k, v in supportedBy.items():
        if not supporting.get(k):
            # this is at the top of the stack, add it automatically
            disintegrate.append(k)
        if len(v) == 1:
            # this is supported by only one thing, can't remove it's supports!
            continue

        for s in list(v):
            # loop through all supports (s) and make sure everything s
            # is supporting is supported by something else
            if s in processed:
                 continue

            canBeRemoved = True
            sSupports = supporting.get(s, [])
            for heldByS in sSupports:
                if len(supportedBy.get(heldByS, [])) < 2:
                    # doesn't work, s is the sole support for this
                    canBeRemoved = False
                    break

            if canBeRemoved:
                disintegrate.append(s)
            
            processed[s] = True

        

    print(disintegrate)




    # print(supportedBy)
    # print(supporting)


    print(f'ANSWER: {len(disintegrate)}')