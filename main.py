import networkx as nx
from numpy.random import choice
from nltk import word_tokenize


class Parser:
    def __init__(self, text_file) -> None:
        """Initialise a parser class to handle the testing text file."""
        self.text_file = text_file
        self.words = self.get_words()
        self.word_count = self.get_word_count()
        self.transition_probabilities = self.compute_transition_probabilities()
    

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


    def compute_transition_probabilities(self) -> dict:
        """Return a dictionary matching the transition probabilities between each pair of words."""
        probs = {}
        tokens = self.get_tokens()
        # Get count
        for _ in range(len(tokens)-1):
            curr_word = tokens[_]
            next_word = tokens[_+1]
            if (curr_word, next_word) in probs:
                probs[(curr_word, next_word)] += 1
            else:
                probs[(curr_word, next_word)] = 1
        # Normalize
        for curr, next in probs:
            probs[(curr, next)] /= self.word_count[curr]
        return probs


    def create_graph(self) -> nx.DiGraph:
        """Create a directed graph from the transition probabilities."""
        G = nx.DiGraph()
        G.add_nodes_from(words)
        for curr, next in self.transition_probabilities:
            G.add_edge(curr, next, weight=self.transition_probabilities[(curr, next)])
        return G
    

    def normalise(self, weights) -> list:
        """Safety check"""
        return [w/sum(weights) for w in weights]


    def random_walk(self, G, start) -> list:
        """Generate a random walk from the graph."""
        path = [start]
        n = 0
        while path[-1] not in ['.', '!', '?']:
            neighbours = list(G.neighbors(path[-1]))
            if len(neighbours) == 0:
                break
            weights = [G[path[-1]][n]['weight'] for n in neighbours]
            path.append(choice(neighbours, p=self.normalise(weights)))
            n += 1
        return path


    def generate_text(self, start_word) -> str:
        """Generate a random text from the graph."""
        start_word = start_word.lower()
        path = self.random_walk(self.create_graph(), start_word)
        return ' '.join(path)


if __name__ == '__main__':
    parser = Parser('testing_sets/phrases.txt')
    words = parser.words
    probs = parser.transition_probabilities
    print(parser.generate_text('The'))
