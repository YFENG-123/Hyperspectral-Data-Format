from views import Views
from models import Models

from jsonp.presenter import JsonPresenter
from jsonp.view import JsonView
from jsonp.model import JsonModel

from mat.presenter import MatPresenter
from mat.view import MatView
from mat.model import MatModel

from tif.presenter import TifPresenter
from tif.view import TifView
from tif.model import TifModel


class Presenters:
    def __init__(self, views: Views, models: Models):
        # 接收上级实例
        self.view = views
        self.model = models

        # 创建下级presenter
        self.json = JsonPresenter(self.view.json, self.model.json)
        self.tif = TifPresenter(self.view.tif, self.model.tif)
        self.mat = MatPresenter(self.view.mat, self.model.mat)

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

        pass

    def json_open(self):
        json_dict, json_path = self.json.load_json()
        self.model.json.set_json_dict(json_dict)
        self.model.json.set_json_path(json_path)

        json_path = self.model.json.get_json_path()
        self.view.set_json_label(json_path)

    def tif_open(self):
        tif_array, tif_path = self.tif.load_tif()
        self.model.tif.set_tif_array(tif_array)
        self.model.tif.set_tif_path(tif_path)

        tif_path = self.model.tif.get_tif_path()
        self.view.set_tif_label(tif_path)

    def tif_save(self):
        tif_array = self.model.tif.get_tif_array()
        if tif_array is None:
            return None
        self.tif.save_tif(tif_array)
        return None

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

    def json_combine(self):  # 数据量大，暂时不持久化
        json_path_list = self.json.get_json_path_list()
        self.model.json.set_json_path_list(json_path_list)
        json_dict_list = self.json.load_json_list(json_path_list)
        json_dict = self.json.combine_json(json_dict_list)
        self.json.save_json(json_dict)

    def json_count_label(self):
        json_dict = self.model.json.get_json_dict()
        count_dict = self.json.count_label(json_dict)
        self.model.json.set_count_dict(count_dict)

        count_dict = self.model.json.get_count_dict()
        self.view.set_count_label(str(count_dict))

    def json_generate_id(self):
        count_dict = self.model.json.get_count_dict()
        id_list = self.json.generate_id(count_dict)
        self.model.json.set_id_list(id_list)

        id_list = self.model.json.get_id_list()
        self.view.set_id_label(str(id_list))

    def json_replace_label(self):
        """
        @chutaiyang
        """
        pass
