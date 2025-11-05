import json
import cv2
import numpy as np
import cupy as cp
import tkinter as tk
from typing import Tuple
from tkinter import filedialog, simpledialog, messagebox
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
        """
        保存JSON文件：通用保存方法
        """
        fold_path = filedialog.asksaveasfilename(
            filetypes=[("JSON", "*.json")],
            defaultextension=".json",
            initialfile="combine.json",
        )
        with open(fold_path, "w", encoding="utf-8") as file:
            json.dump(json_file_dict, file, indent=4, ensure_ascii=False)
        return None

    def save_json_with_name(self, json_file_dict: dict, default_filename: str = "modified.json") -> None:
        """
        @chutaiyang
        保存JSON文件：支持自定义文件名
        
        Args:
            json_file_dict: JSON数据字典
            default_filename: 默认文件名
        """
        fold_path = filedialog.asksaveasfilename(
            filetypes=[("JSON", "*.json")],
            defaultextension=".json",
            initialfile=default_filename,
        )
        with open(fold_path, "w", encoding="utf-8") as file:
            json.dump(json_file_dict, file, indent=4, ensure_ascii=False)
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

    def get_validated_label_input(self, prompt: str = "请输入标签名称:") -> str:
        """
        @chutaiyang
        获取并校验标签输入：通过UI获取用户输入的标签并进行基础校验
        
        Args:
            prompt: 输入提示信息
            
        Returns:
            str: 经过校验的标签字符串，用户取消时返回None
        """
        while True:
            # 通过UI获取标签输入
            label = simpledialog.askstring("标签输入", prompt)
            
            # 用户点击取消
            if label is None:
                return None
            
            # 去除前后空格
            label = label.strip()
            
            # 检查是否为空
            if not label:
                messagebox.showwarning("输入错误", "标签不能为空")
                continue
            
            # 返回有效的标签
            return label

    def _check_label_exists(self, json_dict: dict, label: str) -> bool:
        """
        @chutaiyang
        检查标签存在性：验证指定标签是否存在于JSON数据中
        
        Args:
            json_dict: JSON数据字典
            label: 要检查的标签
            
        Returns:
            bool: 标签是否存在
        """
        if "shapes" not in json_dict:
            return False
            
        for shape in json_dict["shapes"]:
            if shape.get("label") == label:
                return True
        return False

    def _replace_labels_in_shapes(
        self, json_dict: dict, original_label: str, new_label: str
    ) -> dict:
        """
        @chutaiyang
        执行标签替换：遍历JSON字典中的标注数据，将指定的原始标签替换为新的标签
        
        Args:
            json_dict: JSON数据字典
            original_label: 要替换的原始标签
            new_label: 替换后的新标签
            
        Returns:
            dict: 修改后的JSON字典
        """
        # 创建JSON字典的深拷贝，避免修改原始数据
        modified_json = json_dict.copy()
        
        # 执行标签替换
        if "shapes" in modified_json:
            for shape in modified_json["shapes"]:
                if shape.get("label") == original_label:
                    shape["label"] = new_label
        
        return modified_json

    def replace_label(
        self, json_dict: dict, original_label: str, new_label: str
    ) -> dict:
        """
        @chutaiyang
        标签替换功能：完整的标签替换流程
        
        Args:
            json_dict: JSON数据字典
            original_label: 要替换的原始标签
            new_label: 替换后的新标签
            
        Returns:
            dict: 修改后的JSON字典
            
        Raises:
            ValueError: 如果标签不存在或替换失败
        """
        # 检查标签是否相同
        if original_label == new_label:
            return json_dict.copy()
        
        # 检查原始标签是否存在
        if not self._check_label_exists(json_dict, original_label):
            raise ValueError(f"标签 '{original_label}' 不存在于JSON数据中")
        
        # 执行标签替换
        return self._replace_labels_in_shapes(json_dict, original_label, new_label)
    
    def delete_label(self, json_dict: dict, label: str) -> dict:
        """
        @YFENG-123
        """
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

    def convert_to_mat_ndarray(
        self, json_dict: dict, id_list: list
    ) -> dict:
        """
        @chutaiyang
        将JSON标注数据转换为MAT格式的字典
        
        Args:
            json_dict: JSON数据字典
            id_list: 标签ID列表
            
        Returns:
            dict: 包含标注信息的MAT格式字典
        """
        # 提取基本信息
        mat_data = {}
        
        # 保存图像尺寸
        if "imageHeight" in json_dict and "imageWidth" in json_dict:
            mat_data["image_height"] = json_dict["imageHeight"]
            mat_data["image_width"] = json_dict["imageWidth"]
        
        # 保存图像路径（如果存在）
        if "imagePath" in json_dict:
            mat_data["image_path"] = json_dict["imagePath"]
        
        # 保存所有形状数据
        if "shapes" in json_dict:
            shapes_data = []
            for shape in json_dict["shapes"]:
                shape_info = {
                    "label": shape.get("label", ""),
                    "points": shape.get("points", []),
                    "shape_type": shape.get("shape_type", "polygon"),
                    "group_id": shape.get("group_id", None),
                    "flags": shape.get("flags", {})
                }
                shapes_data.append(shape_info)
            mat_data["shapes"] = shapes_data
        
        # 保存标签统计信息
        count_dict = self.count_label(json_dict)
        mat_data["label_counts"] = count_dict
        
        # 保存ID列表
        mat_data["id_list"] = id_list
        
        return mat_data


if __name__ == "__main__":
    root = tk.Tk()
    json_presenter = JsonPresenter(JsonView(root), JsonModel(root))
    json_path_list = json_presenter.get_json_path_list()
    json_dict_list = json_presenter.load_json_list(json_path_list)
    json_pack = json_presenter.combine_json(json_dict_list)
    json_presenter.save_json(json_pack)
