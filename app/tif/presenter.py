import tkinter as tk
import cv2
from tkinter import filedialog
from .view import TifView
from .model import TifModel


class TifPresenter:
    def __init__(self, tif_view: TifView, tif_model: TifModel):
        pass

    def load_tif(self, root):
        tif_path = filedialog.askopenfilename()
        with open(tif_path, "r", encoding="utf-8") as file:
            tif = cv2.imread(file)
        return tif, tif_path


if __name__ == "__main__":
    pass
