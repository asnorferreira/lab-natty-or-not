import random

class MarkovChain:
    def __init__(self):
        self.chains = {}

    def add_to_chain(self, text, style, order=2):
        chain = self.chains.setdefault(style, {})
        words = text.split()
        for i in range(len(words) - order):
            key = tuple(words[i:i + order])
            next_word = words[i + order]
            chain.setdefault(key, []).append(next_word)

    def generate_text(self, style, length=50):
        if style not in self.chains or not self.chains[style]:
            return "No data available for this style."
        
        chain = self.chains[style]
        start = random.choice(list(chain.keys()))
        result = list(start)
        
        for i in range(length - len(start)):
            last = tuple(result[-len(start):])
            next_word = random.choice(chain[last]) if last in chain else random.choice(list(chain.keys()))[0]
            result.append(next_word)

        return ' '.join(result)