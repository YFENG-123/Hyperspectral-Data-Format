from spectral.io.envi import SpectralLibrary
class HdrModel:
    hdr: SpectralLibrary

    def __init__(self, root):
        self.root = root

    # hdr_path
    def set_hdr(self, hdr_path: SpectralLibrary) -> None:
        self.hdr_path = hdr_path

    def get_hdr(self) -> SpectralLibrary:
        return self.hdr_path
