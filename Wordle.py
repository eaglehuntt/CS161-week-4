#!/usr/bin/python3

"""
Milestones 1 & 2 for Wordle.
"""

import random
import re

from WordleDictionary import FIVE_LETTER_WORDS
from WordleGraphics import WordleGWindow, N_COLS, N_ROWS


class Wordle:

    def __init__(self) -> None:
        self.gw = WordleGWindow()
        self.gw.add_enter_listener(self.enter_action)

        self.correct_color = "#66BB66"
        self.present_color = "#CCBB66"
        self.missing_color = "#999999"

        self.__secret_word = self.get_random_word()
        self.__secret_word_arr = list(self.__secret_word)

        self.guess_counter = 0

        self.current_best_guess = None

        self.accuracy_array_table = {
            "correct": "C",
            "partially": "P",
            "incorrect": "I"
        }

        self.accuracy_percentage_table = {
            self.accuracy_array_table["correct"]: 20,
            self.accuracy_array_table["partially"]: 10,
            self.accuracy_array_table["incorrect"]: 0
        }

        # Delete later
        # self.gw.show_message(self.__secret_word)

    def enter_action(self, s):
        """Events that occur after action. For this case, it gets a user's guess
        then checks if it is in the FIVE_LETTER_WORDS array and displays a
        message

        Args:
            (any?): I am not sure why we need this. I tried removing it but
            I was getting errors. I will ask about this during our next class

        Returns:
            None
        """

        user_guess = self.get_user_guess(self.guess_counter)

        if user_guess == self.__secret_word \
                and self.validate_guess(user_guess):
            self.gw.show_message('You win!')
            self.show_win_animation()

        elif self.guess_counter == 5 and user_guess != self.__secret_word \
                and self.validate_guess(user_guess):
            self.gw.show_message(f'You lose! Word: {self.__secret_word}')

            guess_accuracy = self.get_guess_accuracy(user_guess)
            self.set_square_with_respective_color(
                user_guess, guess_accuracy)

        else:
            if self.guess_counter < 5 and self.validate_guess(user_guess):
                self.update_current_best_guess(user_guess)
                guess_accuracy = self.get_guess_accuracy(user_guess)

                self.set_square_with_respective_color(
                    user_guess, guess_accuracy)
                self.guess_counter += 1
                self.gw.set_current_row(self.guess_counter)

    def show_win_animation(self):
        red = "#FF0000"
        orange = "#FFA500"
        yellow = "#FFFF00"
        green = "#00FF00"
        blue = "#0000FF"
        indigo = "#4B0082"
        violet = "#EE82EE"

        rainbow_array = [self.correct_color, red, orange, yellow,
                         green, blue, indigo, violet, self.correct_color]

        delay = 0

        for col in range(5):
            for color in rainbow_array:
                self.set_square_color_after_delay(delay, col, color)
                delay += 50

    def set_square_color_after_delay(self, delay, col, color):
        self.gw.delay_method_call(delay, lambda col=col: self.gw.set_square_color(
            self.guess_counter, col, color))

    def get_random_word(self):
        """Gets a random word from FIVE_LETTER_WORDS array
        Args:
            None

        Returns:
            (string): Random five letter word
        """
        return random.choice(FIVE_LETTER_WORDS).upper()

    def display_word_in_row(self, word, row):
        """Takes a 5 letter word and displays it in box at a row
        Args:
            (string) word: a five letter word
            (int) row: the row to display the word

        Returns:
            None
        """
        # for each letter at index i, set the box to the letter as upper case
        for i in range(5):
            self.gw.set_square_letter(row, i, word[i].upper())

    def get_user_guess(self, row):
        """Gets user guess from boxes at a row and returns the word

        Args:
            (int) row: The row to get word from

        Returns:
            (string) word: word from boxes
        """
        word_array = []
        for i in range(5):
            word_array.append(self.gw.get_square_letter(row, i))

        return "".join(word_array)

    def validate_guess(self, guess):
        """Checks if word is in the dictionary array

        Args:
            (string) word: a 5 letter word

        Returns:
            None
        """

        if guess.lower() in FIVE_LETTER_WORDS:
            return True

        else:
            self.gw.show_message('Not a valid word')
            return False

    def get_guess_accuracy(self, guess):
        """Gets the accuracy of a guess as an object. The array will contain 
        keys indicating how accurate the letter is relative to the guess.
        """

        correct_letter_guesses = []  # used for logic
        guess_accuracy_array = []  # shadow array to the guess containing keys
        guess_accuracy_percentage = 0

        # guess_accuracy_array key:
        # C = Correct placement
        # P = Partially correct placement
        # I = Incorrect placement

        # i is the index for every letter in word
        for i in range(5):

            # if guess letter is in the same place as the secret word letter
            if guess[i] == self.__secret_word_arr[i]:
                correct_letter_guesses.append(guess[i])

                # add C to array because it is correct
                guess_accuracy_array.append("C")

            # else if the guess letter is in the secret word and the number of
            # occurances of the letter are greater in the secret word than
            # the correct guesses array:
                # this is to prevent duplicates from showing yellow
                # for example, if the word is 'haste' and user guesses
                # 'eaten' only one 'e' will be yellow.

            elif guess[i] in self.__secret_word_arr and \
                    self.__secret_word_arr.count(guess[i]) > correct_letter_guesses.count(guess[i]):
                correct_letter_guesses.append(guess[i])
                guess_accuracy_array.append("P")

            else:
                guess_accuracy_array.append("I")

        # the way we calculate the accuracy percentage is by iterating over
        # the accuracy array and checking the accuracy table for percentage
        # values.

        for i in guess_accuracy_array:
            guess_accuracy_percentage += self.accuracy_percentage_table[i]

        # I am not sure if this is conventional in python, but this is how
        # javascript functions return multiple values from a function.

        return {
            "array": guess_accuracy_array,  # this will be used to color squares
            "percentage": guess_accuracy_percentage,  # percentage
        }

    def update_current_best_guess(self, guess):
        if self.current_best_guess == None:
            self.current_best_guess = guess

        elif self.get_guess_accuracy(guess)["percentage"] > \
                self.get_guess_accuracy(self.current_best_guess)["percentage"]:
            self.current_best_guess = guess

    def set_square_with_respective_color(self, guess, accuracy):
        for i in range(5):
            if accuracy["array"][i] == "C":
                self.gw.set_square_color(
                    self.guess_counter, i, self.correct_color)
                self.gw.set_key_color(guess[i], self.correct_color)
            elif accuracy["array"][i] == "P":
                self.gw.set_square_color(
                    self.guess_counter, i, self.present_color)
                self.gw.set_key_color(guess[i], self.present_color)
            else:
                self.gw.set_square_color(
                    self.guess_counter, i, self.missing_color)
                self.gw.set_key_color(guess[i], self.missing_color)

    def get_all_possible_legal_words(self):
        print(self.current_best_guess)

        # Startup code
if __name__ == "__main__":
    Wordle()
