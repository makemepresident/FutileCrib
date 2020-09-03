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
        self.score_cache = []
        for player_name in args:
            self.players.append(Player(player_name))
            self.score_cache.append(0)
        self.no_of_players = len(self.players)
        self.dealer = self.turn % self.no_of_players
        self.crib = []
        self.running = True
        self.someoneWon = False


    def gameLoop(self):
        while self.running:
            self.deck.shuffle()
            self.dealHands()
            self.cut_card = self.deck.drawCard()
            self.cribCall()
            self.p = Points(self.cut_card)
            print("Cut card: {} of {}".format(self.cut_card.getFace(), self.cut_card.getSuit()))
            self.countingRound()
            if self.someoneWon:
                break
            self.peggingRound()
            if self.someoneWon:
                break
            self.peggingRoundEndMessage()
            if self.someoneWon:
                break
            self.nextTurn()
        for player in self.players:
            if player.score > 120:
                print('{} scored {} points. Congratulations!'
                        .format(player.name, player.score))
       

    def peggingRoundEndMessage(self):
        print("\nCounting round start, cut card = {} of {}".format(self.cut_card.getFace(), self.cut_card.getSuit()))
        crib_points = self.p.countPairs(self.crib) + self.p.checkRun(self.crib)
        self.players[self.dealer].score += crib_points
        for i in range(self.dealer + 1, self.dealer + self.no_of_players + 1, 1):
            i = i % self.no_of_players
            # here's where end-of-game handling should be (121 points)
            # for it would be where who-starts-counting-first is taken care of
            print("{}'s hand was worth {} points".format(self.players[i].name, self.score_cache[i]))
            self.players[i].score += self.score_cache[i]
            self.score_cache[i] = 0
            if self.players[i].score > 120:
                self.someoneWon = True
                break
        print("{}'s crib was worth {} points".format(self.players[self.dealer].name, crib_points))
        

    def countingRound(self):
        player_to_go = self.dealer + 1
        if self.cut_card.getFace() == 'J':
            self.players[self.dealer].score += 2
        for i in range(self.no_of_players):
            player = self.players[(player_to_go + i) % self.no_of_players] # start count at certain player s.t. dealer counts last
            self.score_cache[(player_to_go + i) % self.no_of_players] = self.p.getTotal(player)
        self.score_cache[self.dealer] += self.p.countPairs(self.crib) + self.p.checkRun(self.crib)


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
                if self.peg_count == 15:
                    print("Fifteen for 2.")
                    player.score += 2
                elif self.peg_count == 31:
                    print("Thirty-one for 2")
                    player.score += 2
                    self.resetPeggingRound()
            else:
                print("{} says go.".format(player.name))
                player.passed = True
                player_to_go = (player_to_go + 1) % self.no_of_players
                if self.allPlayersPassed():
                    player.score += 1
                    print("Both players said go.")
                    self.resetPeggingRound()
            print('Peg count: {}'.format(self.peg_count))
            self.printScores()
            #########################
            if player.score > 120:
                self.someoneWon = True
                break
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
            if self.peg_count + card.getValue() <= 31:
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
        print('\nRound ' + str(self.turn) + ' has ended.')


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
        self.crib.append(self.cut_card)
