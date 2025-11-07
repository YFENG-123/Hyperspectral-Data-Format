from exceptions import Error, NotFoundError


# 文件不是json格式
class FileTypeNotJsonError(Error):
    def __init__(self, json_path):
        super().__init__(f"File '{json_path}' is not a json file.")


# json数据内容错误
class JsonDataError(Error):
    def __init__(self, json_path, info):
        super().__init__(f"Json data in '{json_path}' is not valid : {info}")


# model
## json_dict不存在
class JsonDictNotFoundError(NotFoundError):
    def __init__(self):
        super().__init__("Json dict is not exist.")


## count_dict 不存在
class CountDictNotFoundError(NotFoundError):
    def __init__(self):
        super().__init__("Count dict is not exist.")


## id_list 不存在
class IdListNotFoundError(NotFoundError):
    def __init__(self):
        super().__init__("Id list is not exist.")


## json_path 不存在
class JsonPathNotFoundError(NotFoundError):
    def __init__(self):
        super().__init__("Json path is not exist.")


## json_path_list 不存在
class JsonPathListNotFoundError(NotFoundError):
    def __init__(self):
        super().__init__("Json path list is not exist.")
