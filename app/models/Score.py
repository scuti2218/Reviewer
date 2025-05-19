from .ModelData import ModelData

class Score(ModelData):
    def __init__(self, **kwargs):
        self.current: int = 0
        self.maximum: int = 0
        super().__init__(**kwargs)
        self.info = f"Score of {self.title}"
    
    def show(self):
        return f"{self.current} / {self.maximum} ({self.average:.2f} %)"
    
    def get_average(self):
        self.average = (self.current * 100) / self.maximum
        return self.average
    
    def check_token(self):
        return True