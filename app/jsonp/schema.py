class JsonSchema:
    version: str
    flags: dict
    shapes: list
    imagePath: str
    imageData: str
    imageHeight: int
    imageWidth: int
    text: str
    description: str

    def __init__(self):
        self.version = "0.0.0"
        self.flags = {}
        self.shapes = []
        self.imagePath = ""
        self.imageData = ""
        self.imageHeight = 0
        self.imageWidth = 0
        self.text = ""
        self.description = ""
