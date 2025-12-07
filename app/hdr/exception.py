from exceptions import Error


class DataNotFoundError(Error):
    def __init__(self, message):
        super().__init__(message)


# model
## hdr_path
class HdrPathNotFoundError(DataNotFoundError):
    def __init__(self):
        super().__init__("Hdr path not found")


## hdr
class HdrNotFoundError(DataNotFoundError):
    def __init__(self):
        super().__init__("Hdr not found")
