from enum import Enum, unique
    
@unique
class GameMode(Enum):
    A = ("Limits", "Reveal scores after all questions")
    B = ("Flashcard", "Reveal score after each question")

@unique
class ChoiceOption(Enum):
    A = ("Multiple Choice", "Choose from sets of answers")
    B = ("Enumeration", "Write your answer")

@unique
class Amount(Enum):
    A = ("Limited", "Specify How many questions to answer.")
    B = ("Infinite", "Answer as long as you like.")