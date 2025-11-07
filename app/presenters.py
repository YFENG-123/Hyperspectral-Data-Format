from views import Views
from models import Models

from jsonp.presenter import JsonPresenter
from mat.presenter import MatPresenter
from tif.presenter import TifPresenter
from hdr.presenter import HdrPresenter

from exceptions import Error


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
        views.bind_json_convert_to_tif(self.json_convert_to_tif)
        views.bind_json_convert_to_mat(self.json_convert_to_mat)
        views.bind_json_convert_to_mat_resize(self.json_convert_to_mat_resize)

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
        try:
            # 获取json路径
            json_path = self.views.ask_open_path("JSON", ".json")
            self.models.json.set_json_path(json_path)

            # 显示json路径
            json_path = self.models.json.get_json_path()
            self.views.set_json_label(json_path)

            # 加载json
            json_dict = self.json.load_json(json_path)
            self.models.json.set_json_dict(json_dict)

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
        except Error as e:
            self.views.show_error(str(e))

    def json_combine(self):  # 数据量大，暂时不持久化
        try:
            # 获取json路径列表
            json_path_list = self.views.ask_open_path("JSON", ".json")
            self.models.json.set_json_path_list(json_path_list)

            # 加载json字典列表
            json_dict_list = self.json.load_json_list(json_path_list)

            # 组合json
            json_dict = self.json.combine_json(json_dict_list)

            # 保存json
            save_path = self.views.ask_save_path("JSON", ".json", "json_combine")
            self.json.seve_json(json_dict, save_path)
        except Error as e:
            self.views.show_error(str(e))

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
        待添加校验
        """
        try:
            label = self.views.ask_label("标签删除", "请输入要删除的标签名称:")
            # 加载 json
            json_dict = self.models.json.get_json_dict()

            # 删除标签
            json_dict = self.json.delete_label(json_dict, label)

            # 保存 json
            save_path = self.views.ask_save_path("JSON", ".json", "json_delete")
            self.json.seve_json(save_path, "deleted")
        except Error as e:
            self.views.show_error(str(e))

    def json_convert_to_tif(self):
        """
        @YFENG-123
        """
        try:
            # 加载 json 和 id
            json_dict = self.models.json.get_json_dict()
            id_list = self.models.json.get_id_list()

            # 转换成 ndarray
            ndarray = self.json.convert_to_ndarray_rgb(json_dict, id_list, -1)

            # 保存 tif
            save_path = self.views.ask_save_path("TIF", ".tif", "json_convert_to_tif")
            self.tif.save_tif(ndarray, save_path)
        except Error as e:
            self.views.show_error(str(e))

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
        try:
            # 加载 json 和 id
            json_dict = self.models.json.get_json_dict()
            id_list = self.models.json.get_id_list()

            # 调用可复用的convert_to_mat接口转换为MAT格式数据
            mat_data = self.json.convert_to_mat(json_dict, id_list, 5)

            # 保存为MAT文件
            self.mat.save_mat(mat_data)
        except Error as e:
            self.views.show_error(str(e))

    def json_convert_to_mat_resize(self):
        """
        @YFENG-123
        """
        try:
            json_dict = self.models.json.get_json_dict()
            id_list = self.models.json.get_id_list()
            json_ndarray = self.json.convert_to_ndarray_gray(json_dict, id_list, -1)

            save_path = self.views.ask_save_path(
                "MAT", ".mat", "json_convert_to_mat_resize"
            )
            '''
            x1 = 1276
            y1 = 7284
            x2 = 6288
            y2 = 11265
            '''
            x1 = 500
            y1 = 500
            x2 = 600
            y2 = 700 
            self.mat.save_mat_resize(json_ndarray, x1, y1, x2, y2, save_path)
        except Error as e:
            self.views.show_error(str(e))

    # Tif
    def tif_open(self):
        try:
            tif_path = self.views.ask_open_path("TIF", ".tif")
            self.models.tif.set_tif_path(tif_path)

            tif_array = self.tif.load_tif(tif_path)
            self.models.tif.set_tif_array(tif_array)

            tif_path = self.models.tif.get_tif_path()
            self.views.set_tif_label(tif_path)
        except Error as e:
            self.views.show_error(str(e))

    def tif_save(self):
        try:
            save_path = self.views.ask_save_path("TIF", ".tif", "tif_save")
            tif_array = self.models.tif.get_tif_array()

            self.tif.save_tif(tif_array, save_path)

        except Error as e:
            self.views.show_error(str(e))

    def tif_draw_label(self):
        try:
            # 获取 json 和 id
            json_dict = self.models.json.get_json_dict()
            id_list = self.models.json.get_id_list()

            # 获取 tif
            tif_ndarray = self.models.tif.get_tif_array()

            # 绘制标签
            tif_ndarray = self.tif.draw_label(tif_ndarray, json_dict, id_list, 5)

            seve_path = self.views.ask_save_path("TIF", ".tif", "tif_draw_label")
            # 保存 tif
            self.tif.save_tif(tif_ndarray, seve_path)
        except Error as e:
            self.views.show_error(str(e))

    # Mat
    def mat_open(self):
        try:
            mat_path = self.views.ask_open_path("MAT", ".mat")
            mat_dict = self.mat.load_mat(mat_path)
            self.models.mat.set_mat_dict(mat_dict)
            self.models.mat.set_mat_path(mat_path)

            mat_path = self.models.mat.get_mat_path()
            self.view.set_mat_label(mat_path)
        except Error as e:
            self.views.show_error(str(e))

    def mat_save(self):
        try:
            save_path = self.views.ask_save_path("MAT", ".mat", "mat_save")
            mat_dict = self.models.mat.get_mat_dict()
            self.mat.save_mat(mat_dict, save_path)
        except Error as e:
            self.views.show_error(str(e))

    # Hdr
    def hdr_open(self):
        try:
            hdr_path = self.views.ask_open_path("HDR", ".hdr")
            self.models.hdr.set_hdr_path(hdr_path)

            hdr_path = self.models.hdr.get_hdr_path()
            self.views.set_hdr_label(hdr_path)

            hdr_ndarray = self.hdr.load_hdr(hdr_path)
            self.models.hdr.set_hdr(hdr_ndarray)

        except Error as e:
            self.views.show_error(str(e))

    def hdr_convert_to_mat(self):
        try:
            hdr_ndarray = self.models.hdr.get_hdr()
            save_path = self.views.ask_save_path("HDF5", ".hdf", "hdr_convert_to_mat")
            self.hdr.save_hdf5(hdr_ndarray, save_path)
        except Error as e:
            self.views.show_error(str(e))

    def hdr_convert_to_mat_resize(self):
        try:
            hdr_ndarray = self.models.hdr.get_hdr()
            '''
            x1 = 1276
            y1 = 7284
            x2 = 6288
            y2 = 11265
            '''
            x1 = 500
            y1 = 500
            x2 = 600
            y2 = 700 
            save_path = self.views.ask_save_path(
                "HDF5", ".hdf", "hdr_convert_to_mat_resize"
            )
            self.hdr.save_hdf5_resize(hdr_ndarray, x1, y1, x2, y2, save_path)
        except Error as e:
            self.views.show_error(str(e))
