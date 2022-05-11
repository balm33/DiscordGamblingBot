import random

CARDS = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
SUITES = ["hearts", "diamonds", "spades", "clubs"]

deck = []
numDecks = 2

def fillDeck(deck):
    for x in range(numDecks):
        for i in range(len(CARDS)):
            for j in range(len(SUITES)):
                deck.append([CARDS[i], SUITES[j]])

def shuffleDeck(deck):
    random.shuffle(deck)

if len(deck) <= 0:
    fillDeck(deck)
    shuffleDeck(deck)

print(len(deck))
print(deck)
