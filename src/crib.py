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
        self.position = 0

    def changePosition(self, points):
        self.position += points

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
        index = int(index) - 1
        if index > len(self.hand) - 1:
            index = len(self.hand) - 1
        return self.hand.pop(index)

class GameHandler:

    def __init__(self, player1, player2):
        self.running = True
        self.deck = Deck()
        self.players = [Player(player1), Player(player2)]
        self.who_deals = 0
        self.dealer = self.players[self.who_deals]

    def resetGame(self):
        self.deck = Deck()
        self.who_deals = (self.who_deals + 1) % 2
        self.players[self.who_deals]

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
                print(self.players[p].getHand())
                print('Player ' + str(p) + ', send a card to the crib - ')
                self.dealer.crib.append(self.players[p].removeFromHand(int(input())))

    def gameLoop(self):
        while(self.running):
            self.deck.shuffle()
            self.dealHands()
            self.cribCall()
            cut = self.cutCard()
            while len(self.playerOne().hand) and len(self.playerTwo().hand): # While any player has a card(s) in their hand
                first = self.players[self.who_deals]
                last = self.players[(self.who_deals + 1) % 2]
                if len(first.hand):
                    first.removeFromHand(input('Choose a card to play: '))
                    # Check to see if any point are gained in pegging
                if len(last.hand):
                    last.removeFromHand(input('Choose a card to play'))
                    # Check to see if any point are gained in pegging
            print('counting starts now')
            # Use Points object (not created yet) in order to calculate the maximum number of points
            # Allow the non-dealer to enter the number of points they think they received
            # if points_input < calculated_points, add points to tally, if points_input > calculated_points
            # force another input (rather than maximize points as could be abused mechanic)
            self.resetGame()

class Points:

    def __init__(self, hand):
        self.hands = [] # Contains every possible hand
        for temp in self.powerset(hand):
            if len(hand) is 4:
                hands.append(hand)

    def countFifteen(self):
        self.corr_points = []
        for i in range(len(hands)):
            fifteen_count = 0
            for j in self.powerset(hands[i]):
                if sum(j) is 15:
                    fifteen_count += 1
            self.corr_points.append(fifteen_count)

    def checkRun(self, hand):
        for i in range(len(hand)):
            

    def checkMatches(self):

    def powerset(s):
        x = len(s)
        masks = [1 << i for i in range(x)]
        for i in range(1 << x):
            yield [ss for mask, ss in zip(masks, s) if i & mask]

    

g = GameHandler('Derik', 'Ryan')            
g.gameLoop()