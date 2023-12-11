

f = open("day_2.txt", "r")

# part 1
# available = {
#     "red": 12,
#     "green": 13,
#     "blue": 14
# }
# res = 0
# for line in f:
#     possible = True
#     game, sets = line.split(":")

#     sets = sets.split(";")

#     for set in sets:
#         cubes  = set.strip().split(",")
#         for cube in cubes:
#             num, color = cube.strip().split(" ")
#             if available.get(color, 0) < int(num):
#                 possible = False
#                 break
        
#         if not possible: break

#     if possible:
#         _, id = game.split(" ")
#         res += int(id)


# part 2
res = 0
for line in f:
    game, sets = line.split(":")

    sets = sets.split(";")
    r, g, b = float('-inf'), float('-inf'), float('-inf')

    for set in sets:
        cubes  = set.strip().split(",")
        for cube in cubes:
            num, color = cube.strip().split(" ")
            if color == 'red' and r < int(num):
                r = int(num)
            elif color == 'green' and g < int(num):
                g = int(num)
            elif color == 'blue' and b < int(num):
                b = int(num)

    res += r * g * b

print(res)
