from jsonp.model import JsonModel
from mat.model import MatModel
from tif.model import TifModel
from hdr.model import HdrModel


class Models:
    def __init__(self):
        self.json = JsonModel(self)
        self.mat = MatModel(self)
        self.tif = TifModel(self)
        self.hdr = HdrModel(self)
