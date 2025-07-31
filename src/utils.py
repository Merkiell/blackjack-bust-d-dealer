# Utility functions

def calculate_hand_value(cards):
    """Calculate the best possible value of a hand considering Aces"""
    total = 0
    aces = 0
    
    for card in cards:
        if card.rank == 'A':
            aces += 1
            total += 11
        else:
            total += card.value()
    
    # Convert Aces from 11 to 1 if needed to avoid bust
    while total > 21 and aces > 0:
        total -= 10
        aces -= 1
    
    return total

def is_bust(cards):
    """Check if a hand is busted (over 21)"""
    return calculate_hand_value(cards) > 21

def format_hand(cards):
    """Format a hand for display"""
    hand_str = ', '.join(str(card) for card in cards)
    value = calculate_hand_value(cards)
    return f"{hand_str} (Value: {value})"
