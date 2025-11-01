import spectral
import numpy as np
from scipy.io import savemat

from views import Views
from models import Models

from jsonp.presenter import JsonPresenter
from mat.presenter import MatPresenter
from tif.presenter import TifPresenter
from hdr.presenter import HdrPresenter


from hdr.model import HdrModel


class Presenters:
    def __init__(self, views: Views, models: Models):
        # 接收上级实例
        self.views = views
        self.models = models

        # 创建下级presenter
        self.json = JsonPresenter(self.views.json, self.models.json)
        self.tif = TifPresenter(self.views.tif, self.models.tif)
        self.mat = MatPresenter(self.views.mat, self.models.mat)
        self.hdr = HdrPresenter(self.views.hdr, self.models.hdr)

        # 绑定函数
        ## json
        views.bind_json_replace_label(self.json_replace_label)
        views.bind_json_delete_label(self.json_delete_label)
        views.bind_json_combine(self.json_combine)
        views.bind_json_open(self.json_open)
        views.bind_json_count(self.json_count_label)
        views.bind_json_id(self.json_generate_id)
        views.bind_json_convert_to_tif(self.json_convert_to_tif)
        views.bind_json_remove_overlap(self.json_remove_overlap)
        views.bind_json_convert_to_mat(self.json_convert_to_mat)

        ## tif
        views.bind_tif_open(self.tif_open)
        views.bind_tif_save(self.tif_save)
        views.bind_tif_draw_label(self.tif_draw_label)

        ## mat
        views.bind_mat_open(self.mat_open)
        views.bind_mat_save(self.mat_save)

        ## hdr
        views.bind_hdr_open(self.hdr_open)
        views.bind_hdr_convert_to_mat(self.hdr_convert_to_mat)
        views.bind_hdr_convert_to_mat_resize(self.hdr_convert_to_mat_resize)

    # Json
    def json_open(self):
        # 加载json，并保存
        json_dict, json_path = self.json.load_json()
        self.models.json.set_json_dict(json_dict)
        self.models.json.set_json_path(json_path)

        # 显示json路径
        json_path = self.models.json.get_json_path()
        self.views.set_json_label(json_path)

    def json_combine(self):  # 数据量大，暂时不持久化
        json_path_list = self.json.get_json_path_list()
        self.models.json.set_json_path_list(json_path_list)
        json_dict_list = self.json.load_json_list(json_path_list)
        json_dict = self.json.combine_json(json_dict_list)
        self.json.save_json(json_dict)

    def json_count_label(self):
        # 统计标签，并保存
        json_dict = self.models.json.get_json_dict()
        count_dict = self.json.count_label(json_dict)
        self.models.json.set_count_dict(count_dict)

        # 显示标签
        count_dict = self.models.json.get_count_dict()
        self.views.set_count_label(str(count_dict))

    def json_generate_id(self):
        # 生成id，并保存
        count_dict = self.models.json.get_count_dict()
        id_list = self.json.generate_id(count_dict)
        self.models.json.set_id_list(id_list)

        # 显示id
        id_list = self.models.json.get_id_list()
        self.views.set_id_label(str(id_list))

    def json_replace_label(self):
        """
        @chutaiyang
        标签替换功能：用户交互界面，输入原始标签和新标签进行替换
        """
        # 检查是否有加载的JSON数据
        json_dict = self.models.json.get_json_dict()
        if json_dict is None:
            # 如果没有数据，先加载JSON文件
            self.json_open()
            json_dict = self.models.json.get_json_dict()
            if json_dict is None:
                return  # 用户取消了文件选择

        # 创建输入对话框
        import tkinter as tk
        from tkinter import simpledialog

        # 获取原始标签输入
        original_label = simpledialog.askstring(
            "标签替换", "请输入要替换的原始标签名称:"
        )
        if original_label is None:  # 用户点击取消
            return

        # 获取新标签输入
        new_label = simpledialog.askstring(
            "标签替换", f"请输入替换'{original_label}'的新标签名称:"
        )
        if new_label is None:  # 用户点击取消
            return

        # 执行标签替换
        modified_json = self.jsons.replace_label(json_dict, original_label, new_label)

        # 更新模型数据
        self.model.json.set_jsons_dict(modified_json)

        # 显示替换结果
        self.view.set_jsons_label(f"标签已替换: {original_label} -> {new_label}")

        # 保存修改后的文件
        save_choice = tk.messagebox.askyesno("保存文件", "是否保存修改后的文件？")
        if save_choice:
            self.jsons.save_json(modified_json)
        pass

    def json_delete_label(self):
        """
        @chutaiyang
        """
        # 加载 json
        json_dict = self.models.json.get_json_dict()

        # 删除标签
        json_dict = self.json.delete_label(json_dict)  #####

        # 保存 json
        self.json.seve_json_with_name(json_dict, "deleted")

    def json_convert_to_tif(self):
        """
        @YFENG-123
        """
        # 加载 json 和 id
        json_dict = self.models.json.get_json_dict()
        id_list = self.models.json.get_id_list()

        # 转换成 ndarray
        ndarray = self.json.convert_to_ndarray(json_dict, id_list, 5)

        # 保存 tif
        self.tif.save_tif(ndarray)

    def json_convert_to_mat(self):
        """
        @chutaiyang
        """
        pass

    def json_remove_overlap(self):
        json_dict = self.models.json.get_json_dict()
        json_dict_remove, json_dict_overlap = self.json.remove_overlap(json_dict)
        self.json.seve_json_with_name(json_dict_remove, "remove")
        self.json.seve_json_with_name(json_dict_overlap, "overlap")

    # Tif
    def tif_open(self):
        tif_array, tif_path = self.tif.load_tif()
        self.models.tif.set_tif_array(tif_array)
        self.models.tif.set_tif_path(tif_path)

        tif_path = self.models.tif.get_tif_path()
        self.views.set_tif_label(tif_path)

    def tif_save(self):
        tif_array = self.models.tif.get_tif_array()
        if tif_array is None:
            return None
        self.tif.save_tif(tif_array)
        return None

    def tif_draw_label(self):
        # 获取 json 和 id
        json_dict = self.models.json.get_json_dict()
        id_list = self.models.json.get_id_list()

        # 获取 tif
        tif_ndarray = self.models.tif.get_tif_array()

        # 绘制标签
        tif_ndarray = self.tif.draw_label(tif_ndarray, json_dict, id_list, 5)

        # 保存 tif
        self.tif.save_tif(tif_ndarray)

    # Mat
    def mat_open(self):
        mat_dict, mat_path = self.mat.load_mat()
        self.model.mat.set_mat_dict(mat_dict)
        self.model.mat.set_mat_path(mat_path)

        mat_path = self.model.mat.get_mat_path()
        self.view.set_mat_label(mat_path)

    def mat_save(self):
        mat_dict = self.model.mat.get_mat_dict()
        if mat_dict is None:
            return None
        self.mat.save_mat(mat_dict)
        return None

    # Hdr
    def hdr_open(self):
        hdr = self.hdr.load_hdr()
        self.models.hdr.set_hdr(hdr)

    def hdr_convert_to_mat(self):
        hdr = self.models.hdr.get_hdr()
        hdr_ndarray = self.hdr.load_hdr_ndarray(hdr)
        self.mat.save_mat(hdr_ndarray)

    def hdr_convert_to_mat_resize(self):
        hdr = self.models.hdr.get_hdr()
        x1 = 500
        x2 = 1000
        y1 = 500
        y2 = 1000
        self.hdr.save_hdf5_resize(hdr, x1, y1, x2, y2)
