import random

# Base User class, shared by both Player and Dealer
class User:
    def __init__(self):
        self.playedHands = 0

# Player class, inherits from User
class Player(User):
    def __init__(self):
        super().__init__()
        self.accurateHands = 0  # Tracks correct decisions made

    def say(self, message):
        print(f"[YOU] {message}")

    def get_win_percentage(self):
        return (self.accurateHands / self.playedHands * 100) if self.playedHands > 0 else 0

    def get_stats(self):
        return {
            "played": self.playedHands,
            "correct": self.accurateHands,
            "percentage": self.get_win_percentage()
        }

# Dealer class, inherits from User
class Dealer(User):
    def __init__(self):
        super().__init__()
        self.numberOfDecks = 4  # Default number of decks

    def say(self, message):
        print(f"[DEALER] {message}")

    def set_number_of_decks(self, numberOfDecks):
        self.numberOfDecks = numberOfDecks

# Represents a single Blackjack hand
class BlackJackHand:
    def __init__(self, user):
        self.user = user
        self.cards = []  # List of cards in hand

    def add_card(self, card):
        if card:
            self.cards.append(card)

    def __str__(self):
        return ', '.join(str(card) for card in self.cards)

# Represents an individual playing card
class Card:
    def __init__(self, suit, rank, faceDown=True):
        self.suit = suit
        self.rank = rank
        self.faceDown = faceDown

    def is_face_down(self):
        return self.faceDown

    def turn_face_down(self):
        self.faceDown = True

    def turn_face_up(self):
        self.faceDown = False

    def __str__(self):
        return f"{self.rank} of {self.suit}" if not self.faceDown else "Face Down Card"

# Shoe (collection) of multiple decks of cards
class CardsShoe:
    def __init__(self):
        self.cards = []

    def add_deck(self):
        # Adds a full 52-card deck
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
        for suit in suits:
            for rank in ranks:
                self.cards.append(Card(suit, rank))

    def shuffle_shoe(self):
        random.shuffle(self.cards)

    def deal_card(self, faceDown=False):
        if not self.cards:
            return None
        card = self.cards.pop()
        card.turn_face_down() if faceDown else card.turn_face_up()
        return card

# Refills the shoe when out of cards
def fillEmptyShoe(numberOfDecks, dealer):
    newShoe = CardsShoe()
    dealer.say(f"We are out of cards, I am filling up a new shoe with {numberOfDecks} decks of cards.")
    for _ in range(numberOfDecks):
        newShoe.add_deck()
    dealer.say("I am shuffling the shoe.")
    newShoe.shuffle_shoe()
    dealer.say("The shoe is ready to be used.")
    return newShoe

# Checks if the player's decision is accurate based on basic Blackjack strategy
def is_decision_accurate(playerHand, dealerHand, decision):
    def card_value(card):
        if card.rank in ['Jack', 'Queen', 'King']:
            return 10
        elif card.rank == 'Ace':
            return 11  # initially treat Ace as 11
        else:
            return int(card.rank)

    def hand_value(cards):
        value = sum(card_value(card) for card in cards)
        aces = sum(1 for card in cards if card.rank == 'Ace')
        while value > 21 and aces:
            value -= 10  # count Ace as 1 instead of 11
            aces -= 1
        is_soft = any(card.rank == 'Ace' for card in cards) and value <= 21
        return value, is_soft

    player_total, is_soft = hand_value(playerHand.cards)
    dealer_upcard = dealerHand.cards[0]
    dealer_value = card_value(dealer_upcard)

    # Normalize input
    decision = decision.upper()

    # Basic strategy simplified rules (without splits)
    # These are rules for learning, not 100% complete

    if not is_soft:
        # Hard hands
        if player_total <= 8:
            return decision == 'H'
        elif player_total == 9:
            return decision == 'D' if 3 <= dealer_value <= 6 else decision == 'H'
        elif player_total == 10:
            return decision == 'D' if dealer_value <= 9 else decision == 'H'
        elif player_total == 11:
            return decision == 'D'
        elif player_total == 12:
            return decision == 'H' if dealer_value in [2, 3, 7, 8, 9, 10, 11] else decision == 'S'
        elif 13 <= player_total <= 16:
            return decision == 'S' if 2 <= dealer_value <= 6 else decision == 'H'
        else:  # 17 or more
            return decision == 'S'
    else:
        # Soft hands
        if player_total <= 17:
            return decision == 'H'
        elif player_total == 18:
            return decision == 'S' if dealer_value in [2, 7, 8] else decision == 'H'
        else:  # Soft 19 or more
            return decision == 'S'

# Entry point of the game
def main():
    print("Welcome to Blackjack training!")
    print("This is a text-based version of the game.")

    player = Player()
    dealer = Dealer()

    # Ask user how many decks to use
    dealer.say("How many decks do you want me to use? (1-8)")
    numberOfDecksStr = input("[YOU] ")
    if not numberOfDecksStr.isdigit() or not 1 <= int(numberOfDecksStr) <= 8:
        dealer.say("That's not a valid number of decks, I'll use 4 decks.")
        numberOfDecks = 4
    else:
        numberOfDecks = int(numberOfDecksStr)
    dealer.set_number_of_decks(numberOfDecks)

    cardsShoe = fillEmptyShoe(dealer.numberOfDecks, dealer)

    while True:
        # Refill shoe if not enough cards
        if len(cardsShoe.cards) < 4:
            cardsShoe = fillEmptyShoe(dealer.numberOfDecks, dealer)

        # Deal new hand
        playerHand = BlackJackHand(player)
        dealerHand = BlackJackHand(dealer)

        print("\n--- New Hand ---")

        playerHand.add_card(cardsShoe.deal_card(faceDown=False))
        dealerHand.add_card(cardsShoe.deal_card(faceDown=False))
        playerHand.add_card(cardsShoe.deal_card(faceDown=False))
        dealerHand.add_card(cardsShoe.deal_card(faceDown=True))

        # Show hands
        dealer.say(f"Your hand: {playerHand}")
        dealer.say(f"My hand: {dealerHand.cards[0]} and a face down card.")

        # Player decision
        dealer.say("Do you want to hit (H), stand (S), or double down (D)?")
        playerChoice = input("[YOU] ").strip().upper()

        if playerChoice not in ['H', 'S', 'D']:
            dealer.say("I did not understand you so you will stand.")
            playerChoice = 'S'

        #  Process player's decision
        accurate = is_decision_accurate(playerHand, dealerHand, playerChoice)

        # Update statistics
        player.playedHands += 1
        if accurate:
            player.accurateHands += 1
            dealer.say("Good job! You made the right choice.")
        else:
            dealer.say("Oops! You made the wrong choice.")

        # Show stats
        stats = player.get_stats()
        dealer.say(f"You have played {stats['played']} hands of which {stats['correct']} correctly.")
        dealer.say(f"Your accuracy percentage is: {stats['percentage']:.2f}%")

        # Ask to continue
        dealer.say("Do you want to play again? (Y/N)")
        playAgain = input("[YOU] ").strip().upper()
        if playAgain != 'Y':
            dealer.say("Get out of this place!")
            print("\n--- Final Stats ---")
            dealer.say(f"Final stats: You played {stats['played']} hands of which {stats['correct']} correctly.")
            dealer.say(f"Your final accuracy percentage is: {stats['percentage']:.2f}%")
            print("------------------")
            break
        else:
            dealer.say("Great! Let's play again.")

# Only runs if this file is executed directly
if __name__ == "__main__":
    main()