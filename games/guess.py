import random


def create_game():

    return random.randint(1, 100)


def check(number, guess):

    if guess == number:
        return "win"

    if guess < number:
        return "higher"

    return "lower"