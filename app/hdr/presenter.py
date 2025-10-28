import spectral
from spectral.io.envi import SpectralLibrary, BilFile, BipFile, BsqFile

import tkinter as tk
from tkinter import filedialog

import numpy as np

from hdr.view import HdrView
from hdr.model import HdrModel


class HdrPresenter:
    def __init__(self, hdr_view: HdrView, hdr_model: HdrModel):
        pass

    def load_hdr(self) -> spectral.envi.SpectralLibrary:
        hdr_path = filedialog.askopenfilename(filetypes=[("HDR", "*.hdr")])
        hdr = spectral.open_image(hdr_path)
        return hdr

    def load_hdr_ndarray(
        self, hdr: SpectralLibrary | BilFile | BipFile | BsqFile
    ) -> np.ndarray:
        hdr_ndarray = hdr.read_bands(list(range(0, hdr.nbands)))
        return hdr_ndarray

    def save_hdr(self, hdr_ndarray):
        """
        @YFENG-123
        """
        file_path = filedialog.asksaveasfilename(
            filetypes=[("HDR", "*.hdr")],
            defaultextension=".hdr",
            initialfile="save.hdr",
        )
        metadata = {
            "lines": hdr_ndarray.shape[0],
            "samples": hdr_ndarray.shape[1],
            "bands": hdr_ndarray.shape[2] if len(hdr_ndarray.shape) > 2 else 1,
            "data type": 4,  # 32-bit float
            "interleave": "bsq",
            "byte order": 0,  # Little endian
            "file type": "ENVI Standard",
        }

        # 使用spectral库的envi模块保存HDR/IMG文件对
        spectral.envi.save_image(file_path, hdr_ndarray, metadata=metadata, force=True)


if __name__ == "__main__":
    pass
