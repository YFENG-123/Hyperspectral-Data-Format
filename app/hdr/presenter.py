import h5py
import numpy as np

import spectral

from tkinter import filedialog

from hdr.view import HdrView
from hdr.model import HdrModel


class HdrPresenter:
    def __init__(self, view: HdrView, model: HdrModel):
        self.view = view
        self.model = model

    def load_hdr(self,hdr_path:str) -> np.ndarray:
        hdr = spectral.open_image(hdr_path)
        hdr = hdr.open_memmap()
        return hdr

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

    def save_hdf5(self, hdr: np.ndarray,save_path:str) -> None:
        height = hdr.shape[0]
        width = hdr.shape[1]
        num_channels = hdr.shape[2]
        # 创建HDF5文件（MATLAB v7.3格式）
        with h5py.File(save_path, "w") as file:
            dset = file.create_dataset(
                "data",
                shape=(height, width, num_channels),
                chunks=(height, width, 3),
                dtype=hdr.dtype,
            )  # 每个通道一个块
            for i in range(0, num_channels, 9):
                print(
                    f"正在处理通道 {i} ，当前进度：",
                    round(i / num_channels * 100, 2),
                    "%",
                )
                end = min(i + 9, num_channels)
                data = hdr[:, :, i:end]
                dset[:, :, i:end] = data
                del data
            print("保存完成")

    def save_hdf5_resize(self, hdr: np.ndarray, x1, y1, x2, y2,save_path:str) -> None:
        num_channels = hdr.shape[2]
        with h5py.File(save_path, "w") as file:
            dset = file.create_dataset(
                "data",
                shape=(num_channels, y2 - y1, x2 - x1),
                chunks=(3, y2 - y1, x2 - x1),
                dtype=hdr.dtype,
            )  # 每个通道一个块
            for i in range(0, num_channels, 9):
                print(
                    f"正在处理通道 {i} ，当前进度：",
                    round(i / num_channels * 100, 2),
                    "%",
                )
                end = min(i + 9, num_channels)
                data = np.transpose(hdr[x1:x2, y1:y2, i:end], (2, 0, 1))
                dset[i:end, :, :] = data
                del data
            print("保存完成")


if __name__ == "__main__":
    pass
