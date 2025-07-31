# Main entry point for the Blackjack simulator
from strategy import get_available_strategies
from game import GameSimulator

class BlackjackSimulator:
    """Main application class for the Blackjack strategy simulator"""
    def __init__(self):
        self.simulator = GameSimulator()
        self.strategies = get_available_strategies()
    
    def display_menu(self):
        """Display the strategy selection menu"""
        print("Select strategy:")
        for i, strategy in enumerate(self.strategies, 1):
            print(f"{i}. {strategy.name}")
    
    def get_strategy_choice(self):
        """Get the user's strategy choice"""
        while True:
            try:
                choice = int(input("Enter 1 or 2: "))
                if 1 <= choice <= len(self.strategies):
                    return self.strategies[choice - 1]
                else:
                    print(f"Please enter a number between 1 and {len(self.strategies)}")
            except ValueError:
                print("Please enter a valid number")
    
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
    
    def run_simulation(self):
        """Run the main simulation"""
        self.display_menu()
        strategy = self.get_strategy_choice()
        num_rounds = self.get_num_rounds()
        
        print(f"\nRunning {num_rounds} simulations with strategy: {strategy.name}")
        print("Please wait...")
        
        stats = self.simulator.simulate(strategy, num_rounds)
        
        print("\n" + "="*50)
        print(stats.get_summary(strategy.name))
        print("="*50)
    
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