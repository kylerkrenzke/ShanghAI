import sys
from enum import Enum
from copy import deepcopy
from itertools import combinations
from deckofcards import *

class Stage(Enum):
    BUY = 1
    DRAW = 2
    PLAY = 3
        
class Player:
    def __init__(self):
        self.hand = Hand()
        self.melds = []
        self.down = False
        self.buys = 0
        
    def addMeld(self, meld):
        self.melds.append(meld)
        
class Simulator:
    def __init__(self, nplayers):
        # attributes
        self.drawPile = DoubleDeck()
        self.discardPile = Pile([])
        self.players = [Player() for i in range(nplayers)]
        self.curstage = Stage.BUY
        self.curaction = 0 # index of player who is currently facing action (buying, passing, melding, discarding, etc.)
        self.curplayer = 0 # index of player whose turn it is (player able to meld during the play stage)
        
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
        return self.__curplayer().melds[index]
        
    def getPossibleActions(self):
        lst = []
        if self.curstage == Stage.BUY:
            if self.curplayer == self.curaction: 
                lst.append(("draw","discard"),)
                lst.append(("pass",))
            else:
                lst.append(("buy",))
        elif self.curstage == Stage.DRAW:
            lst.append(("draw","draw"),)
        elif self.curstage == Stage.PLAY:
            if not self.__curplayer().down: # Meld moves
                sets_avail = self.__curhand().findSets(size=3)
                for a_set in sets_avail:
                    subhand = self.__curhand().without(a_set)
                    subsets_avail = subhand.findSets(size=3)
                    for b_set in subsets_avail:
                        lst.append(("meld",a_set,b_set))
            else: # Build moves
                for player in range(len(self.players)):
                    for meld in range(len(self.players[player].melds)):
                        for card in range(len(self.__curhand())):
                            if self.players[player].melds[meld].canAcceptCard(self.__curhand()[card]):
                                lst.append(("build",str(player)+str(meld)+str(self.indexmap[card])),)
            # Discard moves
            for i in range(len(self.__curhand())):
                lst.append(("discard",str(i)),)
        else:
            raise NotImplementedError()
        return tuple(lst)
            
    def takeAction(self, cmdlst):
        dup = deepcopy(self)
        
        if cmdlst[0] == "draw":
            if cmdlst[1] == "draw":
                dup.drawPile.shuffle()
                card = dup.drawPile.pop(0)
                dup.players[dup.curplayer].hand.put(card)
                dup.curstage = "play"
                if len(dup.drawPile) == 0:
                    dup.drawPile = dup.discardPile
                    dup.discardPile = Pile([])
                    dup.drawPile.shuffle()
            else: # if cmdlst[1] == "discard"
                card = dup.discardPile.pop(len(dup.discardPile) - 1)
                dup.players[dup.curplayer].hand.put(card)
                dup.curstage = Stage.PLAY
        elif cmdlst[0] == "pass":
            dup.curplayer += 1
        elif cmdlst[0] == "discard":
            dup.discardPile.put(dup.players[dup.curplayer].hand.pop(int(cmdlst[1])))
            dup.curplayer += 1
            dup.curstage = Stage.BUY
        elif cmdlst[0] == "meld":
            indexes = [cmdlst[i] for i in range(1,len(cmdlst))]
        elif cmdlst[0] == "build":
            card = dup.__curhand().pop(int(cmdlst[1][2]))
            dup.players[int(cmdlst[1][0])].melds[int(cmdlst[1][1])].put(card)
        elif  cmdlst[0] == "buy":
            last = len(dup.discardPile) - 1
            dup.__curhand().put(self.discardPile.pop(last))
            for i in range(2): self.__curhand().put(self.drawPile.pop(0))
            dup.__curplayer().buys += 1
            dup.curstage = Stage.PLAY
            dup.curaction = dup.curplayer
        else:
            print("ERROR: Cannot parse command ["+cmdlst[0]+"]")
            raise SyntaxError()
            
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
                
