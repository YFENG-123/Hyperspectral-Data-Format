import h5py
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

    def save_hdf5(self, hdr) -> None:
        height = hdr.shape[0]
        width = hdr.shape[1]
        num_channels = hdr.shape[2]
        # 创建HDF5文件（MATLAB v7.3格式）
        with h5py.File("multichannel_data.mat", "w") as file:
            # 创建可扩展的三维数据集（高度 x 宽度 x 通道）
            dset = file.create_dataset(
                "data",
                shape=(num_channels, width, height),
                chunks=(1, width, height),  # 分块大小优化I/O
                dtype=np.uint16,
            )  # 每个通道一个块

            # 循环处理每个通道
            for i in range(0, num_channels):
                print(f"正在处理通道 {i} ...")

                # 显示进度百分比
                print("当前进度：", round(i / num_channels * 100, 2), "%")

                # 数据
                batch_data = hdr.read_band(i)

                # 使用内存映射写入当前通道
                dset[i, :, :] = batch_data.T  # 直接写入新通道

                del batch_data

                print(f"通道 {i} 已保存")

    def save_hdf5_resize(self, hdr, x1, y1, x2 ,y2) -> None:
        height = hdr.shape[0]
        width = hdr.shape[1]
        num_channels = hdr.shape[2]
        # 创建HDF5文件（MATLAB v7.3格式）
        with h5py.File("multichannel_data.mat", "w") as file:
            # 创建可扩展的三维数据集（高度 x 宽度 x 通道）
            dset = file.create_dataset(
                "data",
                shape=(num_channels, width, height),
                chunks=(1, width, height),  # 分块大小优化I/O
                dtype=np.uint16,
            )  # 每个通道一个块
            for i in range(0, num_channels):
                print(f"正在处理通道 {i} ...")
                print("当前进度：", round(i / num_channels * 100, 2), "%")
                #只读取指定区域
                batch_data = hdr.read_band(i)[y1:y2, x1:x2]
                # 使用内存映射写入当前通道
                dset[i, :, :] = batch_data.T  # 直接写入新通道
                del batch_data
                print(f"通道 {i} 已保存")
            


if __name__ == "__main__":
    pass
