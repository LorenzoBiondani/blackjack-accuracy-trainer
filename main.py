import random

class User ():
  def __init__(self):
    self.playedHands = 0

class Player (User):
  def __init__(self):
    super().__init__()
    self.accurateHands = 0
  def say(self, message):
    print(f"[YOU] {message}")
  def get_win_percentage(self):
    return (self.accurateHands / self.playedHands * 100) if self.playedHands > 0 else 0 
  def get_stats(self):
    return 0; #TODO

class Dealer (User):
  def __init__(self):
    super().__init__()
    self.numberOfDecks = 4
  def say(self, message):
    print(f"[DEALER] {message}")
  def set_number_of_decks(self, numberOfDecks):
    self.numberOfDecks = numberOfDecks

class BlackJackHand():
  def __init__(self, user):
    self.user = user
    self.cards = []
    self.value = 0
    self.isBlackJack = False
  def add_card(self, card):
    if card:
      self.cards.append(card)
  def __str__(self):
    return ', '.join(str(card) for card in self.cards)

class Card():
  def __init__(self, suit, rank, faceDown=True):
    self.suit = suit
    self.rank = rank
    self.faceDown = faceDown
  def get_value(self):
    if self.faceDown:
      # Throw an exception
      return Exception("[SYSTEM] Card is face down, cannot read its value.")
    if self.rank in ['Jack', 'Queen', 'King']:
      return 10
    elif self.rank == 'Ace':
      return 11  # Ace can also be 1, but we'll handle that in the hand logic
    else:
      return int(self.rank)
  def is_face_down(self):
    return self.faceDown
  def turn_face_down(self):
    self.faceDown = True
  def turn_face_up(self):
    self.faceDown = False
  def __str__(self):
    return f"{self.rank} of {self.suit}"

class CardsShoe():
  def __init__(self):
    self.cards = []
  def add_deck(self):
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
    for suit in suits:
      for rank in ranks:
        self.cards.append(Card(suit, rank))
  def shuffle_shoe(self):
    random.shuffle(self.cards)
  def deal_card(self, faceDown=False):
    poppedCard = self.cards.pop()
    if poppedCard:
      if faceDown:
        poppedCard.turn_face_down()
      else:
        poppedCard.turn_face_up()
      return poppedCard;
    else:
      print("[SYSTEM] No more cards in the shoe, cannot deal a card.")

    return 
  
def fillEmptyShoe(numberOfDecks, dealer):
  newShoe = CardsShoe()
  dealer.say("We are out of cards, I am filling up a new shue with " + str(numberOfDecks) + " decks of cards.")
  for _ in range(numberOfDecks):
    newShoe.add_deck()
  dealer.say("I am shuffling the shoe.")
  newShoe.shuffle_shoe()
  dealer.say("The shoe is ready to be used.")
  return newShoe

# main
def main():
  print("Welcome to Blackjack training!")
  print("This is a text-based version of the game.")
  print("You will play against the dealer.")

  # Create player and dealer instances
  player = Player()
  dealer = Dealer()

  # Prompt user for number of decks
  dealer.say("How many decks do you want me to use? (1-8)")
  numberOfDecksStr = input("[YOU] ")
  if not numberOfDecksStr.isdigit() or int(numberOfDecksStr) < 1 or int(numberOfDecksStr) > 8:
    dealer.say("That's not a valid number of decks, I'll use 4 decks.")
    numberOfDecks = 4
  else:
    numberOfDecks = int(numberOfDecksStr)
  dealer.set_number_of_decks(numberOfDecks)

  # Initialize an empty shoe of cards
  cardsShoe = CardsShoe()
  wantsToPlay = True

  # Game loop
  while  wantsToPlay:

    # If we don't have enough cards in the shoe for the next round, fill it up
    if len(cardsShoe.cards) < 4:
      cardsShoe = fillEmptyShoe(dealer.numberOfDecks, dealer)
    
    # Create hands for player and dealer
    playerHand = BlackJackHand(player)
    dealerHand = BlackJackHand(dealer)

    print("\n--- New Hand ---")

    # Deal player card faceup
    playerHand.add_card(cardsShoe.deal_card(faceDown=False))
    # Deal dealer card faceup
    dealerHand.add_card(cardsShoe.deal_card(faceDown=False))
    # Deal player card faceup
    playerHand.add_card(cardsShoe.deal_card(faceDown=False))
    # Deal dealer card facedown
    dealerHand.add_card(cardsShoe.deal_card(faceDown=True))

    # Show player and dealer hands
    dealer.say("Your hand: " + str(playerHand))
    dealer.say("My hand: " + str(dealerHand.cards[0]) + " and a face down card.")

    # Aks player if they want to hit, stand, or double down
    dealer.say("Do you want to hit (H), stand (S), or double down (D)?")
    playerChoice = input("[YOU] ").strip().upper()

    if playerChoice not in ['H', 'S', 'D']:
      dealer.say("I did not understand you so you will stand.")
      playerChoice = 'S'

    # Check if the player's choice is correct
    # TODO

    accurate = True  # Placeholder for actual game logic to determine if the player's choice was correct

    player.playedHands += 1
    if accurate:
      player.accurateHands += 1
      dealer.say("Good job! You made the right choice.")
    else:
      dealer.say("Oops! You made the wrong choice.")

    # Show current stats
    dealer.say(f"You have played {player.playedHands} hands of which {player.accurateHands} correctly.")
    dealer.say(f"Your accuracy percentage is: {player.get_win_percentage():.2f}%")

    # Ask player if they want to play again
    dealer.say("Do you want to play again? (Y/N)")
    playAgain = input("[YOU] ").strip().upper()
    if playAgain != 'Y':
      wantsToPlay = False
      dealer.say("Get out of this place!")

      # Show final stats
      print("\n--- Final Stats ---")
      dealer.say(f"Final stats: You played {player.playedHands} hands of which {player.accurateHands} correctly.")
      dealer.say(f"Your final accuracy percentage is: {player.get_win_percentage():.2f}%")
      print("------------------")
      break
    else:
      dealer.say("Great! Let's play again.")

if __name__ == "__main__":
  main()