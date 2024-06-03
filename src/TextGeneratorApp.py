import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import filedialog

from src.DataManager import DataManager
from src.TextDataset import RNN, TextDataset
from src.TextGenerator import TextGenerator

class TextGeneratorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Advanced Text Generator")
        
        tk.Label(self, text="Enter Style:").grid(row=0, column=0)
        self.style_entry = tk.Entry(self)
        self.style_entry.grid(row=0, column=1)

        tk.Button(self, text="Load Text", command=self.load_text).grid(row=1, column=0)
        tk.Button(self, text="Train Model", command=self.train_model).grid(row=1, column=1)
        tk.Button(self, text="Generate Text", command=self.generate_text).grid(row=2, column=0, columnspan=2)

        self.text_output = tk.Text(self, height=15, width=50)
        self.text_output.grid(row=3, column=0, columnspan=2)

        self.model = None
        self.text_data = None

    def load_text(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            with open(file_path, 'r', encoding='utf-8') as file:
                self.text_data = file.read()
            messagebox.showinfo("Info", "Text loaded successfully!")

    def train_model(self):
        if self.text_data:
            dataset = TextDataset(self.text_data)
            self.model = RNN(dataset.chars)
            # Training logic here
            messagebox.showinfo("Info", "Model trained successfully!")

    def generate_text(self):
        if self.model:
            # Generate text logic here
            generated_text = "Generated text appears here."
            self.text_output.delete(1.0, tk.END)
            self.text_output.insert(tk.END, generated_text)
        else:
            messagebox.showinfo("Error", "Model not trained yet.")

if __name__ == "__main__":
    app = TextGeneratorApp()
    app.mainloop()