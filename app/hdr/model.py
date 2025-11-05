import numpy as np


class HdrModel:
    hdr: np.ndarray

    def __init__(self, root):
        self.root = root

    # hdr_path
    def set_hdr_path(self, hdr_path: str) -> None:
        self.hdr_path = hdr_path

    def get_hdr_path(self) -> str:
        return self.hdr_path

    # hdr
    def set_hdr(self, hdr: np.ndarray) -> None:
        self.hdr = hdr

    def get_hdr(self) -> np.ndarray:
        return self.hdr
