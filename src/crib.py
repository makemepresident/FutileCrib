from GameHandler import GameHandler
from Card import Card

hand1 = Card.list2hand([0,2,4,6])
hand2 = Card.list2hand([1,3,5,7])

g = GameHandler("Alice", "Bill", hand1, hand2)
g.gameLoop()