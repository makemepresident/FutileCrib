from Card import Card

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