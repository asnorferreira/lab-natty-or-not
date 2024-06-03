from tkinter import filedialog


class DataManager:
    def load_data(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            with open(file_path, 'r') as file:
                return file.read()
        else:
            return None