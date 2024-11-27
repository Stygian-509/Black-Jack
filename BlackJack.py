import random
import db  # Import the db module to handle money read/write

# List of suits and ranks
suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']

# Card values (point values) for each rank
card_values = {
    '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 
    'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': [1, 11]
}

def print_title():
    print("BLACKJACK!")
    print("Blackjack payout is 3:2")
    print()

# Create a deck where each suit is a list, and each card is a list containing rank and point value
def create_deck():
    deck = []
    for suit in suits:
        for rank in ranks:
            value = card_values[rank] if isinstance(card_values[rank], list) else [card_values[rank]]
            deck.append([rank, suit, value])  # Each card is [rank, suit, value]
    random.shuffle(deck)  # Shuffle the entire deck
    return deck

# Calculate the total value of the hand considering Ace as either 1 or 11
def calculate_hand_value(hand):
    value = 0
    aces = 0
    for card in hand:
        card_value = card_values[card[0]]
        if isinstance(card_value, list):
            aces += 1
        else:
            value += card_value
    for _ in range(aces):
        value += 11 if value + 11 <= 21 else 1
    return value

# Check if the hand is a blackjack (Ace + 10-point card)
def is_blackjack(hand):
    if len(hand) == 2 and 'Ace' in [card[0] for card in hand]:
        value_cards = ['10', 'Jack', 'Queen', 'King']
        return any(card[0] in value_cards for card in hand)
    return False

# Function to prompt player for a valid bet amount
def get_bet_amount(player_money):
    while True:
        try:
            bet = float(input(f"Bet amount: "))
            if bet < 5:
                print("The minimum bet is $5.")
            elif bet > 1000:
                print("The maximum bet is $1000.")
            elif bet > player_money:
                print(f"You don't have enough money to make that bet. You have ${player_money:.2f}.")
            elif bet <= 0:
                print("Bet must be a positive number.")
            else:
                return bet
        except ValueError:
            print("Invalid input. Please enter a valid number.")

# Handle the player's money being below the minimum bet
def handle_low_balance(player_money):
    if player_money < 5:
        while player_money < 5:
            buy_chips = input("Your money is below the minimum bet of $5. Would you like to buy more chips?(y/n): ").lower()
            if buy_chips == 'y':
                while True:
                    try:
                        additional_money = float(input("Enter the amount of money to add: $"))
                        if additional_money <= 0:
                            print("You must enter a positive number.")
                        else:
                            player_money += additional_money
                            db.write_money_to_file(player_money)  # Update money in the file
                            print(f"Your new balance is: ${player_money:.2f}")
                            return player_money
                    except ValueError:
                        print("Invalid input. Please enter a valid number.")
            else:
                print("You chose not to buy more chips.")
                print("Come back soon! Bye!")
                return  # Exit back to main function
    return player_money

# Deal initial hands to player and dealer
def deal_initial_hands(deck):
    player_hand = [draw_card(deck), draw_card(deck)]  # Draw two cards from the shuffled deck
    dealer_hand = [draw_card(deck), draw_card(deck)]  # Draw two cards for the dealer
    return player_hand, dealer_hand

def draw_card(deck):
    if deck:
        return deck.pop()
    else:
        print("The deck is empty!")
        return None  # Return None if no cards left in the deck

# Handle the player's turn
def player_turn(deck, player_hand, dealer_hand):
    while calculate_hand_value(player_hand) < 21:
        if not deck:  # Check if deck is empty
            print("The deck is out of cards.")
            break  # Exit the loop if no more cards can be drawn
        move = input("Hit or stand? (hit/stand): ").lower()
        if move == 'hit':
            card = draw_card(deck)
            player_hand.append(card)
            print(f"\nYOUR CARDS:\n{[(card[0], card[1]) for card in player_hand]}\n")
        elif move == 'stand':
            print(f"\nDEALER'S CARDS:\n{[(card[0], card[1]) for card in dealer_hand]}")
            break

# Handle the dealer's turn
def dealer_turn(deck, dealer_hand):
    dealer_total = calculate_hand_value(dealer_hand)
    while dealer_total < 17:
        dealer_hand.append(draw_card(deck))  # Dealer draws from the first suit
        dealer_total = calculate_hand_value(dealer_hand)
    return dealer_total

def play_again():
    while True:
        play_again = input("\nDo you want to play again? (y/n): ").lower()
        if play_again == 'y':
            break
        elif play_again == 'n':
            print("\nCome back soon!")
            print("Bye!")
            return  # Exit the function
        else:
            print("Please enter 'y' to play again or 'n' to exit.")

# Main game loop
def main():
    print_title()
    player_money = db.read_money_from_file()

    while True:
        print(f"Money: {player_money}")
        # Handle low balance and prompt player for bet amount
        player_money = handle_low_balance(player_money)
        bet = get_bet_amount(player_money)

        # Create a new deck and deal initial hands
        deck = create_deck()
        player_hand, dealer_hand = deal_initial_hands(deck)

        # Show player and dealer hands
        print(f"\nDEALER'S SHOW CARD:\n[{dealer_hand[0][0]} of {dealer_hand[0][1]}]")
        print(f"\nYOUR CARDS:\n{[(card[0], card[1]) for card in player_hand]}\n")

        # Initiate any needed variables
        player_turn(deck, player_hand, dealer_hand)
        player_total = calculate_hand_value(player_hand)
        dealer_total = dealer_turn(deck, dealer_hand)

        # Check for player blackjack
        if is_blackjack(player_hand):
            print(f"\nYOUR POINTS: {player_total}\nDEALER'S POINTS: {dealer_total}")
            print("\nBlackjack! You win 1.5 times your bet.")
            winnings = round(bet * 1.5, 2)  # Blackjack payout (3:2)
            player_money += winnings
            db.write_money_to_file(player_money)  # Update money in the file
            continue

        # Player's turn
        if player_total > 21:
            print(f"\nYOUR POINTS: {player_total}\nDEALER'S POINTS: {dealer_total}")
            print(f"\nSorry. You lose.")
            player_money -= bet
            db.write_money_to_file(player_money)  # Update money in the file
            play_again()

        # Dealer's turn
        if dealer_total > 21:
            print(f"\nYOUR POINTS: {player_total}\nDEALER'S POINTS: {dealer_total}")
            print(f"\nDealer busted! You win your bet.")
            player_money += bet
        elif player_total > dealer_total:
            print(f"\nYOUR POINTS: {player_total}\nDEALER'S POINTS: {dealer_total}")
            print(f"\nYou win!")
            player_money += bet
        elif player_total < dealer_total:
            print(f"\nYOUR POINTS: {player_total}\nDEALER'S POINTS: {dealer_total}")
            print(f"\nSorry. You lose.")
            player_money -= bet
        else:
            print(f"\nYOUR POINTS: {player_total}\nDEALER'S POINTS: {dealer_total}")
            print(f"\nIt's a tie!")
            
        db.write_money_to_file(player_money)  # Update money after the round
        play_again()

    print("\nCome back soon!")
    print("Bye!")

if __name__ == "__main__":
    main()

    db.write_money_to_file(player_money)  # Update money after the round

if __name__ == "__main__":
    main()
   
