# Strategy module
from utils import calculate_hand_value

class Strategy:
    """Base strategy class"""
    def __init__(self, name):
        self.name = name
    
    def decide(self, hand):
        """Decide whether to hit or stand based on the hand"""
        raise NotImplementedError("Strategy must implement decide method")

class AlwaysStandAt12Strategy(Strategy):
    """Strategy A: Always stand at 12+"""
    def __init__(self):
        super().__init__("Always Stand at 12+")
    
    def decide(self, hand):
        """Hit until hand totals 12 or more, then always stand"""
        hand_value = calculate_hand_value(hand)
        if hand_value >= 12:
            return 'stand'
        else:
            return 'hit'

class AlwaysStandAt16Strategy(Strategy):
    """Strategy B: Always stand at 16+"""
    def __init__(self):
        super().__init__("Always Stand at 16+")
    
    def decide(self, hand):
        """Hit until hand totals 16 or more, then always stand"""
        hand_value = calculate_hand_value(hand)
        if hand_value >= 16:
            return 'stand'
        else:
            return 'hit'

def get_available_strategies():
    """Return a list of available strategies"""
    return [
        AlwaysStandAt12Strategy(),
        AlwaysStandAt16Strategy()
    ]
