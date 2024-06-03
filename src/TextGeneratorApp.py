import tkinter as tk
from tkinter import messagebox, simpledialog

from src.DataManager import DataManager
from src.TextGenerator import TextGenerator

class TextGeneratorApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Markov Chain Text Generator")
        
        self.generator = TextGenerator()
        self.style = tk.StringVar(master)
        
        tk.Label(master, text="Enter Style:").pack()
        tk.Entry(master, textvariable=self.style).pack()
        
        tk.Button(master, text="Load Text and Train", command=self.load_text).pack()
        tk.Button(master, text="Generate Text", command=self.generate_text).pack()
        self.text_output = tk.Text(master, height=10, width=50)
        self.text_output.pack()

    def load_text(self):
        text = DataManager().load_data()
        style = simpledialog.askstring("Input", "Enter text style:", parent=self.master)
        self.generator.train(text, style)
        messagebox.showinfo("Training", "Training complete for style: " + style)

    def generate_text(self):
        result = self.generator.generate(self.style.get(), 100)
        self.text_output.delete(1.0, tk.END)
        self.text_output.insert(tk.END, result)