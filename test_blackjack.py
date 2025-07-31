# Test script to verify blackjack 3:2 payout functionality
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from deck import Card, Deck
from game import Game, GameResult
from strategy import AlwaysStandAt12Strategy

def test_blackjack_payout():
    """Test that blackjack pays 3:2 correctly"""
    print("Testing Blackjack 3:2 Payout...")
    
    # Create a game instance
    game = Game(num_decks=1)
    
    # Manually create a blackjack hand (Ace + King)
    ace_hearts = Card("Hearts", "A")
    king_spades = Card("Spades", "K")
    
    # Test blackjack detection
    blackjack_hand = [ace_hearts, king_spades]
    is_bj = game.is_blackjack(blackjack_hand)
    print(f"Ace + King is blackjack: {is_bj}")
    
    # Test non-blackjack hand
    two_hearts = Card("Hearts", "2")
    nine_spades = Card("Spades", "9")
    regular_hand = [two_hearts, nine_spades]
    is_not_bj = game.is_blackjack(regular_hand)
    print(f"2 + 9 is blackjack: {is_not_bj}")
    
    # Test payout calculation
    bet_amount = 50.0
    
    # Regular win result
    regular_win = GameResult(True, False, False, False, False, bet_amount, False)
    print(f"Regular win with ${bet_amount} bet: ${regular_win.money_change}")
    
    # Blackjack win result  
    blackjack_win = GameResult(True, False, False, False, False, bet_amount, True)
    print(f"Blackjack win with ${bet_amount} bet: ${blackjack_win.money_change}")
    
    # Verify 3:2 payout
    expected_blackjack_payout = bet_amount * 1.5
    print(f"Expected blackjack payout: ${expected_blackjack_payout}")
    print(f"Actual blackjack payout: ${blackjack_win.money_change}")
    print(f"Correct payout: {blackjack_win.money_change == expected_blackjack_payout}")

if __name__ == "__main__":
    test_blackjack_payout()
