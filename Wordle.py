#!/usr/bin/python3

"""
Milestones 1 & 2 for Wordle.
"""

import random
import re  # was going to use this for the cheats, but didn't have time

from WordleDictionary import FIVE_LETTER_WORDS
from WordleGraphics import WordleGWindow, N_COLS, N_ROWS


class Wordle:

    def __init__(self) -> None:
        """Init function. Has important constants

        Args:
            (self) : instance of class

        Returns:
            None

        """
        self.gw = WordleGWindow()
        self.gw.add_enter_listener(self.enter_action)

        self.correct_color = "#66BB66"  # green
        self.present_color = "#CCBB66"  # yellow
        self.missing_color = "#999999"  # grey

        self.__secret_word = self.get_random_word()
        self.__secret_word_arr = list(self.__secret_word)

        # used for a few things, mainly identifying the active row
        self.guess_counter = 0

        self.current_best_guess = None  # will be used for cheats

        # these are units to describe how accurate a guess is relative to the
        # secret word.
        #
        # e.g.
        # secret word = EATEN
        # guess = EERIE
        # accuracy_table will help create -> [C,P,I,I,I]

        self.accuracy_table = {
            "correct": "C",
            "partially": "P",
            "incorrect": "I"
        }

        # will be relevant for cheats. Helps create an accuracy percentage
        self.accuracy_percentage_table = {
            self.accuracy_table["correct"]: 20,
            self.accuracy_table["partially"]: 10,
            self.accuracy_table["incorrect"]: 0
        }

        # display secret word at beginning, for dev purpose but also grading
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
        self.update_game_state(user_guess)

    def update_game_state(self, user_guess):
        """This is the main function. Ultimately it updates the game state but
        to be more specific it:

            1) Checks if the guess is the secret word, and if so displays a win
            animation

            2) If the user has guessed 5 times and hasn't guessed correctly 
            a lose screen will show up

            3) Sets the current row and gets the guess accuracy. 

            4) Ensures user input is a valid word and displays correct error 
            message if it isn't the dictionary

            5) Working on adding cheats when enter is pressed.
        """

        # if user's guess is the secret word
        if user_guess == self.__secret_word \
                and self.validate_guess(user_guess):
            self.gw.show_message('You win!')
            self.show_win_animation()

        # else if we made it to 5 guesses and user hasn't guessed correctly
        elif self.guess_counter == 5 and user_guess != self.__secret_word \
                and self.validate_guess(user_guess):
            self.gw.show_message(f'You lose! Word: {self.__secret_word}')

            guess_accuracy = self.get_guess_accuracy(user_guess)
            self.set_square_with_respective_color(
                user_guess, guess_accuracy)

        # else the game is still running
        else:

            # basic codepath for guesses 1-5.
            if self.guess_counter < 5 and self.validate_guess(user_guess):
                self.update_current_best_guess(user_guess)
                guess_accuracy = self.get_guess_accuracy(user_guess)
                self.set_square_with_respective_color(
                    user_guess, guess_accuracy)
                self.guess_counter += 1
                self.gw.set_current_row(self.guess_counter)

            # if we get here, that means guess was not valid.
            else:

                # logic for cheat functionality
                all_empty = True

                for i in range(5):
                    if self.gw.get_square_letter(self.guess_counter, i) == " ":
                        all_empty = True
                    else:
                        all_empty = False

                if all_empty:
                    self.gw.show_message("Cheats activated. Check console.")
                    self.get_all_possible_legal_words()

                else:
                    self.gw.show_message("Not a valid word")

    def show_win_animation(self):
        """Shows win animation

        Args:
            (self)

        Returns:
            None
        """
        red = "#FF0000"
        orange = "#FFA500"
        yellow = "#FFFF00"
        green = "#00FF00"
        blue = "#0000FF"
        indigo = "#4B0082"
        violet = "#EE82EE"

        # order colors will show
        rainbow_array = [self.correct_color, red, orange, yellow,
                         green, blue, indigo, violet, self.correct_color]

        delay = 0  # initialize delay as 0. this will change

        # play animation in for loop
        for col in range(5):
            for color in rainbow_array:
                self.set_square_color_after_delay(delay, col, color)
                delay += 50

    def set_square_color_after_delay(self, delay, col, color):
        """This is a wrapper used to call the delay_method_call method I added
        to the Wordle object. 

        Args:
            self
            (int) delay: delay in ms for method call to be delayed
            (int) col: the column to update
            (string) color: the color to set the square to

        Returns:
            None
        """

        self.gw.delay_method_call(delay, lambda col=col: self.gw.set_square_color(
            self.guess_counter, col, color))

    def get_random_word(self):
        """Gets a random word from FIVE_LETTER_WORDS array
        Args:
            self

        Returns:
            (string): Random five letter word
        """
        return random.choice(FIVE_LETTER_WORDS).upper()

    def display_word_in_row(self, word, row):
        """Takes a 5 letter word and displays it in box at a row
        Args:
            self
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
            self
            (int) row: The row to get word from

        Returns:
            (string) word: word from boxes
        """
        word_array = []
        for i in range(5):
            word_array.append(self.gw.get_square_letter(row, i))

        return "".join(word_array)

    def validate_guess(self, guess):
        """Checks if word is in the wordle dictionary array

        Args:
            self
            (string) word: a 5 letter word

        Returns:
            (bool): if guess in FIVE_LETTER_WORDS
        """
        return guess.lower() in FIVE_LETTER_WORDS

    def get_guess_accuracy(self, guess):
        """Gets the accuracy of a guess as an object. The array will contain 
        keys indicating how accurate the letter is relative to the guess. The
        percentage is used to determine the 'best guess' 

        Args:
            (string) guess: a word

        Returns:
            (dict)
                {
                    (list) "array" : an array containing keys of accuracy
                    (int) "percentage" : how accurate the guess is / 100
                }
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
            if guess[i] == self.__secret_word_arr[i]:
                correct_letter_guesses.append(guess[i])
                guess_accuracy_array.append(
                    self.accuracy_table["correct"])

            elif guess[i] in self.__secret_word_arr:
                if self.__secret_word_arr.count(guess[i]) > correct_letter_guesses.count(guess[i]):
                    correct_letter_guesses.append(guess[i])
                    guess_accuracy_array.append(
                        self.accuracy_table["partially"])
                else:
                    guess_accuracy_array.append(
                        self.accuracy_table["incorrect"])

            else:
                guess_accuracy_array.append(
                    self.accuracy_table["incorrect"])

        for i in guess_accuracy_array:
            guess_accuracy_percentage += self.accuracy_percentage_table[i]

        return {
            "array": guess_accuracy_array,
            "percentage": guess_accuracy_percentage,
        }

    def update_current_best_guess(self, guess):
        """Updates the best guess

        Args:
            self
            (string) guess: user's guess
        """
        if self.current_best_guess == None:
            self.current_best_guess = guess

        elif self.get_guess_accuracy(guess)["percentage"] > \
                self.get_guess_accuracy(self.current_best_guess)["percentage"]:
            self.current_best_guess = guess

    def set_square_with_respective_color(self, guess, accuracy):
        """Takes a guess and updates the active row with the colors that 
        represent the accuracy.

        Args:
            self
            (string) guess: user's guess
            (dict) accuracy: object containing an array and an accuracy percent

        Returns:
            None
        """
        for i in range(5):
            if accuracy["array"][i] == self.accuracy_table["correct"]:
                self.gw.set_square_color(
                    self.guess_counter, i, self.correct_color)

                if self.gw.get_key_color(guess[i]) != self.correct_color:
                    self.gw.set_key_color(guess[i], self.correct_color)

            elif accuracy["array"][i] == self.accuracy_table["partially"]:
                self.gw.set_square_color(
                    self.guess_counter, i, self.present_color)

                if self.gw.get_key_color(guess[i]) not in [self.correct_color, self.present_color]:
                    self.gw.set_key_color(guess[i], self.present_color)

            else:
                self.gw.set_square_color(
                    self.guess_counter, i, self.missing_color)

                if self.gw.get_key_color(guess[i]) not in [self.correct_color, self.present_color, self.missing_color]:
                    self.gw.set_key_color(guess[i], self.missing_color)

    def get_all_possible_legal_words(self):
        """Cheats for add ons not yet done.
        Args:
            self

        Returns:
            None
        """
        print(f'Your closest guess: {self.current_best_guess}')
        print('Here are the possible answers based on what you know so far:')

        # Startup code
if __name__ == "__main__":
    Wordle()
