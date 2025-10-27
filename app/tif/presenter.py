import tkinter as tk
import numpy as np
import cv2

from tkinter import filedialog
from .view import TifView
from .model import TifModel


class TifPresenter:
    def __init__(self, tif_view: TifView, tif_model: TifModel):
        pass

    def load_tif(self, root) -> tuple[np.ndarray, str]:
        tif_path = filedialog.askopenfilename()
        with open(tif_path, "r", encoding="utf-8") as file:
            tif_matlike = cv2.imread(file)
            tif_ndarray = np.array(tif_matlike)
        return tif_ndarray, tif_path

    def save_tif(self, tif_ndarray) -> None:
        """
        @wwwyy3555-oss, @liux11111111
        """
        pass


if __name__ == "__main__":
    pass
