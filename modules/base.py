class BaseModule:
    def __init__(self, target, username):
        self.target = target
        self.username = username

    def connect(self, password):
        raise NotImplementedError("Implemente o método connect no modulo especifico.")