


f = open("day_9.txt", "r")
lines = f.read().splitlines()

results = []


for line in lines:
    curr = [int(i) for i in line.split()]
    q = [curr]
    print(curr)
    while len(set(curr)) > 1:
        newArr = []
        for i in range(0, len(curr) - 1):
            newArr.append(curr[i+1] - curr[i])
        
        curr = newArr
        print(curr)
        q.insert(0, newArr)

    print('----')
    toAdd = 0
    while q:
        currSequence = q.pop(0)
        if not currSequence: continue
        
        toAdd = currSequence[0] - toAdd
        
    results.append(toAdd)
        
print(results)

print(f"ANSWER: {sum(results)}")