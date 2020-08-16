from Deck import Deck
from Player import Player
from Points import Points

class GameHandler:

    def __init__(self, *args): 
        self.premadeHand = False
        wrong_number_of_players = (len(args) < 2 or len(args) > 4)
        for player_name in args:
            if type(player_name) != str or wrong_number_of_players:
                print('Cannot initialize... bad arguments or wrong number of players.')
                return
        self.turn = 0
        self.deck = Deck()
        self.cut_card = None
        self.peg_count = 0
        self.players = []
        for player_name in args:
            self.players.append(Player(player_name))
        self.no_of_players = len(self.players)
        self.dealer = self.turn % self.no_of_players
        self.crib = []
        self.running = True
            

    def gameLoop(self):
        while self.running:
            self.deck.shuffle()
            self.dealHands()
            self.cribCall()
            self.cut_card = self.deck.drawCard()
            self.p = Points(self.cut_card)
            print("Cut card: {} of {}".format(self.cut_card.getFace(), self.cut_card.getSuit()))
            self.countingRound()
            self.peggingRound()
            self.nextTurn()


    def countingRound(self):
        print("\nCounting round start, cut card = {} of {}".format(self.cut_card.getFace(), self.cut_card.getSuit()))
        if self.cut_card.getFace() == 'J':
            self.players[self.dealer].score += 2
        for i in range(self.no_of_players):
            player = self.players[(self.dealer + i + 1) % 2] # start count at certain player s.t. dealer counts last
            print("{}'s turn.".format(player.name))
            for player in self.players:
                self.p.getTotal(player)
            print("{} scores {} points.".format(player.name, player.score))
        current_dealer = self.players[self.dealer]
        # dealer score += self.p.getTotal(dealer.hand)        


    def peggingRound(self):
        print("Pegging round start.")
        p = Points()
        player_to_go = (self.dealer + 1) % 2
        player = self.players[player_to_go]
        played_cards = []
        if self.cut_card.getFace() == 'J':
            self.players[self.dealer].score += 2
        while(True):
            if self.canPlay(player):
                played_card = self.takeTurn(player)
                played_cards.append(played_card)
                self.peg_count += played_card.getValue()
                player.score += p.checkPeggingRun(played_cards) + p.countPeggingPairs(played_cards)
                if played_card.getValue() + self.peg_count == 15:
                    player.score += 2
                elif played_card.getValue() + self.peg_count == 31:
                    player.score += 2
                    self.resetPeggingRound()
            else:
                print("{} says go.".format(player.name))
                player.passed = True
                player_to_go += 1
                if self.allPlayersPassed():
                    player.score += 1
                    print("Both players said go.")
                    self.resetPeggingRound()
            print('Peg count: {}'.format(self.peg_count))
            self.printScores()
            player_to_go = (player_to_go + 1) % self.no_of_players
            player = self.players[player_to_go]
            if self.noOneHasCards():
                break


    def noOneHasCards(self):
        for player in self.players:
            if len(player.hand) > 0:
                return False
        return True


    def printScores(self):
        for player in self.players:
            print("{}: {}    ".format(player.name, player.score), end='')
        print("\n")


    def allPlayersPassed(self):
        for player in self.players:
            if not player.passed:
                return False
        return True
    

    def canPlay(self, player):
        if len(player.hand) == 0 or player.passed:
            return False
        for card in player.hand:
            if self.peg_count + card.getValue() < 31:
                return True
        return False


    def resetPeggingRound(self):
        self.peg_count = 0
        self.played_cards = []
        for player in self.players:
            player.passed = False
        pass


    def dealHands(self):
        if self.no_of_players == 2:
            hand_length = 6
        else:
            hand_length = 5
        for p in range(self.no_of_players):
            for i in range(hand_length):
                self.players[p].addToHand(self.deck.drawCard())


    def nextTurn(self):
        self.turn += 1
        self.deck = Deck()
        self.cut_card = None
        self.peg_count = 0
        self.dealer = self.turn % self.no_of_players
        self.crib = []
        for player in self.players:
            player.resetHand()
        print('Round ' + str(self.turn) + ' has ended.')


    def takeTurn(self, player):
        print(player.name, player.getHand())
        choice = self.getChoice("Choose a card: ")
        if int(choice) == 0:
                print('Player says go')
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
        if self.no_of_players == 2:
            cards_to_give = 2
        else:
            cards_to_give = 1
        if self.no_of_players == 3:
            self.crib.append(self.deck.drawCard())
        print("\nCalling {}'s crib.".format(self.players[self.dealer].name))
        for i in range(self.no_of_players):
            for j in range(cards_to_give):
                print("{}'s hand:".format(self.players[i].name))
                print(self.players[i].getHand())
                print()
                self.crib.append(self.players[i].removeFromHand(input('Choose a card to send to the crib: '), True))
                print("\n")

