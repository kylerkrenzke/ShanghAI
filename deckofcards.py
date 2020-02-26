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
        
        
        
class SetMeld(Pile):
    def __init__(self, initial):
        Pile.__init__(initial)
        
    def canAcceptCard(self, card):
        return card.rank == self.cards[0].rank

        