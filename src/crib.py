from random import random
import math

class Card:

    # Could hold colour information
    # Could hold image information

    card_values = {
        'J': 10,
        'Q': 10,
        'K': 10,
    }

    def __init__(self, suit, value):
        self.suit = suit
        if value == 0:
            value = 1
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

    def removeFromHand(self, index, destructive):
        index = int(index) - 1
        if index > len(self.hand) - 1:
            index = len(self.hand) - 1
        if destructive:
            return self.hand.pop(index)
        return self.hand[index]

    def handIsEmpty(self):
        if len(self.hand) == 0:
            return True
        return False

class GameHandler:

    def __init__(self, player1, player2):
        if type(player1) != str and type(player2) != str:
            print('Cannot initialize...')
            return
        else:
            self.turn = 0
            self.deck = Deck()
            self.cut_card = None
            self.peg_count = 0
            self.players = [Player(player1), Player(player2)]
            self.dealer = self.turn % len(self.players)
            self.crib = []
            self.running = True

    def gameLoop(self):
        while self.running:
            self.deck.shuffle()
            self.dealHands()
            self.cribCall()
            self.cut_card = self.deck.drawCard()
            self.peggingRound()
            # count now
            self.nextTurn()

    def peggingRound(self):
        while not self.players[0].handIsEmpty() and not self.players[1].handIsEmpty(): # Either player has cards
            for i in range(len(self.players)):
                played = self.takeTurn(self.players[(self.dealer + i) % 2])
                if played == 0:
                    self.peg_count = 0
                    continue
                self.peg_count += played.getValue()
                print('Current peg count: ' + str(self.peg_count))
                print()

    def dealHands(self):
        for p in range(2):
            for i in range(6):
                self.players[p].addToHand(self.deck.drawCard())

    def nextTurn(self):
        self.turn += 1
        self.deck = Deck()
        self.cut_card = None
        self.peg_count = 0
        self.dealer = self.turn % len(self.players)
        self.crib = []

    def takeTurn(self, player):
        print(player.getHand())
        choice = self.getChoice("Choose a card: ")
        if choice == 0:
            return 0
        temp_card = player.removeFromHand(choice, False)
        print()
        while temp_card.getValue() + self.peg_count > 31:
            choice = self.getChoice('Exceeds 31 - choose another card: ')
            if int(choice) == 0:
                print('Player says go')
                return 0
            temp_card = player.removeFromHand(choice, False)
            print()
        temp_card = player.removeFromHand(choice, True)
        return temp_card

    def getChoice(self, prompt):
        result = input(prompt)
        return int(result)


    def cribCall(self):
        for i in range(len(self.players)):
            for j in range(3):
                print(self.players[i].getHand())
                print()
                if j == 0:
                    self.crib.append(self.players[i].removeFromHand(input('Choose a card to send to the crib: '), True))
                    print()
                elif j == 1:
                    self.crib.append(self.players[i].removeFromHand(input('Choose another card to send to the crib: '), True))
                    print()
                else:
                    print('Your current hand is: ')
                    print(self.players[i].getHand())
                    print()
                    print()

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
  
g = GameHandler('Derik', 'Ryan')            
g.gameLoop()