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

    def getTotal(self, hand, cut_card):
        if hand is None:
            return
        total = 0
        hand.append(cut_card)
        total += self.countFifteens(hand)
        total += self.checkRun(hand)
        total += self.countPairs(hand)
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
        result = 0
        length = len(played_cards)
        last_card = played_cards[-1]
        if length > 1 and played_cards[-2] == last_card:
            result = 2
            if length > 2 and played_cards[-3] == last_card:
                result += 2
                if length > 3 and played_cards[-4] == last_card:
                    result += 2
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
        return sum

    def checkRun(self, hand):
        result = 0
        # WATCH OUT FOR THIS
        hand = self.sortHand(hand)
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
        # given the last several cards played in pegging round, find runs
        # check the last three played; if comprise a run score >= 3
        # ie check if there's a run of four; if not return 3
        # otherwise check for a run of five; if not return 4
        # otherwise check for a run of six etc
        # note played_cards is constant length
        if played_cards == None:
            return
        result = 0
        length = len(played_cards)
        played_cards3 = played_cards[-3:]
        played_cards4 = played_cards[-4:]
        played_cards5 = played_cards[-5:]
        played_cards3.sort(key=lambda card: Card.card_ordering[card.getFace()])
        played_cards4.sort(key=lambda card: Card.card_ordering[card.getFace()])
        played_cards5.sort(key=lambda card: Card.card_ordering[card.getFace()])
        if length > 2 and self.toString(played_cards3) in self.all_cards:
            result = 3
            if length > 3 and self.toString(played_cards4) in self.all_cards:
                result = 4
                if length > 4 and self.toString(played_cards5) in self.all_cards:
                    result = 5
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

    def sortHand(self, hand):
        temp = hand.sort(key=lambda card: Card.card_ordering[card.getFace()])
        return hand.sort(key=lambda card: Card.card_ordering[card.getFace()])
