from jsonp.exception import (
    JsonDictNotFoundError,
    CountDictNotFoundError,
    IdListNotFoundError,
    JsonPathNotFoundError,
    JsonPathListNotFoundError,
)


class JsonModel:
    json_dict: dict
    json_path: str
    count_dict: dict
    id_list: list
    json_path_list: list

    def __init__(self, root):
        self.root = root

    # json_dict
    def set_json_dict(self, json_dict: dict):
        self.json_dict = json_dict

    def get_json_dict(self) -> dict:
        if self.json_dict is None:
            raise JsonDictNotFoundError("Json file not exist")
        return self.json_dict

    # count_dict
    def set_count_dict(self, count_dict: dict):
        self.count_dict = count_dict

    def get_count_dict(self) -> dict:
        if self.count_dict is None:
            raise CountDictNotFoundError("Count dict not exist")
        return self.count_dict

    # id_list
    def set_id_list(self, id_list: list):
        self.id_list = id_list

    def get_id_list(self) -> list:
        if self.id_list is None:
            raise IdListNotFoundError("Id list not exist")
        return self.id_list

    # json_path
    def set_json_path(self, json_path: str):
        self.json_path = json_path

    def get_json_path(self) -> str:
        if self.json_path is None:
            raise JsonPathNotFoundError("Json path not exist")
        return self.json_path

    # json_path_list
    def set_json_path_list(self, json_path_list: list):
        self.json_path_list = json_path_list

    def get_json_path_list(self) -> list:
        if self.json_path_list is None:
            raise JsonPathListNotFoundError("Json path list not exist")
        return self.json_path_list
