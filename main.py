from time import time
from functools import wraps
from corpus_parser import Parser
from corpus_classifier import WordClassifier
from core_engine import TextGeneratorEngine

def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time()
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(e)
        finally:
            end = time()
            print(f'Model loaded in : {(end - start):.3f} seconds')
    return wrapper


@timer
def load_model():
    parser = Parser('testing_sets/phrases.txt')
    tokens = parser.get_tokens()
    wc = WordClassifier(tokens)
    word_pairs = wc.word_pairs
    tag_pairs = wc.tag_pairs
    engine = TextGeneratorEngine(word_pairs, tag_pairs)
    return engine


def main():
    engine = load_model()
    print(engine.generate_text())


if __name__ == '__main__':
    main()