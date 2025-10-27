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
        self.view = views
        self.model = models

        self.json = JsonPresenter(self.view.json, self.model.json)
        self.tif = TifPresenter(self.view.tif, self.model.tif)
        self.mat = MatPresenter(self.view.mat, self.model.mat)

        views.bind_json_combine(self.combine_jsons)
        views.bind_json_open(self.open_json)
        views.bind_json_count(self.count_label)
        views.bind_json_id(self.generate_id)

    def open_json(self):
        json_dict, json_path = self.json.load_json()
        self.model.json.set_json_dict(json_dict)
        self.model.json.set_json_path(json_path)

        json_path = self.model.json.get_json_path()
        self.view.set_json_label(json_path)

    def combine_jsons(self):  # 数据量大，不用持久化
        json_path_list = self.json.get_json_path_list()
        json_dict_list = self.json.load_json_list(json_path_list)
        json_dict = self.json.combine_json(json_dict_list)
        self.json.save_json(json_dict)

    def count_label(self):
        json_dict = self.model.json.get_json_dict()
        count_dict = self.json.count_label(json_dict)
        self.model.json.set_count_dict(count_dict)

        count_dict = self.model.json.get_count_dict()
        self.view.set_count_label(str(count_dict))

    def generate_id(self):
        count_dict = self.model.json.get_count_dict()
        id_list = self.json.generate_id(count_dict)
        self.model.json.set_id_list(id_list)

        id_list = self.model.json.get_id_list()
        self.view.set_id_label(str(id_list))

    def open_tif(self):
        pass

    def open_mat(self):
        mat_dict, file_path = self.mat.load_mat()
        self.view.label_mat.config(text="Mat: " + file_path)
