# Game module
from deck import Deck
from player import Player, Dealer
from utils import calculate_hand_value

class GameResult:
    """Represents the result of a single game"""
    def __init__(self, player_wins, dealer_wins, is_draw, dealer_busted, player_busted):
        self.player_wins = player_wins
        self.dealer_wins = dealer_wins
        self.is_draw = is_draw
        self.dealer_busted = dealer_busted
        self.player_busted = player_busted

class GameStats:
    """Tracks statistics across multiple games"""
    def __init__(self):
        self.player_wins = 0
        self.dealer_wins = 0
        self.draws = 0
        self.dealer_busts = 0
        self.player_busts = 0
        self.total_games = 0
    
    def add_result(self, result):
        """Add a game result to the statistics"""
        self.total_games += 1
        if result.player_wins:
            self.player_wins += 1
        elif result.dealer_wins:
            self.dealer_wins += 1
        else:
            self.draws += 1
        
        if result.dealer_busted:
            self.dealer_busts += 1
        if result.player_busted:
            self.player_busts += 1
    
    def get_summary(self, strategy_name):
        """Get a formatted summary of the statistics"""
        return f"""Results after {self.total_games} rounds (Strategy: {strategy_name}):
Player Wins: {self.player_wins}
Dealer Wins: {self.dealer_wins}
Draws: {self.draws}
Dealer Busts: {self.dealer_busts}
Player Busts: {self.player_busts}"""

class Game:
    """Manages a single blackjack game"""
    def __init__(self):
        self.deck = Deck()
        self.player = Player("Player")
        self.dealer = Dealer()
    
    def deal_initial_cards(self):
        """Deal initial two cards to player and dealer"""
        self.player.clear_hand()
        self.dealer.clear_hand()
        
        # Deal two cards to each
        for _ in range(2):
            self.player.add_card(self.deck.deal_card())
            self.dealer.add_card(self.deck.deal_card())
    
    def play_player_turn(self, strategy):
        """Play the player's turn using the given strategy"""
        while not self.player.is_busted():
            action = strategy.decide(self.player.hand)
            if action == 'hit':
                self.player.add_card(self.deck.deal_card())
            else:  # stand
                break
    
    def play_dealer_turn(self):
        """Play the dealer's turn according to standard rules"""
        while self.dealer.should_hit() and not self.dealer.is_busted():
            self.dealer.add_card(self.deck.deal_card())
    
    def determine_winner(self):
        """Determine the winner and return a GameResult"""
        player_value = self.player.get_hand_value()
        dealer_value = self.dealer.get_hand_value()
        
        player_busted = self.player.is_busted()
        dealer_busted = self.dealer.is_busted()
        
        # Player busts - dealer wins
        if player_busted:
            return GameResult(False, True, False, dealer_busted, True)
        
        # Dealer busts - player wins
        if dealer_busted:
            return GameResult(True, False, False, True, False)
        
        # Compare values
        if player_value > dealer_value:
            return GameResult(True, False, False, False, False)
        elif dealer_value > player_value:
            return GameResult(False, True, False, False, False)
        else:
            return GameResult(False, False, True, False, False)
    
    def play_round(self, strategy):
        """Play a complete round and return the result"""
        self.deal_initial_cards()
        self.play_player_turn(strategy)
        
        if not self.player.is_busted():
            self.play_dealer_turn()
        
        return self.determine_winner()

class GameSimulator:
    """Simulates multiple games for statistical analysis"""
    def __init__(self):
        self.game = Game()
    
    def simulate(self, strategy, num_rounds):
        """Simulate multiple rounds with a given strategy"""
        stats = GameStats()
        
        for _ in range(num_rounds):
            result = self.game.play_round(strategy)
            stats.add_result(result)
        
        return stats
