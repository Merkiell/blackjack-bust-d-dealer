# Game module
from deck import Deck
from player import Player, Dealer
from utils import calculate_hand_value


class HandRecord:
    """Records detailed information about a single hand"""
    
    def __init__(self, hand_number, scenario_number, player_cards, dealer_cards, 
                 player_total, dealer_total, player_action, bet_amount, result, 
                 money_change, player_busted, dealer_busted, bankroll_after, is_blackjack=False):
        self.hand_number = hand_number
        self.scenario_number = scenario_number
        self.player_cards = player_cards  # List of card strings
        self.dealer_cards = dealer_cards  # List of card strings
        self.player_total = player_total
        self.dealer_total = dealer_total
        self.player_action = player_action  # "Hit" or "Stand"
        self.bet_amount = bet_amount
        self.result = result  # "Win", "Loss", "Draw"
        self.money_change = money_change
        self.player_busted = player_busted
        self.dealer_busted = dealer_busted
        self.bankroll_after = bankroll_after
        self.is_blackjack = is_blackjack  # Player got natural blackjack
        # Deck tracking attributes (set after creation)
        self.deck_penetration = 0.0
        self.cards_remaining = 0
        self.reshuffled_after = False


class GameResult:
    """Represents the result of a single game"""
    
    def __init__(self, player_wins, dealer_wins, is_draw, dealer_busted, player_busted, bet_amount=0.0, is_blackjack=False):
        self.player_wins = player_wins
        self.dealer_wins = dealer_wins
        self.is_draw = is_draw
        self.dealer_busted = dealer_busted
        self.player_busted = player_busted
        self.bet_amount = float(bet_amount)
        self.is_blackjack = is_blackjack  # Player got natural blackjack
        
        # Calculate money won/lost
        if player_wins:
            if is_blackjack:
                # Blackjack pays 3:2 (1.5x the bet)
                self.money_change = self.bet_amount * 1.5
            else:
                # Regular win pays 1:1
                self.money_change = self.bet_amount
        elif dealer_wins:
            self.money_change = -self.bet_amount  # Lose the bet amount
        else:  # Draw
            self.money_change = 0.0  # No money change on push


class GameStats:
    """Tracks statistics across multiple games"""
    
    def __init__(self, starting_bankroll=1000.0, target_multiplier=0.5):
        self.player_wins = 0
        self.dealer_wins = 0
        self.draws = 0
        self.dealer_busts = 0
        self.player_busts = 0
        self.player_blackjacks = 0  # Track player blackjacks
        self.total_games = 0
        self.starting_bankroll = float(starting_bankroll)
        self.current_bankroll = float(starting_bankroll)
        self.total_bet = 0.0
        self.total_winnings = 0.0
        self.biggest_win = 0.0
        self.biggest_loss = 0.0
        self.stopped_early = False
        self.stop_reason = ""
        self.reached_target = False
        self.target_multiplier = target_multiplier
        self.hand_records = []  # Store detailed hand records
        self.current_scenario = 1  # Track which scenario we're in
    
    def add_result(self, result):
        """Add a game result to the statistics"""
        self.total_games += 1
        
        if result.player_wins:
            self.player_wins += 1
            if result.is_blackjack:
                self.player_blackjacks += 1
        elif result.dealer_wins:
            self.dealer_wins += 1
        else:
            self.draws += 1
        
        if result.dealer_busted:
            self.dealer_busts += 1
        if result.player_busted:
            self.player_busts += 1
            
        # Update money tracking
        self.current_bankroll += result.money_change
        self.total_bet += result.bet_amount
        
        if result.money_change > 0:
            self.total_winnings += result.money_change
            if result.money_change > self.biggest_win:
                self.biggest_win = result.money_change
        elif result.money_change < 0:
            if abs(result.money_change) > self.biggest_loss:
                self.biggest_loss = abs(result.money_change)
    
    def get_summary(self, strategy_name):
        """Get a formatted summary of the statistics"""
        net_profit = self.current_bankroll - self.starting_bankroll
        win_rate = (self.player_wins / self.total_games) * 100 if self.total_games > 0 else 0
        blackjack_rate = (self.player_blackjacks / self.total_games) * 100 if self.total_games > 0 else 0
        target_profit = self.starting_bankroll * self.target_multiplier
        
        summary = (f"Results after {self.total_games} rounds (Strategy: {strategy_name}):\n"
                  f"Player Wins: {self.player_wins} ({win_rate:.1f}%)\n"
                  f"Player Blackjacks: {self.player_blackjacks} ({blackjack_rate:.1f}%)\n"
                  f"Dealer Wins: {self.dealer_wins}\n"
                  f"Draws: {self.draws}\n"
                  f"Dealer Busts: {self.dealer_busts}\n"
                  f"Player Busts: {self.player_busts}\n"
                  f"\n--- MONEY RESULTS ---\n"
                  f"Starting Bankroll: ${self.starting_bankroll:,.2f}\n"
                  f"Final Bankroll: ${self.current_bankroll:,.2f}\n"
                  f"Net Profit/Loss: ${net_profit:+,.2f}\n"
                  f"Total Amount Bet: ${self.total_bet:,.2f}\n")
        
        if self.total_bet > 0:
            roi = (net_profit/self.total_bet)*100
            summary += f"Return on Investment: {roi:.2f}%\n"
        
        if self.stopped_early:
            summary += f"\n--- EARLY STOP ---\n{self.stop_reason}\n"
        
        if self.reached_target:
            summary += f"🎉 TARGET REACHED: Profit ≥ ${target_profit:,.2f} ({self.target_multiplier}x bankroll)\n"
            
        return summary


class Game:
    """Manages a single blackjack game"""
    
    def __init__(self, num_decks=6):
        self.deck = Deck(num_decks)
        self.player = Player("Player")
        self.dealer = Dealer()
        self.reshuffle_pending = False
    
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
    
    def check_reshuffle_after_hand(self):
        """Check if deck should be reshuffled after this hand"""
        if self.deck.should_reshuffle():
            self.deck.reshuffle_after_hand()
            self.reshuffle_pending = False
            return True
        return False
    
    def is_blackjack(self, hand):
        """Check if a hand is a natural blackjack (Ace + 10-value card in first 2 cards)"""
        if len(hand) != 2:
            return False
        
        # Check if we have exactly one Ace and one 10-value card
        has_ace = False
        has_ten = False
        
        for card in hand:
            if card.rank == 'A':
                has_ace = True
            elif card.value() == 10:  # 10, J, Q, K
                has_ten = True
        
        return has_ace and has_ten
    
    def determine_winner(self, bet_amount=10.0):
        """Determine the winner and return a GameResult"""
        player_value = self.player.get_hand_value()
        dealer_value = self.dealer.get_hand_value()
        
        player_busted = self.player.is_busted()
        dealer_busted = self.dealer.is_busted()
        
        # Check for blackjacks
        player_blackjack = self.is_blackjack(self.player.hand)
        dealer_blackjack = self.is_blackjack(self.dealer.hand)
        
        # Handle blackjack scenarios first
        if player_blackjack and dealer_blackjack:
            # Both have blackjack - push (draw)
            return GameResult(False, False, True, dealer_busted, player_busted, bet_amount, False)
        elif player_blackjack and not dealer_blackjack:
            # Player blackjack wins with 3:2 payout
            return GameResult(True, False, False, dealer_busted, player_busted, bet_amount, True)
        elif dealer_blackjack and not player_blackjack:
            # Dealer blackjack wins (player loses immediately)
            return GameResult(False, True, False, dealer_busted, player_busted, bet_amount, False)
        
        # No blackjacks - proceed with normal rules
        # Player busts - dealer wins
        if player_busted:
            return GameResult(False, True, False, dealer_busted, True, bet_amount, False)
        
        # Dealer busts - player wins
        if dealer_busted:
            return GameResult(True, False, False, True, False, bet_amount, False)
        
        # Compare values
        if player_value > dealer_value:
            return GameResult(True, False, False, False, False, bet_amount, False)
        elif dealer_value > player_value:
            return GameResult(False, True, False, False, False, bet_amount, False)
        else:
            return GameResult(False, False, True, False, False, bet_amount, False)
    
    def play_round(self, strategy, bet_amount=10.0, hand_number=1, scenario_number=1, stats=None):
        """Play a complete round and return the result with detailed hand record"""
        self.deal_initial_cards()
        
        # Record initial cards
        player_cards = [str(card) for card in self.player.hand]
        dealer_cards = [str(card) for card in self.dealer.hand]
        
        # Check for blackjacks first
        player_blackjack = self.is_blackjack(self.player.hand)
        dealer_blackjack = self.is_blackjack(self.dealer.hand)
        
        # Track player actions
        player_action = "Stand"  # Default
        
        # If player has blackjack, no hitting allowed
        if not player_blackjack:
            # Play player turn and track if they hit
            while not self.player.is_busted():
                action = strategy.decide(self.player.hand)
                if action == 'hit':
                    player_action = "Hit"
                    self.player.add_card(self.deck.deal_card())
                    player_cards.append(str(self.player.hand[-1]))  # Add new card to record
                else:  # stand
                    break
        else:
            player_action = "Blackjack"
        
        # Dealer plays only if player doesn't have blackjack or both have blackjack
        if not player_blackjack or dealer_blackjack:
            if not self.player.is_busted():
                self.play_dealer_turn()
        
        # Update dealer cards if dealer drew more
        if len(self.dealer.hand) > 2:
            dealer_cards = [str(card) for card in self.dealer.hand]
        
        result = self.determine_winner(bet_amount)
        
        # Check for reshuffle after hand is complete
        reshuffled = self.check_reshuffle_after_hand()
        
        # Create detailed hand record if stats provided
        if stats is not None:
            player_total = self.player.get_hand_value()
            dealer_total = self.dealer.get_hand_value()
            
            # Determine result string
            if result.player_wins:
                if result.is_blackjack:
                    result_str = "Blackjack"
                else:
                    result_str = "Win"
            elif result.dealer_wins:
                result_str = "Loss" 
            else:
                result_str = "Draw"
            
            # Calculate bankroll after this hand
            bankroll_after = stats.current_bankroll + result.money_change
            
            # Get deck info for this hand
            deck_info = self.deck.get_deck_info()
            
            hand_record = HandRecord(
                hand_number=hand_number,
                scenario_number=scenario_number,
                player_cards=player_cards,
                dealer_cards=dealer_cards,
                player_total=player_total,
                dealer_total=dealer_total,
                player_action=player_action,
                bet_amount=bet_amount,
                result=result_str,
                money_change=result.money_change,
                player_busted=result.player_busted,
                dealer_busted=result.dealer_busted,
                bankroll_after=bankroll_after,
                is_blackjack=result.is_blackjack
            )
            
            # Add deck information to hand record
            hand_record.deck_penetration = deck_info['penetration']
            hand_record.cards_remaining = deck_info['cards_remaining']
            hand_record.reshuffled_after = reshuffled
            
            stats.hand_records.append(hand_record)
        
        return result


class GameSimulator:
    """Simulates multiple games for statistical analysis"""
    
    def __init__(self, num_decks=6):
        self.game = Game(num_decks)
        self.num_decks = num_decks
    
    def simulate(self, strategy, num_rounds, starting_bankroll=1000.0, base_bet_amount=10.0, target_multiplier=0.5, scenario_number=1):
        """Simulate multiple rounds with progressive betting strategy"""
        # Reset the game with fresh deck for each scenario
        self.game = Game(self.num_decks)
        
        stats = GameStats(starting_bankroll, target_multiplier)
        stats.current_scenario = scenario_number
        current_bet = base_bet_amount
        target_profit = starting_bankroll * target_multiplier
        
        for round_num in range(num_rounds):
            # Check if player has enough money to bet
            if stats.current_bankroll < current_bet:
                stats.stopped_early = True
                stats.stop_reason = f"Insufficient funds after {stats.total_games} rounds (Need ${current_bet:.2f}, Have ${stats.current_bankroll:.2f})"
                break
            
            # Check if target profit reached
            current_profit = stats.current_bankroll - starting_bankroll
            if current_profit >= target_profit:
                stats.reached_target = True
                stats.stopped_early = True
                stats.stop_reason = f"Target profit reached after {stats.total_games} rounds (${current_profit:,.2f} ≥ ${target_profit:,.2f})"
                break
                
            # Play the round with detailed tracking
            result = self.game.play_round(strategy, current_bet, round_num + 1, scenario_number, stats)
            stats.add_result(result)
            
            # Adjust bet based on result
            if result.player_wins or result.is_draw:
                # Win or draw - reset to base bet
                current_bet = base_bet_amount
            else:
                # Loss - triple the bet for next round
                current_bet *= 3
        
        return stats
