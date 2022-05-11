import random

CARDS = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
SUITES = ["hearts", "diamonds", "spades", "clubs"]

numDecks = 2

def fillDeck(deck):
    for x in range(numDecks):
        for i in range(len(CARDS)):
            for j in range(len(SUITES)):
                deck.append([CARDS[i], SUITES[j]])

def shuffleDeck(deck):
    random.shuffle(deck)

def getCard(deck):
    card = deck[0]
    deck.pop(0)
    return card