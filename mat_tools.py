import tkinter as tk
import scipy.io as sio
from tkinter import filedialog

class Mat_tools:
    def __init__(self,root):
        self.menu = tk.Menu(root.menu)
        root.menu.add_cascade(label="Mat", menu=self.menu)

        self.menu.add_command(label="Open", command=lambda:self.load_mat(root))
        self.menu.add_command(label="Save_mat", command=self.save_mat)

        self.label = tk.Label(root, text="Mat:")
        self.label.pack()

    def load_mat(self,root):
        file_path = filedialog.askopenfilename(filetypes=[("MATLAB", "*.mat")])
        with open(file_path, 'r', encoding='utf-8') as file:
            root.imggt = sio.loadmat(file_path)
        self.label.config(text="Mat: " + file_path)

    def save_mat(self,imggt):
        fold_path = filedialog.asksaveasfilename(filetypes=[("MATLAB", "*.mat")])
        sio.savemat(fold_path, {'imggt': self.imggt})

if __name__ == '__main__':
    root = tk.Tk()
    Mat_tools(root)
    root.mainloop()