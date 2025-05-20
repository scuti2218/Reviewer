from .ModelData import ModelData

class Answer(ModelData):
    def __init__(self, **kwargs):
        self.is_correct = False
        super().__init__(**kwargs)
    
    def show(self):
        return f"{self.title}"