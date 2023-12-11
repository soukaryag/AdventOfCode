

def getMatches(winning, mine):
    winners = {w:True for w in winning}
    m = 0
    for num in mine:
        if winners.get(num):
            # print(num)
            m += 1

    return m


if __name__ == '__main__':
    f = open('day_4.txt', 'r')

    lines = []
    for line in f:
        lines.append(line)

    n = len(lines)
    scratchCards = {i + 1:1 for i in range(n)}
    for line in lines:
        card, numbers = line.split(':')
        mine, winning = numbers.split('|')
        cardNum = int(card.split(' ')[-1].strip())
        
        mine = [int(i.strip()) for i in mine.strip().split(' ') if i != '']
        winning = [int(i.strip()) for i in winning.strip().split(' ') if i != '']

        matches = getMatches(winning, mine)
        # print(matches, min(n, cardNum + 1), min(n, matches + cardNum + 1))
        for m in range(cardNum + 1, matches + cardNum + 1):
            if m > n: break
            scratchCards[m] = scratchCards.get(m, 1) + scratchCards.get(cardNum)
        
    print(sum(scratchCards.values()))