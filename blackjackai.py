import random

# Global variables
suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8, 'Nine': 9, 'Ten': 10,
          'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}

playing = True


# Card class
class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank]

    def __str__(self):
        return f"{self.rank} of {self.suit}"


# Deck class
class Deck:
    def __init__(self):
        self.deck = []
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        return self.deck.pop()


# Hand class
class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    def add_card(self, card):
        self.cards.append(card)
        self.value += card.value
        if card.rank == 'Ace':
            self.aces += 1

    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1


# Chips class
class Chips:
    def __init__(self):
        self.total = 100
        self.bet = 0

    def win_bet(self):
        self.total += self.bet

    def lose_bet(self):
        self.total -= self.bet


# Functions

def take_bet(chips):
    while True:
        try:
            chips.bet = int(input("How many chips would you like to bet? "))
        except ValueError:
            print("Please enter a valid number of chips.")
        else:
            if chips.bet > chips.total:
                print("Sorry, your bet cannot exceed", chips.total)
            else:
                break


def hit(deck, hand):
    hand.add_card(deck.deal())
    hand.adjust_for_ace()


def hit_or_stand(deck, hand):
    global playing

    while True:
        choice = input("Do you want to Hit or Stand? Enter 'h' or 's': ").lower()

        if choice == 'h':
            hit(deck, hand)
        elif choice == 's':
            print("Player stands. Dealer's turn.")
            playing = False
        else:
            print("Please enter a valid input.")
            continue
        break


def show_some(player, dealer):
    print("\nDealer's Hand:")
    print("<hidden card>")
    print(dealer.cards[1])
    print("\nPlayer's Hand:", *player.cards, sep='\n')


def show_all(player, dealer):
    print("\nDealer's Hand:", *dealer.cards, sep='\n')
    print("Dealer's Hand value:", dealer.value)
    print("\nPlayer's Hand:", *player.cards, sep='\n')
    print("Player's Hand value:", player.value)


def player_busts(player, dealer, chips):
    print("Player busts!")
    chips.lose_bet()


def player_wins(player, dealer, chips):
    print("Player wins!")
    chips.win_bet()


def dealer_busts(player, dealer, chips):
    print("Dealer busts! Player wins!")
    chips.win_bet()


def dealer_wins(player, dealer, chips):
    print("Dealer wins!")
    chips.lose_bet()


def push(player, dealer):
    print("It's a tie! Push.")


# Game logic

while True:
    print("Welcome to Blackjack!")

    # Create and shuffle the deck
    deck = Deck()
    deck.shuffle()

    # Deal two cards to each player
    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())

    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())

    # Set up the player's chips
    player_chips = Chips()

    # Prompt the player for their bet
    take_bet(player_chips)

    # Show the initial hands
    show_some(player_hand, dealer_hand)

    while playing:
        # Prompt the player to Hit or Stand
        hit_or_stand(deck, player_hand)

        # Show the cards, but keep one dealer card hidden
        show_some(player_hand, dealer_hand)

        # Check if player's hand exceeds 21
        if player_hand.value > 21:
            player_busts(player_hand, dealer_hand, player_chips)
            break

    # If the player hasn't busted, play dealer's hand until dealer reaches 17
    if player_hand.value <= 21:
        while dealer_hand.value < 17:
            hit(deck, dealer_hand)

        # Show all cards
        show_all(player_hand, dealer_hand)

        # Check for different winning scenarios
        if dealer_hand.value > 21:
            dealer_busts(player_hand, dealer_hand, player_chips)
        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_hand, dealer_hand, player_chips)
        elif dealer_hand.value < player_hand.value:
            player_wins(player_hand, dealer_hand, player_chips)
        else:
            push(player_hand, dealer_hand)

    # Inform the player of their chip total
    print("Player's chips:", player_chips.total)

    # Ask the player if they want to play again
    play_again = input("Do you want to play again? Enter 'y' or 'n': ")
    if play_again.lower() != 'y':
        break