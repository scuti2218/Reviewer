from .Player import Player
from .Topic import Topic

from .Enums import GameMode, ChoiceOption
from .CRUD import check_dir, make_dir
from .FileData import get_configs, get_data
from .Printer import print_question, print_options, print_spacer, print_title, input_stopper, clear_console
from .Prompter import prompt

def evaluate(func):
    def wrapper(self, *args, **kwargs):
        self.initialized = func(self, *args, **kwargs)
        return self.initialized
    return wrapper

class SystemInfo:
    gamemode: GameMode = None
    choiceoption : ChoiceOption = None
    initialized : bool = False
    
    topics: list[Topic] = []
    selected: Topic = None
    amount: int = 0
    
    def __init__(self):
        self.initialize()

    def __str__(self):
        return f"SystemInfo"

    def __repr__(self):
        return f"SystemInfo()"
    
    @evaluate
    def initialize(self):
        if not check_dir("data"):
            make_dir("data")
            
        topics = get_configs("data")
        if len(topics) == 0:
            input("Add Topics in Data!")
            return False
        self.topics = topics
        return True
    
    def get_topic(self):
        self.selected = self.topics[0]
        if len(self.topics) > 1:
            print_question("Choose your Topic: ", 1)
            topics = [topic.show() for topic in self.topics]
            print_options(topics)
            self.selected = self.topics[prompt(topics)]  
            print_spacer()
            
    def get_gamemode(self):
        print_question("Choose your Gamemode: ", 2)
        gamemodes = [f"{gamemode.value[0]} : {gamemode.value[1]}" for gamemode in GameMode]
        print_options(gamemodes)
        self.gamemode = GameMode[chr(65 + prompt(gamemodes))]
        print_spacer()
        
    def get_choiceoption(self):
        print_question("Choose your Choice Option: ", 3)
        choiceoptions = [f"{choiceoption.value[0]} : {choiceoption.value[1]}" for choiceoption in ChoiceOption]
        print_options(choiceoptions)
        self.choiceoption = ChoiceOption[chr(65 + prompt(choiceoptions))]
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
        self.amount = amounts[prompt(amounts)]
        print_spacer()
            
    def show_configs(self):
        print_title(f"CONFIGURATIONS", True)
        print(f"Topic         : {self.selected.title}")
        print(f"Information   : {self.selected.info}")
        print(f"Gamemode      : {self.gamemode.value[0]}")
        print(f"Choice Option : {self.choiceoption.value[0]}")
        print(f"Amount        : {self.amount}")
        print_title(f"CONFIGURATIONS", True)
        print_spacer()
        input_stopper()
        
    def start(self):
        if not self.initialized:
            return
        
        clear_console()
        print_title(f"WELCOME TO THE GAME OF REVIEWER", True)
        print_spacer()
        
        self.get_topic()
        question_list = get_data(self.selected.dir)
        
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
        if prompt(listed) == 0:
            self.start()