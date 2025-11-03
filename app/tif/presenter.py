import tkinter as tk
import numpy as np
import cv2

from tkinter import filedialog
from .view import TifView
from .model import TifModel


class TifPresenter:
    def __init__(self, tif_view: TifView, tif_model: TifModel):
        self.view = tif_view
        self.model = tif_model

    def load_tif(self) -> tuple[np.ndarray, str]:
        tif_path = filedialog.askopenfilename()
        tif_matlike = cv2.imread(tif_path)
        tif_ndarray = np.array(tif_matlike)
        return tif_ndarray, tif_path

    def save_tif(self, tif_ndarray) -> None:
        fold_path = filedialog.asksaveasfilename(
            filetypes=[("TIFF", "*.tif"), ("TIFF", "*.tiff")],
            defaultextension=".tif",
            initialfile="output.tif",
        )
        if fold_path:
            cv2.imwrite(fold_path, tif_ndarray)
        return None

    def draw_label(
        self, tif_ndarray: np.ndarray, json_dict: dict, id_list: list, thickness: int
    ) -> np.ndarray:
        """
        @YFENG-123
        """
        colors = np.random.randint(0, 256, size=(len(id_list), 3))

        # tif_ndarray = tif_ndarray.astype(int)
        # 绘制每个形状
        for shape in json_dict["shapes"]:
            points = np.array(shape["points"], dtype=np.int32)
            print(points)
            color = tuple(colors[id_list.index(shape["label"])])
            print(color)
            color = (int(color[0]), int(color[1]), int(color[2]))
            if thickness == -1:  # 填充多边形
                cv2.fillPoly(tif_ndarray, [points], color)
            else:  # 绘制多边形轮廓
                cv2.polylines(tif_ndarray, [points], True, color, thickness)
        return tif_ndarray


if __name__ == "__main__":
    pass
