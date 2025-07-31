# Deck module
import random

class Card:
    """Represents a single card in the deck"""
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        
    def value(self):
        """Return the value of the card for blackjack"""
        if self.rank in ['J', 'Q', 'K']:
            return 10
        elif self.rank == 'A':
            return 11  # Ace is 11 by default, handled as 1 in hand calculation
        else:
            return int(self.rank)
    
    def __str__(self):
        return f"{self.rank} of {self.suit}"

class Deck:
    """Represents a deck of 52 cards"""
    def __init__(self):
        self.cards = []
        self.reset()
    
    def reset(self):
        """Create a new deck of 52 cards"""
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        
        self.cards = []
        for suit in suits:
            for rank in ranks:
                self.cards.append(Card(suit, rank))
        
        self.shuffle()
    
    def shuffle(self):
        """Shuffle the deck"""
        random.shuffle(self.cards)
    
    def deal_card(self):
        """Deal one card from the deck"""
        if len(self.cards) == 0:
            self.reset()  # Auto-reshuffle when deck is empty
        return self.cards.pop()
