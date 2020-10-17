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


if __name__ == '__main__':
    deck = Deck()
    deck.shuffle()

    hand = Hand("My hand")
    print(find_defining_class(hand, 'shuffle'))

    deck.move_cards(hand, 5)
    hand.sort()
    print(hand.label)
    print(hand)