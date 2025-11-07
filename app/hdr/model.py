import numpy as np
from hdr.exception import HdrNotFoundError, HdrPathNotFoundError


class HdrModel:
    hdr: np.ndarray

    def __init__(self, root):
        self.root = root

    # hdr_path
    def set_hdr_path(self, hdr_path: str) -> None:
        self.hdr_path = hdr_path

    def get_hdr_path(self) -> str:
        if self.hdr_path is None:
            raise HdrPathNotFoundError()
        return self.hdr_path

    # hdr
    def set_hdr(self, hdr: np.ndarray) -> None:
        self.hdr = hdr

    def get_hdr(self) -> np.ndarray:
        if self.hdr is None:
            raise HdrNotFoundError()
        return self.hdr
