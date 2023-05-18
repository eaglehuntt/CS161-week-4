#!/usr/bin/python3

"""
Milestones 1 & 2 for Wordle.
"""

import random

from WordleDictionary import FIVE_LETTER_WORDS
from WordleGraphics import WordleGWindow, N_COLS, N_ROWS


class wordle:

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
                and self.validate_guess_and_color_squares(entered_word):
            self.gw.show_message('You win!')
        elif self.guess_counter == 5 and entered_word != self.__secret_word \
                and self.validate_guess_and_color_squares(entered_word):
            self.gw.show_message(f'You lose! Word: {self.__secret_word}')

        if self.guess_counter < 5 and self.validate_guess_and_color_squares(entered_word):
            self.guess_counter += 1
            self.gw.set_current_row(self.guess_counter)

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

    # def color_keys(self):

    def validate_guess_and_color_squares(self, guess):
        """Checks if word is in the dictionary array, and sets color

        Args:
            (string) word: a 5 letter word

        Returns:
            None
        """
        print(guess, self.__secret_word)

        if guess.lower() in FIVE_LETTER_WORDS:

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

            return True

        else:
            self.gw.show_message('Not a valid word')
            return False


# Startup code
if __name__ == "__main__":
    wordle()
