
f = open("day_1.txt", "r")
res = 0
nums = [str(i) for i in range(0, 10)]
replacements = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9"
}

for line in f:
    val = ""
    print(line)
    newLine = ""
    itr = 0
    while itr < len(line):
        swapped = False
        for x in range(3, 6):
            subStr = line[itr: itr + x]
            # print(subStr)
            if replacements.get(subStr):
                newLine += replacements[subStr]
                swapped = True
                break

        if not swapped:
            newLine += line[itr]

        itr += 1

    print(newLine)
    for i in range(len(newLine)):
        if newLine[i] in nums:
            val = newLine[i]
            break
    
    for i in range(len(newLine) - 1, -1, -1):
        if newLine[i] in nums:
            val += newLine[i]
            break

    if val:
        res += int(val)

print(res)