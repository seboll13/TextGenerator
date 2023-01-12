from random import choice
from corpus_parser import Parser
from corpus_classifier import WordClassifier
from core_engine import TextGeneratorEngine

def main():
    parser = Parser('testing_sets/phrases.txt')
    tokens = parser.get_tokens()
    wc = WordClassifier(tokens)
    word_pairs = wc.word_pairs
    tag_pairs = wc.tag_pairs
    engine = TextGeneratorEngine(word_pairs, tag_pairs)
    print(engine.generate_text())


if __name__ == '__main__':
    main()