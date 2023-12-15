from collections import defaultdict
from functools import lru_cache
import sys
sys.path.append('../..')
from utils.constants import *


@lru_cache(maxsize=None)
def hash(word):
    value = 0

    for c in word:
        value += ord(c)
        value *= 17
        value = value %256

    return value


def focusingPower(hashmap):
    power = 0
    for k, v in hashmap.items():
        for i, lens in enumerate(v):
            addingPower = (k + 1) * (i + 1) * int(lens[1])
            power += addingPower 

    return power


if __name__ == '__main__':
    global n, m
    lines = JUST_READ_FILE()

    hashmap = defaultdict(list)

    answer = 0
    for word in lines[0].split(','):
        hsh = 0
        word = word.strip()
        if '=' in word:
            label, focalLength = word.split('=')
            hsh = hash(label)

            arr = hashmap.get(hsh)
            exists = None
            if arr:
                exists = next((i for i, v in enumerate(arr) if v[0] == label), None)

            if exists != None:
                arr[exists] = (label, focalLength)
                hashmap[hsh] = arr
            elif arr:
                hashmap[hsh] = arr + [(label, focalLength)]
            else:
                hashmap[hsh] = [(label, focalLength)]

        elif '-' in word:
            label = word.split('-')[0]
            hsh = hash(label)

            arr = hashmap.get(hsh)
            exists = None
            if arr:
                exists = next((i for i, v in enumerate(arr) if v[0] == label), None)

                if exists != None:
                    del arr[exists]
                    hashmap[hsh] = arr

                
    answer = focusingPower(hashmap)

    PRINT_ANSWER(answer)

    