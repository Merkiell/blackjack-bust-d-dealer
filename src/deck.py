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

class CutCard:
    """Special card used to mark when deck should be reshuffled"""
    def __init__(self):
        pass
    
    def __str__(self):
        return "Cut Card"

class Deck:
    """Represents a multi-deck shoe with cut card mechanism"""
    def __init__(self, num_decks=6):
        self.num_decks = num_decks
        self.cards = []
        self.cut_card_position = 0
        self.cut_card_reached = False
        self.cards_dealt_since_shuffle = 0
        self.total_cards = num_decks * 52
        self.reset()
    
    def create_single_deck(self):
        """Create a single 52-card deck"""
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        
        deck = []
        for suit in suits:
            for rank in ranks:
                deck.append(Card(suit, rank))
        return deck
    
    def reset(self):
        """Create a new multi-deck shoe with cut card"""
        self.cards = []
        
        # Create multiple decks
        for _ in range(self.num_decks):
            self.cards.extend(self.create_single_deck())
        
        self.shuffle()
        self.place_cut_card()
        self.cut_card_reached = False
        self.cards_dealt_since_shuffle = 0
    
    def shuffle(self):
        """Shuffle the multi-deck shoe"""
        random.shuffle(self.cards)
    
    def place_cut_card(self):
        """Place cut card at 75th percentile (random position within that range)"""
        # 75th percentile means 25% of cards remain when cut card is reached
        min_position = int(self.total_cards * 0.70)  # 70-80% range for more realism
        max_position = int(self.total_cards * 0.80)
        self.cut_card_position = random.randint(min_position, max_position)
    
    def deal_card(self):
        """Deal one card from the deck"""
        if len(self.cards) == 0:
            self.reset()  # Emergency reshuffle if somehow empty
            return self.deal_card()
        
        # Check if we've reached the cut card position
        if self.cards_dealt_since_shuffle >= self.cut_card_position:
            self.cut_card_reached = True
        
        card = self.cards.pop()
        self.cards_dealt_since_shuffle += 1
        return card
    
    def should_reshuffle(self):
        """Check if deck should be reshuffled after current hand"""
        return self.cut_card_reached
    
    def reshuffle_after_hand(self):
        """Reshuffle the deck after a hand is completed (when cut card was reached)"""
        if self.cut_card_reached:
            self.reset()
    
    def cards_remaining(self):
        """Return number of cards remaining in the shoe"""
        return len(self.cards)
    
    def penetration_percentage(self):
        """Return how much of the deck has been dealt (penetration percentage)"""
        return (self.cards_dealt_since_shuffle / self.total_cards) * 100
    
    def get_deck_info(self):
        """Return information about the current deck state"""
        return {
            'num_decks': self.num_decks,
            'total_cards': self.total_cards,
            'cards_remaining': self.cards_remaining(),
            'cards_dealt': self.cards_dealt_since_shuffle,
            'penetration': self.penetration_percentage(),
            'cut_card_position': self.cut_card_position,
            'cut_card_reached': self.cut_card_reached
        }
