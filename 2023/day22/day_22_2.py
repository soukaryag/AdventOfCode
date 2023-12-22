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


def dropBrick(brick, brickName, dropped=False):
    global visited
    a, b = brick
    x1, y1, z1 = a
    x2, y2, z2 = b

    # first coord will ALWAYS be lower 
    # because of sorting during input parsing
    if z1 == 1:
        # ground, end it here
        addBrickToState(brick, brickName)
        return brick, dropped
    
    z1 -= 1
    z2 -= 1
    newBrickLocation = [[x1, y1, z1], [x2, y2, z2]]
    allCollisions = checkBrickCollision(newBrickLocation, brickName)
    if allCollisions:
        addBrickToState(brick, brickName)
        return brick, dropped

    return dropBrick(newBrickLocation, brickName, True)


def stablize(br):
    bricks = sorted(br, key=lambda y: y[0][2])
    newBricks = []
    dropped = 0
    for idx, brick in enumerate(bricks):
        newBrick, wasDropped = dropBrick(brick, getBrickName(idx))
        if wasDropped: dropped += 1
        newBricks.append(newBrick)

    return newBricks, dropped


if __name__ == '__main__':
    global n, VERTICAL, HORIZONTAL, visited
    lines = open('day_22.txt', 'r')

    VERTICAL = 'v'
    HORIZONTAL = 'h'

    GROUND = 1

    visited = {}    # {(x,y,z): brickIdx, ...}          Maps coords to what brick owns it
    BRICKS = []
    for line in lines:
        positions = line.strip().split('~')
        brick = [[int(i) for i in p.split(',')] for p in positions]
        brick = sorted(brick, key=lambda y: y[2])
        BRICKS.append(brick)

    n = len(BRICKS)  
    BRICKS, _ = stablize(BRICKS)

    answer = 0
    for i, _ in enumerate(BRICKS):
        visited = {}
        # remove a brick a restablize
        removedBrick = BRICKS[:i] + BRICKS[i+1:]
        _, affected = stablize(removedBrick)
        answer += affected
        print(getBrickName(i), affected)


    print(f'ANSWER: {answer}')
