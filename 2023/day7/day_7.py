from functools import lru_cache


strength = ['J', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'Q', 'K', 'A']
strengthStr = ''.join(strength)

@lru_cache(maxsize=None)
def getType(hand):
    count = {i: 0 for i in strength}

    for h in hand:
        count[h] += 1

    J = count['J']
    del count['J']
    vals = sorted(list(count.values()), reverse=True)[:5]
    
    # print(hand, vals)
    if vals[0] + J == 5:
        return '5'
    elif vals[0] + J == 4:
        return '4'
    elif (vals[0] == 3 and vals[1] + J == 2) or (vals[0] + J == 3 and vals[1] == 2):
        return 'F'
    elif vals[0] + J == 3:
        return '3'
    elif vals[0] == 2 and vals[1] + J == 2:
        return '2P'
    elif vals[0] + J == 2:
        return 'P'
    elif vals[0] == 1 and J == 0:
        return 'H'

    return None


def breakTie(type):
    lst = rankings.get(type, [])
    return sorted(lst, key=lambda word: [strengthStr.index(lst) for lst in word])


if __name__ == '__main__':
    f = open('day_7.txt', 'r')

    lines = f.read().splitlines()
    
    n = len(lines)
    ranks = ['H', 'P', '2P', '3', 'F', '4', '5']
    rankings = {r: [] for r in ranks}
    bids = {}

    for i in range(n):
        hand, bid = lines[i].split(' ')
        rankings[getType(hand)] += [hand]
        bids[hand] = int(bid)

    ordering = []

    for r in ranks:
        ordering += breakTie(r)

    # print(ordering)

    answer = 0
    for i, h in enumerate(ordering):
        answer += (i + 1) * bids.get(h, 0)

    print(f"ANSWER: {answer}")
