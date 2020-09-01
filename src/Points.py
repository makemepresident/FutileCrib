from Card import Card

class Points:

    def __init__(self, cut_card=None):
        self.all_cards = 'A2345678910JQK'
        # self.hands = [] # Contains every possible hand [1,2,3,4,5,6] --> [],[1],[2]...[1,2,3],[2,3,4],[2,3,5]... [1,2,3,4]
        self.cut = cut_card
        #
        # if hand is not None:
        #     self.hand = hand
        #     for temp in self.powerset(hand):
        #         if len(temp) == 4:
        #             self.hands.append(temp)
        # I don't see a reason for all the code in here any longer.
        pass


    def getTotal(self, player):
        if player.hand is None:
            return 0
        total = 0
        player.hand.append(self.cut)
        total += self.countFifteens(player.hand)
        total += self.checkRun(player.hand)
        total += self.countPairs(player.hand)
        player.hand.remove(self.cut)
        return total


    def countPairs(self, hand):
        result = 0
        pairs = list(filter(lambda subset: len(subset) == 2, self.powerset(hand)))
        for pair in pairs:
            if pair[0].getFace() == pair[1].getFace():
                result += 2
        return result


    def countPeggingPairs(self, played_cards):
        # take a look at only the last two cards
        # if there's a pair, check for a triplet etc.
        n_tuple = "pair"
        result = 0
        length = len(played_cards)
        last_card = played_cards[-1].getFace()
        if length > 1 and played_cards[-2].getFace() == last_card:
            result = 2
            if length > 2 and played_cards[-3].getFace() == last_card:
                result = 6
                n_tuple = 'triplet'
                if length > 3 and played_cards[-4].getFace() == last_card:
                    result = 12
                    n_tuple = 'quartet'
        if result > 0:
            print("A {} for {}.".format(n_tuple, result))
        return result
        

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
        return points


    def checkRun(self, hand):
        result = 0
        # WATCH OUT FOR THIS
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


    def checkPeggingRun(self, played_cards):
        if played_cards == None:
            return 0
        result = 0
        length = len(played_cards)
        if length < 3: 
            return 0
        for i in range(3, (length + 1)): 
            subset = played_cards[-i:]
            subset.sort(key=lambda card: Card.card_ordering[card.getFace()])
            if self.toString(subset) in self.all_cards:
                result = length
        if result > 0:
            print("A run is {}.".format(result))
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

