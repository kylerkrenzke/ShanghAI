import random
from copy import deepcopy
from itertools import combinations

class Card:
    __ranks = ("ace","2","3","4","5","6","7","8","9","T","J","Q","K")
    __suits = ("clubs","diamonds","hearts","spades")

    def __init__(self, rank, suit):
        self.__rank = rank
        self.__suit = suit
        
    def __lt__(self, other):
        if self.__suit == other.__suit:
            return self.__rank < other.__rank
        return self.__suit < other.__suit
        
    def __eq__(self, other):
        return self.__rank == other.__rank
        
    def __str__(self):
        return self.__ranks[self.__rank-1] + " of "+ self.__suits[self.__suit]
        
class Pile:
    def __init__(self, initial):
        self.cards = initial
        
    def __getitem__(self, key):
        return self.cards[key]
        
    def __len__(self):
        return len(self.cards)
        
    def __str__(self):
        ret = "["
        i = 0
        while i < len(self.cards):
            ret += str(self.cards[i])
            if i < (len(self.cards) - 1):
                ret+=", "
            i+=1
            
        ret += "]"
        return ret
        
    def remove(self, item):
        self.cards.remove(item)
        
    def pop(self, index):
        card = self.cards[index]
        return self.cards.pop(index)
        
    def put(self, card):
        self.cards.append(card)
        
    def sort(self):
        self.cards.sort()
        
    def shuffle(self):
        for i in range(len(self.cards)-1, 0, -1):
            j = random.randint(0, i)
            self.cards[i], self.cards[j] = self.cards[j], self.cards[i]
            
class Hand(Pile):
    indexmap = ("0","1","2","3","4","5","6","7","8","9","a","b","c","d","e","f","g")
    
    def __init__(self):
        Pile.__init__(self, [])
        
    def __decodeIndex(self, index):
        if index == "a": return 10
        elif index == "b": return 11
        elif index == "c": return 12
        elif index == "d": return 13
        elif index == "e": return 14
        elif index == "f": return 15
        elif index == "g": return 16
        else: return int(index)
        return self.cards[val]
        
    def __getCard(self, index):
        return self.cards[self.__decodeIndex(index)]
        
    def findSets(self, size):
        set_lst = []
        index_lst = [self.indexmap[i] for i in range(len(self.cards))]
        all_combos = combinations(index_lst, size) # sequence of all combos of hand's indexes
        for combo in all_combos:
            if self.__getCard(combo[0]) == self.__getCard(combo[1]) == self.__getCard(combo[2]):
                set_lst.append(combo[0]+combo[1]+combo[2])
        
        return tuple(set_lst)
        
    def without(self, str_indexes):
        dup = deepcopy(self)
        for char in reversed(str_indexes):
            dup.cards.pop(dup.__decodeIndex(char))
        return dup
        
class DoubleDeck(Pile):
    def __init__(self):
        ranks = [i for i in range(1, 14)]
        suits = [j for j in range(0, 4)]
        lst = []
        for i in range(2):
            for suit in suits:
                for rank in ranks:
                    lst.append(Card(rank, suit))
        Pile.__init__(self, lst)
        
class Meld(Pile):
    def __init__(self, initial):
        Pile.__init__(self, initial)
        
    def canAcceptCard(self, card):
        raise NotImplementedError()
        
class SetMeld(Pile):
    def __init__(self, initial):
        Meld.__init__(self, initial)
        
    def canAcceptCard(self, card):
        return card.rank == self.cards[0].rank

        