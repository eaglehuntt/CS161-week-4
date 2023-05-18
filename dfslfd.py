
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
