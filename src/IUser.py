from src.TextGeneratorApp import TextGeneratorApp
import tkinter as tk

def main():
    root = tk.Tk()
    app = TextGeneratorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()