class JsonModel:
    json_dict: dict
    json_path: str
    json_path_list: list
    count_dict: dict
    id_list: list

    def __init__(self, root):
        self.root = root

    # json_dict
    def set_json_dict(self, json_dict: dict):
        self.json_dict = json_dict

    def get_json_dict(self) -> dict:
        return self.json_dict

    # count_dict
    def set_count_dict(self, count_dict: dict):
        self.count_dict = count_dict

    def get_count_dict(self) -> dict:
        return self.count_dict

    # id_list
    def set_id_list(self, id_list: list):
        self.id_list = id_list

    def get_id_list(self) -> list:
        return self.id_list

    # json_path
    def set_json_path(self, json_path: str):
        self.json_path = json_path

    def get_json_path(self) -> str:
        return self.json_path

    # json_path_list
    def set_json_path_list(self, json_path_list: list):
        self.json_path_list = json_path_list

    def get_json_path_list(self) -> list:
        return self.json_path_list
