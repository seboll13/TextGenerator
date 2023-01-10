from corpus_parser import Parser
from core_engine import TextGeneratorEngine

def main():
    parser = Parser('testing_sets/phrases.txt')
    word_pairs = parser.word_pairs
    engine = TextGeneratorEngine(word_pairs)
    print(engine.generate_text('The'))


if __name__ == '__main__':
    main()