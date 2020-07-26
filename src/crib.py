# pylint: disable=unused-variable
from random import random
import random
import math

class Card:

    # Could hold colour information
    # Could hold image information
    
    all_cards = 'A2345678910JQK'
    card_values = {
        'A': 1,
        'J': 10,
        'Q': 10,
        'K': 10,
    }
    card_ordering = {
        'A': 1,
        2: 2,
        3: 3,
        4: 4,
        5: 5,
        6: 6,
        7: 7,
        8: 8,
        9: 9,
        10: 10,
        'J': 11,
        'Q': 12,
        'K': 13,
    }

    def __init__(self, suit, value):
        self.suit = suit
        if value == 0:
            self.value = 'A'
        if value < 10 and value > 0:
            self.value = value + 1
        elif value == 10:
            self.value = 'J'
        elif value == 11:
            self.value = 'Q'
        elif value == 12:
            self.value = 'K'

    def getValue(self):
        return self.value if self.value not in self.card_values else self.card_values.get(self.value)
    
class Deck:

    suits = ['Spades', 'Clubs', 'Hearts', 'Diamonds']

    def __init__(self):
        self.cards = []
        for i in range(52):
            self.cards.append(Card(self.suits[int(i / 13)], int(i % 13)))

    def shuffle(self):
        temp_cards = self.cards.copy()
        self.cards = []
        for i in range(52):
            self.cards.append(temp_cards.pop(random.randint(0, 51 - i)))
        return

    def drawCard(self):
        return self.cards.pop()

    def resetDeck(self):
        self.__init__()

class Player:

    def __init__(self, name):
        self.name = name
        self.hand = []
        self.position = 0
        self.score = 0

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
            self.countingRound()
            # count now
            # make points object
            # start at dealer index + 1 % 2
            # count for dealer
            # count for crib
            self.nextTurn()

    def countingRound(self):
        p = Points()
        for i in range(len(self.players)):


    def peggingRound(self):
        p = Points()
        while not self.players[0].handIsEmpty() and not self.players[1].handIsEmpty(): # Either player has cards
            for i in range(len(self.players)):
                played_cards = []
                player_index = (self.dealer + i) % 2
                played = self.takeTurn(self.players[player_index])
                if played == 0:
                    played_cards = []
                    self.peg_count = 0
                    self.players[(player_index + 1) % 2].score += 1
                    continue
                if played.getValue() + self.peg_count == 31:
                    
                    self.players[(player_index) % 2].score += 2
                    self.peg_count = 0
                    # add points to player
                else:
                    self.peg_count += played.getValue()
                print('Current peg count: ' + str(self.peg_count))
                print(self.players[0].name, self.players[0].score, self.players[1].name, self.players[1].score)
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
        print(player.name, player.getHand())
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
        print("\nCalling crib.")
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

    def __init__(self, hand=None, cut_card=None):
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
        # want: hand to be sorted according to Card.card_ordering
        # use string Card.all_cards
        # make power set of hand
        # eliminate all 1- and 2-element sets
        # start at 5-element set; turn into string and see if in all_cards
        # repeat for the 4-element sets and 3-ones too
        hand.sort(key=lambda card: Card.card_ordering[card])
        powerset = list(filter(lambda subset: len(subset) > 2, self.powerset(hand)))
        whole_hand = list(filter(lambda set: len(set) == 5, powerset))
        four_hands = list(filter(lambda set: len(set) == 4, powerset))
        three_hands = list(filter(lambda set: len(set) == 3, powerset))
        
        hand_string = toString(whole_hand)



        # run = 0
        # for i in range(len(hand)):
        #     temp = [hand[i] + j for j in range(1, len(hand))]
        #     for j in range(len(temp)):
        #         if temp[j] not in hand:
        #             break
        #         if j == len(temp) - 1:
        #             # print(hand)
        #             if len(hand) > 3:
        #                 run += len(hand) - 6
        #                 if len(hand) == 5:
        #                     run += 1
        #             else:
        #                 run += 3
        # return run
        pass

    def toString(self, subset):
        result = ''
        for card in subset:
            result += card
        return result


    def powerset(self, s):
        x = len(s)
        masks = [1 << i for i in range(x)]
        for i in range(1 << x):
            yield [ss for mask, ss in zip(masks, s) if i & mask]
  
# g = GameHandler('Derik', 'Ryan')            
# g.gameLoop()

p = Points()
g = GameHandler('Derik', 'Zak')
g.gameLoop()

# p.checkRun(['K', 3, 4, 'Q'])