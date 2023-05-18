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

        # Delete later
        self.gw.show_message(self.__secret_word)

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

        entered_word = self.get_user_guess(self.guess_counter)

        if entered_word == self.__secret_word \
                and self.validate_guess(entered_word):
            self.gw.show_message('You win!')
            self.show_win_animation()

        elif self.guess_counter == 5 and entered_word != self.__secret_word \
                and self.validate_guess(entered_word):
            self.gw.show_message(f'You lose! Word: {self.__secret_word}')
            self.set_square_with_respective_color(entered_word)

        else:
            if self.guess_counter < 5 and self.validate_guess(entered_word):
                self.set_square_with_respective_color(entered_word)
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
        """Checks if word is in the dictionary array, and sets color

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

    def set_square_with_respective_color(self, guess):
        correct_letter_guesses = []

        # i is the index for every letter in word
        for i in range(5):

            # if guess letter is in the same place as the secret word letter
            if guess[i] == self.__secret_word_arr[i]:
                correct_letter_guesses.append(guess[i])

                # set color accordingly
                self.gw.set_square_color(
                    self.guess_counter, i, self.correct_color)
                self.gw.set_key_color(guess[i], self.correct_color)

            # else if guess letter is in the secret word and the number of
            # occurances of the letter are greater in the secret word than
            # the correct guesses array
            elif guess[i] in self.__secret_word_arr and \
                    self.__secret_word_arr.count(guess[i]) > correct_letter_guesses.count(guess[i]):
                correct_letter_guesses.append(guess[i])

                # set color accordingly
                self.gw.set_square_color(
                    self.guess_counter, i, self.present_color)

                # the only time we need to use get_key color is if
                # the letter is present. otherwise, if it is correct
                # we can keep updating at green and if it is incorrect
                # it will never be present

                if self.gw.get_key_color(guess[i]) != self.correct_color:
                    self.gw.set_key_color(guess[i], self.present_color)

            else:
                self.gw.set_square_color(
                    self.guess_counter, i, self.missing_color)
                self.gw.set_key_color(guess[i], self.missing_color)


        # Startup code
if __name__ == "__main__":
    Wordle()
