from exceptions import Error


# 文件不是json格式
class FileTypeNotJsonError(Error):
    def __init__(self, json_path):
        super().__init__(f"File '{json_path}' is not a json file.")
        self.json_path = json_path


class JsonDataError(Error):
    def __init__(self, json_path, info):
        super().__init__(f"Json data in '{json_path}' is not valid.", info)
        self.json_path = json_path
