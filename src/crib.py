from Points import Points
from GameHandler import GameHandler
from Player import Player
from Card import Card

p = Points()
#print(p.checkRun(Player.generateHand()))
fabricated_hand = [
    Card('Spades', 12),
    Card('Hearts', 9),
    Card('Spades', 11),
    Card('Diamonds', 10),
    Card('Clubs', 9)
]

print(p.checkRun(fabricated_hand))

# used for debugging