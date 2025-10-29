from spectral.io.envi import SpectralLibrary
class HdrModel:
    hdr: SpectralLibrary

    def __init__(self, root):
        self.root = root

    # mat_path
    def set_hdr(self, mat_path: SpectralLibrary) -> None:
        self.mat_path = mat_path

    def get_hdr(self) -> SpectralLibrary:
        return self.mat_path
