import unittest
import torch

from src.TextDataset import RNN, TextDataset

class TestTextGenerator(unittest.TestCase):
    def test_data_loading(self):
        dataset = TextDataset("Hello world")
        self.assertEqual(len(dataset), 10) 

    def test_rnn_output(self):
        dataset = TextDataset("Hello world")
        model = RNN(dataset.chars)
        hidden = model.init_hidden(1)
        char_to_int = {ch: ii for ii, ch in dict(enumerate(dataset.chars)).items()}
        input = torch.tensor([[char_to_int['H']]], dtype=torch.long)
        output, hidden = model(input, hidden)
        self.assertTrue(output is not None)

if __name__ == '__main__':
    unittest.main()
