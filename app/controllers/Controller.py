from ..views import View
from ..models import Model, Score
from ..services.Printer import print_title, print_question, print_options, print_spacer, print_divider, print_definitions, clear_console, print_pause, delay
from ..services.Prompter import prompt, prompt_multiple_int
from ..services.Mode import modes, tournament as mode_tournament, quiz as mode_quiz, flashcard as mode_flashback

class Controller:
    def __init__(self, view: View, model: Model):
        self.view = view
        self.model = model
        self.initialize()
        
    def initialize(self):
        self.view.initialize()
        self.model.initialize()
    
    # MAIN MENU ==================================================
    def get_topic(self):
        clear_console()
        self.view.show_header()
        self.model.selected_topic = self.model.topics[0]
        if len(self.model.topics) > 1:
            print_question("Choose your Topic: ", self.config_count)
            topics = [topic.show() for topic in self.model.topics]
            print_spacer()
            print_options(topics)
            print_spacer()
            result = prompt(topics)
            if (result.crashed):
                self.get_topic()
                return
            self.model.selected_topic = self.model.topics[result.index]
            self.config_count += 1
            print_spacer()
            
        print_divider()
        print_question(f"Topic Selected    : {self.model.selected_topic.title}")
        print_question(f"Topic Information : {self.model.selected_topic.info}")
        print_spacer()
        
        self.model.get_topic_categories()
        categories = [category.show() for category in self.model.categories]
        print_question("Categories: ")
        print_options(categories)
        print_spacer()
        
        self.model.get_topic_questions()
        print_question(f"Total Questions   : {self.model.questions_count}")
        print_divider()
        print_pause()
        
    def get_mode(self):
        clear_console()
        self.view.show_header()
        print_question("Choose your Mode: ", self.config_count)
        print_spacer()
        listed_modes = [(mode.title, mode.listed_info) for mode in modes if mode.active and ((mode.requires_token and self.model.selected_topic.check_token()) or (not mode.requires_token))]
        for i, mode in enumerate(listed_modes):
            print_options([mode[0]], chr(65 + i))
            print_definitions(mode[1])
            print_spacer()
        result = prompt(modes)
        if (result.crashed):
            self.get_mode()
            return
        self.mode = modes[result.index]
        self.config_count += 1
        print_spacer()
        
        print_divider()
        print_question(f"Mode Selected     : {self.mode.title}")
        print_question(f"Mode Information  : {self.mode.info}")
        for i, info in enumerate(self.mode.listed_info):
            print_question(f"{[" " * 18, "Mode Configuration"][i == 0]} : {info}")
        print_divider()
        print_pause()
        
    def get_amount(self):
        clear_console()
        self.view.show_header()
        questions_count = len(self.model.questions)
        temp_amounts = [10, 30, 60, 100]
        amounts = [i for i in temp_amounts if i < questions_count]
        if len(amounts) != 4:
            amounts.append(questions_count)
            
        self.model.selected_amount = amounts[0]
        if len(amounts) > 1:
            print_question("Choose Amount of Questions: ", self.config_count)
            amounts_txt = [f"{i}" for i in amounts]
            print_spacer()
            print_options(amounts_txt)
            print_spacer()
            result = prompt(amounts)
            if (result.crashed):
                self.get_mode()
                return
            self.model.selected_amount = amounts[result.index]
            self.config_count += 1
        else:
            print_question(f"Amount of Questions automatically set to {self.model.selected_amount}")
        print_spacer()
            
        print_divider()
        print_question(f"Amount of Questions : {self.model.selected_amount}")
        print_question(f"Total Questions     : {self.model.questions_count}")
        print_divider()
        print_pause()
        
    def show_configurations(self):
        print_spacer()
        clear_console()
        self.view.show_header()
        print_title(self.model.selected_topic.title, True)
        print_question(f"Information        : {self.model.selected_topic.info}")
        print_question(f"Mode Selected      : {self.mode.title}")
        print_question(f"Mode Information   : {self.mode.info}")
        for i, info in enumerate(self.mode.listed_info):
            print_question(f"{[" " * 18, "Mode Configuration"][i == 0]} : {info}")
        print_question(f"Questions Amount   : {self.model.questions_count}")
        print_divider()
        print_spacer()
        print_pause()
        
    def prompt_restart(self):
        print_question("Do you want to restart? ")
        print_spacer()
        result = prompt(["Yes", "No"])
        if (result.crashed):
            return self.prompt_restart()
        return result.index == 0
        
    # MAIN MENU ==================================================
        
        
    # REVIEW ==================================================
    def start(self):
        self.model.score.current = 0
        self.model.score.maximum = 0
        if self.mode.title in [mode_tournament.title, mode_quiz.title]:
            self.model.score.maximum = self.model.selected_amount
        
        self.model.get_randomized_questions()
        questions = self.model.randomized_questions
        i: int = 0
        i_max: int = self.model.selected_amount
        all_answers: list[list[int]] = [[] for _ in range(i_max)]
        while i < i_max:
            print_spacer()
            clear_console()
            self.view.show_header()
            
            question = questions[i]
            answers = question.get_randomized_data()
            print_question(question.show(), i)
            
            answers_txt = [answer.show() for answer in answers]
            print_spacer()
            print_options(answers_txt)
            print_spacer()
            result = prompt_multiple_int(answers, question.count_correct)
            if (result.crashed):
                self.get_mode()
                return
            if result.message == "int":
                i = int(result.err_val)
                continue
            elif result.message == "obj":
                all_answers[i] = result.indexes
                if self.mode.show_after:
                    is_right = all([answers[i].is_correct for i in result.indexes])
                    self.model.score.maximum += 1
                    if is_right:
                        self.model.score.current += 1
                        is_corrects[i] = True
                    print_spacer()
                    print_question(f"{["Wrong", "Right"][is_right]} Answer!")
                    print_spacer()
                    print_title(self.model.get_category(question.category), True)
                    print_spacer()
                    [print_options([answer.title], chr(65 + i)) for i, answer in enumerate(answers) if answer.is_correct]
                    print_spacer()
                    print_question(self.model.score.show())
                    print_divider()
            else:
                continue
            
                 
        clear_console()
        print_title("Questions", True)
        is_corrects: list[bool] = [False for _ in range(i_max)]
        category_scores: dict[str, list[int, int]] = {cat.key : [0, 0] for cat in self.model.categories}
        for i, question in enumerate(questions):
            answers = question.get_randomized_data()
            is_right = all([answers[j].is_correct for j in all_answers[i]])
            if is_right:
                self.model.score.current += 1
                is_corrects[i] = True
                category_scores[question.category][0] += 1
            category_scores[question.category][1] += 1
            print_question(f"{["Wrong", "Right"][is_right]} Answer!")
            
            print_title(self.model.get_category(question.category), True)
            [print_options([answer.title], chr(65 + j)) for j, answer in enumerate(answers)]
            print_spacer()
            
            print_title("Correct Answers", True)
            [print_options([answer.title], chr(65 + j)) for j, answer in enumerate(answers) if answer.is_correct]
            print_divider()
            print_spacer()
            
        print_spacer(3)
        print_title("Final Score", True)
        print_question(self.model.score.show())
        print_question([f"({key}) {self.model.get_category(key)} {Score(current = value[0], maximum = value[1]).show()}" for key, value in category_scores])
        print_title("Final Score", True)
        print_spacer(2)
        print_pause()
    # REVIEW ==================================================
        
        
    def update(self):
        self.config_count: int = 1
        self.get_topic()
        self.get_mode()
        self.get_amount()
        self.show_configurations()
        
        self.start()
    
        if self.prompt_restart():
            self.update()
        