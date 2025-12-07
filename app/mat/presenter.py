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

    def load_mat(self, mat_path: str) -> dict:
        mat_dict = sio.loadmat(mat_path)
        return mat_dict

    def save_mat(self, data, save_path: str):
        """
        保存MAT文件
        Args:
            data: 可以是 np.ndarray 或 dict，如果是dict则直接保存，如果是ndarray则包装成字典
            save_path: 保存路径
        """
        if isinstance(data, dict):
            sio.savemat(save_path, data)
        else:
            sio.savemat(save_path, {"mat_ndarray": data})

    def save_mat_resize(self, ndarray: np.ndarray, x1, y1, x2, y2, save_path):
        ndarray = ndarray[x1:x2,y1:y2]
        sio.savemat(save_path, {"mat_ndarray": ndarray})


if __name__ == "__main__":
    root = tk.Tk()
    mat_presenter = MatPresenter(MatView(root), MatModel(root))
    mat_path = filedialog.askopenfilename(
        filetypes=[("MAT", "*.mat")], defaultextension=".mat"
    )
    if mat_path:
        mat_dict = mat_presenter.load_mat(mat_path)
        print("Loaded MAT file:", mat_path)
    pass
