class WordClassifier:
    def __init__(self, tokens) -> None:
        self.tokens = tokens
        self.word_pairs = self.get_word_pairs()
        self.tag_pairs = self.get_tag_pairs()
    

    def get_word_count(self) -> dict:
        """Return a dictionary matching each word with the number of times it appears in the text file."""
        word_counts = {}
        for (word,_) in self.tokens:
            if word in word_counts:
                word_counts[word] += 1
            else:
                word_counts[word] = 1
        return word_counts
    

    def get_word_pairs(self) -> dict:
        """Return a dictionary matching each word with a dictionary of possible follow up words and their frequency, all based on the given text file."""
        word_pairs = {}
        for _ in range(len(self.tokens)-1):
            curr_token = self.tokens[_]
            next_token = self.tokens[_+1]
            if curr_token not in word_pairs:
                word_pairs[curr_token] = {next_token[0]: (1, next_token[1])}
            else:
                t = word_pairs[curr_token].get(next_token[0], (0, next_token[1]))
                word_pairs[curr_token][next_token[0]] = (t[0]+1, t[1])
        return word_pairs
    

    def get_tag_pairs(self) -> dict:
        """Return a dictionary matching each tag with a dictionary of possible follow up tags and their frequency, all based on the given text file."""
        tag_pairs = {}
        tags = [tag for (_, tag) in self.tokens]
        for _ in range(len(tags)-1):
            curr_tag = tags[_]
            next_tag = tags[_+1]
            if curr_tag in tag_pairs:
                if next_tag in tag_pairs[curr_tag]:
                    tag_pairs[curr_tag][next_tag] += 1
                else:
                    tag_pairs[curr_tag][next_tag] = 1
            else:
                tag_pairs[curr_tag] = {next_tag: 1}
        return tag_pairs
