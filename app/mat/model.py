class MatModel:
    mat_path: dict

    def __init__(self, root):
        self.root = root

    # mat_path
    def set_mat_path(self, mat_path: dict) -> None:
        self.mat_path = mat_path

    def get_mat_path(self) -> dict:
        return self.mat_path
