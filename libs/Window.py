from .utils import GameMode, ChoiceOption, Question, Question_List, Player, print_options, print_question, prompt_answer, clear_console, print_title, input_stopper, print_spacer
from .CRUD import *
from .Reviewer import fix_config, evaluate_config

def evaluate(func):
    def wrapper(self, *args, **kwargs):
        self.initialized = func(self, *args, **kwargs)
        return self.initialized
    return wrapper

class Window:
    gamemode : GameMode = None
    choiceoption : ChoiceOption = None
    initialized : bool = False
    topics : list[list[Path]] = []
    selected : list[Path] = []
    amount : int = 0
    def __init__(self):
        self.initialize()

    def __str__(self):
        return f"Window"

    def __repr__(self):
        return f"Window()"
    
    @evaluate
    def initialize(self) -> bool:
        # Check if there is folder data
        if not check_dir("data"):
            print("Please add csv of questions and classifications (if necessary).")
            return False
            
        topics = get_sub_folders("data", fix_config)
        if len(topics) == 0:
            print("Please add csv of questions and classifications (if necessary).")
            return False
        self.topics = topics
    
        return True
    
    def start(self):
        if not self.initialized:
            return
        
        clear_console()
        print_title(f"WELCOME TO THE GAME OF REVIEWER", True)
        print_spacer()
        
        self.get_reviewer()
        raw_questions = evaluate_config(self.selected[2])
        question_list = self.create_question_list(raw_questions)
        
        self.get_gamemode()
        self.get_choiceoption()
        question_list.activate(self.choiceoption)
        
        self.get_amount(question_list.length)
        
        self.show_configs()
        player = Player(question_list)
        player.start(self.gamemode, self.choiceoption, self.amount)
        
        print_question("Do you want to restart?", 1)
        listed = ["Y", "N"]
        print_options(listed)
        if prompt_answer(2, 1)[0] == 0:
            self.start()
        
    def create_question_list(self, raw_questions: list[dict[str, str]]) -> Question_List:
        questions : list[Question] = []
        for raw_question in raw_questions:
            question : Question = Question()
            question.set_question(raw_question["question"])
            for answer in raw_question["correct_answers"]:
                question.add_answer(answer, True)
            for answer in raw_question["wrong_answers"]:
                question.add_answer(answer, False)
            question.set_type(raw_question["type"])
            question.set_classification(raw_question["classification"])
            questions.append(question)
        return Question_List(questions)
        
    def get_reviewer(self):
        self.selected = self.topics[0]
        if len(self.topics) > 1:
            self.get_topic()
        
    def get_topic(self):
        print_question("Choose your Topic: ", 1)
        topics = [f"{topic[0]} : {topic[1]}" for topic in self.topics]
        print_options(topics)
        self.selected = self.topics[prompt_answer(len(topics), 1)[0]]  
        print_spacer()
            
    def get_gamemode(self):
        print_question("Choose your Gamemode: ", 2)
        gamemodes = [f"{gamemode.value[0]} : {gamemode.value[1]}" for gamemode in GameMode]
        print_options(gamemodes)
        self.gamemode = GameMode[chr(65 + prompt_answer(len(gamemodes), 1)[0])]
        print_spacer()
        
    def get_choiceoption(self):
        print_question("Choose your Choice Option: ", 3)
        choiceoptions = [f"{choiceoption.value[0]} : {choiceoption.value[1]}" for choiceoption in ChoiceOption]
        print_options(choiceoptions)
        self.choiceoption = ChoiceOption[chr(65 + prompt_answer(len(choiceoptions), 1)[0])]
        print_spacer()
        
    def get_amount(self, max: int):
        temp_amounts = [10, 30, 60, 100]
        amounts = [i for i in temp_amounts if i < max]
        amounts.append(max)
        if len(amounts) == 1:
            self.amount = amounts[0]
            return
        
        print_question("Choose your Question Amount: ", 4)
        print_options(amounts)
        self.amount = amounts[prompt_answer(len(amounts), 1)[0]]
        print_spacer()
            
    def show_configs(self):
        print_title(f"CONFIGURATIONS", True)
        print(f"Topic         : {self.selected[0]}")
        print(f"Information   : {self.selected[1]}")
        print(f"Gamemode      : {self.gamemode.value[0]}")
        print(f"Choice Option : {self.choiceoption.value[0]}")
        print(f"Amount        : {self.amount}")
        print_title(f"CONFIGURATIONS", True)
        print_spacer()
        input_stopper()