from .ModelData import ModelData

class Category(ModelData):
    def __init__(self, **kwargs):
        self.key = ""
        super().__init__(**kwargs)
    
    def show(self):
        return f"{self.title}" + [f" : {self.info}", ""][len(self.info.strip()) == 0 ]