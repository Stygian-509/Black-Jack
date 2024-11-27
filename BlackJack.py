import random

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

def main():
    deck = create_deck()
    player_hand = [deck[0].pop(), deck[1].pop()]  # Draw from the first two suits
    dealer_hand = [deck[2].pop(), deck[3].pop()]  # Draw from the next two suits

    while True:
        try:
            bet = float(input("Bet amount: "))
            if bet <= 0:
                print("Bet must be a positive number.")
            else:
                break
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    print(f"Your hand:\n{[(card[0], card[1]) for card in player_hand]}\nTotal: {calculate_hand_value(player_hand)}")
    print(f"Dealer's hand:\n[{dealer_hand[0][0]} of {dealer_hand[0][1]}, ?]")

    # Check for player blackjack right away
    if is_blackjack(player_hand):
        print("Blackjack! You win 1.5 times your bet.")
        return round(bet * 1.5, 2)

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
        return -bet

    print(f"Dealer's hand:\n{[(card[0], card[1]) for card in dealer_hand]}\nTotal: {calculate_hand_value(dealer_hand)}")
    dealer_total = calculate_hand_value(dealer_hand)
    
    # Check for dealer blackjack
    if is_blackjack(dealer_hand):
        print("Dealer has a Blackjack!")
        if player_total > 21:
            print("You busted! You lose your bet.")
            return -bet
        elif player_total == 21:
            print("You also have 21! It's a tie.")
            return 0
        else:
            print(f"You lose! Your total: {player_total} | Dealer's total: {dealer_total}")
            return -bet

    while dealer_total < 17:
        dealer_hand.append(deck[0].pop())  # Dealer draws from the first suit
        dealer_total = calculate_hand_value(dealer_hand)
        print(f"Dealer draws: {dealer_hand[-1][0]} of {dealer_hand[-1][1]}")
        print(f"Dealer's hand:\n{[(card[0], card[1]) for card in dealer_hand]}\nTotal: {dealer_total}")

        if dealer_total > 21:
            print("Dealer busted! You win your bet.")
            return bet

    if player_total > dealer_total:
        print(f"You win!\nYour total: {player_total}\nDealer's total: {dealer_total}")
        return bet
    elif player_total < dealer_total:
        print(f"You lose!\nYour total: {player_total}\nDealer's total: {dealer_total}")
        return -bet
    else:
        print(f"It's a tie!\nYour total: {player_total}\nDealer's total: {dealer_total}")
        return 0

if __name__ == "__main__":
    main()
