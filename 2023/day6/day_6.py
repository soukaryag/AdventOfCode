import re 
from math import sqrt


def quad(a, b, c):
    upper = int((-1 * b + sqrt((b ** 2) - (4 * a * c))) / (2 * a))
    lower = int((-1 * b - sqrt((b ** 2) - (4 * a * c))) / (2 * a))

    return abs(upper-lower)

f = open("day_6.txt", "r")
lines = f.read().splitlines()

b = int(re.sub(' +', ' ', lines[0]).split(':')[1].strip())
c = int(re.sub(' +', ' ', lines[1]).split(':')[1].strip())
res = quad(-1, b, -c)

print("ANSWER:", res)
