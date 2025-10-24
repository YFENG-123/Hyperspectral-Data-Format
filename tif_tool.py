import tkinter as tk
import skimage.io
from tkinter import filedialog

class Tif_tools:
    def __init__(self,root):
        self.menu = tk.Menu(root.menu)
        root.menu.add_cascade(label="TIF", menu=self.menu)

        self.menu.add_command(label="Open", command=lambda:self.load_tif(root))

        self.label = tk.Label(root, text="TIF:")
        self.label.pack()

    def load_tif(self,root):
        file_path = filedialog.askopenfilename()
        with open(file_path, 'r', encoding='utf-8') as file:
            root.tif = skimage.io.imread(file_path)
        self.label.config(text="TIF: " + file_path)
    


if __name__ == "__main__":
    root = tk.Tk()
    tif_tool = Tif_tools(root)
    root.mainloop()

