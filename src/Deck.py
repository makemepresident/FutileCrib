from Card import Card
from random import random
import random

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