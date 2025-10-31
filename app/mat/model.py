import numpy as np


class MatModel:
    mat_path: str
    mat_dict: dict

    def __init__(self, root):
        self.root = root
        self.mat_path = ""
        self.mat_dict = None
    
    def set_mat_path(self, mat_path: str) -> None:
        self.mat_path = mat_path

    def get_mat_path(self) -> str:
        return self.mat_path

    def set_mat_dict(self, mat_dict: dict) -> None:
        self.mat_dict = mat_dict

    def get_mat_dict(self) -> dict:
        return self.mat_dict
