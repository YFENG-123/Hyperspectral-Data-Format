import cv2
import numpy as np

class TifModel:
    tif_path : np.ndarray
    def __init__(self, root):
        self.root = root
    
    def set_tif_path(self, tif_path: np.ndarray) -> None:
        self.tif_path = tif_path
    
    def get_tif_path(self) -> np.ndarray:
        return self.tif_path
