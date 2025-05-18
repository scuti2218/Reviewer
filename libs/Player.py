from .Score import Score
from .Enums import GameMode, ChoiceOption
from .Question_List import Question_List
from .Question import Question
from .Printer import clear_console, print_title, input_stopper, print_spacer
from .Prompter import prompt_answer
from .Classification_List import Classification_List

class Player:
    score: Score = None
    history: list[Score] = []
    def __init__(self):
        self.activated = False

    def __str__(self):
        return f"Player"

    def __repr__(self):
        return f"Player"
    
    def show_classification(self, question: Question):
        print_title(f"Classification: {self.classifications.get_by_label(question.classification).value.title()}")
    
    def activate(self, question_list: Question_List, classifications: Classification_List):
        self.activated = False
        self.question_list = question_list
        self.classifications = classifications
    
    def start(self, gamemode: GameMode, choice_option: ChoiceOption, amount: int):
        self.choiceoption = choice_option
        self.gamemode = gamemode
        self.question_list.activate(choice_option)
        self.score = Score(max(0, min(amount, self.question_list.length)))
        
        for i in range(self.score.get_max()):
            clear_console()
            print_title(f"Question #{i + 1}", True)
        
            question: Question = self.question_list.get_from_randomized(i)
            question.show_question(i + 1)
            
            is_right = prompt_answer(question)
            self.score.update_classification_max(question.classification)
            if is_right:
                self.score.add(question.classification)
                
            if self.gamemode == GameMode.B:
                print(f"{["Wrong", "Right"][is_right]} Answer!")
                print_spacer(2)
                self.show_classification(question)
                question.show_correct(i)
                self.score.set_whole(i + 1, self.score.get_value())
                print_spacer(2)
                self.score.print()
                input_stopper()
                
        clear_console()
        print_title("Questions", True)
        for i in range(self.score.get_max()):
            question: Question = self.question_list.get_from_randomized(i)
            self.show_classification(question)
            question.show_correct(i)
            print_spacer()
            
        print_spacer(3)
        print_title("Final Score", True)
        self.score.print()
        self.score.print_classification(self.classifications)
        self.score.lock()
        print_title("Final Score", True)
        
        print_spacer(2)
        self.history.append(self.score)