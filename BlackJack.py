import random

def print_title():
    print("BLACKJACK!")

suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']

card_values = {
    '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 
    'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': [1, 11]
}

def create_deck():
    deck = [(value, suit) for value in values for suit in suits]
    random.shuffle(deck)
    return deck

def calculate_hand_value(hand):
    value = 0
    aces = 0
    for card in hand:
        card_value = card_values[card[0]]
        if card[0] == 'Ace':
            aces += 1
        else:
            value += card_value

    for _ in range(aces):
        if value + 11 <= 21:
            value += 11
        else:
            value += 1
    return value

def main():
    print_title()
    
    deck = create_deck()
    player_hand = [deck.pop(), deck.pop()]
    dealer_hand = [deck.pop(), deck.pop()]

    while True:
        try:
            bet = float(input("Bet amount: "))
            if bet <= 0:
                print("Bet must be a positive number.")
            else:
                break
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    print(f"Your hand:\n{player_hand}\nTotal: {calculate_hand_value(player_hand)}")
    print(f"Dealer's hand:\n[{dealer_hand[0]}, ?]")

    while calculate_hand_value(player_hand) < 21:
        move = input("Hit or stand? (hit/stand): ").lower()
        if move == 'hit':
            player_hand.append(deck.pop())
            print(f"You drew:\n{player_hand[-1]}")
            print(f"Your hand:\n{player_hand}\nTotal: {calculate_hand_value(player_hand)}")
        elif move == 'stand':
            break

    player_total = calculate_hand_value(player_hand)
    if player_total > 21:
        print("You busted! You lose your bet.")
        return -bet

    print(f"Dealer's hand:\n{dealer_hand}\nTotal: {calculate_hand_value(dealer_hand)}")
    dealer_total = calculate_hand_value(dealer_hand)
    
    while dealer_total < 17:
        dealer_hand.append(deck.pop())
        dealer_total = calculate_hand_value(dealer_hand)
        print(f"Dealer draws:\n{dealer_hand[-1]}")
        print(f"Dealer's hand:\n{dealer_hand}\nTotal: {dealer_total}")

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
