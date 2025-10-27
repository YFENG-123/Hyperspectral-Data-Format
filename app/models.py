from jsonp.model import JsonModel
from mat.model import MatModel
from tif.model import TifModel


class Models:
    def __init__(self):
        self.json = JsonModel(self)
        self.mat = MatModel(self)
        self.tif = TifModel(self)
