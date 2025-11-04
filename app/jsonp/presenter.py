import json
import cv2
import numpy as np
import cupy as cp
import copy
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
        fold_path = filedialog.asksaveasfilename(
            filetypes=[("JSON", "*.json")],
            defaultextension=".json",
            initialfile="combine.json",
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

    def get_validated_label_input(self, prompt: str, title: str = "标签输入") -> str:
        """
        @chutaiyang
        获取并验证标签输入：封装标签输入和校验逻辑
        
        Args:
            prompt (str): 输入提示信息
            title (str, optional): 对话框标题，默认为"标签输入"
            
        Returns:
            str: 验证通过的标签字符串，如果用户取消或输入无效则返回None
        """
        label = simpledialog.askstring(title, prompt)
        if label is None:  # 用户点击取消
            return None
        
        label = label.strip()
        if not label:  # 输入为空
            messagebox.showerror("输入错误", "标签不能为空！")
            return None
            
        return label

    def _get_replacement_labels(self) -> tuple:
        """
        @chutaiyang
        获取替换标签对：封装原始标签和新标签的输入逻辑
        
        Returns:
            tuple: (original_label, new_label) 或 None（用户取消时）
        """
        # 获取原始标签
        original_label = self.get_validated_label_input("请输入要替换的原始标签名称:", "标签替换")
        if original_label is None:
            return None
            
        # 获取新标签
        new_label = self.get_validated_label_input(f"请输入替换'{original_label}'的新标签名称:", "标签替换")
        if new_label is None:
            return None
            
        return (original_label, new_label)

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
            json_path = filedialog.askopenfilename()
            if not json_path:  # 用户取消了文件选择
                return
            try:
                with open(json_path, "r", encoding="utf-8") as file:
                    json_dict = json.load(file)
            except Exception as e:
                messagebox.showerror("文件错误", f"加载JSON文件失败: {str(e)}")
                return
        
        # 获取标签输入
        labels = self._get_replacement_labels()
        if labels is None:  # 用户取消或输入无效
            return
        original_label, new_label = labels
        
        # 检查标签是否相同
        if original_label == new_label:
            messagebox.showinfo("提示", "原始标签与新标签一致，无需替换")
            return
        
        # 检查原始标签是否存在
        label_exists = False
        if "shapes" in json_dict:
            for shape in json_dict["shapes"]:
                if shape.get("label") == original_label:
                    label_exists = True
                    break
        
        if not label_exists:
            messagebox.showerror("标签不存在", f"标签'{original_label}'在数据中不存在")
            return
        
        # 执行标签替换并统计替换数量
        modified_json = copy.deepcopy(json_dict)
        replaced_count = 0
        
        if "shapes" in modified_json:
            for shape in modified_json["shapes"]:
                # 检查当前形状的标签是否与原始标签匹配
                if shape.get("label") == original_label:
                    # 替换标签名称
                    shape["label"] = new_label
                    replaced_count += 1
        
        # 显示替换结果
        if replaced_count > 0:
            messagebox.showinfo("替换成功", f"成功替换 {replaced_count} 处标签")
            
            # 保存修改后的文件
            save_choice = messagebox.askyesno("保存文件", "是否保存修改后的文件？")
            if save_choice:
                fold_path = filedialog.asksaveasfilename(
                    filetypes=[("JSON", "*.json")],
                    defaultextension=".json",
                    initialfile="modified.json",
                )
                if fold_path:
                    with open(fold_path, "w", encoding="utf-8") as file:
                        json.dump(modified_json, file, indent=4, ensure_ascii=False)
            
            # 更新模型数据（如果存在模型）
            if hasattr(self, 'model') and hasattr(self.model, 'set_json_dict'):
                self.model.set_json_dict(modified_json)
        else:
            messagebox.showwarning("替换失败", "未找到匹配的标签进行替换")
    


    
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
                "version": json_dict.get("version")
            }
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


if __name__ == "__main__":
    root = tk.Tk()
    json_presenter = JsonPresenter(JsonView(root), JsonModel(root))
    json_path_list = json_presenter.get_json_path_list()
    json_dict_list = json_presenter.load_json_list(json_path_list)
    json_pack = json_presenter.combine_json(json_dict_list)
    json_presenter.save_json(json_pack)
