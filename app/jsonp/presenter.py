import json
import cv2
import numpy as np
import cupy as cp
import copy
import tkinter as tk
from typing import Tuple
from tkinter import simpledialog, messagebox
from shapely.geometry import Polygon
from jsonp.view import JsonView
from jsonp.model import JsonModel
from jsonp.schema import JsonSchema
from jsonp.exception import JsonDataError


class JsonPresenter:
    def __init__(self, view: JsonView, model: JsonModel):
        self.view = view
        self.model = model

    def load_json(self, json_path: str) -> dict:
        """
        @YFENG-123
        """

        with open(json_path, "r", encoding="utf-8") as file:
            try:
                json_dict = json.load(file)
            except json.JSONDecodeError as e:
                raise JsonDataError(json_path, str(e))
        return json_dict

    def load_json_list(self, json_path_list) -> list:
        """
        @YFENG-123
        """
        json_dict_list = []
        for file_path in json_path_list:
            with open(file_path, "r", encoding="utf-8") as file:
                try:
                    json_dict = json.load(file)
                except json.JSONDecodeError as e:
                    raise JsonDataError(file_path, str(e))
            json_dict_list.append(json_dict)
        return json_dict_list

    def combine_json(self, json_dict_list) -> dict:
        """
        @YFENG-123
        """
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

    def seve_json(self, json_file_dict: dict, file_path) -> None:
        """
        @YFENG-123
        """
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(json_file_dict, file, indent=4, ensure_ascii=False)

    def count_label(self, json_dict: dict) -> dict:
        """
        @YFENG-123
        """
        count_dict = {}
        for shape in json_dict["shapes"]:
            if shape["label"] in count_dict:
                count_dict[shape["label"]] += 1
            else:
                count_dict[shape["label"]] = 1
        return count_dict

    def generate_id(self, count_dict: dict) -> list:
        """
        @YFENG-123
        """
        key_list = list(count_dict.keys())
        value_list = list(count_dict.values())
        id_list = ["背景"]
        for _ in range(len(key_list)):
            idx = value_list.index(max(value_list))  # 获取最大值索引
            id_list.append(key_list[idx])  # 添加最大值索引对应键
            value_list[idx] = 0  # 将最大值索引对应值置零
        return id_list

    def replace_label_with_ui(self, json_dict: dict = None) -> None:
        """
        @chutaiyang
        标签替换功能：用户交互界面，输入原始标签和新标签进行替换

        Args:
            json_dict (dict, optional): JSON数据字典，如果为None则加载文件

        Returns:
            None: 无返回值，所有业务逻辑和数据处理由本方法完成
        """
        # 检查是否有加载的JSON数据
        if json_dict is None:
            # 如果没有数据，先加载JSON文件
            json_dict, _ = self.load_json()
            if json_dict is None:
                return  # 用户取消了文件选择

        # 获取原始标签输入
        original_label = simpledialog.askstring(
            "标签替换", "请输入要替换的原始标签名称:"
        )
        if original_label is None:  # 用户点击取消
            return

        # 输入校验：去除首尾空格
        original_label = original_label.strip()
        if not original_label:
            messagebox.showerror("输入错误", "原始标签不能为空！")
            return

        # 获取新标签输入
        new_label = simpledialog.askstring(
            "标签替换", f"请输入替换'{original_label}'的新标签名称:"
        )
        if new_label is None:  # 用户点击取消
            return

        # 输入校验：去除首尾空格
        new_label = new_label.strip()
        if not new_label:
            messagebox.showerror("输入错误", "新标签不能为空！")
            return

        # 检查标签是否相同
        if original_label == new_label:
            messagebox.showinfo("提示", "原始标签与新标签一致，无需替换")
            return

        # 检查原始标签是否存在
        if not self._check_label_exists(json_dict, original_label):
            messagebox.showerror("标签不存在", f"标签'{original_label}'在数据中不存在")
            return

        # 执行标签替换并统计替换数量
        modified_json, replaced_count = self.replace_label(
            json_dict, original_label, new_label
        )

        # 显示替换结果
        if replaced_count > 0:
            messagebox.showinfo("替换成功", f"成功替换 {replaced_count} 处标签")

            # 保存修改后的文件
            save_choice = messagebox.askyesno("保存文件", "是否保存修改后的文件？")
            if save_choice:
                self.save_json(modified_json)

            # 更新模型数据（如果存在模型）
            if hasattr(self, "model") and hasattr(self.model, "set_json_dict"):
                self.model.set_json_dict(modified_json)
        else:
            messagebox.showwarning("替换失败", "未找到匹配的标签进行替换")

    def replace_label(
        self, json_dict: dict, original_label: str, new_label: str
    ) -> Tuple[dict, int]:
        """
        @chutaiyang
        标签替换功能：遍历JSON字典中的标注数据，将指定的原始标签替换为新的标签

        Args:
            json_dict (dict): 原始JSON数据字典
            original_label (str): 要替换的原始标签名称
            new_label (str): 替换后的新标签名称

        Returns:
            Tuple[dict, int]: 修改后的JSON数据字典和替换数量
        """
        # 创建JSON字典的深拷贝，避免修改原始数据
        modified_json = copy.deepcopy(json_dict)

        # 调用可复用的标签替换接口并获取替换数量
        replaced_count = self._replace_labels_in_shapes(
            modified_json, original_label, new_label
        )

        return modified_json, replaced_count

    def _check_label_exists(self, json_dict: dict, label: str) -> bool:
        """
        @chutaiyang
        检查标签是否存在于JSON数据中
        """
        if "shapes" in json_dict:
            for shape in json_dict["shapes"]:
                if shape.get("label") == label:
                    return True
        return False

    def _replace_labels_in_shapes(
        self, json_dict: dict, original_label: str, new_label: str
    ) -> int:
        """
        @chutaiyang
        可复用的标签替换接口：在shapes数组中替换指定标签，返回替换数量
        """
        replaced_count = 0
        if "shapes" in json_dict:
            for shape in json_dict["shapes"]:
                # 检查当前形状的标签是否与原始标签匹配
                if shape.get("label") == original_label:
                    # 替换标签名称
                    shape["label"] = new_label
        # return modified_json

    def delete_label(self, json_dict: dict, label: str) -> dict:
        """
        @YFENG-123
        """
        # 获取新标签输入
        data = [shape for shape in json_dict["shapes"] if shape["label"] != label]
        json_dict["shapes"] = data
        return json_dict

    def convert_to_ndarray_rgb(
        self, json_dict: dict, id_list: list, thickness: int = -1
    ) -> np.ndarray:
        """
        @YFENG-123
        """

        # 获取图像尺寸
        image_height = json_dict["imageHeight"]
        image_width = json_dict["imageWidth"]
        image_array = (
            np.ones((image_height, image_width, 3), dtype=np.uint8) * 255
        )  # 创建一个与图像大小相同的三维全一数组
        # 生成颜色列表（数量无限，不重复）
        colors = np.random.randint(0, 256, size=(len(id_list), 3))
        # 固定颜色列表（常用的20种颜色）
        colors = [
            (255, 0, 0),  # 红色
            (0, 255, 0),  # 绿色
            (0, 0, 255),  # 蓝色
            (255, 255, 0),  # 黄色
            (255, 0, 255),  # 洋红
            (0, 255, 255),  # 青色
            (128, 0, 0),  # 深红
            (0, 128, 0),  # 深绿
            (0, 0, 128),  # 深蓝
            (128, 128, 0),  # 橄榄色
            (128, 0, 128),  # 紫色
            (0, 128, 128),  # 深青
            (255, 165, 0),  # 橙色
            (255, 192, 203),  # 粉红
            (165, 42, 42),  # 棕色
            (128, 128, 128),  # 灰色
            (0, 0, 0),  # 黑色
            (255, 255, 255),  # 白色
            (192, 192, 192),  # 银色
            (255, 215, 0),  # 金色
        ]
        # 绘制每个形状
        for shape in json_dict["shapes"]:
            points = np.array(shape["points"], dtype=np.int32)
            color = colors[id_list.index(shape["label"])]
            color = (int(color[0]), int(color[1]), int(color[2]))
            if thickness == -1:  # 填充多边形
                cv2.fillPoly(image_array, [points], color)
            else:  # 绘制多边形轮廓
                cv2.polylines(image_array, [points], True, color, thickness)

        return image_array

    def convert_to_ndarray_gray(
        self, json_dict: dict, id_list: list, thickness: int = -1
    ) -> np.ndarray:
        """
        @YFENG-123
        """
        # 获取图像尺寸
        image_height = json_dict["imageHeight"]
        image_width = json_dict["imageWidth"]
        image_array = np.zeros((image_height, image_width), dtype=np.uint8)
        # 绘制每个形状
        for shape in json_dict["shapes"]:
            points = np.array(shape["points"], dtype=np.int32)
            id = id_list.index(shape["label"])
            if thickness == -1:  # 填充多边形
                cv2.fillPoly(image_array, [points], id_list.index(shape["label"]))
            else:  # 绘制多边形轮廓
                cv2.polylines(
                    image_array,
                    [points],
                    True,
                    id,
                    thickness,
                )

        return image_array

    def convert_to_mat(
        self, json_dict: dict, id_list: list, thickness: int = 5
    ) -> dict:
        """
        @chutaiyang
        JSON转MAT功能：将JSON标注数据转换为MAT格式的字典

        实现方式：
        1. 调用convert_to_ndarray接口将JSON转换为图像数组
        2. 构建包含标注信息的MAT数据结构
        3. 返回适合保存为MAT文件的字典格式

        Args:
            json_dict (dict): JSON数据字典
            id_list (list): 标签ID列表
            thickness (int, optional): 多边形绘制厚度，默认5

        Returns:
            dict: 包含标注数据的MAT格式字典
        """
        # 调用可复用的convert_to_ndarray接口转换为图像数组
        annotation_array = self.convert_to_ndarray(json_dict, id_list, thickness)

        # 构建MAT数据结构（移除可能导致问题的imageData字段）
        mat_data = {
            "annotation_data": annotation_array,
            "image_height": json_dict.get("imageHeight"),
            "image_width": json_dict.get("imageWidth"),
            "shapes_count": len(json_dict.get("shapes", [])),
            "labels": id_list,
            "original_json": {
                "imagePath": json_dict.get("imagePath"),
                "version": json_dict.get("version"),
            },
        }

        return mat_data

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
