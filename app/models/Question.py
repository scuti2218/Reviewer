from .ModelData import ModelData
from .Answer import Answer
from ..services import Randomizable

class Question(ModelData, Randomizable[Answer]):
    def __init__(self, **kwargs):
        self.token: str = ""
        self.question: str = ""
        self.category: str = ""
        self.correct_answers: list[str] = []
        self.wrong_answers: list[str] = []
        super().__init__(**kwargs)
        self.set_value(*[Answer(title = i, is_correct = True) for i in self.correct_answers],
                       *[Answer(title = i, is_correct = False) for i in self.wrong_answers])
        self.count_correct = len(self.correct_answers)
    
    def show(self):
        return f"{self.question}"