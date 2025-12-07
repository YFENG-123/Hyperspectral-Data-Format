import numpy as np
from tif.exception import TifArrayNotFoundError, TifPathNotFoundError

class TifModel:
    tif_path: str
    tif_array: np.ndarray

    def __init__(self, root):
        self.root = root
        self.tif_path = ""
        self.tif_array = None

    def set_tif_path(self, tif_path: str) -> None:
        self.tif_path = tif_path

    def get_tif_path(self) -> str:
        if self.tif_path == "":
            raise TifPathNotFoundError()
        return self.tif_path

    def set_tif_array(self, tif_array: np.ndarray) -> None:
        self.tif_array = tif_array

    def get_tif_array(self) -> np.ndarray:
        if self.tif_array is None:
            raise TifArrayNotFoundError()
        return self.tif_array
