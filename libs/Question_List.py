from .Randomizable import Randomizable
from .Question import Question
from .Enums import ChoiceOption

class Question_List(Randomizable[Question]):
    id = 0
    def __init__(self):
        super().__init__()
        self.question_lists : dict[ChoiceOption, list[Question]] = {i:[] for i in ChoiceOption }
        self.id += 1
        self.activated = False

    def __str__(self):
        return f"Question List"

    def __repr__(self):
        return f"QuestionList({self.length})"
            
    # SETTERS
    def set_value(self, questions: list[Question]):
        map(self.add_question, questions)
    
    def add_question(self, question: Question):
        for choice_option in question.choice_options:
            self.question_lists[choice_option].append(question)
        
    # ACTIVATOR
    def activate(self, choice_option: ChoiceOption):
        self.data = self.question_lists[choice_option]
        self.randomize()
        self.activated = True
        
    # ACTIVATE-BASED METHODS
    def get_data(self):
        if not self.activated:
            raise Exception("Please activate before usage!")
        return self.data
    
    def get_question_from_randomized(self, index: int):
        if not self.activated:
            raise Exception("Please activate before usage!")
        return self.get_from_randomized(index)