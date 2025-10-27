import json
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

        #json_pack.flag = json_dict_list[0]["flags"]
        #json_pack.imagePath = json_dict_list[0]["imagePath"]
        #json_pack.imageData = json_dict_list[0]["imageData"]
        #json_pack.imageHeight = json_dict_list[0]["imageHeight"]
        #json_pack.imageWidth = json_dict_list[0]["imageWidth"]
        #json_pack.text = json_dict_list[0]["text"]
        #json_pack.description = json_dict_list[0]["description"]
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


if __name__ == "__main__":
    root = tk.Tk()
    json_presenter = JsonPresenter(JsonView(root), JsonModel(root))
    json_path_list = json_presenter.get_json_path_list()
    json_dict_list = json_presenter.load_json_list(json_path_list)
    json_pack = json_presenter.combine_json(json_dict_list)
    json_presenter.save_json(json_pack)
