from copy import deepcopy
from itertools import combinations
import random
import sys
        
class Card:
    ranks = ("ace","2","3","4","5","6","7","8","9","T","J","Q","K")
    suits = ("clubs","diamonds","hearts","spades")

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        
    def __lt__(self, other):
        if self.suit == other.suit:
            return self.rank < other.rank
        return self.suit < other.suit
        
    def __eq__(self, other):
        return self.rank == other.rank
        
    def __str__(self):
        return self.ranks[self.rank-1] + " of "+ self.suits[self.suit]

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
        
class Deck(Pile):
    def __init__(self):
        ranks = [i for i in range(1, 14)]
        suits = [j for j in range(0, 4)]
        lst = []
        for i in range(2):
            for suit in suits:
                for rank in ranks:
                    lst.append(Card(rank, suit))
        Pile.__init__(self, lst)
        
class Player:
    def __init__(self):
        self.hand = Pile([])
        self.melds = []
        self.down = False
        
    def addMeld(self, meld):
        self.melds.append(meld)

class Shanghai:
    indexmap = ["0","1","2","3","4","5","6","7","8","9","a","b","c","d","e","f","g"]
    
    def __init__(self, nplayers):
        # attributes
        self.drawPile = Deck()
        self.discardPile = Pile([])
        self.players = [Player() for i in range(nplayers)]
        self.curplayer = 0
        self.curstage = "draw"
        
        # deck initialization
        self.drawPile.shuffle()
        for i in range(11):
            for player in self.players:
                player.hand.put(self.drawPile.pop(0))
	self.discardPile.put(self.drawPile.pop(0))
                
    def __str__(self):
        ret = "Draw: " + str(self.drawPile) + "\n"
        ret += "Discard: " + str(self.discardPile) + "\n"
        i = 0
        while i < len(self.players):
            ret += "P"+str(i)+": "+str(self.players[i].hand) + "\n"
            ret += "Melds: [ "
            for meld in self.players[i].melds: ret += str(meld)+" "
            ret += "]\n"
            i+=1
        return ret
        
    def __curplayer(self): 
        return self.players[self.curplayer]
        
    def __curhand(self): 
        return self.__curplayer().hand
        
    def __curmelds(self):
        return self.__curplayer().melds
        
    def __decodeIndex(self, index):
        if index == "a": return 10
        elif index == "b": return 11
        elif index == "c": return 12
        elif index == "d": return 13
        elif index == "e": return 14
        elif index == "f": return 15
        elif index == "g": return 16
        else: return int(index)
        
    def getPossibleActions(self):
        if self.curstage == "draw":
            lst = []
            if len(self.discardPile) > 0:
                lst.append(("draw","discard"),)
            lst.append(("draw","draw"),)
            return lst
        elif self.curstage == "play":
            indexes = [self.indexmap[i] for i in range(len(self.__curhand()))]
            iterable = combinations(indexes, 3)
            lst = []
            for iter in iterable:
                c1 = iter[0]
                c2 = iter[1]
                c3 = iter[2]
                if self.__curhand()[self.__decodeIndex(c1)] == self.__curhand()[self.__decodeIndex(c2)] and self.__curhand()[self.__decodeIndex(c2)] == self.__curhand()[self.__decodeIndex(c3)]:
                    lst.append(("meld",str(c1)+str(c2)+str(c3)),)
            for i in range(len(self.players[self.curplayer].hand)):
                lst.append(("discard", str(i)),)
                
            if self.__curplayer().down:
                for player in range(len(self.players)):
                    for meld in range(len(self.players[player].melds)):
                        for card in range(len(self.__curhand())):
                            if self.__curhand()[card].rank == self.players[player].melds[meld][0].rank:
                                lst.append(("build",str(player)+str(meld)+str(self.indexmap[card])),)
            return tuple(lst)
            
    def takeAction(self, cmdlst):
        dup = deepcopy(self)
        if cmdlst[0] == "draw" and self.curstage == "draw":
            if cmdlst[1] == "draw":
		dup.drawPile.shuffle()
                card = dup.drawPile.pop(0)
                dup.players[dup.curplayer].hand.put(card)
                dup.curstage = "play"
                if len(dup.drawPile) == 0:
                    dup.drawPile = dup.discardPile
                    dup.discardPile = Pile([])
                    dup.drawPile.shuffle()
            else:
                card = dup.discardPile.pop(len(dup.discardPile) - 1)
                dup.players[dup.curplayer].hand.put(card)
                dup.curstage = "play"
        elif cmdlst[0] == "discard" and dup.curstage == "play":
            dup.discardPile.put(dup.players[dup.curplayer].hand.pop(int(cmdlst[1])))
            dup.curplayer += 1
            dup.curstage = "draw"
        elif cmdlst[0] == "meld" and dup.curstage == "play":
            indexes = [dup.__decodeIndex(chars) for chars in cmdlst[1]]
            for i in range(len(indexes)):
                indexes[i] -= i
            lst = [dup.players[dup.curplayer].hand.pop(i) for i in indexes]
            meld = Pile(lst)
            dup.players[dup.curplayer].addMeld(meld)
            dup.players[dup.curplayer].down = True
        elif cmdlst[0] == "build" and dup.curstage == "play":
            card = dup.__curhand().pop(int(cmdlst[1][2]))
            dup.players[int(cmdlst[1][0])].melds[int(cmdlst[1][1])].put(card)
        elif cmdlst[0] == "fringe":
            print(dup.getPossibleActions())
        else:
            raise ValueError(cmdlst[0])
            
        if dup.curplayer == len(dup.players):
            dup.curplayer = 0
            
        return dup
            
    def isTerminal(self):
        for player in self.players:
            if len(player.hand) == 0:
                return True
        return False
        
    def getReward(self):
        if self.curplayer == 0:
            return 0
        else:
            count = 0
            for card in self.__curhand():
                if card.rank == 1: count -= 15
                elif card.rank <= 9: count -= 5
                else: count -= 10
            return count
                
