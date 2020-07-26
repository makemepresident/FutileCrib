# pylint: disable=unused-variable
from random import random
import random
import math
from Player import Player
from Card import Card
from Deck import Deck
from GameHandler import GameHandler
from Points import Points

# g = GameHandler('Derik', 'Ryan')            
# g.gameLoop()

p = Points()
g = GameHandler('Derik', 'Zak')
g.gameLoop()

# p.checkRun(['K', 3, 4, 'Q'])