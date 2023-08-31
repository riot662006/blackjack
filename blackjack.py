import os
import random
import time

class art:
    logo = r"""
    .------.            _     _            _    _            _    
    |A_  _ |.          | |   | |          | |  (_)          | |   
    |( \/ ).-----.     | |__ | | __ _  ___| | ___  __ _  ___| | __
    | \  /|K /\  |     | '_ \| |/ _` |/ __| |/ / |/ _` |/ __| |/ /
    |  \/ | /  \ |     | |_) | | (_| | (__|   <| | (_| | (__|   < 
    `-----| \  / |     |_.__/|_|\__,_|\___|_|\_\ |\__,_|\___|_|\_\
          |  \/ K|                            _/ |                
          `------'                           |__/           
    """


    card = """ _______ 
|XX     |
|       |
|   Y   |
|       |
|       |
|_____XX|
"""

    face_down = r""" _______ 
|/// \\\|
|\\\ ///|
|<<<|>>>|
|/// \\\|
|\\\ ///|
|_______|
"""

class Card:
    suits = ["♥", "♦", "♠", "♣"]

    def __init__(self, num, shape_index, face_down=False):
        self.card_art = None

        assert 1 <= num <= 13, "card number \
        must be between 1 and 13 inclusive"
        assert 0 <= shape_index <= 4, "card shape index \
        must be between 0 and 3 inclusive"

        self.num = num
        self.shape_index = shape_index
        self.suit = Card.suits[shape_index]

        self.face_down = face_down
        self.card_art = self.display()

    def display(self):
        if self.face_down: return art.face_down.splitlines()
        if self.card_art is not None: return self.card_art
        num = {1: "A", 11: "J", 12: "Q", 13: "K"}.get(self.num, str(self.num))
        card_art = art.card.splitlines()

        card_art[1] = card_art[1].replace("XX", num.ljust(2))
        card_art[3] = card_art[3].replace("Y", self.suit)
        card_art[6] = card_art[6].replace("XX", num.rjust(2, "_"))

        return card_art

    def __str__(self, *, art=False):
        if art:
            return "\n".join(self.card_art)
        if self.face_down:
            return "a mystery card"
        num = {1: "Ace of", 11: "Jack of", 12: "Queen of", 13: "King of"}.get(self.num, str(self.num))
        suit = ["Hearts", "Diamonds", "Spades", "Clubs"][self.shape_index]

        return num + " " + suit

    def __lt__(self, other): return self.num < other.num

    def __gt__(self, other): return self.num > other.num

    def __eq__(self, other): return self.num == other.num


class Deck(list):
    @staticmethod
    def generate_full_deck():
        deck = Deck()
        card_args = [(i, j) for i in range(1, 14) for j in range(4)]
        random.shuffle(card_args)
        for args in card_args:
            deck.append(Card(*args))
        return deck

    def __init__(self, *args):
        if not args:
            super().__init__(self)
        else:
            card_list = []
            for i in args:
                if "__iter__" in dir(i):
                    card_list.append(Card(*i))
                elif isinstance(i, Card):
                    card_list.append(i)
                else:
                    card_list.append(Card(i))
            super().__init__(self)
            self += card_list

    def display_hand(self, start=0, end=-1, step=1):
        hand = [""] * 7
        for card in self[start:end:step]:
            for i in range(7):
                hand[i] += card.display()[i] + " "

        return "\n".join(hand)

    def pick_card(self, deck, n=1):
        for _ in range(n):
            card = deck.pop(0)
            self.append(card)

    def __str__(self):
        if len(self) == 0:
            return "EMPTY"
        final_display = ['']
        for i in range(len(self[::10])):
            final_display += [self.display_hand(i * 10, i * 10 + 10)]
        return "\n".join(final_display)

    def shuffle(self):
        random.shuffle(self)

    def place_card(self, i, deck):
        card = self.pop(i)
        deck.append(card)

    def liquidate(self, deck):
        while len(self):
            deck.append(self.pop(0))


os.system("cls")


def print_error(msg):
    print(f"\033[31m{msg}\033[0m")


def int_input(msg, input_min=0, input_max=None):
    while True:
        try:
            user_input = input(msg)
            if "." in user_input:
                print_error("Input must be a whole number.")
            else:
                integer = int(user_input)
                if integer < input_min:
                    print_error(f"Input must not be below {input_min}")
                elif input_max is not None and integer > input_max:
                    print_error(f"Input must not exceed {input_max}")
                else:
                    return integer
        except ValueError:
            print_error("Invalid input.")


def input_from_choice(msg, choices={"y": ('yes',), "n": ('no',)}):
    choice_dict = {opt: i for i, choice in choices.items() for opt in choice}

    while True:
        user_input = input(msg).lower()

        if user_input in choice_dict:
            return choice_dict[user_input]
        elif user_input in choices:
            return user_input

        print_error("Invalid input")


def hand_value(hand):
    value = 0
    aces = []

    for card in hand:
        if card.num == 1:
            aces.append(card)
        else:
            value += min(card.num, 10)
    if aces:
        value += len(aces) - 1
        value += 11 if value + 11 <= 21 else 1

    return value


def dealer_turn(dealer, hand, deck):

    while hand_value(dealer) < 17:
        print(f"Dealer picked the {deck[0]}")
        dealer.pick_card(deck)
        print("Dealer cards: ", dealer)
        time.sleep(2)
        if hand_value(hand) < hand_value(dealer) < 21:
            return hand_value(dealer)

    else:
        return hand_value(dealer)


def main(first, cur_round=0, cash=0 , bid=0 , deck=None):
    if first:
        print("*Shuffling deck*...*Generating dealers*")
        time.sleep(1)
        print(art.logo)
        print("Welcome to the blackjack simulator")

        deck = Deck.generate_full_deck()
        deck.shuffle()

        cash = int_input("What amount of money did you come with today (must be at least $50): $", 50)
        bid = int_input(f"How much is at stake for each round (must be at least $5): $", 5, cash)
        cur_round = 1

        print("Let's begin!!!")
        time.sleep(1)

    os.system("cls")

    print(f"----ROUND {cur_round}----")
    print(f"You have paid entry fee (${bid})")

    cash -= bid
    pot = bid * 2

    hand = Deck()
    dealer = Deck()
    hand.pick_card(deck, 2)
    print(f"You are dealt the", deck[0], "and", deck[1], hand)

    time.sleep(1)

    dealer.pick_card(deck, 2)
    dealer[1].face_down = True

    print(f"The dealer deals the", deck[2], "and another card", dealer)
    time.sleep(1.5)

    user_choice = {"h": ["hit"], "s": ["stand"], "d": ["double", "double down", "doubledown"]}

    while True:
        print(f"\nCurrent balance: ${cash}")
        print(f"Pot: ${pot}")
        print("\nCurrent hand:", hand)
        if hand_value(hand) >= 21:
            break

        print("\nWould you like to do?")

        while True:
            user_input = input_from_choice("Hit[h]   Stand[s]  Double-down[d] => ", user_choice)
            if user_input == "d" and cash < bid:
                print_error("You do not have enough cash to double down")
            else:
                break

        if user_input == "d":
            cash -= bid
            pot *= 2
            print(f"You have just double-downed. The pot value has increased to {pot}")
            time.sleep(2)

        if user_input != "s":
            print(f"You picked the {deck[0]} from the deck")
            print(deck[0].__str__(art=True))
            hand.pick_card(deck)
            time.sleep(1.5)
            os.system("cls")
            if hand_value(hand) >= 21:
                continue

        if user_input != "h":
            os.system("cls")
            print(f"\nCurrent balance: ${cash}")
            print(f"Pot: ${pot}")
            print("\nCurrent hand:", hand)
            print(f"You stand. Your card value currently at {hand_value(hand)}")
            time.sleep(1.5)

            break
    if hand_value(hand) > 21:
        print_error(f"You bust.=(. The dealer won ${pot}")
    elif hand_value(hand) == 21:
        print(f"\033[32mBlackjack!!! You win ${pot}\033[0m")
        cash += pot
        print(f"\nCurrent balance: ${cash}")
    else:
        time.sleep(1)

        os.system("cls")

        dealer[1].face_down = False
        print(f"\nDealer reveals his second card as the {dealer[1]}", dealer)
        time.sleep(2)

        if hand_value(hand) >= hand_value(dealer):
            os.system("cls")

            print(f"\nPlayer balance: ${cash}\t\tPlayer Value: {hand_value(hand)}")
            print("\n\nDealer's turn: ")
            time.sleep(1)

            dealer_value = dealer_turn(dealer, hand, deck)
        else:
            dealer_value = hand_value(dealer)
        if hand_value(hand) < dealer_value < 21:
            print_error(f"Dealer wins with a value of {dealer_value}. The dealer won ${pot}")
            cash -= pot
        elif hand_value(hand) > dealer_value:
            print(f"\033[32mDealer stands at {dealer_value}. You win ${pot}\033[0m")
        elif hand_value(hand) == dealer_value:
            print(f"\033[33mDealer stands at {dealer_value}. It's a draw. You get ${pot // 2}\033[0m")
            cash -= pot // 2
        elif dealer_value == 21:
            print_error(f"Dealer got a blackjack.=(. The dealer won ${pot}")
            cash -= pot
        else:
            print(f"\033[32mDealer bust. You win ${pot}\033[0m")
        cash += pot

    print(f"Current balance: ${cash}")

    time.sleep(1)
    if cash < bid:
        print_error(f"You cannot afford to play the next round. You leave with ${cash}. Better luck next time.")
    else:
        print(f"Do you wish to keep playing or are you content with ${cash}?")
        user_input = input_from_choice("Play[p]\tLeave[l] => ", {"p":["play",], "l":["leave", "exit"]})
        if user_input == "p":
            hand.liquidate(deck)
            dealer.liquidate(deck)
            main(False, cur_round+1, cash, bid, deck)
        else:
            print(f"You leave with ${cash}. Bye!")

main(True)
