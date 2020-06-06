from random import random
import math

class Card:

    # Could hold colour information
    # Could hold image information

    card_values = {
        'J': 11,
        'Q': 12,
        'K': 13,
    }

    def __init__(self, suit, value):
        self.suit = suit
        if value == 0:
            value == 1
        if value < 11:
            self.value = value
        elif value == 11:
            self.value = 'J'
        elif value == 12:
            self.value = 'Q'
        elif value == 13:
            self.value = 'K'

    def getValue(self):
        return self.value if self.value not in self.card_values else self.card_values.get(self.value)
    
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
        self.peg = 0
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
            self.cut = self.cutCard()
            while len(self.playerOne().hand) and len(self.playerTwo().hand): # While any player has a card(s) in their hand
                first = self.players[self.who_deals]
                last = self.players[(self.who_deals + 1) % 2]
                if len(first.hand):
                    choice = first.removeFromHand(input('Choose a card to play: '))
                    self.lastCard = choice
                    # Check to see if any point are gained in pegging
                if len(last.hand):
                    choice = last.removeFromHand(input('Choose a card to play'))
                    self.lastCard = choice
                    # Check to see if any point are gained in pegging
            # Needs handling for resetting "board"
            print('counting starts now')
            # Use Points object (not created yet) in order to calculate the maximum number of points
            # Allow the non-dealer to enter the number of points they think they received
            # if points_input < calculated_points, add points to tally, if points_input > calculated_points
            # force another input (rather than maximize points as could be abused mechanic)
            self.resetGame()

class Points:

    def __init__(self, hand, cut_card):
        self.hands = [] # Contains every possible hand [1,2,3,4,5,6] --> [],[1],[2]...[1,2,3],[2,3,4],[2,3,5]... [1,2,3,4]
        self.cut = cut_card
        self.peg = 0 # heh
        if hand is not None:
            for temp in self.powerset(hand):
                if len(temp) == 4:
                    self.hands.append(temp)

    def checkPeg(self, value):
        position = 0
        fin = self.peg + value
        if fin < 32:
            if fin == 15 or fin == 31:
                position += 2

    def countHand(self, hand):
        fifteens = 0
        runs = 0
        pairs = 0
        if 11 or 12 or 13 in hand:
            temp_hand = [x if x < 11 else 10 for x in hand]
        temp_hand.append(self.cut.getValue())
        for i in self.powerset(temp_hand):
            if sum(i) == 15:
                fifteens += 1
            if len(i) == 2 and i[0] == i[1]:
                pairs += 1
            if len(i) >= 3:
                runs += self.checkRun(i)
        return fifteens * 2, runs, pairs * 2

    def checkRun(self, hand):
        run = 0
        for i in range(len(hand)):
            temp = [hand[i] + j for j in range(1, len(hand))]
            for j in range(len(temp)):
                if temp[j] not in hand:
                    break
                if j == len(temp) - 1:
                    # print(hand)
                    if len(hand) > 3:
                        run += len(hand) - 6
                        if len(hand) == 5:
                            run += 1
                    else:
                        run += 3
        return run

    def powerset(self, s):
        x = len(s)
        masks = [1 << i for i in range(x)]
        for i in range(1 << x):
            yield [ss for mask, ss in zip(masks, s) if i & mask]

th = [4,5,5,6]
p = Points(None, Card('Spade', 5))

x = p.countHand(th)
print('For the hand ' + str(th) + ':')
print(str(x[0]) + ' points in 15s')
print(str(x[1]) + ' points in runs')
print(str(x[2]) + ' points in pairs')

  
# g = GameHandler('Derik', 'Ryan')            
# g.gameLoop()