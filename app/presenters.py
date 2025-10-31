import spectral
import numpy as np
from scipy.io import savemat

from views import Views
from models import Models

from jsonp.presenter import JsonPresenter
from mat.presenter import MatPresenter
from tif.presenter import TifPresenter
from hdr.presenter import HdrPresenter


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
        views.bind_json_combine(self.json_combine)
        views.bind_json_open(self.json_open)
        views.bind_json_count(self.json_count_label)
        views.bind_json_id(self.json_generate_id)

        ## tif
        views.bind_tif_open(self.tif_open)
        views.bind_tif_save(self.tif_save)

        ## mat
        views.bind_mat_open(self.mat_open)
        views.bind_mat_save(self.mat_save)

        ## hdr
        views.bind_hdr_open(self.hdr_open)
        views.bind_hdr_convert_to_mat(self.hdr_convert_to_mat)
        views.bind_hdr_convert_to_mat_resize(self.hdr_convert_to_mat_resize)



    # Json
    def json_open(self):
        json_dict, json_path = self.json.load_json()
        self.models.json.set_json_dict(json_dict)
        self.models.json.set_json_path(json_path)

        json_path = self.models.json.get_json_path()
        self.views.set_json_label(json_path)
    def json_combine(self):  # 数据量大，暂时不持久化
        json_path_list = self.json.get_json_path_list()
        self.models.json.set_json_path_list(json_path_list)
        json_dict_list = self.json.load_json_list(json_path_list)
        json_dict = self.json.combine_json(json_dict_list)
        self.json.save_json(json_dict)

    def json_count_label(self):
        json_dict = self.models.json.get_json_dict()
        count_dict = self.json.count_label(json_dict)
        self.models.json.set_count_dict(count_dict)

        count_dict = self.models.json.get_count_dict()
        self.views.set_count_label(str(count_dict))

    def json_generate_id(self):
        count_dict = self.models.json.get_count_dict()
        id_list = self.json.generate_id(count_dict)
        self.models.json.set_id_list(id_list)

        id_list = self.models.json.get_id_list()
        self.views.set_id_label(str(id_list))

    def json_replace_label(self):
        """
        @chutaiyang
        """
        pass

    # Tif
    def tif_open(self):
        """
        @wwwyy3555-oss, @liux11111111
        """
        pass

    def tif_save(self):
        """
        @wwwyy3555-oss, @liux11111111
        """
        pass

    # Mat
    def mat_open(self):
        """
        @wwwyy3555-oss, @liux11111111
        """
        pass

    def mat_save(self):
        """
        @wwwyy3555-oss, @liux11111111
        """
        pass

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


