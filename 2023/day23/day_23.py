from collections import defaultdict
import sys
sys.path.append('../..')
from utils.constants import *

"""
Intuition: 
Reduce the probelm from a matrix to a graph of nodes represnting intersections in the graph.
Intersection is given by nodes that have > 2 paths outgoing from it.
Then the edges between these nodes is the direct distance within the matrix from one intersection to another

Perform longest distance on this graph q.e.d
"""


def isIntersection(coords):
    global n, m, matrix
    y, x = coords

    waysForward = 0
    for dy, dx in FOUR_WAY_DIRECTIONS:
        newY, newX = y + dy, x + dx

        if IS_INBOUNDS(newY, newX, n, m) and matrix[newY][newX] != '#':
            waysForward += 1
        
        if waysForward >= 3: return True

    return False


def findAllEdges(coords):
    global n, m, matrix, nodes, edges
    for delY, delX in FOUR_WAY_DIRECTIONS:
        start = (coords[0] + delY, coords[1] + delX)
        if not IS_INBOUNDS(start[0], start[1], n, m) or matrix[start[0]][start[1]] == '#': continue
        
        visited = {coords: True}
        q = [(start, 1)]
        while q:
            curr, currLength = q.pop()
            y, x = curr

            if curr in nodes:
                # reached another intersection, terminate and add to edges
                nodes[coords] += [curr]
                if (curr, coords) not in edges:
                    edges[(coords, curr)] = currLength
                continue

            visited[curr] = True

            for dy, dx in FOUR_WAY_DIRECTIONS:
                newY, newX = y + dy, x + dx
                newCoords = (newY, newX)
                if IS_INBOUNDS(newY, newX, n, m) and matrix[newY][newX] != '#' and not visited.get(newCoords):
                    q.append((newCoords, currLength + 1))


if __name__ == '__main__':
    global n, m, matrix, nodes, edges
    lines = JUST_READ_FILE()

    matrix = []
    for line in lines:
        matrix.append(list(line.replace('>', '.').replace('v', '.').replace('<', '.').replace('^', '.')))

    n, m = len(matrix), len(matrix[0])
    start = (0, matrix[0].index('.'))
    end = (n - 1, matrix[n-1].index('.'))

    nodes = defaultdict(list)                                       # These are the intersections, mapping to their immediate neighbors
    edges = defaultdict(int)                                        # These are the distance between intersections
    
    nodes[start] = []
    nodes[end] = []

    # find all intersections
    for i in range(n):
        for j in range(m):
            curr = (i, j)
            if matrix[i][j] != '#' and isIntersection(curr):
                nodes[curr] = []

    # calculate all edges
    for node in nodes.keys():
        findAllEdges(node)

    PRINT_DICT(edges)
    LONGEST_HIKE = -INFINITY
    q = [(start, 0, [])]         # currNode, currPath, visited
    while q:
        curr, currPath, v = q.pop()
        visited = [i for i in v]
        visited.append(curr)

        if curr == end:
            print('END', currPath)
            LONGEST_HIKE = max(LONGEST_HIKE, currPath)
            # matrixCopy = [[matrix[i][j] for j in range(m)] for i in range(n)]
            # for idx, ij in enumerate(v):
            #     i, j = ij
            #     matrixCopy[i][j] = str(idx + 1)
            # PRINT_MATRIX_NOARR(matrixCopy)
            continue
        
        neighbors = nodes[curr]
        for neighbor in neighbors:
            if neighbor not in visited:
                edgeLength = edges.get((curr, neighbor))
                if not edgeLength: edgeLength = edges.get((neighbor, curr))
                q.append((neighbor, currPath + edgeLength, visited))
        
    PRINT_ANSWER_MAC(LONGEST_HIKE)
    