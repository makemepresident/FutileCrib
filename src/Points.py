class Points:

    def __init__(self, hand=None, cut_card=None):
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
        total += self.countHand(self.hand)
        total += self.checkRun(self.hand)
        return total

    def countHand(self, hand):
        fifteens = 0
        runs = 0
        pairs = 0
        if 11 or 12 or 13 in hand:
            temp_hand = [x if x < 11 else 10 for x in hand]
        temp_hand.append(self.cut.getValue())
        for i in self.powerset(temp_hand):
            if sum(i) == 15:
                fifteens += 1
            if len(i) == 2 and i[0] == i[1]:
                pairs += 1
            if len(i) >= 3:
                runs += self.checkRun(i)
        return fifteens * 2, runs, pairs * 2

    def checkRun(self, hand):
        # want: hand to be sorted according to Card.card_ordering
        # use string Card.all_cards
        # make power set of hand
        # eliminate all 1- and 2-element sets
        # start at 5-element set; turn into string and see if in all_cards
        # repeat for the 4-element sets and 3-ones too
        hand.sort(key=lambda card: Card.card_ordering[card])
        powerset = list(filter(lambda subset: len(subset) > 2, self.powerset(hand)))
        whole_hand = list(filter(lambda set: len(set) == 5, powerset))
        four_hands = list(filter(lambda set: len(set) == 4, powerset))
        three_hands = list(filter(lambda set: len(set) == 3, powerset))
        
        hand_string = toString(whole_hand)



        # run = 0
        # for i in range(len(hand)):
        #     temp = [hand[i] + j for j in range(1, len(hand))]
        #     for j in range(len(temp)):
        #         if temp[j] not in hand:
        #             break
        #         if j == len(temp) - 1:
        #             # print(hand)
        #             if len(hand) > 3:
        #                 run += len(hand) - 6
        #                 if len(hand) == 5:
        #                     run += 1
        #             else:
        #                 run += 3
        # return run
        pass

    def toString(self, subset):
        result = ''
        for card in subset:
            result += card
        return result


    def powerset(self, s):
        x = len(s)
        masks = [1 << i for i in range(x)]
        for i in range(1 << x):
            yield [ss for mask, ss in zip(masks, s) if i & mask]