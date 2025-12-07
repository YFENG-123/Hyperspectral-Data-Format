class Error(Exception):
    def __init__(self, message):
        self.message = message

class NotFoundError(Error):
    def __init__(self,message):
        super().__init__(message)