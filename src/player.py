# Player module
from utils import calculate_hand_value, is_bust, format_hand

class Player:
    """Represents a player in the blackjack game"""
    def __init__(self, name):
        self.name = name
        self.hand = []
    
    def add_card(self, card):
        """Add a card to the player's hand"""
        self.hand.append(card)
    
    def clear_hand(self):
        """Clear the player's hand for a new round"""
        self.hand = []
    
    def get_hand_value(self):
        """Get the current value of the hand"""
        return calculate_hand_value(self.hand)
    
    def is_busted(self):
        """Check if the player is busted"""
        return is_bust(self.hand)
    
    def get_hand_display(self):
        """Get a formatted display of the hand"""
        return format_hand(self.hand)
    
    def make_move(self, strategy=None):
        """Make a move based on strategy (to be overridden or use strategy)"""
        if strategy:
            return strategy.decide(self.hand)
        return 'stand'  # Default action

class Dealer(Player):
    """Represents the dealer in the blackjack game"""
    def __init__(self):
        super().__init__("Dealer")
    
    def should_hit(self):
        """Dealer hits on 16 or less, stands on 17+"""
        return self.get_hand_value() <= 16
    
    def get_upcard(self):
        """Get the dealer's face-up card (first card)"""
        if len(self.hand) > 0:
            return self.hand[0]
        return None
    
    def get_hidden_display(self):
        """Get display with one card hidden"""
        if len(self.hand) < 2:
            return self.get_hand_display()
        
        visible_cards = [self.hand[0]]
        hand_str = f"{visible_cards[0]}, [Hidden]"
        return f"{hand_str} (Visible: {visible_cards[0].value()})"
