import tkinter as tk
import scipy.io as sio
import numpy as np
from tkinter import filedialog

from mat.view import MatView
from mat.model import MatModel


class MatPresenter:
    def __init__(self, mat_view: MatView, mat_model: MatModel):
        pass

    def load_mat(self) -> tuple[np.ndarray, str]:
        mat_path = filedialog.askopenfilename(filetypes=[("MATLAB", "*.mat")])
        mat_dict = sio.loadmat(mat_path)
        """
        @ww973, @liux11111111
        """
        #return mat_ndarry, mat_path

    def save_mat(self, mat_ndarray):
        fold_path = filedialog.asksaveasfilename(
            filetypes=[("MATLAB", "*.mat")],
            defaultextension=".mat",
            initialfile="save.mat",
        )
        """
        @ww973, @liux11111111
        """
        pass


if __name__ == "__main__":
    root = tk.Tk()
    mat_presenter = MatPresenter(MatView(root), MatModel(root))
    mat_presenter.load_mat()
    pass
