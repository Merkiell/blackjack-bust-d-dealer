# Blackjack Bust-the-Dealer Strategy Simulator

## Project Overview

This project simulates and compares two specific Blackjack player strategies designed to maximize the chance of the dealer busting. The simulator is modular, beginner-friendly, and extensible for future strategy additions.

## Strategies Compared

### Strategy A: Always Stand at 12+
- The player hits until their hand totals 12 or more, then always stands.
- This approach minimizes player busts and puts pressure on the dealer to bust.

### Strategy B: Always Stand at 16+
- The player hits until their hand totals 16 or more, then always stands.
- This approach maximizes hand value while still attempting to avoid a bust.

The simulator tracks win/loss/draw rates and how often the dealer busts for each strategy.

## Rules & Features

- Standard Blackjack rules: player vs dealer, handling of Aces (1 or 11), busts, dealer hits on 16 or less, stands on 17+.
- Automated play for both strategies.
- Simulate hundreds or thousands of rounds for statistical comparison.
- Command-line interface for selecting the strategy and number of rounds.
- Output includes statistics for each strategy.

## How to Run

1. **Install requirements**  
   This project only requires Python 3 (standard library). No external packages are needed.
   ```
   python3 --version
   ```

2. **Navigate to the src directory and run:**
   ```
   python3 main.py
   ```
   Follow the prompts to select a strategy and number of simulation rounds.

## Example Output

```
Select strategy:
1. Always Stand at 12+
2. Always Stand at 16+
Enter 1 or 2: 1
How many rounds to simulate? 10000

Results after 10000 rounds (Strategy: Always Stand at 12+):
Player Wins: 4201
Dealer Wins: 4922
Draws: 877
Dealer Busts: 2850
```

## Adding New Strategies

To add a new strategy, implement a function or class in `strategy.py` and add it to the CLI in `main.py`.

## Directory Structure

```
blackjack-bust-d-dealer/
├── README.md
├── requirements.txt
└── src/
    ├── main.py         # CLI and simulation management
    ├── deck.py         # Deck and card logic
    ├── player.py       # Player and dealer classes
    ├── strategy.py     # Strategy implementations
    ├── game.py         # Game flow and result tracking
    └── utils.py        # Helper functions
```

## License

MIT License
