from src.MarkovChain import MarkovChain


class TextGenerator:
    def __init__(self, order=2):
        self.markov = MarkovChain()
        self.order = order

    def train(self, text, style):
        if text:
            self.markov.add_to_chain(text, style, self.order)

    def generate(self, style, length=50):
        return self.markov.generate_text(style, length)