from exceptions import Error, NotFoundError


# model
## tif_path
class TifPathNotFoundError(NotFoundError):
    def __init__(self):
        super().__init__("Tif path not found")

## tif_array
class TifArrayNotFoundError(NotFoundError):
    def __init__(self):
        super().__init__("Tif array not found")