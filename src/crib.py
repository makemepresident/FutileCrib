from random import random
import math

class Card:

    # Could hold colour information
    # Could hold image information

    def __init__(self, suit, value):
        self.suit = suit
        value += 1
        if value < 11:
            self.value = value
        elif value == 11:
            self.value = 'J'
        elif value == 12:
            self.value = 'Q'
        elif value == 13:
            self.value = 'K'
    
class Deck:

    suits = ['Spades', 'Clubs', 'Hearts', 'Diamonds']

    def __init__(self):
        self.cards = []
        for i in range(52):
            self.cards.append(Card(self.suits[int(i / 13)], int(i % 13)))

    def shuffle(self): # Needs implementation
        return

    def drawCard(self):
        return self.cards.pop(math.floor(random() * 52) - (52 % len(self.cards)))

    def resetDeck(self):
        self.__init__()

class Player:

    def __init__(self, name):
        self.name = name
        self.hand = []
        self.crib = []

    def getHand(self):
        string_hand = []
        for i in range(len(self.hand)):
            string_hand.append(str(self.hand[i].value) + ' of ' + str(self.hand[i].suit))
        return string_hand

    def getCrib(self):
        string_crib = []
        for i in range(len(self.crib)):
            string_crib.append(str(self.crib[i].value) + ' of ' + str(self.crib[i].suit))
        return string_crib

    def resetHand(self):
        self.hand = []

    def resetCrib(self):
        self.crib = []

    def addToHand(self, card):
        if isinstance(card, Card):
            self.hand.append(card)

    def removeFromHand(self, index):
        index -= 1
        return self.hand.pop(index)

class GameHandler:

    def __init__(self, player1, player2):
        self.deck = Deck()
        self.players = [Player('one'), Player('two')]
        dealer = math.floor(random())
        self.dealer = self.players[math.floor(random())]

    def playerOne(self):
        return self.players[0]

    def playerTwo(self):
        return self.players[1]
        
    def dealHands(self):
        for p in range(2):
            for i in range(6):
                self.players[p].addToHand(self.deck.drawCard())
    
    def cutCard(self):
        return self.deck.drawCard()

    def generateRandom(self):
        return math.floor(random() * 52) - (52 % len(self.deck))

    def cribCall(self):
        for p in range(len(self.players)):
            for i in range(2):
                print('Player ' + str(p) + ', send a card to the crib - ')
                self.dealer.crib.append(self.players[p].removeFromHand(int(input())))

g = GameHandler('derik', 'lorby')
g.dealHands()
x = g.cutCard()
print(str(x.value) + ' of ' + str(x.suit))