from Deck import Deck
from Player import Player
from Points import Points

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
            self.p = Points()

    def gameLoop(self):
        while self.running:
            self.deck.shuffle()
            self.dealHands()
            self.cribCall()
            self.cut_card = self.deck.drawCard()
            #self.peggingRound()
            self.countingRound()
            # count now
            # make points object
            # start at dealer index + 1 % 2
            # count for dealer
            # count for crib
            self.nextTurn()

    def countingRound(self):
        print("\nCounting round start, cut card = {} of {}".format(self.cut_card.getFace(), self.cut_card.getSuit()))
        for i in range(len(self.players)):
            player = self.players[(self.dealer + i + 1) % 2] # start count at certain player s.t. dealer counts last
            print("{}'s turn.".format(player.name))
            player.score += self.p.getTotal(player.hand, self.cut_card)
            print("{} scores {} points.".format(player.name, player.score))
        current_dealer = self.players[self.dealer]
        # dealer score += self.p.getTotal(dealer.hand)        

    def peggingRound(self):
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
        for player in self.players:
            player.resetHand()
        print('Round ' + str(self.turn) + ' has ended.')

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
        while result == '':
            result = input('Invalid string, try again: ')
        return int(result)

    def cribCall(self):
        print("\nCalling {}'s crib.".format(self.players[self.dealer].name))
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