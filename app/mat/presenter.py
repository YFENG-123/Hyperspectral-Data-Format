import tkinter as tk
import scipy.io as sio
from tkinter import filedialog

from mat.view import MatView
from mat.model import MatModel


class MatPresenter:
    def __init__(self, mat_view: MatView, mat_model: MatModel):
        pass

    def load_mat(self):  #####
        mat_path = filedialog.askopenfilename(filetypes=[("MATLAB", "*.mat")])
        imggt = sio.loadmat(mat_path)
        for key, value in imggt.items():
            print(key)
        return imggt, mat_path

    def save_mat(self, imggt):  ####
        fold_path = filedialog.asksaveasfilename(
            filetypes=[("MATLAB", "*.mat")],
            defaultextension=".mat",
            initialfile="imggt.mat",
        )
        sio.savemat(fold_path, {"imggt": self.imggt})


if __name__ == "__main__":
    root = tk.Tk()
    mat_presenter = MatPresenter(MatView(root), MatModel(root))
    mat_presenter.load_mat()
    pass
