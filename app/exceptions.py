class Error(Exception):
    def __init__(self, message,info):
        self.message = message
        self.info = info

