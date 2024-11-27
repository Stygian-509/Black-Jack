import random
import db  # Import the db module to handle money read/write

# List of suits
suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
# List of card ranks
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']

# Card values (point values) for each rank
card_values = {
    '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 
    'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': [1, 11]
}

# Create a deck where each suit is a list, and each card is a list containing rank and point value
def create_deck():
    deck = []
    for suit in suits:
        # Create a list of cards for each suit
        suit_cards = []
        for rank in ranks:
            suit_cards.append([rank, card_values[rank]])  # Add card as a list [rank, point_value]
        deck.append(suit_cards)  # Add the suit's cards to the deck
    random.shuffle(deck)  # Shuffle the deck
    return deck

# Calculate the total value of the hand considering the Ace can be 1 or 11
def calculate_hand_value(hand):
    value = 0
    aces = 0
    for card in hand:
        # Get the card's point value from the card_values dictionary
        card_value = card_values[card[0]]  # card[0] is the rank
        if isinstance(card_value, list):  # Check if it's an Ace
            aces += 1
        else:
            value += card_value  # Add the card value if it's not an Ace

    # Add the Ace values (either 1 or 11)
    for _ in range(aces):
        if value + 11 <= 21:
            value += 11
        else:
            value += 1
    return value

# Check if the hand is a blackjack (Ace + 10-point card)
def is_blackjack(hand):
    if len(hand) == 2:
        if 'Ace' in [card[0] for card in hand]:
            value_cards = ['10', 'Jack', 'Queen', 'King']
            if any(card[0] in value_cards for card in hand):
                return True
    return False

# Main function
def main():
    # Read the player's money from the file
    player_money = db.read_money_from_file()
    
    print(f"Welcome to the game! You have ${player_money:.2f} available.")

    # Main game loop
    while True:
        if player_money <= 0:
            print("You don't have enough money to continue playing!")
            # Prompt the player to buy more chips if they don't have enough money
            while player_money < 5:
                buy_chips = input("Your money is below the minimum bet of $5. Would you like to buy more chips? (yes/no): ").lower()
                if buy_chips == 'yes':
                    while True:
                        try:
                            additional_money = float(input("Enter the amount of money to add: $"))
                            if additional_money <= 0:
                                print("You must enter a positive number.")
                            else:
                                player_money += additional_money
                                db.write_money_to_file(player_money)  # Update money in the file
                                print(f"Your new balance is: ${player_money:.2f}")
                                break
                        except ValueError:
                            print("Invalid input. Please enter a valid number.")
                else:
                    print("You chose not to buy more chips. Exiting the game.")
                    return  # Exit the game if the player chooses not to buy more chips
        # Prompt player for bet amount with added validation
        while True:
            try:
                bet = float(input(f"You have ${player_money:.2f}. Bet amount (Min: $5, Max: $1000): "))
                
                if bet < 5:
                    print("The minimum bet is $5.")
                elif bet > 1000:
                    print("The maximum bet is $1000.")
                elif bet > player_money:
                    print(f"You don't have enough money to make that bet. You have ${player_money:.2f}.")
                elif bet <= 0:
                    print("Bet must be a positive number.")
                else:
                    break  # Exit the loop if the bet is valid
            except ValueError:
                print("Invalid input. Please enter a valid number.")

        # Create a new deck and deal hands
        deck = create_deck()
        player_hand = [deck[0].pop(), deck[1].pop()]  # Draw from the first two suits
        dealer_hand = [deck[2].pop(), deck[3].pop()]  # Draw from the next two suits

        print(f"Your hand:\n{[(card[0], card[1]) for card in player_hand]}\nTotal: {calculate_hand_value(player_hand)}")
        print(f"Dealer's hand:\n[{dealer_hand[0][0]} of {dealer_hand[0][1]}, ?]")

        # Check for player blackjack right away
        if is_blackjack(player_hand):
            print("Blackjack! You win 1.5 times your bet.")
            winnings = round(bet * 1.5, 2)
            player_money += winnings
            db.write_money_to_file(player_money)  # Update money in the file
            continue

        while calculate_hand_value(player_hand) < 21:
            move = input("Hit or stand? (hit/stand): ").lower()
            if move == 'hit':
                player_hand.append(deck[0].pop())  # Draw from the first suit
                print(f"You drew: {player_hand[-1][0]} of {player_hand[-1][1]}")
                print(f"Your hand:\n{[(card[0], card[1]) for card in player_hand]}\nTotal: {calculate_hand_value(player_hand)}")
            elif move == 'stand':
                break

        player_total = calculate_hand_value(player_hand)
        if player_total > 21:
            print("You busted! You lose your bet.")
            player_money -= bet
            db.write_money_to_file(player_money)  # Update money in the file
            continue

        print(f"Dealer's hand:\n{[(card[0], card[1]) for card in dealer_hand]}\nTotal: {calculate_hand_value(dealer_hand)}")
        dealer_total = calculate_hand_value(dealer_hand)

        # Check for dealer blackjack
        if is_blackjack(dealer_hand):
            print("Dealer has a Blackjack!")
            if player_total > 21:
                print("You busted! You lose your bet.")
                player_money -= bet
            elif player_total == 21:
                print("You also have 21! It's a tie.")
            else:
                print(f"You lose! Your total: {player_total} | Dealer's total: {dealer_total}")
                player_money -= bet
            db.write_money_to_file(player_money)  # Update money in the file
            continue

        while dealer_total < 17:
            dealer_hand.append(deck[0].pop())  # Dealer draws from the first suit
            dealer_total = calculate_hand_value(dealer_hand)
            print(f"Dealer draws: {dealer_hand[-1][0]} of {dealer_hand[-1][1]}")
            print(f"Dealer's hand:\n{[(card[0], card[1]) for card in dealer_hand]}\nTotal: {dealer_total}")

            if dealer_total > 21:
                print("Dealer busted! You win your bet.")
                player_money += bet
                db.write_money_to_file(player_money)  # Update money in the file
                continue

        if player_total > dealer_total:
            print(f"You win!\nYour total: {player_total}\nDealer's total: {dealer_total}")
            player_money += bet
        elif player_total < dealer_total:
            print(f"You lose!\nYour total: {player_total}\nDealer's total: {dealer_total}")
            player_money -= bet
        else:
            print(f"It's a tie!\nYour total: {player_total}\nDealer's total: {dealer_total}")

        db.write_money_to_file(player_money)  # Update money after the round

if __name__ == "__main__":
    main()
    
