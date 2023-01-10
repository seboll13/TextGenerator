import networkx as nx
from numpy.random import choice

class TextGeneratorEngine:
    def __init__(self, word_pairs):
        """Initialise a text generator engine."""
        self.word_pairs = word_pairs
        self.transition_probabilities = self.compute_transition_probabilities()


    def compute_transition_probabilities(self) -> dict:
        """Return a dictionary matching the transition probabilities between each pair of words."""
        probs = {}
        # Count
        for curr_word in self.word_pairs:
            for next_word in self.word_pairs[curr_word]:
                if (curr_word, next_word) in probs:
                    probs[(curr_word, next_word)] += self.word_pairs[curr_word][next_word]
                else:
                    probs[(curr_word, next_word)] = self.word_pairs[curr_word][next_word]
        # Normalise
        for curr_word in self.word_pairs:
            for next_word in self.word_pairs[curr_word]:
                probs[(curr_word, next_word)] /= self.word_pairs[curr_word][next_word]
        return probs


    def create_graph(self) -> nx.DiGraph:
        """Create a directed graph from the transition probabilities."""
        G = nx.DiGraph()
        G.add_nodes_from(self.word_pairs.keys())
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