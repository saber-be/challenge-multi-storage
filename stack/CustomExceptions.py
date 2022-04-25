class NoneElementException(Exception):
    def __init__(self, message = "Element cannot be None"):
        super().__init__(message)

class EmptyStackException(Exception):
    pass