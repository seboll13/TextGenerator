from nltk import pos_tag
from nltk.tokenize import TweetTokenizer

class Parser:
    def __init__(self, text_file) -> None:
        """Initialise a parser class to handle the testing text file."""
        self.text_file = text_file
        self.tokens = self.get_tokens()
    

    def __repr__(self) -> str:
        """Return the text file as a string."""
        with open(self.text_file, 'r') as f:
            return f.read().lower()


    def get_tokens(self) -> list:
        """Get each individual word from the text file along with its matching tag."""
        tokenizer = TweetTokenizer()
        return pos_tag(tokenizer.tokenize(self.__repr__()))
    

    def get_words(self) -> set:
        """Get a single copy of each word in the text file."""
        return set(self.get_tokens())