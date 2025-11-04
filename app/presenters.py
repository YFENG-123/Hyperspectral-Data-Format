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

        # 统计标签
        json_dict = self.models.json.get_json_dict()
        count_dict = self.json.count_label(json_dict)
        self.models.json.set_count_dict(count_dict)

        # 显示标签
        count_dict = self.models.json.get_count_dict()
        self.views.set_count_label(str(count_dict))

        # 生成id
        id_list = self.json.generate_id(count_dict)
        self.models.json.set_id_list(id_list)

        # 显示id
        id_list = self.models.json.get_id_list()
        self.views.set_id_label(str(id_list))


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
        标签替换功能：调用下级接口实现用户交互界面
        
        Returns:
            None: 无返回值，具体替换结果由下级接口通过弹窗显示
        """
        # 获取当前JSON数据
        json_dict = self.models.json.get_json_dict()
        
        # 调用下级接口处理标签替换
        # 下级接口负责所有业务逻辑处理，包括用户交互、数据验证和结果反馈
        self.json.replace_label_with_ui(json_dict)


    def json_delete_label(self):
        """
        @YFENG-123
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
        JSON转MAT功能：将JSON标注数据转换为MAT格式文件
        
        实现方式：
        1. 从models获取JSON数据和ID列表
        2. 调用下级presenter的convert_to_mat接口转换为MAT格式数据
        3. 调用mat presenter的save_mat接口保存为MAT文件
        
        Returns:
            None: 无返回值，具体保存结果由下级接口处理
        """
        # 加载 json 和 id
        json_dict = self.models.json.get_json_dict()
        id_list = self.models.json.get_id_list()

        # 调用可复用的convert_to_mat接口转换为MAT格式数据
        mat_data = self.json.convert_to_mat(json_dict, id_list, 5)

        # 保存为MAT文件
        self.mat.save_mat(mat_data)

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
        self.models.mat.set_mat_dict(mat_dict)
        self.models.mat.set_mat_path(mat_path)

        mat_path = self.models.mat.get_mat_path()
        self.view.set_mat_label(mat_path)

    def mat_save(self):
        mat_dict = self.models.mat.get_mat_dict()
        if mat_dict is None:
            return None
        self.mat.save_mat(mat_dict)
        return None

    # Hdr
    def hdr_open(self):
        hdr_ndarray = self.hdr.load_hdr()
        self.models.hdr.set_hdr(hdr_ndarray)

    def hdr_convert_to_mat(self):
        hdr_ndarray = self.models.hdr.get_hdr()
        self.hdr.save_hdf5(hdr_ndarray)

    def hdr_convert_to_mat_resize(self):
        hdr_ndarray = self.models.hdr.get_hdr()
        x1 = 500
        x2 = 1000
        y1 = 500
        y2 = 1000
        self.hdr.save_hdf5_resize(hdr_ndarray, x1, y1, x2, y2)
