from nltk import word_tokenize

class Parser:
    def __init__(self, text_file) -> None:
        """Initialise a parser class to handle the testing text file."""
        self.text_file = text_file
        self.words = self.get_words()
        self.word_pairs = self.get_word_pairs()
        self.word_count = self.get_word_count()
    

    def __repr__(self) -> str:
        """Return the text file as a string."""
        with open(self.text_file, 'r') as f:
            return f.read().lower()


    def get_tokens(self) -> list:
        """Get each individual word from the text file."""
        return word_tokenize(self.__repr__())
    

    def get_words(self) -> set:
        """Get a single copy of each word in the text file."""
        return set(self.get_tokens())


    def get_word_count(self) -> dict:
        """Return a dictionary matching each word with the number of times it appears in the text file."""
        word_counts = {}
        tokens = self.get_tokens()
        for word in tokens:
            if word in word_counts:
                word_counts[word] += 1
            else:
                word_counts[word] = 1
        return word_counts
    

    def get_word_pairs(self) -> dict:
        """Return a dictionary matching each word with a dictionary of possible follow up words and their frequency, all based on the given text file."""
        word_pairs = {}
        tokens = self.get_tokens()
        for _ in range(len(tokens)-1):
            curr_word = tokens[_]
            next_word = tokens[_+1]
            if curr_word in word_pairs:
                if next_word in word_pairs[curr_word]:
                    word_pairs[curr_word][next_word] += 1
                else:
                    word_pairs[curr_word][next_word] = 1
            else:
                word_pairs[curr_word] = {next_word: 1}
        return word_pairs