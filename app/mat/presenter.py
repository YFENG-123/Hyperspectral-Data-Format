import tkinter as tk
import scipy.io as sio
import numpy as np
from tkinter import filedialog
from mat.view import MatView
from mat.model import MatModel


class MatPresenter:
    def __init__(self, mat_view: MatView, mat_model: MatModel):
        self.view = mat_view
        self.model = mat_model

    def load_mat(self, mat_path: str) -> tuple[dict, str]:
        mat_dict = sio.loadmat(mat_path)
        return mat_dict

    def save_mat(self, ndarray: np.ndarray, save_path: str):
        sio.savemat(save_path, {"mat_ndarray": ndarray})

    def save_mat_resize(self, ndarray: np.ndarray, x1, y1, x2, y2, save_path):
        ndarray = ndarray[x1:y1, x2:y2]
        sio.savemat(save_path, {"mat_ndarray": ndarray})


if __name__ == "__main__":
    root = tk.Tk()
    mat_presenter = MatPresenter(MatView(root), MatModel(root))
    mat_presenter.load_mat()
    pass
