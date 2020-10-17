"""
    This module contains code related to
    Think Python, 2nd Edition
    by Allen Downey
    http://thinkpython2.com

    This is to complete the exercises in Chapter 18: Inheritance in Think Python 2
    
    Note: Using Python 3.9.0
"""
import random


class Card:
    """
        Represents a playing card

        attributes: 
            suit: integer (0-3)
            rank: integer (1-13)
    """
    suit_names = ["Clubs", "Diamonds", "Hearts", "Spades"]
    rank_names = [None, "Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King"]


    def __init__(self, suit = 0, rank = 0):
        """
            Initializes the object when instantiated

            suit: int
            rank: int
        """
        self.suit = suit
        self.rank = rank

    
    def __str__(self):
        """
            Returns a human-readable representation of the card

            return: string
        """
        return "%s of %s" % (Card.rank_names[self.rank], Card.suit_names[self.suit])

    
    def __lt__(self, other):
        """
            Determine if a card is less than another
            Note: this decision was arbitrarily made as to which suit outranked another

            other: Card

            return: boolean; True if the card is less than the other, False otherwise
        """
        t1 = self.suit, self.rank
        t2 = other.suit, other.rank
        return t1 < t2


    def __eq__(self, other):
        """
            Determines if a card is equal to another

            other: Card

            return: boolean; True if the cards are equal, False otherwise
        """
        return (self.suit == other.suit) and (self.rank == other.rank)


    def __gt__(self, other):
        """
            Determine if a card is greater than another
            Note: this decision was arbitrarily made as to which suit outranked another

            other: Card

            return: boolean; True if the card is greater than the other, False otherwise
        """
        t1 = self.suit, self.rank
        t2 = other.suit, other.rank
        return t1 > t2

    
class Deck:
    """
        Represents a deck of cards

        attributes:
            cards: list of Card objects
    """
    def __init__(self):
        """
            Initializes the deck with 52 cards
        """
        self.cards = []
        for suit in range(4):
            for rank in range(1, 14):
                card = Card(suit, rank)
                self.cards.append(card)
    

    def __str__(self):
        """
           Returns a human-readable representation of the deck

            return: string 
        """
        result = []
        for card in self.cards:
            result.append(str(card))
        return "\n".join(result)


    def pop_card(self, i = 1):
        """
            Remove a card from the deck and return it.
            
            i: integer; index of the card to pop; by default, the last card

            return: Card
        """
        return self.cards.pop()
    

    def add_card(self, card):
        """
            Add a card from the deck and return it.
            
            card: Card
        """
        self.cards.append(card)
    

    def shuffle(self):
        """
            Randomly shuffle the cards in the deck
        """
        random.shuffle(self.cards)


    def move_cards(self, hand, num):
        """
            Moves the given number of cards from the deck to the hand

            hand: Hand
            num: int
        """
        for i in range(num):
            hand.add_card(self.pop_card())


    def sort(self):
        """
            Sort the cards in ascending order
        """
        self.cards.sort()


class Hand(Deck):
    """
        Represents a hand of playing cards

        Inherits from Deck
    """
    def __init__(self, label=""):
        """
            Initializes when instantiated

            label: string
        """
        self.cards = []
        self.label = label


def find_defining_class(obj, method_name):
    """
        Finds and determines the class object that will provide the definition of the method name if it is invoked on the object.

        obj: object
        method_name: string

        return: type
    """
    for ty in type(obj).mro():
        if method_name in ty.__dict__:
            return ty
    return None

class Hist(dict):
    """
        A map from each item (x) to its frequency.
    """

    def __init__(self, seq=[]):
        """
            Creates a new histogram starting with the items in seq.

            seq: int
        """
        for x in seq:
            self.count(x)

    def count(self, x, f=1):
        """
            Increments (or decrements) the counter associated with item x.

            x: int
            f: int
        """
        self[x] = self.get(x, 0) + f
        if self[x] == 0:
            del self[x]


class PokerHand(Hand):
    """
        Represents a poker hand.
    """

    all_labels = ['straightflush', 'fourkind', 'fullhouse', 'flush', 'straight', 'threekind', 'twopair', 'pair', 'highcard']

    def make_histograms(self):
        """
            Computes histograms for suits and hands.
            
            Creates attributes:
                suits: a histogram of the suits in the hand.
                ranks: a histogram of the ranks.
                sets: a sorted list of the rank sets in the hand.
        """
        # Instantiate Hist
        self.suits = Hist()
        self.ranks = Hist()
        
        for c in self.cards:
            self.suits.count(c.suit)
            self.ranks.count(c.rank)

        self.sets = list(self.ranks.values())
        self.sets.sort(reverse=True)
 
    def has_highcard(self):
        """
            Determines if this hand has a high card.

            return: boolean; True if this hand has a high card, False otherwise
        """
        return len(self.cards)
        
    def check_sets(self, *t):
        """
            Determines if self.sets contains sets that are at least as big as the requirements in t.
            
            t: list of int

            return: boolean; True if self.sets contains at least the requirements in t, False otherwise
        """
        for need, have in zip(t, self.sets):
            if need > have:
                return False
        return True

    def has_pair(self):
        """
            Determines if this hand has a pair.

            return: boolean; True if has a pair, False otherwise
        """
        return self.check_sets(2)
        
    def has_twopair(self):
        """
            Determines if this hand as two pairs.
            
            return: boolean; True if this hand has two pairs, False otherwise
        """
        return self.check_sets(2, 2)
        
    def has_threekind(self):
        """
            Determines if this hand has three of a kind.

            return: boolean; True if the hand has three of a kind, False otherwise
        """
        return self.check_sets(3)
        
    def has_fourkind(self):
        """
            Determines if this hand has four of a kind.

            return: boolean; True if this hand has four of a kind, False otherwise
        """
        return self.check_sets(4)

    def has_fullhouse(self):
        """
            Determines whether this hand has a full house.

            return: boolean; True if this hand has a full house, False otherwise
        """
        return self.check_sets(3, 2)

    def has_flush(self):
        """
            Determines if this hand has a flush.

            return: boolean; True if this hand has a flush, False otherwise
        """
        for val in self.suits.values():
            if val >= 5:
                return True
        return False

    def has_straight(self):
        """
            Determines if this hand has a straight
            
            return: boolean; True if this hand has a straight, False otherwise
        """
        # make a copy of the rank histogram before we mess with it
        ranks = self.ranks.copy()
        ranks[14] = ranks.get(1, 0)

        # see if we have 5 in a row
        return self.in_a_row(ranks, 5)

    def in_a_row(self, ranks, n=5):
        """
            Determines if the histogram has n ranks in a row

            hist: map from rank to frequency
            n: int

            return: boolean; True if the histogram has n ranks in a row, False otherwise
        """
        count = 0
        for i in range(1, 15):
            if ranks.get(i, 0):
                count += 1
                if count == n:
                    return True
            else:
                count = 0
        return False
    
    def has_straightflush(self):
        """
            Determines if this hand has a straight flush.
            
            return: boolean; True if this hand has a flush, false otherwise
        """
        # partition the hand by suit and check each sub-hand for a straight
        d = {}
        for c in self.cards:
            d.setdefault(c.suit, PokerHand()).add_card(c)

        # determine if any of the partitioned hands has a straight
        for hand in d.values():
            if len(hand.cards) < 5:
                continue            
            hand.make_histograms()
            if hand.has_straight():
                return True
        return False

    def classify(self):
        """
            Classifies this hand.
        
            Creates attributes:
                labels:
        """
        self.make_histograms()

        self.labels = []
        for label in PokerHand.all_labels:
            f = getattr(self, 'has_' + label)
            if f():
                self.labels.append(label)


class PokerDeck(Deck):
    """
        Represents a deck of cards that can deal poker hands.
    """
    def deal_hands(self, num_cards=5, num_hands=10):
        """
            Deals hands from the deck and returns Hands.
            num_cards: cards per hand
            num_hands: number of hands
            
            return: list of Hands
        """
        # Initialize a list
        hands = []
        for i in range(num_hands):
            # Instantiate Pokerhand
            hand = PokerHand()
            self.move_cards(hand, num_cards)
            hand.classify()
            hands.append(hand)
        return hands


def main():
    # the label histogram: map from label to number of occurances
    lhist = Hist()

    # loop n times, dealing 7 hands per iteration, 7 cards each
    n = 10000
    for i in range(n):
        if i % 1000 == 0:
            print(i)
            
        deck = PokerDeck()
        deck.shuffle()

        hands = deck.deal_hands(7, 7)
        for hand in hands:
            for label in hand.labels:
                lhist.count(label)
            
    # print the results
    total = 7.0 * n
    print(total, 'hands dealt:')

    for label in PokerHand.all_labels:
        freq = lhist.get(label, 0)
        if freq == 0: 
            continue
        p = total / freq
        print('%s happens one time in %.2f' % (label, p))

        
if __name__ == '__main__':
    main()