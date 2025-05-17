from .Randomizable import Randomizable
from .Answer import Answer
from .Enums import ChoiceOption
from .Printer import print_question, print_options

class Question(Randomizable[Answer]):
    id = 0
    def __init__(self):
        super().__init__()
        self.id += 1
        self.activated = False

    def __str__(self):
        return f"{self.value}"

    def __repr__(self):
        return f"Question({self.value})"
        
    # SETTERS
    def set_value(self, question: str):
        self.value: str = question
        
    def set_choice_option(self, choice_options: list[str]):
        self.choice_options = [member for member in ChoiceOption for choice_option in choice_options if member.name == choice_option]
        
    def set_classification(self, classification: str):
        self.classification: str = classification
        
    def add_answer(self, answer: Answer):
        self.data.append(answer)
        
    def add_answers(self, answers: list[Answer]):
        self.data += answers
        
    # ACTIVATOR
    def activate(self):
        self.correct_indexes = []
        self.wrong_indexes = []
        for i, answer in enumerate(self.data):
            if answer.is_correct:
                self.correct_indexes.append(i)
            else:
                self.wrong_indexes.append(i)
        self.correct_length = len(self.correct_indexes)
        self.wrong_length = len(self.wrong_indexes)
        self.activated = True
        
    # ACTIVATE-BASED METHODS
    def get_answer_in_randomized(self, index: int) -> Answer:
        if not self.activated:
            raise Exception("Please activate before usage!")
        return self.get_from_randomized(index)
    
    def show_correct(self, number: int):
        if not self.activated:
            raise Exception("Please activate before usage!")
        print_question(f"Correct Answer/s ({self.correct_length})\nQuestion:\t{self.value}", number + 1)
        for i, answer_idx in enumerate(self.arrangement):
            answer = self.data[answer_idx]
            if answer.is_correct:
                print_options([answer.value], chr(i + 65))
        
    def show_question(self, number: int):
        if not self.activated:
            raise Exception("Please activate before usage!")
        self.randomize()
        print_question(self.value, number)
        print_options([answer.value for answer in self.get_randomized_data()])