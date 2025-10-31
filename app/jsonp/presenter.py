import json
import cv2
import numpy as np
import cupy as cp
import tkinter as tk
from typing import Tuple
from tkinter import filedialog
from jsonp.view import JsonView
from jsonp.model import JsonModel
from jsonp.schema import JsonSchema


class JsonPresenter:
    def __init__(self, json_view: JsonView, json_model: JsonModel):
        pass

    def load_json(self) -> Tuple[dict, str]:
        json_path = filedialog.askopenfilename()
        with open(json_path, "r", encoding="utf-8") as file:
            json_dict = json.load(file)
        return json_dict, json_path

    def get_json_path_list(self) -> list:
        json_path_list = list(filedialog.askopenfilenames())
        return json_path_list

    def load_json_list(self, json_path_list) -> list:
        json_dict_list = []
        for file_path in json_path_list:
            with open(file_path, "r", encoding="utf-8") as file:
                json_dict = json.load(file)
            json_dict_list.append(json_dict)
        return json_dict_list

    def combine_json(self, json_dict_list) -> dict:
        json_pack = JsonSchema()
        for json_dict in json_dict_list:
            if int("".join(json_dict["version"].split("."))) > int(
                "".join(json_pack.version.split("."))
            ):
                json_pack.version = json_dict["version"]

            for shapes in json_dict["shapes"]:
                json_pack.shapes.append(shapes)

        json_pack.flag = json_dict_list[0]["flags"]
        json_pack.imagePath = json_dict_list[0]["imagePath"]
        json_pack.imageData = json_dict_list[0]["imageData"]
        json_pack.imageHeight = json_dict_list[0]["imageHeight"]
        json_pack.imageWidth = json_dict_list[0]["imageWidth"]
        # json_pack.text = json_dict_list[0]["text"]
        # json_pack.description = json_dict_list[0]["description"]
        return vars(json_pack)

    def save_json(self, json_file_dict: dict) -> None:
        fold_path = filedialog.asksaveasfilename(
            filetypes=[("JSON", "*.json")],
            defaultextension=".json",
            initialfile="combine.json",
        )
        with open(fold_path, "w", encoding="utf-8") as file:
            json.dump(json_file_dict, file, indent=4)
        return None

    def count_label(self, json_dict: dict) -> dict:
        count_dict = {}
        for shape in json_dict["shapes"]:
            if shape["label"] in count_dict:
                count_dict[shape["label"]] += 1
            else:
                count_dict[shape["label"]] = 1
        print(count_dict)
        return count_dict

    def generate_id(self, count_dict: dict) -> list:
        key_list = list(count_dict.keys())
        value_list = list(count_dict.values())
        id_list = ["背景"]
        for _ in range(len(key_list)):
            idx = value_list.index(max(value_list))  # 获取最大值索引
            id_list.append(key_list[idx])  # 添加最大值索引对应键
            value_list[idx] = 0  # 将最大值索引对应值置零
        return id_list

    def replace_label(
        self, json_dict: dict, original_label: str, new_label: str
    ) -> dict:
        """
        @chutaiyang
        """
        # return json_dict

    def convert_to_ndarray(self, json_dict: dict, id_list: list) -> np.ndarray:
        """
        @YFENG-123
        """
        # 生成颜色列表（数量无限，不重复）
        colors = np.random.randint(0, 256, size=(1000, 3))

        # 获取图像尺寸
        image_height = json_dict["imageHeight"]
        image_width = json_dict["imageWidth"]
        # 创建一个与图像大小相同的全零数组
        image_array = np.zeros((image_height, image_width), dtype=np.uint8)

        # 绘制每个形状
        for shape in json_dict["shapes"]:
            # 提取多边形点坐标
            points = np.array(shape["points"], dtype=np.int32)
            cv2.fillPoly(
                image_array, [points], True, colors[id_list.index(shape["label"])]
            )
        return image_array

    def draw_to_ndarray(self, image_ndarray: np.ndarray, json_dict: dict, id_list: list):
        """
        @YFENG-123
        """
        # 生成颜色列表（数量无限，不重复）
        colors = np.random.randint(0, 256, size=(1000, 3))

        # 绘制每个形状
        for shape in json_dict["shapes"]:
            # 提取多边形点坐标
            points = np.array(shape["points"], dtype=np.int32)
            cv2.fillPoly(
                image_ndarray, [points], True, colors[id_list.index(shape["label"])]
            )
        return image_ndarray
    


if __name__ == "__main__":
    root = tk.Tk()
    json_presenter = JsonPresenter(JsonView(root), JsonModel(root))
    json_path_list = json_presenter.get_json_path_list()
    json_dict_list = json_presenter.load_json_list(json_path_list)
    json_pack = json_presenter.combine_json(json_dict_list)
    json_presenter.save_json(json_pack)
