from enum import Enum, unique
from random import shuffle
from typing import Generic, TypeVar
TData = TypeVar('TData')  # Declare a type variable
from os import system as os_system, name as os_name

def input_stopper():
    input("Enter any key to continue...")
    
def clear_console():
    os_system('cls' if os_name == 'nt' else 'clear')
    
def print_spacer(amount: int = 1):
    print("\n" * amount, end="")
    
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
    
def print_options(data: list):
    for i in range(len(data)):
        print(f"\t({chr(65 + i)}) {data[i]}")
        
def print_question(question: str, number: int):
    print(f"[{number}] {question}")
    
def print_title(text: str, add_separator: bool = False):
    print(f"{["",(10 * "=") + " "][add_separator]}{text.capitalize()}{[""," " + (40 * "=")][add_separator]}")
    
def prompt_answer(amount_choices: int, amount_correct: int, is_multiple_choice: bool = True) -> list[int] | list[str]:
    answers = []
    for i in range(amount_correct):
        while True:
            temp: str = input("> ").strip()
            if is_multiple_choice:
                temp = temp.capitalize()
                if temp == "":
                    print(f"Give an answer!")
                    continue
                
                if ord(temp) in range(65, 65 + amount_choices):
                    if ord(temp) not in answers:
                        answers.append(ord(temp) - 65)
                        break
                    else:
                        print(f"Choose a different answer!")
                else:
                    print(f"Prompt only from A to {chr(65 + amount_choices - 1)}!")
            else:
                answers.append(temp)
                break
    return answers
        
    
class Randomizable(Generic[TData]):
    def __init__(self):
        self.arrangement: list[int] = []
        self.data: list[TData] = []
        self.length: int = 0
    
    def randomize(self):
        self.arrangement = list(range(len(self.data)))
        shuffle(self.arrangement)
        self.length = len(self.data)
        
        
class Question(Randomizable[tuple[str, bool]]):
    def __init__(self):
        super().__init__()
        self.question : str = ""
        self.choiceoptions : list[ChoiceOption] = []
        self.classification : str = ""
        self.correct_answers = []

    def __str__(self):
        return f"{self.question}"

    def __repr__(self):
        return f"Question({self.question})"
    
    def set_question(self, question: str):
        self.question = question
        
    def set_type(self, choiceoptions: str):
        self.choiceoptions = [member for member in Amount for c in choiceoptions if member.name == c]
    
    def set_classification(self, classification: str):
        self.classification = classification
        
    def add_answer(self, answer: str, is_correct: bool):
        if is_correct:
            self.correct_answers.append(len(self.data))
        self.data.append((answer, is_correct))
        
    def show_question(self, count: int):
        self.randomize()
        print_question(self.question, count)
        print_options([self.data[i][0] for i in self.arrangement])
    
    def check(self, answers: list[int]) -> bool:
        return len(answers) == len(self.correct_answers) and all(self.data[self.arrangement[answer]][1] for answer in answers)
    
    def show_correct(self, count: int):
        answers = [answer[0] for i, answer in enumerate(self.data) if answer[1]]
        print_question(f"Correct Answer/s ({len(answers)})\nQuestion:\t{self.question}", count)
        print_options(answers)
            
class Question_List(Randomizable[Question]):
    def __init__(self, data: list[Question]):
        super().__init__()
        self.question_lists : dict[str, list[Question]] = {i.name:[] for i in ChoiceOption }
        for question in data:
            for choiceoption in question.choiceoptions:
                self.question_lists[choiceoption.name].append(question)

    def __str__(self):
        return f"Question List"

    def __repr__(self):
        return f"QuestionList({len(self.data)})"
    
    def activate(self, choiceoption: ChoiceOption):
        self.data = [self.question_lists[choiceoption.name], None][choiceoption.name not in self.question_lists.keys()] 
        self.randomize()
        
    def get_question(self, count: int) -> Question:
        return self.data[count]
    
        
class Player:
    score: int = 0
    max: int = 0
    question_list: Question_List = None
    gamemode: GameMode = None
    choiceoption: ChoiceOption = None
    
    def __init__(self, question_list: Question_List):
        self.question_list = question_list
    
    def show_score(self, maximum: int):
        print(f"SCORE: {self.score} / {maximum}")
        
    def start(self, gamemode: GameMode, choiceoption: ChoiceOption, amount: int):
        self.choiceoption = choiceoption
        self.gamemode = gamemode
        self.question_list.activate(self.choiceoption)
        self.score = 0
        self.max = max(0, min(amount, self.question_list.length))
        
        for i in range(self.max):
            clear_console()
            print_title(f"Question #{i + 1}", True)
            input(i)
        
            question: Question = self.question_list.get_question(i)
            question.show_question(i + 1)
            temp = prompt_answer(question.length, self.choiceoption == ChoiceOption.A)
            is_right = question.check(temp)
            if is_right:
                self.score += 1
                
            if self.gamemode == GameMode.B:
                question.show_correct(i)
                self.show_score(i + 1)
                print(f"{["Wrong", "Right"][is_right]} Answer!")
                input_stopper()
                
        clear_console()
        print_title("Questions", True)
        if self.gamemode == GameMode.A:
            for i in range(self.max):
                question: Question = self.question_list.get_question(i)
                question.show_correct(i)
                print_spacer()
        print_spacer(3)
        print_title("Final Score", True)
        self.show_score(self.max)