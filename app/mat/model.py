class MatModel:
    mat_dict: dict

    def __init__(self, root):
        self.root = root

    # mat_dict
    def get_mat_dict(self) -> dict:
        return self.mat_dict

    def set_mat_dict(self, mat_dict: dict):
        self.mat_dict = mat_dict
