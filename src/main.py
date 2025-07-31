# Main entry point for the Blackjack simulator
import csv
import os
from datetime import datetime
from strategy import get_available_strategies
from game import GameSimulator

class BlackjackSimulator:
    """Main application class for the Blackjack strategy simulator"""
    def __init__(self):
        self.simulator = None  # Will be initialized with deck count
        self.strategies = get_available_strategies()
        self.num_decks = 6  # Default
    
    def get_num_rounds(self):
        """Get the number of rounds to simulate"""
        while True:
            try:
                num_rounds = int(input("How many rounds to simulate? "))
                if num_rounds > 0:
                    return num_rounds
                else:
                    print("Please enter a positive number")
            except ValueError:
                print("Please enter a valid number")
    
    def get_bankroll(self):
        """Get the starting bankroll amount"""
        while True:
            try:
                bankroll = float(input("Starting bankroll (default $1000): ") or "1000")
                if bankroll > 0:
                    return bankroll
                else:
                    print("Please enter a positive amount")
            except ValueError:
                print("Please enter a valid amount")
    
    def get_bet_amount(self, bankroll):
        """Get the bet amount per hand"""
        while True:
            try:
                max_bet = bankroll / 10  # Suggest max 10% of bankroll per bet
                bet = float(input(f"Bet amount per hand (default $10, max recommended ${max_bet:.2f}): ") or "10")
                if bet > 0:
                    if bet > bankroll:
                        print(f"Bet amount cannot exceed your bankroll of ${bankroll:.2f}")
                        continue
                    return bet
                else:
                    print("Please enter a positive amount")
            except ValueError:
                print("Please enter a valid amount")
    
    def get_num_scenarios(self):
        """Get the number of scenarios to run"""
        while True:
            try:
                scenarios = int(input("Number of scenarios to run (default 10): ") or "10")
                if scenarios > 0:
                    return scenarios
                else:
                    print("Please enter a positive number")
            except ValueError:
                print("Please enter a valid number")
    
    def get_target_multiplier(self):
        """Get the target profit multiplier"""
        while True:
            try:
                multiplier = float(input("Target profit multiplier (e.g., 0.5 for half bankroll, 2.0 for double, default 0.5): ") or "0.5")
                if multiplier > 0:
                    return multiplier
                else:
                    print("Please enter a positive number")
            except ValueError:
                print("Please enter a valid number")
    
    def get_num_decks(self):
        """Get the number of decks for the table"""
        print("\n--- TABLE SETTINGS ---")
        print("Select the number of decks used at the table:")
        print("1. Two Decks (2)")
        print("2. Four Decks (4)")
        print("3. Six Decks (6) - Standard")
        print("4. Eight Decks (8)")
        
        while True:
            try:
                choice = input("Enter your choice (1-4, default 3 for 6 decks): ") or "3"
                choice = int(choice)
                
                deck_options = {1: 2, 2: 4, 3: 6, 4: 8}
                
                if choice in deck_options:
                    num_decks = deck_options[choice]
                    print(f"Selected: {num_decks} decks")
                    print(f"Total cards: {num_decks * 52}")
                    print(f"Cut card will be placed at approximately 75% penetration")
                    return num_decks
                else:
                    print("Please enter a number between 1 and 4")
            except ValueError:
                print("Please enter a valid number")
    
    def run_simulation(self):
        """Run the main simulation for both strategies"""
        print("Testing both strategies automatically...")
        
        # Get table settings first
        self.num_decks = self.get_num_decks()
        
        # Initialize simulator with chosen deck count
        self.simulator = GameSimulator(self.num_decks)
        
        num_rounds = self.get_num_rounds()
        
        print("\n--- MONEY SETTINGS ---")
        bankroll = self.get_bankroll()
        bet_amount = self.get_bet_amount(bankroll)
        
        print("\n--- SCENARIO SETTINGS ---")
        num_scenarios = self.get_num_scenarios()
        
        print("\n--- TARGET SETTINGS ---")
        target_multiplier = self.get_target_multiplier()
        target_amount = bankroll * target_multiplier
        
        # Test both strategies and collect all results
        all_strategy_results = {}
        
        for strategy in self.strategies:
            print(f"\n{'='*60}")
            print(f"TESTING STRATEGY: {strategy.name}")
            print(f"{'='*60}")
            
            print(f"\nRunning {num_scenarios} scenarios of {num_rounds} rounds each")
            print(f"Table: {self.num_decks} decks ({self.num_decks * 52} total cards)")
            print(f"Starting bankroll: ${bankroll:,.2f}")
            print(f"Base bet: ${bet_amount:,.2f} (Progressive: x3 on loss, reset on win)")
            print(f"Target: {target_multiplier}x profit (${target_amount:,.2f})")
            print("Please wait...\n")
            
            # Run multiple scenarios for this strategy
            strategy_results = []
            for i in range(num_scenarios):
                print(f"Running scenario {i+1}/{num_scenarios}...", end=" ", flush=True)
                stats = self.simulator.simulate(strategy, num_rounds, bankroll, bet_amount, target_multiplier, i+1)
                strategy_results.append(stats)
                print("✓")
            
            # Store results for combined CSV export
            all_strategy_results[strategy.name] = strategy_results
            
            # Display results for this strategy
            self.display_scenario_summary(strategy_results, strategy.name, num_rounds, bankroll, bet_amount, target_multiplier)
            
            print(f"\n{strategy.name} completed!")
        
        # Export combined results to single CSV
        self.export_combined_csv(all_strategy_results, num_rounds, bankroll, bet_amount, target_multiplier)
        
        # Export detailed hand records for each strategy
        self.export_hand_records(all_strategy_results, num_rounds, bankroll, bet_amount, target_multiplier)
        
        print(f"\n{'='*60}")
        print("ALL STRATEGIES COMPLETED!")
        print(f"{'='*60}")
    
    def display_scenario_summary(self, results, strategy_name, rounds_per_scenario, starting_bankroll, bet_amount, target_multiplier):
        """Display a comprehensive summary of all scenarios"""
        print("\n" + "="*90)
        print(f"SUMMARY: {len(results)} Scenarios of {rounds_per_scenario} rounds each")
        print(f"Strategy: {strategy_name} | Table: {self.num_decks} decks | Starting: ${starting_bankroll:,.2f} | Base Bet: ${bet_amount:,.2f} (Progressive)")
        print(f"Target: {target_multiplier}x bankroll (${starting_bankroll * target_multiplier:,.2f})")
        print("="*90)
        
        # Table header
        print(f"{'Scenario':<10} {'Win%':<8} {'Final $':<12} {'Profit/Loss':<12} {'Rounds':<8} {'Target?':<8} {'Status':<15}")
        print("-" * 90)
        
        # Individual scenario results
        total_profit = 0
        profitable_scenarios = 0
        busted_scenarios = 0
        target_reached_scenarios = 0
        
        for i, stats in enumerate(results, 1):
            profit = stats.current_bankroll - starting_bankroll
            win_rate = (stats.player_wins / stats.total_games) * 100 if stats.total_games > 0 else 0
            target_reached = "YES" if stats.reached_target else "NO"
            
            # Determine status
            if stats.current_bankroll <= 0:
                status = "BUSTED"
                busted_scenarios += 1
            elif stats.reached_target:
                status = "TARGET HIT"
                target_reached_scenarios += 1
            elif stats.stopped_early:
                status = "EARLY STOP"
            elif profit > 0:
                status = "PROFITABLE"
            else:
                status = "LOSS"
            
            if profit > 0:
                profitable_scenarios += 1
                
            total_profit += profit
            
            print(f"{i:<10} {win_rate:<8.1f} ${stats.current_bankroll:<11,.2f} "
                  f"${profit:<11.2f} {stats.total_games:<8} {target_reached:<8} {status:<15}")
        
        # Summary statistics
        print("-" * 90)
        avg_profit = total_profit / len(results)
        success_rate = (profitable_scenarios / len(results)) * 100
        bust_rate = (busted_scenarios / len(results)) * 100
        target_rate = (target_reached_scenarios / len(results)) * 100
        
        print(f"\nOVERALL STATISTICS:")
        print(f"Average Profit/Loss: ${avg_profit:+,.2f}")
        print(f"Profitable Scenarios: {profitable_scenarios}/{len(results)} ({success_rate:.1f}%)")
        print(f"Target Reached: {target_reached_scenarios}/{len(results)} ({target_rate:.1f}%)")
        print(f"Busted Scenarios: {busted_scenarios}/{len(results)} ({bust_rate:.1f}%)")
        print(f"Total Profit/Loss: ${total_profit:+,.2f}")
        
        # Best and worst performance
        best_result = max(results, key=lambda x: x.current_bankroll - starting_bankroll)
        worst_result = min(results, key=lambda x: x.current_bankroll - starting_bankroll)
        
        best_profit = best_result.current_bankroll - starting_bankroll
        worst_profit = worst_result.current_bankroll - starting_bankroll
        
        print(f"\nBEST SCENARIO: ${best_profit:+,.2f} (Final: ${best_result.current_bankroll:,.2f})")
        print(f"WORST SCENARIO: ${worst_profit:+,.2f} (Final: ${worst_result.current_bankroll:,.2f})")
        
        # Progressive betting analysis
        target_amount = starting_bankroll * target_multiplier
        print(f"\nPROGRESSIVE BETTING ANALYSIS:")
        print(f"Target Profit: ${target_amount:,.2f} ({target_multiplier}x starting bankroll)")
        print(f"Success Rate: {target_rate:.1f}% reached target before running out of money/rounds")
        
        print("="*90)
    
    def export_combined_csv(self, all_strategy_results, rounds_per_scenario, starting_bankroll, bet_amount, target_multiplier):
        """Export combined results for both strategies to single CSV files"""
        timestamp = datetime.now().strftime("%m%d_%H%M")
        
        # Create results directory if it doesn't exist
        results_dir = os.path.join(os.path.dirname(__file__), "..", "results")
        os.makedirs(results_dir, exist_ok=True)
        
        # Export detailed scenario results - COMBINED
        detailed_filename = f"BJ_Combined_detail_{timestamp}.csv"
        detailed_path = os.path.join(results_dir, detailed_filename)
        
        with open(detailed_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            
            # Write header
            writer.writerow([
                'Strategy', 'Scenario', 'Player_Wins', 'Player_Blackjacks', 'Dealer_Wins', 'Draws', 'Dealer_Busts', 'Player_Busts',
                'Total_Games', 'Starting_Bankroll', 'Final_Bankroll', 'Profit_Loss', 'Win_Rate_%', 'Blackjack_Rate_%',
                'Target_Reached', 'Stopped_Early', 'Stop_Reason', 'Status'
            ])
            
            # Write data for all strategies
            for strategy_name, results in all_strategy_results.items():
                strategy_short = "S12" if "12" in strategy_name else "S16"
                
                for i, stats in enumerate(results, 1):
                    profit = stats.current_bankroll - starting_bankroll
                    win_rate = (stats.player_wins / stats.total_games) * 100 if stats.total_games > 0 else 0
                    blackjack_rate = (stats.player_blackjacks / stats.total_games) * 100 if stats.total_games > 0 else 0
                    
                    # Determine status
                    if stats.current_bankroll <= 0:
                        status = "BUSTED"
                    elif stats.reached_target:
                        status = "TARGET_HIT"
                    elif stats.stopped_early:
                        status = "EARLY_STOP"
                    elif profit > 0:
                        status = "PROFITABLE"
                    else:
                        status = "LOSS"
                    
                    writer.writerow([
                        strategy_short, i, stats.player_wins, stats.player_blackjacks, stats.dealer_wins, stats.draws, stats.dealer_busts,
                        stats.player_busts, stats.total_games, starting_bankroll, stats.current_bankroll,
                        profit, win_rate, blackjack_rate, stats.reached_target, stats.stopped_early,
                        stats.stop_reason, status
                    ])
        
        # Export summary statistics - COMBINED
        summary_filename = f"BJ_Combined_summary_{timestamp}.csv"
        summary_path = os.path.join(results_dir, summary_filename)
        
        with open(summary_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            
            # Write configuration
            writer.writerow(['Configuration'])
            writer.writerow(['Strategies_Tested', ', '.join(all_strategy_results.keys())])
            writer.writerow(['Num_Decks', self.num_decks])
            writer.writerow(['Total_Cards_Per_Shoe', self.num_decks * 52])
            writer.writerow(['Scenarios_Per_Strategy', len(next(iter(all_strategy_results.values())))])
            writer.writerow(['Rounds_Per_Scenario', rounds_per_scenario])
            writer.writerow(['Starting_Bankroll', starting_bankroll])
            writer.writerow(['Base_Bet_Amount', bet_amount])
            writer.writerow(['Target_Multiplier', target_multiplier])
            writer.writerow(['Target_Profit', starting_bankroll * target_multiplier])
            writer.writerow([])
            
            # Write summary for each strategy
            for strategy_name, results in all_strategy_results.items():
                strategy_short = "S12" if "12" in strategy_name else "S16"
                
                # Calculate summary statistics
                total_profit = sum(stats.current_bankroll - starting_bankroll for stats in results)
                profitable_scenarios = sum(1 for stats in results if (stats.current_bankroll - starting_bankroll) > 0)
                busted_scenarios = sum(1 for stats in results if stats.current_bankroll <= 0)
                target_reached_scenarios = sum(1 for stats in results if stats.reached_target)
                
                avg_profit = total_profit / len(results)
                success_rate = (profitable_scenarios / len(results)) * 100
                bust_rate = (busted_scenarios / len(results)) * 100
                target_rate = (target_reached_scenarios / len(results)) * 100
                
                best_result = max(results, key=lambda x: x.current_bankroll - starting_bankroll)
                worst_result = min(results, key=lambda x: x.current_bankroll - starting_bankroll)
                best_profit = best_result.current_bankroll - starting_bankroll
                worst_profit = worst_result.current_bankroll - starting_bankroll
                
                writer.writerow([f'{strategy_short}_Summary'])
                writer.writerow([f'{strategy_short}_Strategy_Name', strategy_name])
                writer.writerow([f'{strategy_short}_Average_Profit_Loss', avg_profit])
                writer.writerow([f'{strategy_short}_Total_Profit_Loss', total_profit])
                writer.writerow([f'{strategy_short}_Profitable_Scenarios', profitable_scenarios])
                writer.writerow([f'{strategy_short}_Success_Rate_%', success_rate])
                writer.writerow([f'{strategy_short}_Target_Reached_Scenarios', target_reached_scenarios])
                writer.writerow([f'{strategy_short}_Target_Rate_%', target_rate])
                writer.writerow([f'{strategy_short}_Busted_Scenarios', busted_scenarios])
                writer.writerow([f'{strategy_short}_Bust_Rate_%', bust_rate])
                writer.writerow([f'{strategy_short}_Best_Scenario_Profit', best_profit])
                writer.writerow([f'{strategy_short}_Worst_Scenario_Profit', worst_profit])
                writer.writerow([])
            
            # Write comparison summary
            writer.writerow(['Strategy_Comparison'])
            writer.writerow(['Metric', 'Stand_at_12', 'Stand_at_16', 'Better_Strategy'])
            
            # Get strategy results for comparison
            s12_results = None
            s16_results = None
            for strategy_name, results in all_strategy_results.items():
                if "12" in strategy_name:
                    s12_results = results
                else:
                    s16_results = results
            
            if s12_results and s16_results:
                # Calculate metrics for comparison
                s12_avg_profit = sum(stats.current_bankroll - starting_bankroll for stats in s12_results) / len(s12_results)
                s16_avg_profit = sum(stats.current_bankroll - starting_bankroll for stats in s16_results) / len(s16_results)
                
                s12_success_rate = (sum(1 for stats in s12_results if (stats.current_bankroll - starting_bankroll) > 0) / len(s12_results)) * 100
                s16_success_rate = (sum(1 for stats in s16_results if (stats.current_bankroll - starting_bankroll) > 0) / len(s16_results)) * 100
                
                s12_target_rate = (sum(1 for stats in s12_results if stats.reached_target) / len(s12_results)) * 100
                s16_target_rate = (sum(1 for stats in s16_results if stats.reached_target) / len(s16_results)) * 100
                
                s12_bust_rate = (sum(1 for stats in s12_results if stats.current_bankroll <= 0) / len(s12_results)) * 100
                s16_bust_rate = (sum(1 for stats in s16_results if stats.current_bankroll <= 0) / len(s16_results)) * 100
                
                writer.writerow(['Average_Profit', f'${s12_avg_profit:.2f}', f'${s16_avg_profit:.2f}', 'S12' if s12_avg_profit > s16_avg_profit else 'S16'])
                writer.writerow(['Success_Rate_%', f'{s12_success_rate:.1f}%', f'{s16_success_rate:.1f}%', 'S12' if s12_success_rate > s16_success_rate else 'S16'])
                writer.writerow(['Target_Rate_%', f'{s12_target_rate:.1f}%', f'{s16_target_rate:.1f}%', 'S12' if s12_target_rate > s16_target_rate else 'S16'])
                writer.writerow(['Bust_Rate_%', f'{s12_bust_rate:.1f}%', f'{s16_bust_rate:.1f}%', 'S12' if s12_bust_rate < s16_bust_rate else 'S16'])
        
        print(f"\n📊 Combined results exported to CSV files:")
        print(f"   Detailed: {detailed_path}")
        print(f"   Summary:  {summary_path}")
        print(f"   Location: {os.path.abspath(results_dir)}")
    
    def export_hand_records(self, all_strategy_results, rounds_per_scenario, starting_bankroll, bet_amount, target_multiplier):
        """Export detailed hand-by-hand records for each strategy to separate CSV files"""
        timestamp = datetime.now().strftime("%m%d_%H%M")
        
        # Create results directory if it doesn't exist
        results_dir = os.path.join(os.path.dirname(__file__), "..", "results")
        os.makedirs(results_dir, exist_ok=True)
        
        # Export hand records for each strategy separately
        for strategy_name, results in all_strategy_results.items():
            strategy_short = "S12" if "12" in strategy_name else "S16"
            
            # Create filename for this strategy's hand records
            hands_filename = f"BJ_{strategy_short}_hands_{timestamp}.csv"
            hands_path = os.path.join(results_dir, hands_filename)
            
            with open(hands_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                
                # Write header
                writer.writerow([
                    'Strategy', 'Scenario', 'Hand_Number', 'Player_Cards', 'Dealer_Cards',
                    'Player_Total', 'Dealer_Total', 'Player_Action', 'Bet_Amount',
                    'Result', 'Money_Change', 'Player_Busted', 'Dealer_Busted', 'Is_Blackjack',
                    'Bankroll_After', 'Cards_Count', 'Deck_Penetration_%', 'Cards_Remaining', 'Reshuffled_After'
                ])
                
                # Write all hand records for this strategy
                total_hands = 0
                for scenario_stats in results:
                    for hand_record in scenario_stats.hand_records:
                        total_hands += 1
                        
                        # Format card lists as strings
                        player_cards_str = ' | '.join(hand_record.player_cards)
                        dealer_cards_str = ' | '.join(hand_record.dealer_cards)
                        cards_count = len(hand_record.player_cards) + len(hand_record.dealer_cards)
                        
                        writer.writerow([
                            strategy_short,
                            hand_record.scenario_number,
                            hand_record.hand_number,
                            player_cards_str,
                            dealer_cards_str,
                            hand_record.player_total,
                            hand_record.dealer_total,
                            hand_record.player_action,
                            hand_record.bet_amount,
                            hand_record.result,
                            hand_record.money_change,
                            hand_record.player_busted,
                            hand_record.dealer_busted,
                            hand_record.is_blackjack,
                            hand_record.bankroll_after,
                            cards_count,
                            f"{hand_record.deck_penetration:.1f}%",
                            hand_record.cards_remaining,
                            hand_record.reshuffled_after
                        ])
                
                print(f"\n📋 {strategy_short} Hand Records: {total_hands} hands exported to {hands_filename}")
        
        print(f"\n📁 Hand records location: {os.path.abspath(results_dir)}")
    
    def start_game(self):
        """Start the game application"""
        print("=" * 50)
        print("Blackjack Bust-the-Dealer Strategy Simulator")
        print("=" * 50)
        print()
        
        try:
            self.run_simulation()
        except KeyboardInterrupt:
            print("\n\nSimulation interrupted by user.")
        except Exception as e:
            print(f"\nAn error occurred: {e}")
        
        print("\nThank you for using the Blackjack simulator!")

def main():
    """Main function"""
    simulator = BlackjackSimulator()
    simulator.start_game()

if __name__ == '__main__':
    main()