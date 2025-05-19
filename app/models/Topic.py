from .ModelData import ModelData

class Topic(ModelData):
    def __init__(self, **kwargs):
        self.dir = ""
        self.token = ""
        super().__init__(**kwargs)
    
    def show(self):
        return f"{self.title} : {self.info}"
    
    def check_token(self):
        return True