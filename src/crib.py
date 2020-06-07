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
        if index == 'go':
            return 'g'
        if index == 0:
            index = 1
        index = int(index) - 1
        if index > len(self.hand) - 1:
            index = len(self.hand) - 1
        return self.hand.pop(index)

    def handIsEmpty(self):
        if len(hand) == 0:
            return True
        return False

class GameHandler:

    def __init__(self, player1, player2):
        if not isinstance(player1, Player) and not isinstance(player2, Player):
            return
        else:
            self.turn = 0
            self.deck = Deck('p1', 'p2')
            self.cut_card = None
            self.peg_count = 0
            self.players = [player1, player2]
            self.dealer = turn % len(players)
            self.crib = []
            self.running = True

    def gameLoop(self):
        while self.running:
            # self.deck.shuffle()
            self.cribCall()
            self.cut_card = self.deck.drawCard()
            # while not players[0].handIsEmpty() and not players[1].handIsEmpty():
                # PEGGING
            return

    def takeTurn(self, player):
        choice = player.removeFromHand(input('Choose a card'))
        while choice + self.peg_count > 31:
            choice = player.removeFromHand(input('Choose another card idot'))
        return choice

    def cribCall(self):
        for i in range(len(self.players)):
            for j in range(2):
                if j == 0:
                    self.players[i].removeFromHand(input('Choose a card to send to the crib'))
                else:
                    self.players[i].removeFromHand(input('Choose another card to send to the crib'))

class Points:

    def __init__(self, hand, cut_card):
        self.hands = [] # Contains every possible hand [1,2,3,4,5,6] --> [],[1],[2]...[1,2,3],[2,3,4],[2,3,5]... [1,2,3,4]
        self.cut = cut_card
        if hand is not None:
            for temp in self.powerset(hand):
                if len(temp) == 4:
                    self.hands.append(temp)

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