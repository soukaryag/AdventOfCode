from math import gcd
from functools import reduce

def lcm(arr):
    res = reduce(lambda x,y:(x*y) // gcd(x,y),arr)
    return res


f = open("day_8.txt", "r")
lines = f.read().splitlines()

directions = lines.pop(0).strip()
dirLength = len(directions)
lines.pop(0)
nodes = {}
currs = []

for line in lines:
    node, next = line.split(' = ')
    nodes[node] = {'L': next[1:4], 'R': next[6:9]}
    if node[-1] == 'A':
        currs.append(node)
        
print(currs)

def stepsRequired(curr):
    steps = 0
    while curr[-1] != 'Z':
        curr = nodes.get(curr, {}).get(directions[steps % dirLength])
        steps += 1

    return steps

results = []
for idx, curr in enumerate(currs):
    res = stepsRequired(curr)
    print(curr, res)

    results.append(res)

print(lcm(results))
