

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
        
steps = 0
while True:
    done = True
    for idx, curr in enumerate(currs):
        next = nodes.get(curr, {}).get(directions[steps % dirLength])
        currs[idx] = next
        if next[-1] != 'Z': done = False
        
    steps += 1
    if done: break


print("ANSWER:", steps)
