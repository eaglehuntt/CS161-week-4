
def wordle():
    def get_random_word():
        """Gets a random word from FIVE_LETTER_WORDS array
        Args:
            None

        Returns:
            (string): Random five letter word
        """
        return random.choice(FIVE_LETTER_WORDS)

    def enter_action(s):
        """Events that occur after action. For this case, it gets a user's guess
        then checks if it is in the FIVE_LETTER_WORDS array and displays a
        message

        Args:
            (any?): I am not sure why we need this. I tried removing it but 
            I was getting errors. I will ask about this during our next class

        Returns:
            None
        """
        entered_word = get_user_guess(0)
        # milestone_2(entered_word)
        milestone_3(entered_word)

    def milestone_1(word, row):
        """Takes a 5 letter word and displays it in box at a row
        Args:
            (string) word: a five letter word
            (int) row: the row to display the word

        Returns:
            None
        """
        # for each letter at index i, set the box to the letter as upper case
        for i in range(5):
            gw.set_square_letter(row, i, word[i].upper())

    def get_user_guess(row):
        """Gets user guess from boxes at a row and returns the word

        Args:
            (int) row: The row to get word from

        Returns:
            (string) word: word from boxes
        """
        word_array = []
        for i in range(5):
            word_array.append(gw.get_square_letter(row, i))

        return "".join(word_array)

    def milestone_2(word):
        """Checks if word is in the array, and display message

        Args:
            (string) word: a 5 letter word

        Returns:
            None
        """
        if word.lower() in FIVE_LETTER_WORDS:
            gw.show_message('That is a word!')
        else:
            gw.show_message('Not in word list')

    def milestone_3(word):
        """Checks if word is in the array, and display message

        Args:
            (string) word: a 5 letter word

        Returns:
            None
        """
        if word.lower() in FIVE_LETTER_WORDS:
            word = list(word)
            print(word)
        else:
            gw.show_message('Not in word list')

    gw = WordleGWindow()
    gw.add_enter_listener(enter_action)
    milestone_1(get_random_word(), 1)


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
            guess_accuracy_array.append(
                self.accuracy_array_table["correct"])

        # else if the guess letter is in the secret word and the number of
        # occurances of the letter are greater in the secret word than
        # the correct guesses array:
            # this is to prevent duplicates from showing yellow
            # for example, if the word is 'haste' and user guesses
            # 'eaten' only one 'e' will be yellow.

        elif guess[i] in self.__secret_word_arr and \
                self.__secret_word_arr.count(guess[i]) > correct_letter_guesses.count(guess[i]):
            correct_letter_guesses.append(guess[i])
            guess_accuracy_array.append(
                self.accuracy_array_table["partially"])

        else:
            guess_accuracy_array.append(
                self.accuracy_array_table["incorrect"])

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
