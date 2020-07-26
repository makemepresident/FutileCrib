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
    