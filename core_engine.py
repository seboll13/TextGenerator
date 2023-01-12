import networkx as nx
from numpy.random import choice

class TextGeneratorEngine:
    def __init__(self, word_pairs, tag_pairs):
        """Initialise a text generator engine."""
        self.word_pairs = word_pairs
        self.tag_pairs = tag_pairs
        self.transition_probabilities = self.compute_word_transition_probabilities()
    

    def compute_word_transition_probabilities(self) -> dict:
        """Return a dictionary matching the transition probabilities between each pair of words."""
        probs = {}
        tag_probs = self.compute_tag_transition_probabilities()
        # Count
        for t in self.word_pairs:
            (curr_word, _) = t
            for next_word, v in self.word_pairs[t].items():
                i = probs.get((curr_word, next_word), 0)
                probs[(curr_word, next_word)] = i + v[0]
        # Normalise
        for t in self.word_pairs:
            (curr_word, curr_tag) = t
            _sumprob_words = sum([v[0] for v in self.word_pairs[t].values()])
            _sumprob_tags = sum([tag_probs[(curr_tag, v[1])] for v in self.word_pairs[t].values()])
            for next_word, v in self.word_pairs[t].items():
                probs[(curr_word, next_word)] = v[0] / _sumprob_words
                probs[(curr_word, next_word)] *= tag_probs[(curr_tag, v[1])] * (1 / _sumprob_tags)
        return probs
    

    def compute_tag_transition_probabilities(self) -> dict:
        """Return a dictionary matching the transition probabilities between each pair of tags."""
        probs = {}
        # Count
        for curr_el in self.tag_pairs:
            for next_el in self.tag_pairs[curr_el]:
                if (curr_el, next_el) in probs:
                    probs[(curr_el, next_el)] += self.tag_pairs[curr_el][next_el]
                else:
                    probs[(curr_el, next_el)] = self.tag_pairs[curr_el][next_el]
        # Normalise
        for curr_el in self.tag_pairs:
            _sum = sum(self.tag_pairs[curr_el].values())
            for next_el in self.tag_pairs[curr_el]:
                probs[(curr_el, next_el)] = self.tag_pairs[curr_el][next_el] / _sum
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


    start_words = ['A', 'The', 'It', 'He', 'She', 'They', 'We', 'I', 'You', 'There', 'Here', 'This', 'That', 'These', 'Those', 'My', 'Your']

    def generate_text(self) -> str:
        """Generate a random text from the graph."""
        start_word = choice(self.start_words).lower()
        path = self.random_walk(self.create_graph(), start_word)
        return ' '.join(path)
    

    def generate_paragraph(self, num_sentences) -> str:
        """Generate a random paragraph from the graph."""
        return ' '.join([self.generate_text(choice(self.start_words)) for _ in range(num_sentences)])