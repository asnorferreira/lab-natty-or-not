import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
from collections import Counter
import numpy as np

# Carregamento e preparação de dados
class TextDataset(Dataset):
    def __init__(self, text, sequence_length=50):
        self.chars = tuple(set(text))
        self.int2char = dict(enumerate(self.chars))
        self.char2int = {ch: ii for ii, ch in self.int2char.items()}
        encoded = np.array([self.char2int[ch] for ch in text])

        self.data = []
        for i in range(0, len(encoded) - sequence_length):
            self.data.append((encoded[i:i+sequence_length], encoded[i+1:i+sequence_length+1]))

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        return self.data[idx]

class RNN(nn.Module):
    def __init__(self, tokens, n_hidden=256, n_layers=2):
        super(RNN, self).__init__()
        self.n_hidden = n_hidden
        self.n_layers = n_layers
        self.embed = nn.Embedding(len(tokens), n_hidden)
        self.rnn = nn.LSTM(n_hidden, n_hidden, n_layers, batch_first=True)
        self.fc = nn.Linear(n_hidden, len(tokens))

    def forward(self, x, hidden):
        x = self.embed(x)
        out, hidden = self.rnn(x, hidden)
        out = self.fc(out[:, -1])
        return out, hidden

    def init_hidden(self, batch_size):
        weight = next(self.parameters()).data
        hidden = (weight.new(self.n_layers, batch_size, self.n_hidden).zero_(),
                  weight.new(self.n_layers, batch_size, self.n_hidden).zero_())
        return hidden
    
    def train(model, data_loader, epochs=10, lr=0.001):
        criterion = nn.CrossEntropyLoss()
        optimizer = optim.Adam(model.parameters(), lr=lr)
        model.train()

        for epoch in range(epochs):
            for inputs, targets in data_loader:
                optimizer.zero_grad()
                hidden = model.init_hidden(inputs.size(0))
                output, _ = model(inputs, hidden)
                loss = criterion(output, targets.view(-1))
                loss.backward()
                optimizer.step()
            print(f'Epoch {epoch + 1}/{epochs} Loss: {loss.item()}')

    def generate(model, dataset, text_length=100, start='Hello'):
        model.eval()
        chars = [ch for ch in start]
        size = len(dataset.chars)
        int_to_char = dict(enumerate(dataset.chars))
        char_to_int = {ch: ii for ii, ch in int_to_char.items()}
        
        hidden = model.init_hidden(1)
        for ch in start:
            char_tensor = torch.tensor([[char_to_int[ch]]], dtype=torch.long)
            output, hidden = model(char_tensor, hidden)
        
        for _ in range(text_length - len(start)):
            char_tensor = torch.tensor([[output.argmax(dim=1).item()]], dtype=torch.long)
            output, hidden = model(char_tensor, hidden)
            chars.append(int_to_char[output.argmax(dim=1).item()])

        return ''.join(chars)