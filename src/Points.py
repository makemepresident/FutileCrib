from Card import Card

class Points:

    def __init__(self, hand=None, cut_card=None):
        self.all_cards = 'A2345678910JQK'
        self.hands = [] # Contains every possible hand [1,2,3,4,5,6] --> [],[1],[2]...[1,2,3],[2,3,4],[2,3,5]... [1,2,3,4]
        self.cut = cut_card
        if hand is not None:
            self.hand = hand
            for temp in self.powerset(hand):
                if len(temp) == 4:
                    self.hands.append(temp)

    def getTotal(self):
        if self.hand is None:
            return
        total = 0
        temp = self.hand.append(self.cut)
        total += self.countFifteens(self.hand)
        total += self.checkRun(self.hand)
        return total

    def countFifteens(self, hand):
        powerset = list(filter(lambda subset: len(subset) > 1, self.powerset(hand)))
        sum = 0
        points = 0
        for combination in powerset:
            for card in combination:
                sum += card.getValue()
            if sum == 15:
                points += 2
            sum = 0
        

    def checkRun(self, hand):
        result = 0
        hand.sort(key=lambda card: Card.card_ordering[card.getFace()])
        powerset = list(filter(lambda subset: len(subset) > 2, self.powerset(hand)))
        if self.toString(self.subset(powerset, 5)[0]) in self.all_cards:
            return 5
        for four_combo in self.subset(powerset, 4):
            if self.toString(four_combo) in self.all_cards:
                result += 4
        if result > 0:
            return result
        for three_combo in self.subset(powerset, 3):
            if self.toString(three_combo) in self.all_cards:
                result += 3
        return result


    def subset(self, powerset, length):
        return list(filter(lambda set: len(set) == length, powerset))


    def toString(self, subset):
        result = ''
        for card in subset:
            result += str(card.getFace())
        return result


    def powerset(self, s):
        x = len(s)
        masks = [1 << i for i in range(x)]
        for i in range(1 << x):
            yield [ss for mask, ss in zip(masks, s) if i & mask]
