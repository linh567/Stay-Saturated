import random
import sys

# Player class to represent a player in the game
class Player:
    def __init__(self, hand, name):
        self.name = name
        self.vf = hand[0] # Vapor pressure of the liquid phase at the player's position
        self.vg = hand[-1] # Vapor pressure of the vapor phase at the player's position.
        self.critical_point = hand[2] # The middle value of the hand
        self.two_phase_low = hand[1] # The lower bound of the two-phase region
        self.two_phase_high = hand[3] # The upper bound of the two-phase region
        self.score = 0

    def add_score(self, score):
        self.score += score

    def __str__(self):
        return f"{self.name} has a score of {self.score}"


class Queue:
    def __init__(self):
        self.items = []

    def enqueue(self, item):
        self.items.append(item)

    def dequeue(self):
        if len(self.items) > 0:
            return self.items.pop(0)
        else:
            return None 

    def is_empty(self):
        return len(self.items) == 0


# Game class to manage the game's rules and logic. Includes shuffling, hand generation, and card sorting
class Game:
    def __init__(self):
        self.hand1 = []  # Hand 1 for the player
        self.hand2 = []  # Hand 2 for the computer

    #Shuffles a given list of cards and returns a shuffled queue
    def shuffle(self, card_list):
        shuffled = Queue()
        random.shuffle(card_list)
        for card in card_list:
            shuffled.enqueue(card)
        return shuffled

    #Generates two hands with the specified number of cards, ensuring at least one card from vf and one from vg.
    def generate_hand(self, vf, vg, vf_and_vg, num_cards):
        self.hand1 = [vf.dequeue(), vg.dequeue()]  # Dequeue one card from vf and vg for hand 1
        self.hand2 = [vf.dequeue(), vg.dequeue()]  # Dequeue one card from vf and vg for hand 2

        # Fill both hands to the specified number of cards
        while len(self.hand1) < num_cards:
            card = vf_and_vg.dequeue()
            if card not in self.hand1:  # Avoid duplicates in hand1
                self.hand1.append(card)

        while len(self.hand2) < num_cards:
            card = vf_and_vg.dequeue()
            if card not in self.hand2:  # Avoid duplicates in hand2
                self.hand2.append(card)

        return self.hand1, self.hand2

    def bubble_sort(self, sorted_cards):
        n = len(sorted_cards)
        for i in range(n):
            swapped = False
            for j in range(0, n - i - 1):
                if sorted_cards[j] > sorted_cards[j + 1]:
                    sorted_cards[j], sorted_cards[j + 1] = sorted_cards[j + 1], sorted_cards[j]
                    swapped = True
            if not swapped:
                break
        return sorted_cards
    # Sorts both hands using the bubble sort algorithm
    def card_sort(self):
        self.hand1 = self.bubble_sort(self.hand1)
        self.hand2 = self.bubble_sort(self.hand2)
        return self.hand1, self.hand2


# Main game loop
def main():
    """
    The main function to run the game, handling user input, card drawing, and scoring.
    """
    vf = []
    vg = []  
    values = []
    file_path = "C:/Users/Annie/Downloads/data.txt"  # Insert your own file path

    # Read the data from the file
    with open(file_path, "r") as file:
        lines = file.readlines()
    for line in lines:
        l = line.strip().split(",")
        vf.append((l[2]))  # Specific volume liquid at index 2
        vg.append((l[3]))  # Specific volume vapor at index 3
   
    game = Game()

    print("Welcome to Stay Saturated!")
    user_name = input("What's your name? ")
    print(f"Let's play {user_name}!")

    # Shuffle the decks
    vf_and_vg = game.shuffle(vf + vg)
    vf = game.shuffle(vf)
    vg = game.shuffle(vg)

    # Generate hands and sort them
    hand1, hand2 = game.generate_hand(vf, vg, vf_and_vg, 5)
    user_hand, comp_hand = game.card_sort()
  
    # Instantiate players
    user = Player(user_hand, user_name)
    computer = Player(comp_hand, "bot")

    while True:
        print()
        print(f"Your vapor dome is:")
        print(f"   Vf: {user.vf}")
        print(f"   Two-phase low: {user.two_phase_low}")
        print(f"   Critical point: {user.critical_point}")
        print(f"   Two-phase high: {user.two_phase_high}")
        print(f"   Vg: {user.vg}")
        print()
        
        # Ask if the user wants to draw a card
        draw_card = input("Would you like to draw a card? (Yes or No): ")
        print()

        if draw_card.lower() == "yes":
            player_card = vf_and_vg.dequeue()
            computer_card = vf_and_vg.dequeue()
            print(f"   You drew: {player_card}")
            print(f"   The computer drew: {computer_card}")
            print()

            # Scoring logic based on cards drawn
            if user.two_phase_low < player_card < user.two_phase_high:
                user.add_score(10)
                print(f'   Your current score is {user.score}')
                print(f"   The computer's current score is {computer.score}")
            if computer.two_phase_low < computer_card < computer.two_phase_high:
                computer.add_score(10)
            if user.vf < player_card < user.two_phase_low or user.two_phase_high < player_card < user.vg:
                user.add_score(5)
                print(f'   Your current score is {user.score}')
                print(f"   The computer's current score is {computer.score}")
            if computer.vf < computer_card < computer.two_phase_low or computer.two_phase_high < computer_card < computer.vg:
                user.add_score(5)

            # End the game if the card is outside the vapor dome
            if computer_card < computer.vf or computer_card > computer.vg:
                print(f'   {computer_card} is outside the vapor dome.')
                print(f'   Your final score is {user.score}')
                print(f"   The computer's final score is {computer.score}")
                if user.score > computer.score:
                    print("   You won!")
                else:
                    print("   You lost!")
                break
            else:
                print(f'   {player_card} is outside the vapor dome. You are not saturated ')
                print(f'   Your final score is {user.score}')
                print(f"   The computer's final score is {computer.score}")
                if user.score > computer.score:
                    print("   You won!")
                else:
                    print("   You lost!")
                break

        # End the game if the player doesn't draw a card
        else:
            print(f"   Your score is: {user.score}")
            print(f"   The computer's score is {computer.score}")

            if user.score > computer.score:
                print("You won!")
            else:
                print("You lost!")
            break
    print()

if __name__ == "__main__":
    main()
