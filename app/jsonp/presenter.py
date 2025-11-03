import json
from tkinter import simpledialog
import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
from jsonp.view import JsonView
from jsonp.model import JsonModel
from jsonp.schema import JsonSchema
from shapely.geometry import Polygon


class JsonPresenter:
    def __init__(self, view: JsonView, model: JsonModel):
        self.view = view
        self.model = model

    def load_json(self) -> tuple[dict, str]:
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
        """
        避免使用该函数，推荐使用save_json_with_name
        """
        fold_path = filedialog.asksaveasfilename(
            filetypes=[("JSON", "*.json")],
            defaultextension=".json",
            initialfile="combine.json",
        )
        with open(fold_path, "w", encoding="utf-8") as file:
            json.dump(json_file_dict, file, indent=4, ensure_ascii=False)
        return None

    def seve_json_with_name(self, json_file_dict: dict, name: str) -> None:
        fold_path = filedialog.asksaveasfilename(
            filetypes=[("JSON", "*.json")],
            defaultextension=".json",
            initialfile=name,
        )
        with open(fold_path, "w", encoding="utf-8") as file:
            json.dump(json_file_dict, file, indent=4, ensure_ascii=False)

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
        标签替换功能：遍历JSON字典中的标注数据，将指定的原始标签替换为新的标签
        """
        modified_json = json_dict.copy()  # 创建JSON字典的深拷贝，避免修改原始数据

        # 遍历所有标注形状（shapes）
        if "shapes" in modified_json:
            for shape in modified_json["shapes"]:
                # 检查当前形状的标签是否与原始标签匹配
                if shape.get("label") == original_label:
                    # 替换标签名称
                    shape["label"] = new_label
        return modified_json

    def delete_label(self, json_dict: dict) -> dict:
        """
        @YFENG-123
        """
        # 获取新标签输入
        label = simpledialog.askstring("标签删除", "请输入新标签名称:")
        if label is None:  # 用户点击取消
            return
        data = [shape for shape in json_dict["shapes"] if shape["label"] != label]
        json_dict["shapes"] = data
        return json_dict

    def convert_to_ndarray(
        self, json_dict: dict, id_list: list, thickness
    ) -> np.ndarray:
        """
        @YFENG-123
        """
        # 生成颜色列表（数量无限，不重复）
        colors = np.random.randint(0, 256, size=(len(id_list), 3))

        # 获取图像尺寸
        image_height = json_dict["imageHeight"]
        image_width = json_dict["imageWidth"]
        # 创建一个与图像大小相同的三维全一数组
        image_array = np.ones((image_height, image_width, 3), dtype=np.uint8) * 255
        print(image_array)

        # 绘制每个形状
        for shape in json_dict["shapes"]:
            points = np.array(shape["points"], dtype=np.int32)
            print(points)
            color = tuple(colors[id_list.index(shape["label"])])
            print(color)
            color = (int(color[0]), int(color[1]), int(color[2]))
            if thickness == -1:  # 填充多边形
                cv2.fillPoly(image_array, [points], color)
            else:  # 绘制多边形轮廓
                cv2.polylines(image_array, [points], True, color, thickness)

        return image_array

    def draw_to_ndarray(
        self, image_ndarray: np.ndarray, json_dict: dict, id_list: list
    ):
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

    def remove_overlap(self, json_dict: dict) -> tuple[dict, dict]:
        """
        @YFENG-123
        """
        # 创建一个空字典用于存储去重后的数据
        unique_shapes = []
        overlap_shapes = []
        # 遍历原始数据中的每个形状
        for shape in json_dict["shapes"]:
            result = False
            try:
                poly1 = Polygon(shape["points"])
            except Exception:  # 如果无法创建多边形对象，则跳过当前形状
                print("无法创建多边形对象")
                overlap_shapes.append(shape)
                print(shape)
                continue
            for unique_shape in unique_shapes:
                try:
                    poly2 = Polygon(unique_shape["points"])
                except Exception:  # 如果无法创建多边形对象，则跳过当前形状
                    print("无法创建多边形对象")
                    unique_shapes.append(unique_shape)
                    print(unique_shape)
                    continue
                result = result or poly1.intersects(poly2)
            if not result:  # 如果两个形状没有重叠，则添加到去重后的数据中
                unique_shapes.append(shape)
            else:  # 如果两个形状有重叠，则跳过当前形状
                print("重叠")
                overlap_shapes.append(shape)
                print(shape)
        json_dict1 = json_dict.copy()
        json_dict["shapes"] = unique_shapes
        json_dict1["shapes"] = overlap_shapes
        return json_dict, json_dict1


if __name__ == "__main__":
    root = tk.Tk()
    json_presenter = JsonPresenter(JsonView(root), JsonModel(root))
    json_path_list = json_presenter.get_json_path_list()
    json_dict_list = json_presenter.load_json_list(json_path_list)
    json_pack = json_presenter.combine_json(json_dict_list)
    json_presenter.save_json(json_pack)
