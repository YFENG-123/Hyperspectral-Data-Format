import tkinter as tk
import scipy.io as sio
import numpy as np
from tkinter import filedialog

from mat.view import MatView
from mat.model import MatModel


class MatPresenter:
    def __init__(self, mat_view: MatView, mat_model: MatModel):
        pass

    def load_mat(self) -> tuple[dict, str]:

        mat_path = filedialog.askopenfilename(filetypes=[("MATLAB", "*.mat")])
        if not mat_path:
            return None, ""
        mat_dict = sio.loadmat(mat_path)
        return mat_dict, mat_path

    def save_mat(self, mat_dict):
        fold_path = filedialog.asksaveasfilename(
            filetypes=[("MATLAB", "*.mat")],
            defaultextension=".mat",
            initialfile="save.mat",
        )
        if not fold_path:
            return None
        sio.savemat(fold_path, mat_dict)
        return None


if __name__ == "__main__":
    root = tk.Tk()
    mat_presenter = MatPresenter(MatView(root), MatModel(root))
    mat_presenter.load_mat()
    pass
