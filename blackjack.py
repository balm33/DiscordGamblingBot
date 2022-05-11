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

def getHandSum(hand):
    handSum = 0
    for i in range(len(hand)):
        card = hand[i][0]

        if card in ['J', 'Q', 'K']:
            card = 10
        elif card == 'A':
            card = 11
        else:
            card = int(card)
        handSum += card # add value of card
    
    if handSum > 21: # if losing aces become low
        for i in range(len(hand)):
            if handSum > 21:
                card = hand[i][0]
                if card == 'A':
                    handSum -= 10
    return handSum